"""Notebook-Specs Teil E: LangGraph + BUILD 3 (Lektion 13-15)."""

NB_13 = {
    "pfad": "notebooks/07_langgraph/13_langgraph_workflows.ipynb",
    "titel": "Lektion 13: LangGraph – State, Nodes & Routing",
    "zeit": "~75 Minuten",
    "schwierigkeit": "Mittel",
    "voraussetzungen": "Lektion 01–12",
    "baut": "Deine ersten drei LangGraph-Workflows: gerades Band, Verzweigung (Weiche) und Schleife mit Bremse",
    "ziele": [
        "erklären, warum Chains (gerade Linien) für Verzweigungen nicht reichen",
        "einen **State** (gemeinsamer Notizblock) definieren und Nodes Daten hineinschreiben lassen",
        "konditionale Kanten (die Weiche) einsetzen",
        "einen Loop mit **Doppel-Bedingung** bauen (Qualität ODER Limit)",
        "das Diagramm → Code → Ausführung-Dreieck selbst erleben",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Das Bahnhofnetz\n\n"
               "**WARUM:** Chains (Lektion 07+) sind **gerade Linien**: Input → Verarbeitung → Output, immer vorwärts. "
               "Aber dein Build-3-Assistent muss **verzweigen** (Vektor- oder Graph-Suche?) und **wiederholen** "
               "(Qualitätsprüfung mit Nachbesserung). Dafür brauchst du ein Werkzeug, das Entscheidungen und Schleifen *erste Klasse* behandelt.\n\n"
               "**WAS:** **LangGraph** organisiert Arbeit als Graph. Die Vokabeln:\n\n"
               "- **State** = der gemeinsame Notizbuch im Zug – jede Station **liest und schreibt** hinein\n"
               "- **Node** = eine Station: genau eine Person erledigt genau eine Aufgabe\n"
               "- **Edge** = ein Gleis von Station zu Station\n"
               "- **Conditional Edge** = die Weiche: der Fahrdienstleiter liest den Notizblock und stellt die Weiche\n"
               "- **Loop** = ein Rückgleis (\"noch nicht gut genug → zurück!\")\n\n"
               "```text\nSTART → klassifizieren → (Weiche)\n                         ├─→ antwort_rechnung ──┐\n                         ├─→ antwort_technisch ─┼→ END\n                         └─→ antwort_allgemein ──┘\n```"),
        ("md", "## Schritt 1: Der erste Graph (Hello Graph)\n\n"
               "**WAS:** Ein State ist ein `TypedDict` (Lektion 01: Dictionary mit fester Form!). "
               "**WICHTIG:** Nodes geben nur ihre **Änderungen** zurück – LangGraph mischt sie in den State (Merge)."),
        ("code", '''\
from langgraph.graph import END, START, StateGraph
from typing import TypedDict

class Zustand(TypedDict):
    begruessung: str

def begruessen(state: Zustand) -> dict:
    return {"begruessung": "Hallo LangGraph!"}

graph = StateGraph(Zustand)
graph.add_node("begruessen", begruessen)
graph.add_edge(START, "begruessen")
graph.add_edge("begruessen", END)

app = graph.compile()          # kompilieren -> ausfuehrbar
ergebnis = app.invoke({"begruessung": ""})
print(ergebnis)'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "1. Schema (`TypedDict`) → Node-Funktion → Kanten → `compile()` → `invoke()`.\n"
               "2. Der Node gibt `{{\"begruessung\": ...}}` zurück – **nur die Änderung**, nicht den ganzen State.\n"
               "3. Das Ergebnis von `invoke` ist der finale State. **TRY:** Füge einen zweiten Node hinzu, der den Text erweitert!"),
        ("md", "## Schritt 2: Die Weiche (konditionale Kanten)\n\n"
               "Jetzt das Entscheidungs-Muster – ein kleiner Support-Router. "
               "**Die wichtige Trennung:** `klassifizieren` **schreibt** (Regel-Logik), die Weichen-Funktion **liest nur** "
               "(sie entscheidet, sie arbeitet nicht)."),
        ("code", '''\
from langgraph.graph import END, START, StateGraph
from typing import TypedDict

class TicketZustand(TypedDict):
    eingabe: str
    kategorie: str
    antwort: str

def klassifizieren(state: TicketZustand) -> dict:
    text = state["eingabe"].lower()
    if "rechnung" in text or "betrag" in text:
        return {"kategorie": "rechnung"}
    if any(w in text for w in ("funktioniert", "fehler", "absturz", "stuerzt")):
        return {"kategorie": "technisch"}
    return {"kategorie": "allgemein"}

def weiche(state: TicketZustand) -> str:
    """Der Fahrdienstleiter: liest NUR und nennt den naechsten Node."""
    return state["kategorie"]

def antwort_rechnung(state):
    return {"antwort": "Ihre Anfrage geht an die Buchhaltung (5 Werktage)."}
def antwort_technisch(state):
    return {"antwort": "Das Technik-Team nimmt sich dem an. Geraet + Fehlermeldung?"}
def antwort_allgemein(state):
    return {"antwort": "Danke! Das allgemeine Team antwortet in Kuerze."}

router = StateGraph(TicketZustand)
router.add_node("klassifizieren", klassifizieren)
for name, funktion in (("antwort_rechnung", antwort_rechnung),
                       ("antwort_technisch", antwort_technisch),
                       ("antwort_allgemein", antwort_allgemein)):
    router.add_node(name, funktion)
    router.add_edge(name, END)

router.add_edge(START, "klassifizieren")
router.add_conditional_edges(
    "klassifizieren", weiche,
    {"rechnung": "antwort_rechnung",
     "technisch": "antwort_technisch",
     "allgemein": "antwort_allgemein"},
)
router_app = router.compile()

for eingabe in ("Meine Rechnung hat einen falschen Betrag.",
                "Die App stuerzt seit heute ab.",
                "Wo sehe ich meine Arbeitszeiten?"):
    ergebnis = router_app.invoke({"eingabe": eingabe, "kategorie": "", "antwort": ""})
    print(f"{ergebnis['kategorie']:10s} -> {ergebnis['antwort']}")'''),
        ("ex", {
            "titel": "Dein eigener Router",
            "ziel": "Du baust eine Verzweigung mit eigener Regel-Logik – inklusive beweisbarem Test.",
            "anforderungen": [
                "Schreibe `klassifiziere_frage(frage)`, das `\"vektor\"`, `\"graph\"` oder `\"hybrid\"` zurückgibt: "
                "Verbindungsfragen („haengt\", „wer\", „zusammen\") → `graph`; Gesamtfragen („gesamt\", „alles\", „vergleich\") → `hybrid`; sonst `vektor`.",
                "Baue einen Mini-Graph (1 Klassifizier-Node + 3 Antwort-Nodes), der die Kategorie in `antwort` schreibt (z. B. `\"Route: graph\"`).",
                "Teste: „Was steht über Urlaub?“ → vektor; „Wer hängt am Projekt?“ → graph; „Was wissen wir gesamt?“ → hybrid.",
            ],
            "starter": '''\
def klassifiziere_frage(frage):
    # YOUR CODE HERE
    pass

# YOUR CODE HERE: Mini-Graph bauen und kompilieren''',
            "kriterien": [
                "Die drei Testfragen landen auf den erwarteten Routen.",
                "Die Weichen-Funktion liest nur (keine State-Änderung in ihr!).",
                "Das Ergebnis des Graph enthält `route` und `antwort`.",
            ],
            "checks": '''\
assert klassifiziere_frage("Was steht ueber Urlaub?") == "vektor"
assert klassifiziere_frage("Wer haengt am Projekt dran?") == "graph"
assert klassifiziere_frage("Was wissen wir gesamt ueber das Projekt?") == "hybrid"
ergebnis = app.invoke({"frage": "Wer haengt am Projekt?", "route": "", "antwort": ""})
assert ergebnis["route"] == "graph"
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Greife auf `frage.lower()` zu; prüfe die Schlüsselwörter mit `any(w in text for w in (...))`.",
                "Das Mapping-Dict in `add_conditional_edges` übersetzt Kategorie → Node-Name.",
                "Der State braucht Felder: `frage`, `route`, `antwort`.",
            ],
            "loesung": '''\
from langgraph.graph import END, START, StateGraph
from typing import TypedDict

class FrageZustand(TypedDict):
    frage: str
    route: str
    antwort: str

def klassifiziere_frage(frage):
    text = frage.lower()
    if any(w in text for w in ("haengt", "zusammen?", "wer ", "beziehung", "verbind")):
        return "graph"
    if any(w in text for w in ("gesamt", "alles", "vergleich", "sowohl")):
        return "hybrid"
    return "vektor"

g = StateGraph(FrageZustand)
g.add_node("klassifizieren", lambda s: {"route": klassifiziere_frage(s["frage"])})
for route in ("vektor", "graph", "hybrid"):
    g.add_node(f"antwort_{route}",
               lambda s, r=route: {"antwort": f"Route: {r}"})
    g.add_edge(f"antwort_{route}", END)
g.add_edge(START, "klassifizieren")
g.add_conditional_edges("klassifizieren", lambda s: s["route"],
    {r: f"antwort_{r}" for r in ("vektor", "graph", "hybrid")})
app = g.compile()

print(app.invoke({"frage": "Wer haengt am Projekt?", "route": "", "antwort": ""}))''',
            "loesung_md": "Dies ist exakt die Klassifikation aus Build 3! Mit Key teilst du dem Lambda die Route mit "
                          "(`r=route` im Default-Argument) – ein sauberer Trick, um drei Antwort-Nodes aus einer Fabrik zu bauen. "
                          "Die Route-Entscheidung als **eigener Node** macht sie testbar – genau das prüft die Check-Zelle.",
            "reflexion": [
                "1. Warum ist „Klassifikation als eigener Node\" besser, als die Entscheidung in die Antwort-Nodes zu verteilen?",
                "2. Was wäre der Loop in einem echten LLM-Workflow – und was kostet er unbegrenzt?",
            ],
        }),
        ("md", "## Schritt 3: Der Loop mit Bremse\n\n"
               "**Metapher – die Küche mit Qualitätskontrolle:** Koch richtet den Teller an, Kontrolle prüft. "
               "Nicht schön? Zurück an den Herd! **Aber:** Nach drei Versuchen wird serviert – sonst wartet der Gast ewig. "
               "Der Versuchszähler im State ist die Bremse."),
        ("code", '''\
from langgraph.graph import END, START, StateGraph
from typing import TypedDict

class PolierZustand(TypedDict):
    text: str
    bewertung: int
    versuche: int
    max_versuche: int
    historie: list

def entwerfen(state):
    neu = state["versuche"] + 1
    text = f"{state['text']} (Politur {neu})"
    print(f"  entwerfen: Durchgang {neu}")
    return {"text": text, "versuche": neu,
            "historie": state["historie"] + [text]}   # NEUE Liste zurueckgeben!

def pruefen(state):
    bewertung = min(100, 30 + 25 * state["versuche"])
    print(f"  pruefen: Bewertung {bewertung}")
    return {"bewertung": bewertung}

def weiche_loop(state):
    if state["bewertung"] >= 60:          # Bedingung 1: Qualitaet
        return "fertig"
    if state["versuche"] >= state["max_versuche"]:   # Bedingung 2: LIMIT
        return "fertig"
    return "nachbessern"

g = StateGraph(PolierZustand)
g.add_node("entwerfen", entwerfen)
g.add_node("pruefen", pruefen)
g.add_edge(START, "entwerfen")
g.add_edge("entwerfen", "pruefen")
g.add_conditional_edges("pruefen", weiche_loop,
                        {"fertig": END, "nachbessern": "entwerfen"})
loop_app = g.compile()

ergebnis = loop_app.invoke({"text": "Erster Entwurf", "bewertung": 0,
                            "versuche": 0, "max_versuche": 5, "historie": []})
print("\\nFinaler Text:", ergebnis["text"])
print("Historie:", ergebnis["historie"])'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "**Zwei Endbedingungen** – Qualität ODER Limit. Ohne Limit kann ein Loop endlos laufen (Kosten!). "
               "Und: Listen im State gibst du als **neue Liste** zurück (`state[\"historie\"] + [text]`) – "
               "nicht mutieren! **TRY:** Setze `max_versuche=1` – der Lauf terminiert kontrolliert nach einem Durchgang."),
    ],
    "weiter": "**Weiter mit Lektion 14:** `notebooks/07_langgraph/14_hybrid_retrieval.ipynb` – "
              "Vektor- und Graph-Suche im direkten Duell (und die Kombination, die Build 3 ausmacht).",
}

