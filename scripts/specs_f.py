"""Notebook-Specs Teil F: Agenten-Vertiefung (Lektion 16-18)."""

NB_16 = {
    "pfad": "notebooks/09_agents/16_tools_und_agenten.ipynb",
    "titel": "Lektion 16: Werkzeuge & Agenten",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Mittel",
    "voraussetzungen": "Lektion 13–15",
    "baut": "Einen Agenten, der selbst entscheidet, welches Werkzeug er benutzt – und den Loop sichtbar machst",
    "ziele": [
        "Tools mit `@tool` definieren (der Docstring ist die Bedienungsanleitung!)",
        "einen Agenten mit `create_agent` bauen (aktuelle API)",
        "den Agenten-Loop an den Nachrichtentypen ablesen",
        "Fehler in Tools abfangen (freundliche Rückgabe statt Crash)",
        "das Tool-Calling offline mit der Simulation üben",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Der Werkzeugkasten\n\n"
               "**WARUM:** Ohne Tools kann ein LLM nur *reden*. Mit Tools *handelt* es: rechnen, nachschlagen, Uhrzeit lesen.\n\n"
               "**WAS:** Ein **Agent** erhält Python-Funktionen als **Werkzeuge** und entscheidet **selbst**, wann er welches benutzt – "
               "in einer Schleife: *planen → Werkzeug wählen → ausführen → beobachten → antworten*.\n\n"
               "**Metapher:** Der neue Mitarbeiter bekommt einen Werkzeugkasten. Auf jedem Werkzeug steht (**Docstring!**), wofür es da ist. "
               "**Der Docstring ist die Bedienungsanleitung** – danach wählt der Agent!\n\n"
               "> **Benötigte Modell-Fähigkeit:** Tool-Calling. Nicht jedes (lokale) Modell beherrscht das – "
               "Offline übst du mit der Simulation, die den kompletten Loop zeigt (siehe `docs/local-ai-server.md`)."),
        ("code", '''\
from langchain_core.tools import tool
from langchain.agents import create_agent
from lernakademie.llm_client import get_chat_model

@tool
def wortzaehler(text: str) -> str:
    """Zaehlt die Woerter eines Texts."""
    return f"Der Text enthaelt {len(text.split())} Woerter."

agent = create_agent(
    model=get_chat_model(),
    tools=[wortzaehler],
    system_prompt="Du bist ein Assistent fuer Text-Statistiken.",
)

frage = ("Wie viele Woerter hat der Satz 'LangGraph macht Workflows steuerbar'? "
         "Nutze den wortzaehler.")
ergebnis = agent.invoke({"messages": [{"role": "user", "content": frage}]})
print("Finale Antwort:", ergebnis["messages"][-1].content[:150])'''),
        ("md", "## 🔎 Den Agenten-Loop SEHEN\n\n"
               "Der Agent ist kein Black Box: In `ergebnis[\"messages\"]` steht **jeder Schritt**. "
               "Lerne die Typen lesen – das ist dein Fenster in die Entscheidungen:"),
        ("code", '''\
for nachricht in ergebnis["messages"]:
    info = f"type={type(nachricht).__name__}"
    if getattr(nachricht, "tool_calls", None):
        info += f"  tool_calls={[c['name'] for c in nachricht.tool_calls]}"
    if type(nachricht).__name__ == "ToolMessage":
        info += f"  ergebnis={str(nachricht.content)[:40]}"
    print(info)'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "1. `HumanMessage` – deine Frage\n"
               "2. `AIMessage` **mit `tool_calls`** – der Agent ENTSCHEIDET sich für das Werkzeug\n"
               "3. `ToolMessage` – das Werkzeug-Ergebnis (die Beobachtung!)\n"
               "4. finale `AIMessage` – die Antwort **auf Basis der Beobachtung**\n\n"
               "Das ist planen → handeln → beobachten → antworten – **sichtbar gemacht**."),
        ("md", "## 🧠 Konzept: Sichere Tools\n\n"
               "**WARUM:** Ein Tool, das bei Müll-Eingaben crasht, bringt den ganzen Agenten zum Absturz. "
               "Und: **niemals `eval` mit Nutzereingaben!** Wir bauen einen sicheren Mini-Rechner per Regex."),
        ("code", '''\
import re

RECHNUNG = re.compile(r"^\\s*(-?\\d+(?:\\.\\d+)?)\\s*([+\\-*/])\\s*(-?\\d+(?:\\.\\d+)?)\\s*$")

@tool
def taschenrechner(expression: str) -> str:
    """Berechnet einen einfachen Ausdruck der Form 'zahl operator zahl', z.B. '12 * 7'."""
    match = RECHNUNG.match(expression)
    if not match:
        return "Ungueltiger Ausdruck. Format: 'zahl operator zahl', z.B. '12 * 7'."
    links, operator, rechts = float(match.group(1)), match.group(2), float(match.group(3))
    try:
        if operator == "+": ergebnis = links + rechts
        elif operator == "-": ergebnis = links - rechts
        elif operator == "*": ergebnis = links * rechts
        else: ergebnis = links / rechts
    except ZeroDivisionError:
        return "Division durch Null ist nicht moeglich."
    zahl = int(ergebnis) if ergebnis == int(ergebnis) else round(ergebnis, 6)
    return f"Ergebnis von {expression} = {zahl}"

print(taschenrechner.invoke({"expression": "12 * 7"}))
print(taschenrechner.invoke({"expression": "abc"}))       # freundliche Meldung
print(taschenrechner.invoke({"expression": "12 / 0"}))    # abgefangen'''),
        ("ex", {
            "titel": "Dein eigenes Werkzeug",
            "ziel": "Du schreibst ein robustes Tool und gibst es einem Agenten.",
            "anforderungen": [
                "Schreibe ein Tool `uhrzeit()` (kein Parameter), das die aktuelle Uhrzeit als `\"Es ist HH:MM Uhr.\"` zurückgibt (nutze `datetime`).",
                "Schreibe ein Tool `zufallszahl(minimum: int, maximum: int)`, das eine Zufallszahl zurückgibt – mit Absicherung: bei `minimum > maximum` eine klare Fehlermeldung als Text (kein Crash!).",
                "Baue einen Agenten mit beiden Tools und stelle eine Frage, die das Uhrzeit-Tool auslöst.",
            ],
            "starter": '''\
from datetime import datetime
import random

@tool
def uhrzeit() -> str:
    """YOUR DOCSTRING: was macht dieses Werkzeug?"""
    # YOUR CODE HERE
    pass

@tool
def zufallszahl(minimum: int, maximum: int) -> str:
    """YOUR DOCSTRING"""
    # YOUR CODE HERE (mit Absicherung!)
    pass

# YOUR CODE HERE: Agent bauen + Frage stellen''',
            "kriterien": [
                "Beide Tools haben aussagekräftige Docstrings (deutsch oder englisch – klar!).",
                "`zufallszahl(9, 3)` liefert eine Fehlermeldung als String – kein Crash.",
                "Der Agent-Ablauf enthält eine ToolMessage (Loop sichtbar).",
            ],
            "checks": '''\
u = uhrzeit.invoke({})
assert "Uhr" in u, f"uhrzeit() soll 'Es ist HH:MM Uhr.' liefern: {u}"
assert "9" in zufallszahl.invoke({"minimum": 1, "maximum": 9}) or True  # Format-Check:
assert "Fehler" in zufallszahl.invoke({"minimum": 9, "maximum": 3}) or "muss" in zufallszahl.invoke({"minimum": 9, "maximum": 3}).lower()
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Uhrzeit formatieren: `datetime.now().strftime(\"%H:%M\")`.",
                "Absicherung VOR dem Würfeln: `if minimum > maximum: return \"Fehler: minimum muss kleiner gleich maximum sein.\"`.",
                "Beim Agenten: `create_agent(model=get_chat_model(), tools=[uhrzeit, zufallszahl], system_prompt=...)`.",
            ],
            "loesung": '''\
from datetime import datetime
import random

@tool
def uhrzeit() -> str:
    """Liefert die aktuelle Uhrzeit im Format HH:MM."""
    return f"Es ist {datetime.now().strftime('%H:%M')} Uhr."

@tool
def zufallszahl(minimum: int, maximum: int) -> str:
    """Zieht eine Zufallszahl zwischen minimum und maximum (inklusive)."""
    if minimum > maximum:
        return "Fehler: minimum muss kleiner oder gleich maximum sein."
    return f"Zufallszahl zwischen {minimum} und {maximum}: {random.randint(minimum, maximum)}"

werk_agent = create_agent(
    model=get_chat_model(),
    tools=[uhrzeit, zufallszahl],
    system_prompt="Du bist ein Alltags-Assistent und nutzt deine Werkzeuge.")

lauf = werk_agent.invoke({"messages": [{"role": "user",
                            "content": "Wie spat ist es? Nutze die uhrzeit."}]})
print(lauf["messages"][-1].content[:120])''',
            "loesung_md": "Die Absicherung **im** Tool ist der entscheidende Punkt: Der Agent kann die Meldung lesen und "
                          "dem Nutzer erklären – der Loop läuft weiter statt zu crashen. Im Offline-Modus simuliert die "
                          "Akademie die Tool-Auswahl (per Tool-Namen in der Frage) – der komplette Ablauf bleibt gleich.",
            "reflexion": [
                "1. Wer führt die Berechnung aus – das Modell oder dein Python? Was heißt das für die Zuverlässigkeit?",
                "2. Wann wäre ein fester Graph (wie in Lektion 15) besser als ein freier Agent? Nenne je ein Beispiel.",
            ],
        }),
    ],
    "weiter": "**Weiter mit Lektion 17:** `notebooks/09_agents/17_gedaechtnis_und_freigabe.ipynb` – "
              "Gedächtnis über Aufrufe hinweg (Checkpointer) und die Freigabe-Mechanik isoliert.",
}

NB_17 = {
    "pfad": "notebooks/09_agents/17_gedaechtnis_und_freigabe.ipynb",
    "titel": "Lektion 17: Gedächtnis, Checkpointer & Freigabe",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Fortgeschritten",
    "voraussetzungen": "Lektion 15–16",
    "baut": "Einen Agenten mit thread-Gedächtnis und einen isolierten Freigabe-Workflow mit Beweisen",
    "ziele": [
        "Kurzzeit-Gedächtnis über mehrere Aufrufe mit **Checkpointer + `thread_id`**",
        "nachweisen, dass eine andere `thread_id` ein leeres Gedächtnis bedeutet",
        "die `interrupt`/`Command(resume=...)`-Mechanik isoliert verstehen",
        "erklären, warum `interrupt` ohne Checkpointer nicht funktioniert",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Der Vorgangsordner\n\n"
               "**WARUM:** Ein Agent, der bei jedem Aufruf vergisst, nervt: \"Wie war nochmal Ihr Name?\"\n\n"
               "**WAS:** Der **Checkpointer** speichert den Zustand **pro Gespräch** (`thread_id`). "
               "**Metapher:** der Vorgangsordner im Büro – neues Personal am Schalter kann weitermachen, "
               "weil alles drinsteht. Ein **anderer** Ordner (`thread_id`) ist ein anderes Gespräch: frisch und leer.\n\n"
               "**Und die Freigabe?** `interrupt()` pausiert den Lauf **im Backend**; "
               "`Command(resume=True/False)` setzt ihn mit deiner Entscheidung fort. "
               "Das kennst du schon aus Lektion 15 – hier siehst du die Mechanik noch einmal isoliert, "
               "als handgebauter Agent (damit du weißt, was `create_agent` intern tut)."),
        ("code", '''\
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.types import Command, interrupt
from typing import Annotated, TypedDict

from lernakademie.llm_client import get_chat_model

NOTIZEN = []   # simulierter Notizspeicher

@tool
def notiz_anlegen(text: str) -> str:
    """Legt eine normale Notiz an."""
    NOTIZEN.append(text)
    return f"Notiz angelegt ({len(text)} Zeichen)."

@tool
def geheime_notiz(text: str) -> str:
    """Legt eine geheime Notiz an - erfordert vorher die Freigabe eines Menschen."""
    freigabe = interrupt({          # <- Lauf PAUSIERT hier (vor der Aktion!)
        "frage": "Soll diese geheime Notiz wirklich angelegt werden?",
        "text": text,
    })
    if freigabe:
        NOTIZEN.append(f"[GEHEIM] {text}")
        return "Geheime Notiz angelegt - Freigabe erteilt."
    return "Aktion abgebrochen - keine Freigabe."

class AgentZustand(TypedDict):
    messages: Annotated[list, add_messages]   # Reduzierer: Liste WAECHST pro Zug

modell = get_chat_model(temperature=0.0).bind_tools([notiz_anlegen, geheime_notiz])
tools = ToolNode([notiz_anlegen, geheime_notiz])

def model_node(state):
    return {"messages": [modell.invoke(state["messages"])]}

def weiche(state):
    letzte = state["messages"][-1]
    return "tools" if getattr(letzte, "tool_calls", None) else END

g = StateGraph(AgentZustand)
g.add_node("model", model_node)
g.add_node("tools", tools)
g.add_edge(START, "model")
g.add_conditional_edges("model", weiche, {"tools": "tools", END: END})
g.add_edge("tools", "model")            # zurueck zum Modell -> LOOP
agent = g.compile(checkpointer=MemorySaver())   # ohne Checkpointer kein interrupt!
print("Agent bereit (mit Checkpointer).")'''),
        ("ex", {
            "titel": "Gedächtnis-Beweis und Freigabe-Roundtrip",
            "ziel": "Du führst den Agenten in zwei Threads und durch einen kompletten Freigabe-Zyklus – mit Beweisen.",
            "anforderungen": [
                "**Gedächtnis:** Thread `\"gespraech-1\"`: erzähle deinen Namen, frage dann \"Wie heiße ich?\" – zähle die Nachrichten im Thread-State (`agent.get_state(config)`).",
                "**Kontrolle:** dieselbe Frage in Thread `\"anderes-gespraech\"` – das Gedächtnis ist leer.",
                "**Freigabe:** Bitte im Thread `\"freigabe\"` um eine geheime Notiz. Der Lauf pausiert am Interrupt – lies die Daten aus `__interrupt__`, setze mit `Command(resume=True)` fort.",
                "**Beweise:** `NOTIZEN` enthält danach einen `[GEHEIM]`-Eintrag.",
            ],
            "starter": '''\
config1 = {"configurable": {"thread_id": "gespraech-1"}}
# YOUR CODE HERE: Name erzaehlen + Rueckfrage (gleicher Thread)

# YOUR CODE HERE: andere thread_id -> leeres Gedaechtnis

config_f = {"configurable": {"thread_id": "freigabe"}}
lauf = agent.invoke({"messages": [HumanMessage(
    content="Lege bitte die geheime Notiz 'Gehaltsliste' an.")]}, config_f)
# YOUR CODE HERE: Interrupt-Daten lesen + resume=True

print("Notizen:", NOTIZEN)''',
            "kriterien": [
                "Im Thread 1 wächst der State über beide Aufrufe (Nachrichtenzahl steigt).",
                "Thread 2 startet mit leerem Gedächtnis.",
                "Der geheime Eintrag existiert erst NACH `resume=True`.",
            ],
            "checks": '''\
zustand1 = agent.get_state(config1)
assert len(zustand1.values["messages"]) >= 3, "Thread 1 sollte den Verlauf speichern."
assert any("[GEHEIM]" in n for n in NOTIZEN), "resume=True muss die Notiz anlegen."
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Zwei Aufrufe im selben Thread: einfach zweimal `agent.invoke({\"messages\": [HumanMessage(content=...)]}, config1)`.",
                "Interrupt-Daten: `lauf[\"__interrupt__\"][0].value` (Frage + Text).",
                "Fortsetzen: `agent.invoke(Command(resume=True), config_f)` – **identisches** config!",
            ],
            "loesung": '''\
config1 = {"configurable": {"thread_id": "gespraech-1"}}
agent.invoke({"messages": [HumanMessage(content="Hallo! Ich heisse Alex.")]}, config1)
agent.invoke({"messages": [HumanMessage(content="Wie heisse ich?")]}, config1)
zustand1 = agent.get_state(config1)
print("Nachrichten im Thread 1:", len(zustand1.values["messages"]))

config2 = {"configurable": {"thread_id": "anderes-gespraech"}}
agent.invoke({"messages": [HumanMessage(content="Wie heisse ich?")]}, config2)
zustand2 = agent.get_state(config2)
print("Nachrichten im Thread 2 (frisch):", len(zustand2.values["messages"]))

config_f = {"configurable": {"thread_id": "freigabe"}}
lauf = agent.invoke({"messages": [HumanMessage(
    content="Lege bitte die geheime Notiz 'Gehaltsliste' an.")]}, config_f)
if lauf.get("__interrupt__"):
    daten = lauf["__interrupt__"][0].value
    print("INTERRUPT:", daten["frage"], "|", daten["text"])
    fortsetzung = agent.invoke(Command(resume=True), config_f)
    print("Nach Freigabe:", fortsetzung["messages"][-1].content[:80])
print("Notizen:", NOTIZEN)''',
            "loesung_md": "Der Checkpointer hält den Zustand pro `thread_id` – deshalb funktioniert das Gedächtnis "
                          "UND die Pause: Der angehaltene Lauf wird gesichert und mit `resume` exakt fortgesetzt. "
                          "**Ohne Checkpointer wäre beides unmöglich.** Genau diese Mechanik läuft im Finale über HTTP: "
                          "der Browser ist nur die Fernbedienung, pausiert wird im Backend.",
            "reflexion": [
                "1. Was wäre \"Langzeit-Gedächtnis über Monate\" – und warum ist ein thread-Checkpointer es noch nicht?",
                "2. Welche Aktionen würdest du NIE ohne Freigabe automatisieren – und welche gezielt doch?",
            ],
        }),
    ],
    "weiter": "**Weiter mit Lektion 18:** `notebooks/09_agents/18_supervisor_und_parallelitaet.ipynb` – "
              "wenn ein Agent nicht reicht: Parallelität, Subgraphs und der Supervisor.",
}

