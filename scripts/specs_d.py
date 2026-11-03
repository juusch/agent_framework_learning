"""Notebook-Specs Teil D: Knowledge Graphs (Lektion 10-12)."""

NB_10 = {
    "pfad": "notebooks/06_knowledge_graph/10_graphen_in_python.ipynb",
    "titel": "Lektion 10: Knowledge Graphs – Wissen als Beziehungen",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Mittel",
    "voraussetzungen": "Lektion 01–09 (besonders Build 2 und seine Grenze)",
    "baut": "Deinen ersten Knowledge Graph – zuerst als reines Python-Dict, dann als echte Graph-Datenstruktur",
    "ziele": [
        "erklären, warum Beziehungsfragen („Wer arbeitet woran?\") Text-Suche sprengen",
        "einen Graph als Python-Dictionary darstellen (Nodes, Kanten, Properties)",
        "mit dem `GraphStore` Nodes, Labels und Beziehungen anlegen",
        "per **Traversierung** Fragen beantworten, die in keinem Text stehen (**Emergenz**)",
        "den Graph als Mermaid-Diagramm visualisieren",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Das Ermittlungsbrett\n\n"
               "**WARUM:** Stell die Frage **„Wie hängt Ben mit dem AI-Assistant-Projekt zusammen?\"** – "
               "kein Abschnitt der Dokumente enthält diesen Satz! Text-Suche (Build 2) findet sinngleiche **Texte**, "
               "aber folgt **keinen Verbindungen**.\n\n"
               "**WAS:** Ein **Knowledge Graph** speichert Wissen als **Entities** (Dinge) und **Relationships** (Verbindungen). "
               "**Metapher:** das **Ermittlungsbrett** aus Krimiserien: Fotos (Nodes) an einer Pinnwand, "
               "verbunden mit roten Fäden (Relationships), Notizen an jedem Foto (Properties). "
               "Einem Faden nachgehen (**Traversierung**) enthüllt Muster, die auf keinem einzelnen Foto stehen.\n\n"
               "**Wichtig:** Der Graph speichert Verbindungen **als Daten** – nicht als Sätze in Textform. "
               "Dadurch ist „Wer arbeitet woran?\" eine *strukturelle* Frage, keine Textsuche."),
        ("md", "## Schritt 1: Der Graph als pure Python-Datenstruktur\n\n"
               "Zuerst – wie bei Build 1! – ganz ohne Werkzeug: ein Dictionary. "
               "Jede Person mappt auf das, womit sie verbunden ist:"),
        ("code", '''\
graph_als_dict = {
    "Anna": ["Acme", "Engineering", "AI Assistant"],
    "Ben": ["Acme", "Data & Analytics"],
    "Engineering": ["AI Assistant"],
}

# Frage: Mit wem/ was ist Anna verbunden?
print("Anna verbunden mit:", graph_als_dict["Anna"])
print("Ben verbunden mit:", graph_als_dict["Ben"])'''),
        ("md", "### 🔎 Was sehen wir hier – und was fehlt?\n"
               "Das Dict kann already Verbindungen speichern – aber es fehlen: **Richtungen** (wer → wen?), "
               "**Typen** der Verbindung (arbeitet_für? gehört_zu?) und **Notizen** (Properties). "
               "Für echte Anwendungen brauchen wir mehr Struktur – und die kommt jetzt."),
        ("md", "## Schritt 2: Der GraphStore (unser Trainings-Graph)\n\n"
               "Die Akademie enthält `lernakademie.graph_store.GraphStore` – das Python-Pendant zu einer Graph-Datenbank "
               "(wie der Mock zum LLM). Konzepte, die du hier lernst, gelten 1:1 in **Neo4j** (Lektion 11).\n\n"
               "**Vokabular:**\n"
               "- **Node** = Karteikarte mit **Label** (Typ, z. B. `Person`) und **Properties** (`name`, `rolle`)\n"
               "- **Relationship** = gerichteter Faden mit **Typ** (`WORKS_FOR`) und optionalen Properties (`seit: 2021`)\n"
               "- **WICHTIG:** Kanten verbinden **IDs**, nie Namen – sonst werden zwei Annas zu einer!"),
        ("code", '''\
from lernakademie.graph_store import GraphStore

store = GraphStore()

# Nodes anlegen (IDs merken!)
anna = store.add_node(["Person"], name="Anna", rolle="Entwicklerin")
ben = store.add_node(["Person"], name="Ben", rolle="Analyst")
acme = store.add_node(["Company"], name="Acme", branche="Technologie")
engineering = store.add_node(["Department"], name="Engineering")
projekt = store.add_node(["Project"], name="AI Assistant", status="aktiv")

# Beziehungen (gerichtet: von -> zu, Typ in GROSSBUCHSTABEN)
store.add_relationship(anna, acme, "WORKS_FOR", seit=2021)
store.add_relationship(anna, engineering, "BELONGS_TO")
store.add_relationship(engineering, projekt, "WORKS_ON")
store.add_relationship(ben, acme, "WORKS_FOR")

print(f"{len(store.nodes())} Nodes, {len(store.relationships())} Kanten")
for node in store.nodes():
    print(" ", node.properties)'''),
        ("md", "## Schritt 3: Traversierung – den Fäden folgen\n\n"
               "Jetzt die Superkraft des Graphen: Fragen durch **Nachbarn folgen** beantworten."),
        ("code", '''\
anna_node = store.find_node("Person", name="Anna")
print("Annas direkte Nachbarn:")
for kante, ziel in store.neighbors(anna_node.id):
    print(f"  Anna --{kante.typ}--> {ziel.properties['name']}")'''),
        ("ex", {
            "titel": "Emergenz beweisen – zweistufige Traversierung",
            "ziel": "Du beantwortest eine Frage, die **in keinem Text steht** – nur durch Kombination von zwei Fäden.",
            "anforderungen": [
                "Schreibe `verbunden_ueber_zwei_schritte(store, start_name, ziel_name)`, das True/False zurückgibt, ob zwei Entities über maximal zwei Kanten verbunden sind (Nutze `neighbors` zweimal – kein `path`!).",
                "Wende es an: Ist **Ben** über zwei Schritte mit **AI Assistant** verbunden?",
                "Zusatzausgabe: Gib den gefundenen Weg lesbar aus (z. B. `Ben --WORKS_FOR--> Acme`…). Tipp: Ben → Acme ist ein Sackgasse – der Weg läuft über Data & Analytics, wenn du die Kante ergänzt! Füge dafür zunächst `BELONGS_TO` für Ben und `PROVIDES_DATA_FOR` für Data & Analytics hinzu (siehe Lösung).",
            ],
            "starter": '''\
# ZUSATZ-Kanten fuer den Emergenz-Beweis (fuer Ben):
daten_analytik = store.find_node("Department", name="Data & Analytics")
if daten_analytik is None:
    daten_analytik_id = store.add_node(["Department"], name="Data & Analytics")
else:
    daten_analytik_id = daten_analytik.id
# YOUR CODE HERE: Ben BELONGS_TO Data & Analytics
# YOUR CODE HERE: Data & Analytics PROVIDES_DATA_FOR AI Assistant

def verbunden_ueber_zwei_schritte(store, start_name, ziel_name):
    # YOUR CODE HERE
    pass

print(verbunden_ueber_zwei_schritte(store, "Ben", "AI Assistant"))''',
            "kriterien": [
                "Ben ist über zwei Schritte mit AI Assistant verbunden (True) – über Data & Analytics.",
                "Die Funktion nutzt zwei verschachtelte `neighbors`-Aufrufe (kein `path`).",
                "Der Weg wird lesbar ausgegeben.",
            ],
            "checks": '''\
assert verbunden_ueber_zwei_schritte(store, "Ben", "AI Assistant") is True, \
    "Ben sollte (ueber Data & Analytics) mit dem Projekt verbunden sein!"
assert verbunden_ueber_zwei_schritte(store, "Anna", "Acme") is True
print("Alle Prüfungen bestanden! ✅ Der Weg existiert – obwohl er in keinem Text steht.")''',
            "loesung": '''\
daten_node = store.find_node("Department", name="Data & Analytics")
if daten_node is None:
    daten_analytik_id = store.add_node(["Department"], name="Data & Analytics")
else:
    daten_analytik_id = daten_node.id

ben_node = store.find_node("Person", name="Ben")
projekt_node = store.find_node("Project", name="AI Assistant")
store.add_relationship(ben_node.id, daten_analytik_id, "BELONGS_TO")
store.add_relationship(daten_analytik_id, projekt_node.id, "PROVIDES_DATA_FOR")

def verbunden_ueber_zwei_schritte(store, start_name, ziel_name):
    start = store.find_node(None, name=start_name)
    if start is None:
        return False
    for kante1, nachbar in store.neighbors(start.id):
        if nachbar.properties.get("name") == ziel_name:
            return True
        for kante2, ziel2 in store.neighbors(nachbar.id):
            if ziel2.properties.get("name") == ziel_name:
                print(f"  Weg: {start_name} --{kante1.typ}--> "
                      f"{nachbar.properties['name']} --{kante2.typ}--> {ziel_name}")
                return True
    return False

print(verbunden_ueber_zwei_schritte(store, "Ben", "AI Assistant"))''',
            "loesung_md": "Der Weg `Ben --BELONGS_TO--> Data & Analytics --PROVIDES_DATA_FOR--> AI Assistant` "
                          "steht **nirgends** in den Dokumenten als Satz – er entsteht durch das **Kombinieren** zweier Fakten. "
                          "Das ist **Emergenz**: Wissen, das größer ist als die Summe seiner Teile. "
                          "Genau hier liegt der Grund, warum Build 3 einen Knowledge Graph braucht.",
            "reflexion": [
                "1. Formuliere eine Frage aus deinem Leben, die ein Graph leicht, ein Textarchiv schwer beantwortet.",
                "2. Was würde passieren, wenn du Beziehungen als Property modellieren würdest (`arbeite_bei: \"Acme\"`) statt als Kante?",
            ],
            "challenge": ("Erzeuge mit `store.to_mermaid()` den Diagramm-Code und speichere ihn in eine Datei `mein_graph.md` "
                          "(mit ```mermaid-Block) – GitHub rendert ihn!",
                          '''\
# YOUR CODE HERE (Challenge)'''),
        }),
    ],
    "weiter": "**Weiter mit Lektion 11:** `notebooks/06_knowledge_graph/11_neo4j_und_cypher.ipynb` – "
              "dieselben Konzepte in einer **echten Graph-Datenbank** mit der Abfragesprache **Cypher**.",
}

