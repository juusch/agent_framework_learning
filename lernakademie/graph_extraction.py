"""LLM-Gestuetzte Graph-Extraktion – mit Offline-Fallback.

Drei Bausteine:
1. Extraktion von Entitaeten + Beziehungen aus Text
   (mit Key: echtes LLM via with_structured_output; offline: Regel-Fallback)
2. Ueberfuehrung der Extraktion in GraphStore-Strukturen (Graph-Population)
3. Sichere Ausfuehrung LLM-generierter Cypher-Abfragen
   (nur lesende Whitelist – Schutz vor Prompt-Injection & Zerstoerung)
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from lernakademie.graph_store import GraphStore
from lernakademie.mock_llm import get_chat_model, is_offline_mode


class Extraktion(BaseModel):
    """Strukturiertes Ergebnis der Text->Graph-Analyse (Pydantic, Stufe 3.3!)."""
    entitaeten: List[Dict[str, Any]] = Field(
        description="Liste von {name, label}-Objekten")
    beziehungen: List[Dict[str, Any]] = Field(
        description="Liste von {von, typ, zu}-Objekten")


# Bekannte Labels und Beziehungstypen fuer den Offline-Fallback
BEKANNTE_LABELS = {
    "anna": "Person", "ben": "Person",
    "acme": "Company", "engineering": "Department",
    "ai assistant": "Project", "projekt": "Project",
}
BEKANNTE_BEZIEHUNGEN = {
    "works_for": "WORKS_FOR", "arbeitet fuer": "WORKS_FOR",
    "arbeitet bei": "WORKS_FOR",
    "belongs_to": "BELONGS_TO", "gehoert zu": "BELONGS_TO",
    "works_on": "WORKS_ON", "arbeitet an": "WORKS_ON",
    "contributes_to": "CONTRIBUTES_TO", "traegt bei zu": "CONTRIBUTES_TO",
}


def extrahiere_offline(text: str) -> Extraktion:
    """Regel-Fallback: erkennt bekannte Namen und 'A ... B'-Muster."""
    entitaeten, beziehungen = [], []
    for name, label in BEKANNTE_LABELS.items():
        if re.search(rf"\b{re.escape(name)}", text.lower()):
            entitaeten.append({"name": name.title() if name != "ai assistant" else "AI Assistant",
                               "label": label})
    klein = text.lower()
    for schluessel, typ in BEKANNTE_BEZIEHUNGEN.items():
        # Anchor-Suche: bekannte Entitaet VOR und NACH dem Beziehungsmuster
        muster = re.search(rf"([\w ]+?)\s+{re.escape(schluessel)}\s+([\w ]+?)(?:\.|$)", klein)
        if not muster:
            continue
        vor_teil, nach_teil = muster.group(1), muster.group(2)
        von = zu = None
        for kandidat in BEKANNTE_LABELS:
            if von is None and re.search(rf"\b{re.escape(kandidat)}\b", vor_teil):
                von = "AI Assistant" if kandidat == "ai assistant" else kandidat.title()
            if zu is None and re.search(rf"\b{re.escape(kandidat)}\b", nach_teil):
                zu = "AI Assistant" if kandidat == "ai assistant" else kandidat.title()
        if von and zu:
            beziehungen.append({"von": von, "typ": typ, "zu": zu})
    return Extraktion(entitaeten=entitaeten, beziehungen=beziehungen)


def extrahiere(text: str) -> Extraktion:
    """Extrahiert Entitaeten + Beziehungen (Key: LLM, offline: Regeln)."""
    if is_offline_mode():
        return extrahiere_offline(text)
    modell = get_chat_model(temperature=0.0)
    chain = modell.with_structured_output(Extraktion)
    ergebnis = chain.invoke(
        "Extrahiere alle Entitaeten (mit Typ-Label: Person, Company, "
        "Department oder Project) und alle Beziehungen aus diesem Text:\n" + text)
    return ergebnis


def fuelle_graph(store: GraphStore, extraktion: Extraktion) -> int:
    """Ueberfuehrt eine Extraktion in den GraphStore. Liefert Anzahl Kanten."""
    ids: Dict[str, int] = {}
    for entitaet in extraktion.entitaeten:
        name, label = entitaet["name"], entitaet.get("label", "Entity")
        vorhanden = store.find_node(label, name=name)
        if vorhanden is None:  # Entity Resolution: vorhandene nicht duplizieren
            ids[name] = store.add_node([label], name=name)
        else:
            ids[name] = vorhanden.id
    gesetzt = 0
    for beziehung in extraktion.beziehungen:
        von, zu = beziehung["von"], beziehung["zu"]
        if von in ids and zu in ids:
            store.add_relationship(ids[von], ids[zu], beziehung["typ"])
            gesetzt += 1
    return gesetzt


# ---------------------------------------------------------------------------
# Sichere Cypher-Ausfuehrung (Stufe-12-Kern: generierte Abfragen schuetzen)
# ---------------------------------------------------------------------------

_VERBOTENE_SCHLUESSELWOERTER = (
    "CREATE", "DELETE", "MERGE", "SET ", "DROP", "REMOVE", "DETACH", "LOAD",
    "CALL", "FOREACH",
)


def ist_sicher(cypher: str) -> bool:
    """True, wenn die Abfrage nur lesend ist (Whitelist-Prinzip).

    Warum so streng? Ein LLM kann per Prompt-Injection dazu gebracht
    werden, destruktive Abfragen zu 'erfinden'. Wir pruefen VOR jeder
    Ausfuehrung – und fuehren im Zweifel NICHT aus.
    """
    if not cypher or not cypher.strip().upper().startswith("MATCH"):
        return False
    if " RETURN " not in cypher.upper():
        return False
    gross = " " + cypher.upper() + " "
    return not any(wort in gross for wort in _VERBOTENE_SCHLUESSELWOERTER)


def fuehre_sicher_aus(store: GraphStore, cypher: str) -> List[Dict[str, Any]]:
    """Fuehrt nur sichere (lesende) Abfragen aus – sonst klarer Fehler."""
    if not ist_sicher(cypher):
        raise ValueError(
            f"Abfrage abgelehnt (nur lesende MATCH...RETURN erlaubt): {cypher[:80]}"
        )
    return store.run_cypher(cypher)


def cypher_aus_frage(frage: str) -> Optional[str]:
    """Offline-Fallback: natuerliche Frage -> Mini-Cypher (Regel-Logik)."""
    klein = frage.lower()
    match_person = re.search(r"(\w+)", klein.replace("?", ""))
    name = None
    label = None
    for kandidat in BEKANNTE_LABELS:
        if re.search(rf"\b{re.escape(kandidat)}\b", klein):
            name = "AI Assistant" if kandidat == "ai assistant" else kandidat.title()
            label = BEKANNTE_LABELS[kandidat]
            break
    if name is None:
        return None
    if "arbeitet" in klein or "works" in klein or "works_for" in klein:
        return f"MATCH (a {{name: '{name}'}})-[r]->(b) RETURN a, type(r), b"
    return f"MATCH (n:{label} {{name: '{name}'}}) RETURN n" if label else None