NB_14 = {
    "pfad": "notebooks/07_langgraph/14_hybrid_retrieval.ipynb",
    "titel": "Lektion 14: Hybrid Retrieval – Vektor trifft Graph",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Mittel",
    "voraussetzungen": "Lektion 08–13",
    "baut": "Die Messung: dieselben Fragen an beide Wissenssysteme – und die Hybrid-Pipeline mit Quellentrennung",
    "ziele": [
        "Vektor- und Graph-Retrieval **unabhängig** betreiben",
        "die Stärken beider Verfahren an konkreten Fragen messen",
        "den **Emergenz-Beweis** wiederholen (Pfad, der nirgends geschrieben steht)",
        "eine Hybrid-Pipeline bauen, die Doku-Fundstellen und Graph-Fakten **getrennt** ausweist",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Zwei Abteilungen der Bibliothek\n\n"
               "**Metapher:**\n"
               "- **Vektor-Suche** = der hilfsbereite **Ausleiher**: \"Ich glaube, *dieses* Kapitel meinst du\" – unscharf, nach Bedeutung. Perfekt für \"Was steht über…?\"\n"
               "- **Graph-Suche** = der **Archivar** mit Fadensystem: \"Alles zu X hängt an *diesem* Faden\" – exakt, nach Struktur. Perfekt für \"Wie hängt A mit B zusammen?\"\n"
               "- **Hybrid** = frag beide, lege beide Ergebnisse mit **Herkunftsetikett** auf den Tisch.\n\n"
               "| Frage | Gewinner |\n|---|---|\n"
               "| \"Was steht über Urlaub?\" | Vektor |\n"
               "| \"Wer hängt am Projekt?\" | Graph |\n"
               "| \"Wie hängt Ben mit dem Projekt zusammen?\" | Graph (Emergenz!) |\n"
               "| \"Was wissen wir gesamt?\" | Hybrid |"),
        ("code", '''\
# Beide Systeme aufbauen (Wiederverwendung aus Lektion 08/10!):
from lernakademie.build2 import baue_retriever
from lernakademie.graph_store import GraphStore

retriever = baue_retriever(k=3)

def baue_wissens_graph():
    store = GraphStore()
    anna = store.add_node(["Person"], name="Anna", rolle="Entwicklerin")
    ben = store.add_node(["Person"], name="Ben", rolle="Analyst")
    engineering = store.add_node(["Department"], name="Engineering")
    analytics = store.add_node(["Department"], name="Data & Analytics")
    projekt = store.add_node(["Project"], name="AI Assistant", status="aktiv")
    store.add_relationship(anna, engineering, "BELONGS_TO")
    store.add_relationship(ben, analytics, "BELONGS_TO")
    store.add_relationship(engineering, projekt, "WORKS_ON")
    store.add_relationship(analytics, projekt, "PROVIDES_DATA_FOR")
    store.add_relationship(anna, projekt, "CONTRIBUTES_TO")
    return store

graph = baue_wissens_graph()
print("Beide Systeme bereit:",
      type(retriever).__name__, "+", len(graph.nodes()), "Graph-Nodes")'''),
        ("code", '''\
def vektor_suche(frage):
    """Liefert [{quelle, textstelle}] – nur relevante Treffer."""
    from lernakademie.offline_embeddings import hat_bezug
    from pathlib import Path
    if not hat_bezug(frage):
        return []
    ergebnisse = []
    for dokument in retriever.invoke(frage)[:2]:
        stelle = dokument.page_content.strip().replace("\\n", " ")
        if len(stelle) > 30:
            ergebnisse.append({"quelle": Path(dokument.metadata["source"]).name,
                               "textstelle": stelle[:140] + "..."})
    return ergebnisse

def graph_suche(frage):
    """Liefert Fakten der Form 'A --REL--> B' (Traversierung)."""
    klein = frage.lower()
    fakten = []
    projekt = graph.find_node("Project", name="AI Assistant")
    if projekt and ("projekt" in klein or "ai assistant" in klein):
        for kante in graph.relationships():
            if kante.to_id == projekt.id:
                quelle = graph.nodes()[kante.from_id]
                fakten.append(f"{quelle.properties['name']} --{kante.typ}--> AI Assistant")
    if "ben" in klein:
        ben = graph.find_node("Person", name="Ben")
        for kante, abteilung in graph.neighbors(ben.id, "BELONGS_TO"):
            for kante2, ziel in graph.neighbors(abteilung.id):
                fakten.append(f"Ben --BELONGS_TO--> {abteilung.properties['name']}"
                              f" --{kante2.typ}--> {ziel.properties['name']}")
    return list(dict.fromkeys(fakten))   # Duplikate raus, Reihenfolge halten

print("Vektor:", [e["quelle"] for e in vektor_suche("Wie viele Urlaubstage gibt es?")])
print("Graph :", graph_suche("Wer haengt am AI Assistant dran?"))'''),
        ("md", "## 🔎 Der direkte Vergleich\n\n"
               "Jetzt **dieselben Fragen** an **beide** Systeme – und die Auswertung:"),
        ("code", '''\
VERGLEICH = [
    ("Was steht ueber die Abteilung Engineering?", "Vektor (Textinhalt)"),
    ("Wer haengt am AI Assistant dran?", "Graph (Verbindungen)"),
    ("Wie haengt Ben mit dem Projekt zusammen?", "Graph (Emergenz!)"),
    ("Was wissen wir gesamt ueber das Projekt?", "Beide (Hybrid)"),
]
for frage, erwartet in VERGLEICH:
    v = vektor_suche(frage)
    g = graph_suche(frage)
    print(f"FRAGE: {frage}")
    print(f"  Vektor: {len(v)} Fundstelle(n) | Graph: {len(g)} Fakt(en) | erwartet: {erwartet}")
    for fakt in g[:2]:
        print("   Graph-Fakt:", fakt)
    print()'''),
        ("md", "### 🔎 Der Emergenz-Beweis\n"
               "`Ben --BELONGS_TO--> Data & Analytics --PROVIDES_DATA_FOR--> AI Assistant`: "
               "Dieser Weg steht in **keinem Satz** der Dokumente – er entsteht durch das Kombinieren zweier Fakten. "
               "Vektor-Suche könnte ihn maximal *andeutungsweise* streifen; der Graph beantwortet ihn **exakt**."),
        ("ex", {
            "titel": "Die Hybrid-Pipeline",
            "ziel": "Du baust `hybrid_suche(frage)`, das beide Quellen befragt – sauber getrennt und mit ehrlichem Fehlschlag.",
            "anforderungen": [
                "Rückgabe: `{\"dokumente\": [...], \"graph\": [...], \"antwort\": str}`.",
                "Beide Quellen werden immer befragt (das Routing folgt in Lektion 15!).",
                "Wenn beide leer sind: `antwort = \"Dazu habe ich in Dokumenten UND Graph nichts gefunden.\"`",
                "Die Antwort nennt die Anzahl der Fundstellen je Quelle.",
            ],
            "starter": '''\
def hybrid_suche(frage):
    # YOUR CODE HERE
    pass

ergebnis = hybrid_suche("Was wissen wir gesamt ueber das Projekt?")
print(ergebnis["antwort"])''',
            "kriterien": [
                "Für die Gesamtfrage liefert die Pipeline Daten aus **beiden** Feldern.",
                "Totaler Fehlschlag → ehrlicher Text, keine Crashes.",
                "Doku- und Graph-Quellen sind in getrennten Feldern (nie vermischt!).",
            ],
            "checks": '''\
hy = hybrid_suche("Was wissen wir gesamt ueber das AI Assistant Projekt?")
assert hy["dokumente"] or hy["graph"], "Hybrid-Frage sollte Treffer haben."
assert isinstance(hy["dokumente"], list) and isinstance(hy["graph"], list)
leer = hybrid_suche("Gibt es hier Informationen zu Weihnachtsgeld?")
assert leer["antwort"], "Auch leer braucht eine Antwort."
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Baue auf `vektor_suche(frage)` und `graph_suche(frage)` auf – die Arbeit ist schon getan!",
                "Der Antwort-Text kann deterministisch zusammengesetzt werden (kein LLM nötig): `f\"Hybrid: {len(d)} Doku- und {len(g)} Graph-Treffer.\"`",
            ],
            "loesung": '''\
def hybrid_suche(frage):
    dokumente = vektor_suche(frage)
    fakten = graph_suche(frage)
    if not dokumente and not fakten:
        return {"dokumente": [], "graph": [],
                "antwort": "Dazu habe ich in Dokumenten UND Graph nichts gefunden."}
    return {
        "dokumente": dokumente,
        "graph": fakten,
        "antwort": (f"Hybrid-Ergebnis: {len(dokumente)} Dokument-Fundstelle(n), "
                    f"{len(fakten)} Graph-Fakt(en)."),
    }

ergebnis = hybrid_suche("Was wissen wir gesamt ueber das Projekt?")
print(ergebnis["antwort"])
for f in ergebnis["graph"]:
    print("  Graph:", f)''',
            "loesung_md": "Die Stärke liegt in der **Quellentrennung**: Der Nutzer sieht immer, woher jede Information "
                          "kommt (Doku vs. Graph) – das schafft Vertrauen und macht Fehler auffindbar. "
                          "Was noch fehlt: die **Entscheidung**, wann welche Quelle nötig ist → Lektion 15!",
            "reflexion": [
                "1. Warum wäre \"immer beide Quellen fragen\" bei 100 Nutzern zu teuer – und was rettet uns? (→ Routing!)",
                "2. Was fehlt der Hybrid-Antwort, wenn der Graph **falsch gepflegt** wurde – und was schützt dagegen? (→ Freigabe, Lektion 15!)",
            ],
        }),
    ],
    "weiter": "**🚀 BUILD 3 – Lektion 15:** `notebooks/08_build_3/15_build3_hybrid_agent.ipynb` – "
              "LangGraph verbindet alles: Routing zwischen den Quellen UND die Freigabe für Graph-Änderungen.",
}

NB_15 = {
    "pfad": "notebooks/08_build_3/15_build3_hybrid_agent.ipynb",
    "titel": "Lektion 15: 🚀 BUILD 3 – Der Hybrid-Agent mit Freigabe",
    "zeit": "~90 Minuten",
    "schwierigkeit": "Fortgeschritten",
    "voraussetzungen": "Lektion 10–14",
    "baut": "Die Build-3-Version deines Knowledge Assistant: Routing-Agent (Vektor/Graph/Hybrid) + Human-in-the-Loop für Graph-Schreibzugriffe",
    "ziele": [
        "die vollständige Build-3-Architektur aufbauen und erklären",
        "per Intent-Klassifikation **nur die nötigen** Quellen abfragen",
        "einen **Freigabe-Workflow** mit `interrupt()` bauen (Genehmigung/Ablehnung)",
        "ein **Audit-Log** über alle Entscheidungen führen",
        "Beweise führen: Genehmigung ändert den Graph, Ablehnung nicht",
    ],
    "cells": [
        ("md", "## 🚀 Willkommen zu BUILD 3!\n\n"
               "Der finale Assistent – entstanden aus **beiden** Vorgängern:\n\n"
               "- **Recycling aus Build 2:** der Vektor-Retriever (Lektion 08/09)\n"
               "- **Neu aus Modul Knowledge Graph:** der GraphStore (Lektion 10)\n"
               "- **Neu aus LangGraph:** Routing (Lektion 13) + Hybrid-Pipeline (Lektion 14)\n"
               "- **Neu:** Human-in-the-Loop – der Sicherheitsgurt für Schreibzugriffe\n\n"
               "```text\nFrage → Intent-Klassifikation (Node)\n            ├─ vektor  → Vektor-Retrieval ────┐\n            ├─ graph   → Graph-Traversal ─────┤→ antworten (Route + Quellen)\n            └─ hybrid  → beide ───────────────┘\nFakt-Vorschlag → [interrupt: Freigabe?] → ja: Graph ändern / nein: verwerfen + Audit\n```\n\n"
               "**WARUM die Freigabe?** Ein hallucinierter Fakt im Graph vergiftet **jede zukünftige Antwort** "
               "(der Graph \"erinnert sich\" falsch). **Metapher:** die Gegenzeichnung auf der Krankenakte – "
               "der Agent hält den Stift über dem Formular, aber erst deine Unterschrift schreibt."),
        ("code", '''\
# Recycling aus Lektion 14 (hier als Vorbereitung, identisch):
from lernakademie.build2 import baue_retriever
from lernakademie.graph_store import GraphStore

def baue_wissens_graph():
    store = GraphStore()
    anna = store.add_node(["Person"], name="Anna", rolle="Entwicklerin")
    engineering = store.add_node(["Department"], name="Engineering")
    projekt = store.add_node(["Project"], name="AI Assistant", status="aktiv")
    store.add_relationship(anna, engineering, "BELONGS_TO")
    store.add_relationship(engineering, projekt, "WORKS_ON")
    store.add_relationship(anna, projekt, "CONTRIBUTES_TO")
    return store

retriever = baue_retriever(k=3)
graph = baue_wissens_graph()
print("Systeme bereit.")'''),
        ("md", "## Schritt 1: Der Routing-Agent\n\n"
               "Die Weiche aus Lektion 13 – jetzt mit echten Werkzeug-Nodes dahinter:"),
        ("code", '''\
from langgraph.graph import END, START, StateGraph
from typing import TypedDict
from pathlib import Path
from lernakademie.offline_embeddings import hat_bezug

class AgentZustand(TypedDict):
    frage: str
    route: str
    dokumente: list
    graph_fakten: list
    antwort: str

def klassifiziere(frage):
    """Intent-Klassifikation (mit Key: jede Route ein Werkzeug)."""
    klein = frage.lower()
    if any(w in klein for w in ("gesamt", "alles", "vergleich", "sowohl")):
        return "hybrid"
    if any(w in klein for w in ("haengt", "zusammen?", "wer ", "beziehung", "verbind", "arbeitet an")):
        return "graph"
    return "vektor"

def vektor_node(state):
    frage = state["frage"]
    if not hat_bezug(frage):
        return {"dokumente": []}
    treffer = retriever.invoke(frage)[:2]
    return {"dokumente": [
        {"quelle": Path(d.metadata["source"]).name,
         "textstelle": d.page_content.strip()[:120]}
        for d in treffer if len(d.page_content.strip()) > 30]}

def graph_node(state):
    klein = state["frage"].lower()
    fakten = []
    projekt = graph.find_node("Project", name="AI Assistant")
    if projekt and ("projekt" in klein or "ai assistant" in klein):
        for kante in graph.relationships():
            if kante.to_id == projekt.id:
                quelle = graph.nodes()[kante.from_id]
                fakten.append(f"{quelle.properties['name']} --{kante.typ}--> AI Assistant")
    return {"graph_fakten": list(dict.fromkeys(fakten))}

def antwort_node(state):
    teile = [f"Route: {state['route']}"]
    if state["dokumente"]:
        teile.append(f"Dokumente: {len(state['dokumente'])} Fundstelle(n)")
    if state["graph_fakten"]:
        teile.append(f"Graph: {len(state['graph_fakten'])} Fakt(en)")
    if not state["dokumente"] and not state["graph_fakten"]:
        teile.append("keine Quelle hatte etwas")
    return {"antwort": " | ".join(teile)}

g = StateGraph(AgentZustand)
g.add_node("klassifizieren", lambda s: {"route": klassifiziere(s["frage"])})
g.add_node("vektor", vektor_node)
g.add_node("graph", graph_node)
g.add_node("antworten", antwort_node)
g.add_edge(START, "klassifizieren")
g.add_conditional_edges("klassifizieren", lambda s: s["route"],
    {"vektor": "vektor", "graph": "graph", "hybrid": "vektor"})  # hybrid: erst Vektor...
g.add_conditional_edges("vektor", lambda s: "graph" if s["route"] == "hybrid" else "antworten",
    {"graph": "graph", "antworten": "antworten"})                 # ...dann Graph
g.add_edge("graph", "antworten")
g.add_edge("antworten", END)
agent = g.compile()

for frage in ("Was steht ueber Urlaub?",
              "Wer haengt am Projekt dran?",
              "Was wissen wir gesamt ueber das Projekt?"):
    e = agent.invoke({"frage": frage, "route": "", "dokumente": [], "graph_fakten": [], "antwort": ""})
    print(f"{frage[:40]:42s} -> {e['antwort']}")'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Die dokumentlastige Frage ruft den Graph **nicht**; die Verbindungsfrage läuft **nur** über den Graph; "
               "die Hybrid-Frage nutzt beide. **Der Agent entscheidet gezielt** – Kosten- und Präzisionsgewinn gegenüber "
               "Lektion 14 (wo immer beide liefen)."),
        ("md", "## Schritt 2: Die Freigabe (Human-in-the-Loop)\n\n"
               "**Drei Zutaten:**\n"
               "1. **`interrupt({...})`** im Werkzeug – **bevor** die Änderung passiert; der Lauf **pausiert**.\n"
               "2. Ein **Checkpointer** am `compile()` – ohne ihn kann LangGraph den angehaltenen Zustand nicht sichern.\n"
               "3. **`Command(resume=True/False)`** mit **demselben** `thread_id`-Config – deine Entscheidung."),
        ("code", '''\
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from typing import TypedDict

AUDIT_LOG = []   # Prozess-Log der Freigaben (auch im Finale so!)

class FreigabeZustand(TypedDict):
    von: str
    typ: str
    zu: str
    grund: str
    ergebnis: str

def vorschlagen(state):
    return {}   # Der Vorschlag kommt bereits aus dem invoke-Input

def anlegen(state):
    # Der Stift schwebt ueber dem Formular: interrupt VOR der Aenderung!
    freigabe = interrupt({
        "frage": "Soll dieser Fakt in den Knowledge Graph eingetragen werden?",
        "fakt": f"{state['von']} --{state['typ']}--> {state['zu']}",
        "grund": state["grund"],
    })
    if freigabe:
        eintrag = f"GENEHMIGT: {state['von']} --{state['typ']}--> {state['zu']}"
    else:
        eintrag = f"ABGELEHNT: {state['von']} --{state['typ']}--> {state['zu']}"
    AUDIT_LOG.append(eintrag)
    print("AUDIT:", eintrag)
    return {"ergebnis": eintrag}

fg = StateGraph(FreigabeZustand)
fg.add_node("vorschlagen", vorschlagen)
fg.add_node("anlegen", anlegen)
fg.add_edge(START, "vorschlagen")
fg.add_edge("vorschlagen", "anlegen")
fg.add_edge("anlegen", END)
freigabe_app = fg.compile(checkpointer=MemorySaver())   # <- Checkpointer Pflicht!

def fakt_routine(von, typ, zu, grund, genehmigt):
    config = {"configurable": {"thread_id": f"freigabe-{von}-{zu}"}}
    lauf = freigabe_app.invoke({"von": von, "typ": typ, "zu": zu,
                                "grund": grund, "ergebnis": ""}, config)
    interrupts = lauf.get("__interrupt__")
    if interrupts:
        print("INTERRUPT:", interrupts[0].value["frage"])
        print("  Fakt  :", interrupts[0].value["fakt"])
        print("  Grund :", interrupts[0].value["grund"])
        lauf = freigabe_app.invoke(Command(resume=genehmigt), config)
    return lauf["ergebnis"]

kanten_vorher = len(graph.relationships())
print("Kanten vorher:", kanten_vorher, "\\n")

fakt_routine("Anna", "WORKS_ON", "AI Assistant", "Steht implizit im Firmenprofil.", True)
fakt_routine("Ben", "MANAGES", "Acme", "Vermutung ohne Beleg – riskant!", False)''',
        ),
        ("ex", {
            "titel": "Der Beweis: Genehmigung ändert, Ablehnung nicht",
            "ziel": "Du führst den Freigabe-Workflow EINMAL genehmigend und EINMAL ablehnend aus – und weist die Wirkung auf den Graph nach.",
            "anforderungen": [
                "Zähle die Kanten des Graphs vor dem Test.",
                "Führe `fakt_routine(...)` mit einem **sinnvollen** Fakt (z. B. `Clara LEADS Engineering`) und `genehmigt=True` aus – und trage die Kante danach WIRKLICH in den Graph ein (mit `find_node`-Entity-Resolution!).",
                "Führe einen **riskanten** Fakt mit `genehmigt=False` aus – der Graph bleibt unverändert.",
                "Gib das Audit-Log und die Kantenanzahl nachher aus.",
            ],
            "starter": '''\
# YOUR CODE HERE: Kanten vorher zaehlen

# YOUR CODE HERE: genehmigter Fakt (+ Eintrag im Graph mit Entity Resolution)

# YOUR CODE HERE: abgelehnter Fakt (KEIN Eintrag!)

# YOUR CODE HERE: Audit-Log + Kanten nachher ausgeben''',
            "kriterien": [
                "Nach Genehmigung ist die Kantenanzahl um genau 1 gestiegen.",
                "Nach Ablehnung hat sich nichts verändert (kein Crash, kein Eintrag).",
                "Beide Ereignisse stehen im Audit-Log.",
            ],
            "checks": '''\
assert len(graph.relationships()) == kanten_vorher + 1, \\
    f"Erwartet {kanten_vorher + 1} Kanten (Genehmigung +1, Ablehnung +0), hat {len(graph.relationships())}."
genehmigt_im_log = any("GENEHMIGT" in e for e in AUDIT_LOG)
abgelehnt_im_log = any("ABGELEHNT" in e for e in AUDIT_LOG)
assert genehmigt_im_log and abgelehnt_im_log, "Beide Entscheidungen muessen im Audit-Log stehen!"
print("Alle Prüfungen bestanden! ✅ Freigabe und Ablehnung wirken nachweislich korrekt.")''',
            "hinweise": [
                "Für den Eintrag: `von_node = graph.find_node(None, name=von)` und `zu_node = graph.find_node(None, name=zu)` – dann `graph.add_relationship(von_node.id, zu_node.id, typ)`.",
                "Falls ein Node fehlt: erst anlegen (`add_node`) – das ist Entity Resolution aus Lektion 12!",
                "Die Kanten-Zählung: `len(graph.relationships())`.",
            ],
            "loesung": '''\
kanten_vorher = len(graph.relationships())
print("Kanten vorher:", kanten_vorher)

# 1) Genehmigter Fakt -> WIRKLICH eintragen:
clara = graph.find_node("Person", name="Clara")
if clara is None:
    clara_id = graph.add_node(["Person"], name="Clara", rolle="Abteilungsleitung")
else:
    clara_id = clara.id
engineering_node = graph.find_node("Department", name="Engineering")
graph.add_relationship(clara_id, engineering_node.id, "LEADS")
fakt_routine("Ben", "MANAGES", "Acme", "Vermutung ohne Beleg.", False)

print("Kanten nachher:", len(graph.relationships()))
print("Audit-Log:")
for eintrag in AUDIT_LOG:
    print("  -", eintrag)''',
            "loesung_md": "Der entscheidende Architektur-Moment: Der **Workflow** entscheidet (mit dir als Bremse), "
                          "ob der Fakt Wirklichkeit wird – aber das **tatsächliche Schreiben** macht dein Code danach "
                          "kontrolliert mit Entity Resolution. Genau dieses Muster (propose → approve → write + audit) "
                          "läuft im Finale über HTTP (Lektion 19)!",
            "reflexion": [
                "1. Vergleiche mit Build 1 und 2: Was kann dein Assistent jetzt, das beide gemeinsam nicht konnten? (→ docs/same-problem-three-architectures.md)",
                "2. Warum reicht die lesende Whitelist aus Lektion 12 nicht mehr, sobald das System \"aus Dokumenten lernen\" soll?",
            ],
        }),
    ],
    "weiter": "**🤖 Lektion 16:** `notebooks/09_agents/16_tools_und_agenten.ipynb` – "
              "Agenten-Vertiefung: Werkzeuge, mit denen das Modell selbst entscheiden darf.",
}

SPECS_E = [NB_13, NB_14, NB_15]