NB_11 = {
    "pfad": "notebooks/06_knowledge_graph/11_neo4j_und_cypher.ipynb",
    "titel": "Lektion 11: Neo4j & Cypher – die echte Graph-Datenbank",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Mittel",
    "voraussetzungen": "Lektion 10",
    "baut": "Deine ersten Cypher-Abfragen – gegen echtes Neo4j (Docker) oder den Offline-Fallback",
    "ziele": [
        "erklären, was eine Graph-Datenbank gegenüber dem RAM-GraphStore bietet (Persistenz, Abfragesprache)",
        "Neo4j per Docker starten (oder bewusst den Offline-Fallback nutzen)",
        "Cypher-Grundmuster lesen und schreiben (`MATCH ... RETURN`, Kanten-Muster)",
        "Python mit Neo4j verbinden – mit **MERGE** (idempotent!) und **Parametern** (Injection-Schutz)",
        "die lesende Sicherheits-Whitelist verstehen",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Vom RAM in die Datenbank\n\n"
               "**WARUM:** Dein GraphStore lebt im Arbeitsspeicher – Programm zu, Daten weg. "
               "Und echte Datenbanken können Abfragen, die unser einfacher Store nicht kann.\n\n"
               "**WAS:** **Neo4j** ist die bekannteste Graph-Datenbank: persistent, mehrnutzerfähig, mit eigener Abfragesprache **Cypher**.\n\n"
               "**Metapher Cypher = ASCII-Art:** In SQL beschreibst du Verknüpfungslogik abstrakt. "
               "In Cypher **zeichnest du das gesuchte Muster wörtlich**:\n\n"
               "```cypher\nMATCH (a:Person)-[:WORKS_FOR]->(c:Company) RETURN a, c\n```\n\n"
               "Klammern sind Nodes, `[:WORKS_FOR]` die Kante, `->` die Richtung – wer Graphen denken kann, kann Cypher **lesen**."),
        ("md", "## Setup: Zwei Wege (du entscheidest)\n\n"
               "**Weg A – Docker (empfohlen, wenn verfügbar):**\n"
               "```bash\ndocker run -d --name neo4j-academy -p 7474:7474 -p 7687:7687 \\\\\n  -e NEO4J_AUTH=neo4j/lernakademie neo4j:5\n```\n"
               "Danach im Browser: http://localhost:7474 (Login: `neo4j` / `lernakademie`).\n\n"
               "**Weg B – Offline-Fallback (immer möglich):** Der GraphStore versteht einen kleinen lesenden Cypher-Subset – "
               "dieselben Muster, keine Installation. **Das Notebook läuft in beiden Fällen.**"),
        ("code", '''\
from lernakademie.graph_store import baue_beispiel_graph

# Vier Standard-Muster (funktionieren in Neo4j UND im Fallback):
ABFRAGEN = [
    ("Alle Personen", "MATCH (n:Person) RETURN n"),
    ("Eine bestimmte Person", "MATCH (n:Person) WHERE n.name = 'Anna' RETURN n"),
    ("Wer arbeitet wo?", "MATCH (a:Person)-[r:WORKS_FOR]->(c:Company) RETURN a, c"),
    ("Alles von Anna (mit Kantentyp)", "MATCH (a {name: 'Anna'})-[r]->(b) RETURN a, type(r), b"),
]

store = baue_beispiel_graph()
for name, abfrage in ABFRAGEN:
    ergebnis = store.run_cypher(abfrage)
    print(f"{name}  [{len(ergebnis)} Treffer]")'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Vier Muster, die du in fast jeder Graph-Anfrage wiederfindest: Label-Filter (`:Person`), "
               "Werte-Bedingung (`WHERE`), Kanten-Muster (`-[r:TYP]->`) und der `type(r)`-Trick. "
               "**TRY:** Ändere `'Anna'` zu `'Ben'` und beobachte die Trefferzahl."),
        ("code", '''\
# SICHERHEIT: Der Fallback ist eine WHITELIST – nur lesende MATCH...RETURN!
for verboten in ("CREATE (n:Person {name: 'Boesewicht'})",
                 "MATCH (n) DETACH DELETE n"):
    try:
        store.run_cypher(verboten)
        print("FEHLER IM DESIGN: ausgefuehrt!", verboten)
    except ValueError as fehler:
        print("Korrekt abgelehnt:", verboten[:35], "->", str(fehler)[:50], "...")'''),
        ("md", "**WARUM die Ablehnung wichtig ist:** Später (Lektion 12) lässt du ein **LLM Cypher generieren**. "
               "Ein manipulierter Prompt könnte sonst `DELETE` erzeugen. Die Prüfung muss **deterministischer Code** sein – "
               "niemals ein LLM (Prompt 12 erklärt warum)."),
        ("md", "## Python ↔ Neo4j: die Brücke (mit Fallback)\n\n"
               "Die Brücke probiert echtes Neo4j; ist es nicht erreichbar, läuft derselbe Code gegen den Fallback:"),
        ("code", '''\
from lernakademie.graph_store import GraphStore

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORT = "lernakademie"

def verbinde():
    """Echtes Neo4j – oder None (dann nutzt der Aufrufer den Fallback)."""
    try:
        from neo4j import GraphDatabase
        treiber = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORT),
            connection_timeout=3)
        treiber.verify_connectivity()
        return treiber
    except Exception as fehler:
        print(f"Neo4j nicht erreichbar -> Offline-Fallback. ({str(fehler)[:50]}...)")
        return None