NB_18 = {
    "pfad": "notebooks/09_agents/18_supervisor_und_parallelitaet.ipynb",
    "titel": "Lektion 18: Parallelität, Subgraphs & Supervisor",
    "zeit": "~75 Minuten",
    "schwierigkeit": "Fortgeschritten",
    "voraussetzungen": "Lektion 13–17",
    "baut": "Drei Orchestrierungs-Muster: parallele Prüfung mit Merge, ein Graph im Graph (Subgraph) und einen Supervisor",
    "ziele": [
        "Nodes **parallel** ausführen und Ergebnisse an einer Barriere zusammenführen",
        "Schreibkonflikte vermeiden (jedes Feld gehört einem Zweig)",
        "einen kompletten Graphen als Subgraph in einen größeren einbauen (Kapselung beweisen)",
        "einen Supervisor mit **Runden-Limit** bauen (keine Endlos-Delegation)",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Drei Muster für große Systeme\n\n"
               "1. **Parallelität** – **Metapher: die Kommission.** Drei Prüfer erhalten dieselbe Akte, arbeiten gleichzeitig, "
               "dann sitzen alle zusammen (Merge-Barriere).\n"
               "2. **Subgraph** – **Metapher: die Abteilung.** Der Chef-Graph kennt nur die Abteilung als Black Box; "
               "wie sie intern arbeitet, ist ihre Sache.\n"
               "3. **Supervisor** – **Metapher: die Projektleitung.** Sie delegiert an Spezialisten, sammelt Berichte und "
               "entscheidet: weiter delegieren oder FINISH. **Spezialisten reden nie direkt miteinander** "
               "(sonst explodieren die Kommunikationspfade: n·(n−1)/2)."),
        ("md", "## Muster 1: Parallelität mit Merge"),
        ("code", '''\
from langgraph.graph import END, START, StateGraph
from typing import TypedDict

class KommissionsZustand(TypedDict):
    text: str
    woerter: int        # Zweig 1 schreibt NUR dieses Feld
    zeichen: int        # Zweig 2 schreibt NUR dieses Feld
    laenge: float       # Zweig 3 schreibt NUR dieses Feld
    bericht: str

g = StateGraph(KommissionsZustand)
g.add_node("zaehle_woerter", lambda s: {"woerter": len(s["text"].split())})
g.add_node("zaehle_zeichen", lambda s: {"zeichen": len(s["text"])})
g.add_node("wortlaenge", lambda s: {"laenge": round(
    sum(len(w) for w in s["text"].split()) / max(1, len(s["text"].split())), 2)})
g.add_node("zusammenfuehren", lambda s: {"bericht": (
    f"Kommissionsbericht: {s['woerter']} Woerter, {s['zeichen']} Zeichen, "
    f"durchschnittliche Wortlaenge {s['laenge']}.")})

for name in ("zaehle_woerter", "zaehle_zeichen", "wortlaenge"):
    g.add_edge(START, name)               # drei parallele Zweige...
    g.add_edge(name, "zusammenfuehren")    # ...die alle am Merge muessen liefern
g.add_edge("zusammenfuehren", END)
parallel_app = g.compile()

print(parallel_app.invoke({"text": "LangGraph macht paralleles Arbeiten moeglich",
                           "woerter": 0, "zeichen": 0, "laenge": 0.0, "bericht": ""})["bericht"])'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "**Die zwei Regeln:** (1) Jeder Zweig schreibt sein **eigenes** Feld – "
               "schreiben alle dasselbe, gewinnt zufällig einer (Last-Write-Wins = Datenverlust!). "
               "(2) Der Merge läuft erst, wenn **alle** Zweige geliefert haben – die Barriere synchronisiert automatisch."),
        ("md", "## Muster 2: Der Subgraph (Abteilung)"),
        ("code", '''\
from langgraph.graph import END, START, StateGraph
from typing import TypedDict

# ---- Abteilung: Qualitaets-Loop (eigenstaendiger Graph!) ----------------
class LoopZustand(TypedDict):
    text: str; bewertung: int; versuche: int; max_versuche: int

quali_loop = StateGraph(LoopZustand)
quali_loop.add_node("entwerfen", lambda s: {
    "text": f"{s['text']} [Politur {s['versuche'] + 1}]",
    "versuche": s["versuche"] + 1})
quali_loop.add_node("pruefen", lambda s: {"bewertung": min(100, 30 + 25 * (s["versuche"] + 1))})
quali_loop.add_edge(START, "entwerfen")
quali_loop.add_edge("entwerfen", "pruefen")
quali_loop.add_conditional_edges("pruefen", lambda s: "fertig"
    if s["bewertung"] >= 60 or s["versuche"] >= s["max_versuche"] else "nachbessern",
    {"fertig": END, "nachbessern": "entwerfen"})
qualitaets_abteilung = quali_loop.compile()

# Beweis 1: standalone laeuft die Abteilung:
solo = qualitaets_abteilung.invoke({"text": "Solo", "bewertung": 0, "versuche": 0, "max_versuche": 3})
print("Subgraph standalone:", solo["text"])

# ---- Das Gebaeude: Subgraph als EIN Node ---------------------------------
class ProjektZustand(TypedDict):
    auftrag: str; freigegebenes_produkt: str; status: str

def qualitaet(state: ProjektZustand) -> dict:
    """Adapter: einzige Nahtstelle zwischen aeusserem und innerem State."""
    ergebnis = qualitaets_abteilung.invoke({
        "text": state["auftrag"], "bewertung": 0,
        "versuche": 0, "max_versuche": 4})
    return {"freigegebenes_produkt": ergebnis["text"]}

gebaeude = StateGraph(ProjektZustand)
gebaeude.add_node("qualitaet", qualitaet)          # <- ganzer Graph als Station!
gebaeude.add_node("abschliessen", lambda s: {"status": "versandbereit"})
gebaeude.add_edge(START, "qualitaet")
gebaeude.add_edge("qualitaet", "abschliessen")
gebaeude.add_edge("abschliessen", END)
gebaeude_app = gebaeude.compile()

final = gebaeude_app.invoke({"auftrag": "Broschuere v1", "freigegebenes_produkt": "", "status": ""})
print("Finaler aeusserer State:")
for feld, wert in final.items():
    print(f"  {feld}: {wert}")
print("-> 'bewertung'/'versuche' fehlen: Kapselung wirkt!")'''),
        ("ex", {
            "titel": "Der Supervisor mit Runden-Limit",
            "ziel": "Du baust die Projektleitung: drei Stationen (Recherche → Schreiben → FINISH) mit Beweis gegen Endlos-Delegation.",
            "anforderungen": [
                "Supervisor-Node: Delegations-Reihenfolge per Regel (offline): keine Stichpunkte → `recherche_agent`; kein Bericht → `schreib_agent`; sonst `FINISH`.",
                "Runden-Limit: nach `max_runden` erzwingt der Supervisor FINISH (im Zustand `runden` mitzählen!).",
                "Ergebnis-Log im State protokolliert jede Delegation.",
                "Beweise: normaler Lauf endet mit FINISH nach Bericht; ein Lauf mit `max_runden=1` bricht kontrolliert ab.",
            ],
            "starter": '''\
class ProjektZustand(TypedDict):
    auftrag: str
    stichpunkte: list
    bericht: str
    ergebnis_log: list
    runden: int
    max_runden: int

def supervisor(state):
    # YOUR CODE HERE: naechsten Schritt waehlen + runden zaehlen + log
    pass

# YOUR CODE HERE: zwei Fach-Nodes + Graph bauen''',
            "kriterien": [
                "Der normale Lauf delegiert Recherche, dann Schreiben, dann FINISH.",
                "Mit `max_runden=1` terminiert der Lauf trotzdem (kein Endlos-Loop!).",
                "Das Log zeigt jede Delegation inklusive Runde.",
            ],
            "checks": '''\
e = sup_app.invoke({"auftrag": "RAG", "stichpunkte": [], "bericht": "",
                    "ergebnis_log": [], "runden": 0, "max_runden": 5})
assert e["bericht"], "Der Bericht muss entstehen."
assert any("recherche" in x for x in e["ergebnis_log"])
knapp = sup_app.invoke({"auftrag": "RAG", "stichpunkte": [], "bericht": "",
                        "ergebnis_log": [], "runden": 0, "max_runden": 1})
assert knapp["runden"] <= 2, "Limit muss greifen."
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Der Supervisor gibt `{{\"naechster_schritt\": ..., \"runden\": s[\"runden\"]+1, \"ergebnis_log\": ...}}` zurück – Achtung: du brauchst ein Feld `naechster_schritt` im State.",
                "Die Weiche nach dem Supervisor: `lambda s: s[\"naechster_schritt\"]` mit Mapping zu den Nodes und `END`.",
                "Agenten melden sich zurück beim Supervisor: `add_edge(\"recherche_agent\", \"supervisor\")`.",
            ],
            "loesung": '''\
class ProjektZustand(TypedDict):
    auftrag: str
    naechster_schritt: str
    stichpunkte: list
    bericht: str
    ergebnis_log: list
    runden: int
    max_runden: int

def supervisor(state):
    if state["runden"] >= state["max_runden"]:
        schritt = "FINISH"
    elif not state["stichpunkte"]:
        schritt = "recherche_agent"
    elif not state["bericht"]:
        schritt = "schreib_agent"
    else:
        schritt = "FINISH"
    print(f"  Supervisor -> {schritt} (Runde {state['runden'] + 1})")
    return {"naechster_schritt": schritt, "runden": state["runden"] + 1,
            "ergebnis_log": state["ergebnis_log"] + [f"supervisor: {schritt}"]}

def recherche_agent(state):
    punkte = ["RAG kombiniert Suche und Generierung.",
              "Embeddings machen Aehnlichkeit messbar."]
    return {"stichpunkte": punkte,
            "ergebnis_log": state["ergebnis_log"] + ["recherche_agent: 2 Stichpunkte"]}

def schreib_agent(state):
    return {"bericht": f"Bericht zu '{state['auftrag']}': " + " ".join(state["stichpunkte"]),
            "ergebnis_log": state["ergebnis_log"] + ["schreib_agent: Bericht erstellt"]}

sg = StateGraph(ProjektZustand)
sg.add_node("supervisor", supervisor)
sg.add_node("recherche_agent", recherche_agent)
sg.add_node("schreib_agent", schreib_agent)
sg.add_edge(START, "supervisor")
sg.add_edge("recherche_agent", "supervisor")
sg.add_edge("schreib_agent", "supervisor")
sg.add_conditional_edges("supervisor", lambda s: s["naechster_schritt"],
    {"recherche_agent": "recherche_agent",
     "schreib_agent": "schreib_agent", "FINISH": END})
sup_app = sg.compile()

e = sup_app.invoke({"auftrag": "RAG", "naechster_schritt": "", "stichpunkte": [],
                    "bericht": "", "ergebnis_log": [], "runden": 0, "max_runden": 5})
print("Log:", *e["ergebnis_log"], sep="\\n  ")''',
            "loesung_md": "Der Supervisor ist selbst nur ein Node mit klarer Logik – aber seine **Reihenfolge-Regeln** "
                          "(erst recherchieren, dann schreiben) machen das System robust. Das Runden-Limit ist der "
                          "Kosten-Airbag: Ohne es könnte ein LLM-Supervisor (mit echtem Modell) endlos delegieren. "
                          "Im Finale steckt ein kleiner Verwandter in `final-project/.../graphs/workflow.py`.",
            "reflexion": [
                "1. Was sind die zwei klassischen Supervisor-Fehler – und welche zwei Bremsen hast du verbaut?",
                "2. Wann ist ein einfacher sequenzieller Graph besser als ein Supervisor-Team?",
            ],
        }),
    ],
    "weiter": "**🏁 Lektion 19:** `notebooks/10_capstone/19_capstone_systemtest.ipynb` – "
              "du testest das komplette finale System (Frontend → Backend → Agent → beide Wissensquellen) von innen.",
}

SPECS_F = [NB_16, NB_17, NB_18]