treiber = verbinde()
verwende_fallback = treiber is None
if verwende_fallback:
    store = baue_beispiel_graph()
else:
    treiber.close()
print("Modus:", "Fallback (GraphStore)" if verwende_fallback else "Echtes Neo4j")'''),
        ("ex", {
            "titel": "Parametrisierte Abfrage + MERGE",
            "ziel": "Du schreibst die produktionsreife Version der Brücke: Abfragen mit Parametern (Injection-sicher) und idempotentes Laden.",
            "anforderungen": [
                "Schreibe `frage(cypher, **parameter)`: im Fallback mit `store.run_cypher`, sonst per `session.run(cypher, **parameter)` – Ergebnis als Liste von Dicts (`.data()`).",
                "Schreibe `lade_firmen_graph()`, das die Firma per **MERGE** anlegt (mehrfaches Ausführen → KEINE Duplikate) – im Fallback: GraphStore mit `find_node`-Check (Entity Resolution!).",
                "Rufe `lade_firmen_graph()` **zweimal** auf und beweise: Die Anzahl der Nodes ist identisch.",
            ],
            "starter": '''\
def frage(cypher, **parameter):
    # YOUR CODE HERE (Fallback oder session.run mit Parametern)
    pass

def lade_firmen_graph():
    # YOUR CODE HERE: MERGE bzw. Entity Resolution
    pass

lade_firmen_graph()
vorher = len(store.nodes()) if verwende_fallback else None
lade_firmen_graph()
# YOUR CODE HERE: Beweis (Anzahl unveraendert?)''',
            "kriterien": [
                "Die Abfrage nutzt Parameter (`$name`), niemals f-Strings.",
                "Doppeltes Laden erzeugt keine Duplikate.",
                "Der Code läuft im Fallback UND würde mit echtem Neo4j funktionieren (gleiche Struktur).",
            ],
            "checks": '''\
# Im Fallback: Anzahl muss nach zweimaligem Laden stabil sein:
if verwende_fallback:
    assert len(store.nodes()) == len(baue_beispiel_graph().nodes()), \\
        "Fallback: keine Duplikate erlaubt!"
ergebnis = frage("MATCH (n:Person) WHERE n.name = 'Anna' RETURN n", name="Anna")
assert ergebnis, "Anna sollte gefunden werden."
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Parameter in Cypher: `MATCH (n:Person {{name: $name}}) RETURN n` – übergeben als `frage(cypher, name='Anna')`.",
                "MERGE = \"finde ODER lege an\" – das Neo4j-Äquivalent von Entity Resolution.",
                "Im Fallback übernimmt `find_node` diese Rolle: nur anlegen, wenn nicht gefunden.",
            ],
            "loesung": '''\
def frage(cypher, **parameter):
    if verwende_fallback:
        return store.run_cypher(cypher)
    with treiber.session() as session:
        return [dict(datensatz) for datensatz in session.run(cypher, **parameter)]

def lade_firmen_graph():
    """Laedt den Beispielgraphen IDEMPOTENT (keine Duplikate)."""
    if verwende_fallback:
        if store.find_node("Company", name="Acme") is None:
            acme = store.add_node(["Company"], name="Acme", branche="Technologie")
            anna = store.find_node("Person", name="Anna") or store.add_node(
                ["Person"], name="Anna", rolle="Entwicklerin")
            store.add_relationship(anna.id, acme, "WORKS_FOR", seit=2021)
        return len(store.nodes())
    with treiber.session() as session:
        session.run("MERGE (a:Person {name: 'Anna'}) SET a.rolle = 'Entwicklerin'")
        session.run("MERGE (c:Company {name: 'Acme'}) SET c.branche = 'Technologie'")
        session.run("MERGE (a:Person {name: 'Anna'})-[k:WORKS_FOR]->(c:Company {name: 'Acme'}) SET k.seit = 2021")
        return len(frage("MATCH (n) RETURN count(n) AS anzahl"))

vorher = lade_firmen_graph()
nachher = lade_firmen_graph()
print("Idsempotenz-Beweis:", vorher, "->", nachher)''',
            "loesung_md": "MERGE/Entity Resolution verhindern Graph-Müll: \"Acme\" zweimal würde jede Abfrage kaputtmachen. "
                          "Parameter schützen vor Injection – bei LLM-generierten Abfragen (Lektion 12) wird das überlebenswichtig.",
            "reflexion": [
                "1. SQL-JOIN vs. Kante: Wie viele \"Sprünge\" bräuchte eine relationale DB für „Wer arbeitet an AI Assistant?\" – und warum skaliert Graph-Traversal besser?",
                "2. Was müsste passieren, bevor dein Assistent **schreibend** auf Neo4j darf? (→ Freigabe! Lektion 15)",
            ],
        }),
    ],
    "weiter": "**Weiter mit Lektion 12:** `notebooks/06_knowledge_graph/12_llm_extraktion_graph.ipynb` – "
              "der Graph füllt sich **selbst**: ein LLM extrahiert Entitäten und Beziehungen aus Text.",
}

NB_12 = {
    "pfad": "notebooks/06_knowledge_graph/12_llm_extraktion_graph.ipynb",
    "titel": "Lektion 12: Der Graph füllt sich selbst – LLM-Extraktion & NL→Cypher",
    "zeit": "~75 Minuten",
    "schwierigkeit": "Fortgeschritten",
    "voraussetzungen": "Lektion 10–11",
    "baut": "Eine Pipeline: Text → LLM-Extraktion → Graph (mit Entity Resolution) → Fragen auf Deutsch → Cypher → Antwort",
    "ziele": [
        "ein LLM Entitäten und Beziehungen **strukturiert** extrahieren lassen (Pydantic-Vertrag)",
        "**Entity Resolution** implementieren (keine Duplikate)",
        "natürliche Fragen in Cypher übersetzen – abgesichert durch die **Whitelist**",
        "einen Angriffs-Test durchführen (`DETACH DELETE` wird abgelehnt)",
        "die zwei Risiken (Injection, Doppel-Entities) und ihre Bremsen benennen",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Extraktion – der Leser mit Formular\n\n"
               "**WARUM:** Bislang hast du den Graph von Hand gepflegt. Echte Systeme lassen ihn aus Dokumenten **wachsen**: "
               "Text rein → Entitäten + Beziehungen raus → Graph gefüllt.\n\n"
               "**WAS:** Das LLM hält statt einer freien Zusammenfassung ein **Formular** (Pydantic, Lektion 09!): "
               "`entitaeten` (Name + Label) und `beziehungen` (von, Typ, zu). **Das LLM schlägt vor – Python entscheidet.**"),
        ("code", '''\
from lernakademie.graph_extraction import extrahiere, Extraktion

TEXT = ("Anna arbeitet bei Acme und gehoert zu Engineering. "
        "Ben arbeitet bei Acme. Engineering arbeitet an AI Assistant.")

extraktion = extrahiere(TEXT)
print("Entitaeten:")
for e in extraktion.entitaeten:
    print("  -", e["name"], f"({e['label']})")
print("Beziehungen:")
for b in extraktion.beziehungen:
    print(f"  - {b['von']} --{b['typ']}--> {b['zu']}")'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Die Extraktion ist ein **geprüftes Objekt** (kein freier Text!). "
               "Offline nutzt die Akademie eine Regel-Extraktion (bekannte Namen + Muster „X arbeitet bei Y\") – "
               "mit echtem Modell extrahiert Mistral frei. Die Schnittstelle bleibt identisch.\n\n"
               "**TRY:** Führe die Extraktion mit einem Tippfehler („Anya arbeitet bei Acme“) aus – was passiert ehrlich?"),
        ("md", "## 🧠 Konzept: Entity Resolution – der Türsteher\n\n"
               "**Metapher:** Vor dem Club steht ein Türsteher mit Gästeliste: \"Anna? Steht schon drauf – kein zweiter Stempel!\" "
               "Vor jedem `add_node` steht deshalb ein `find_node`-Check. **Das verhindert Graph-Müll** – "
               "denn doppelt gespeicherte Entities zerreißen jede Traversierung."),
        ("code", '''\
from lernakademie.graph_extraction import fuelle_graph
from lernakademie.graph_store import GraphStore

store = GraphStore()

kanten1 = fuelle_graph(store, extrahiere(TEXT))
print(f"Erster Lauf: {len(store.nodes())} Nodes, {kanten1} Kanten")

kanten2 = fuelle_graph(store, extrahiere(TEXT))   # DER DUPLIKAT-TEST
print(f"Zweiter Lauf: {len(store.nodes())} Nodes, {kanten2} Kanten")
print("-> Nodes duerfen NICHT gestiegen sein (Entity Resolution wirkt).")'''),
        ("ex", {
            "titel": "Der Duplikat-Beweis",
            "ziel": "Du implementierst die Entity-Resolution selbst und beweist ihre Wirkung.",
            "anforderungen": [
                "Schreibe `fuelle_graph_eigen(store, extraktion)`, das alle Entitäten und Beziehungen anlegt.",
                "**Vor jedem Anlegen:** prüfe mit `find_node`, ob die Entity schon existiert (Existing-ID wiederverwenden!).",
                "Führe die Funktion zweimal mit derselben Extraktion aus und vergleiche die Node-Anzahl.",
            ],
            "starter": '''\
def fuelle_graph_eigen(store, extraktion):
    ids = {}
    for entitaet in extraktion.entitaeten:
        # YOUR CODE HERE: find_node vor add_node!
        pass
    gesetzt = 0
    for beziehung in extraktion.beziehungen:
        # YOUR CODE HERE: nur anlegen, wenn beide Seiten existieren
        pass
    return gesetzt

fuelle_graph_eigen(store, extrahiere(TEXT))
vorher = len(store.nodes())
fuelle_graph_eigen(store, extrahiere(TEXT))
print("Vorher:", vorher, "Nachher:", len(store.nodes()))''',
            "kriterien": [
                "Der zweite Lauf erzeugt **null** neue Nodes.",
                "Unvollständige Beziehungen (unbekannte Entity) werden übersprungen – kein Absturz.",
                "Kanten verbinden IDs, niemals Namen.",
            ],
            "checks": '''\
neu = GraphStore()
ex = extrahiere(TEXT)
fuelle_graph_eigen(neu, ex)
stand = len(neu.nodes())
fuelle_graph_eigen(neu, ex)
assert len(neu.nodes()) == stand, "Entity Resolution: Nodes duerfen beim 2. Lauf nicht steigen!"
assert stand >= 3, "Mindestens Anna, Acme, Engineering sollten angelegt sein."
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "`vorhanden = store.find_node(label, name=name)` – `None` heißt: neu anlegen.",
                "IDs im `ids`-Dictionary sammeln: `ids[name] = node.id`.",
                "Für Beziehungen: `if von in ids and zu in ids: store.add_relationship(...)` – sonst überspringen.",
            ],
            "loesung": '''\
def fuelle_graph_eigen(store, extraktion):
    ids = {}
    for entitaet in extraktion.entitaeten:
        name, label = entitaet["name"], entitaet.get("label", "Entity")
        vorhanden = store.find_node(label, name=name)
        ids[name] = vorhanden.id if vorhanden else store.add_node([label], name=name)
    gesetzt = 0
    for beziehung in extraktion.beziehungen:
        von, zu = beziehung["von"], beziehung["zu"]
        if von in ids and zu in ids:      # unvollstaendig -> ueberspringen
            store.add_relationship(ids[von], ids[zu], beziehung["typ"])
            gesetzt += 1
    return gesetzt

fuelle_graph_eigen(store, extrahiere(TEXT))
vorher = len(store.nodes())
fuelle_graph_eigen(store, extrahiere(TEXT))
print("Vorher:", vorher, "| Nachher:", len(store.nodes()), "(beweis: identisch)")''',
            "loesung_md": "Der `find_node`-Check pro Entity ist der Türsteher. Unvollständige Beziehungen "
                          "überspringst du bewusst – raten wäre schlimmer als weglassen. "
                          "Du hast gerade die wichtigste Qualitätsregel jedes Knowledge Graphs implementiert.",
            "reflexion": [
                "1. Warum führt \"das LLM darf Labels frei erfinden\" zu Graph-Chaos – und wie wirkt die Struktur dagegen?",
                "2. Was kostet die Extraktion bei 500 Dokumenten – und wo würdest du cachen?",
            ],
        }),
        ("md", "## 🧠 Konzept: Natürliche Sprache → Cypher (mit Bremse!)\n\n"
               "**WARUM:** Nutzer fragen in Worten („Wo arbeitet Anna?\"), der Graph versteht Cypher. "
               "Die Übersetzung übernimmt ein LLM (offline: Regel-Fallback) – **ABER:**\n\n"
               "> **Generierte Abfragen sind nicht vertrauenswürdig.** Ein manipulierter Prompt kann `DELETE` erzeugen. "
               "Deshalb: deterministische **Whitelist vor** jeder Ausführung. Die Prüfung muss Python-Code sein – "
               "**niemals ein LLM**, denn LLMs prüfen Sicherheitsregeln nicht zuverlässig."),
        ("code", '''\
from lernakademie.graph_extraction import cypher_aus_frage, ist_sicher, fuehre_sicher_aus

fragen = ["Wo arbeitet Anna?", "Was gibt es ueber Acme?", "Wie hoch ist das Weihnachtsgeld?"]
for frage in fragen:
    cypher = cypher_aus_frage(frage)
    print(f"FRAGE: {frage}")
    print(f"  Cypher: {cypher}")
    if cypher and ist_sicher(cypher):
        ergebnis = fuehre_sicher_aus(store, cypher)
        print(f"  -> {len(ergebnis)} Treffer")
    else:
        print("  -> ehrlich: nicht uebersetzbar / keine Treffer")
    print()'''),
        ("code", '''\
# DER ANGRIFFS-TEST (Pflicht in dieser Lektion!):
boese = "MATCH (n:Person) DETACH DELETE n"
try:
    fuehre_sicher_aus(store, boese)
    print("FEHLER IM DESIGN: destruktive Abfrage wurde ausgefuehrt!")
except ValueError as fehler:
    print("Korrekt abgelehnt ✅")
    print("Grund:", str(fehler)[:90])'''),
        ("md", "## 📝 Reflexion (abschließend fürs Graph-Modul)\n\n"
               "1. Warum reicht die lesende Whitelist nicht mehr, sobald das System „aus Dokumenten lernen\" (also schreiben) soll? (→ Freigabe in Lektion 15!)\n"
               "2. Vergleiche: Was kann der Graph, was Vektor-Suche (Build 2) nicht kann – und umgekehrt? Schreib zwei Fragen als Beleg.\n\n"
               "**Genau diese zwei Welten kombiniert Build 3** – nächste Lektion: LangGraph steuert den Ablauf."),
    ],
    "weiter": "**🚀 Lektion 13:** `notebooks/07_langgraph/13_langgraph_workflows.ipynb` – "
              "LangGraph: State, Nodes, konditionale Kanten. Deine Steuerzentrale für Build 3.",
}

SPECS_D = [NB_10, NB_11, NB_12]
