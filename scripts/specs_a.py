"""Notebook-Specs Teil A: START_HERE + Python-Grundlagen (Lektion 01-02)."""

START_HERE = {
    "pfad": "START_HERE.ipynb",
    "titel": "🎓 Willkommen in der LangChain & LangGraph Lernakademie",
    "zeit": "~15 Minuten",
    "schwierigkeit": "Anfänger",
    "voraussetzungen": "Keine! Du hast noch nie programmiert? Genau richtig hier.",
    "baut": "Deinen allerersten Programmier-Erfolg – und den Fahrplan für deine ganze Lernreise",
    "hat_loesung": False,
    "fuehre_lernnotebook_aus": True,
    "ziele": [
        "verstehen, was du in dieser Akademie bauen wirst (dreimal!)",
        "wissen, wie du Jupyter-Notebook-Zellen ausführst, den Kernel neu startest und alles zurücksetzt",
        "dein erstes Python-Programm in einer Zelle ausführen",
    ],
    "cells": [
        ("md", "## Was ist das hier?\n\nDas ist **kein Lehrbuch**, das du liest – das ist ein **geführtes Programmier-Labor**. "
               "Du liest eine Erklärung, führst sofort Code aus, änderst ihn, löst kleine Aufgaben und bekommst sofort Rückmeldung. "
               "Alles passiert **hier in diesem Notebook** – du musst nirgendwo hinwechseln.\n\n"
               "**Für wen?** Für Menschen, die noch nie programmiert haben. Kein Vorwissen nötig – nur ein Computer, Internet und Neugier.\n\n"
               "**Was wirst du bauen?** Einen **Personal Knowledge Assistant** – und zwar **dreimal**, jedes Mal mit besseren Werkzeugen:\n\n"
               "| Build | Werkzeuge | Was du lernst |\n|---|---|---|\n"
               "| 🧱 **Build 1** | reines Python + direkter LLM-Aufruf | was wirklich passiert – von Hand gebaut |\n"
               "| 🔗 **Build 2** | LangChain + Vektor-RAG | semantische Suche, Fließband-Chains |\n"
               "| 🚀 **Build 3** | LangGraph + Knowledge Graph + Agent | der vollwertige, entscheidende Assistent |\n\n"
               "Am Ende startest du eine fertige Web-Oberfläche (Streamlit) und bedienst **dein eigenes System**."),
        ("md", "## 🧭 Wie funktioniert so ein Notebook?\n\nEin Notebook ist eine Liste von **Zellen**. Es gibt zwei Sorten:\n\n"
               "- **Text-Zellen** (wie diese) erklären etwas.\n"
               "- **Code-Zellen** enthalten Python-Code. Sie erkennen sie an `In [ ]:` links.\n\n"
               "**Das Wichtigste – so führst du eine Zelle aus:**\n\n"
               "1. Klicke in die Zelle.\n"
               "2. Drücke **Shift + Enter** (oder den ▶-Play-Button oben).\n\n"
               "Probiere es gleich bei der Setup-Zelle unten aus! Unter der Zelle erscheint dann eine Nummer (`In [1]:`) und die Ausgabe.\n\n"
               "**Drei Rettungsanker, wenn etwas seltsam ist:**\n"
               "- **Kernel → Restart Kernel**: Python \"vergisst\" alles und startet frisch (bei komischen Fehlern oft die Lösung).\n"
               "- **Run → Run All Cells**: führt das ganze Notebook von oben nach unten aus.\n"
               "- **File → Save** und danach einfach weitermachen. Nichts kann kaputtgehen – du kannst jedes Notebook neu vom Repository holen.\n\n"
               "**Hilfe bei Fehlern:** `docs/troubleshooting.md` – und: Fehler sind **Teil des Lernens**. Wir erklären sie dir, sobald sie auftauchen."),
        ("code", SETUP_FALLBACK := '''\
# Deine allererste Code-Zelle! Fuehre sie mit Shift + Enter aus.
print("Hallo Akademie! Diese Zelle funktioniert.")'''),
        ("md", "## ⚙️ Setup: Umgebung prüfen\n\nDiese Zelle prüft, dass Python alles Wichtige findet. Führe sie aus – "
               "sie zeigt dir auch, welche KI konfiguriert ist (ohne jemals Geheimnisse anzuzeigen)."),
        ("code", '''\
import sys
from pathlib import Path

ROOT = Path.cwd()
while not (ROOT / "lernakademie").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from lernakademie.config import llm_zusammenfassung
info = llm_zusammenfassung()
print("Python:", sys.version.split()[0])
print("Projektwurzel:", ROOT)
print("KI-Anbieter:", info["anbieter"], "| Modell:", info["modell"], "| API-Key:", info["api_key"])
if info["anbieter"] == "offline":
    print("\\nAlles laeuft im OFFLINE-Modus: jede Lektion funktioniert sofort,")
    print("kostenlos und ohne Anmeldung – Antworten sind dann Simulationen ([OFFLINE]).")'''),
        ("md", "### Woher kommt die KI-Antwort? Du entscheidest – ohne Code zu ändern!\n\n"
               "Diese Akademie ist **anbieter-unabhängig**. In der Datei `.env` (Kopie von `.env.example`) legst du fest, "
               "wo deine KI läuft – **Mistral Cloud**, ein **lokaler AI-Server** (z. B. LM Studio, Ollama) oder jeder "
               "OpenAI-kompatible Dienst. Ohne Eintrag: Offline-Modus.\n\n"
               "Die \"Wo/Wie/Welche\"-Regel:\n\n"
               "| Variable | Frage | Beispiel |\n|---|---|---|\n"
               "| `LLM_BASE_URL` | **WO** lebt der Server? | `http://localhost:1234/v1` |\n"
               "| `LLM_API_KEY` | **WIE** darf ich zugreifen? (oft leer!) | – |\n"
               "| `LLM_MODEL` | **WELCHES** Modell? | `mistral-small-latest` |\n\n"
               "Alles Weitere dazu: **[docs/local-ai-server.md](docs/local-ai-server.md)** – du kannst es später jederzeit ändern."),
        ("md", "## ✏️ Deine erste Mini-Aufgabe\n\nVerändere den Code so, dass er **dich** begrüßt: Setze deinen Namen in die Zeichenkette ein "
               "und füge eine zweite `print`-Zeile hinzu, die etwas über dich erzählt."),
        ("ex", {
            "titel": "Dein erster Code",
            "ziel": "Verändere die Zelle unten: trage deinen Namen ein und ergänze eine zweite Ausgabe.",
            "anforderungen": [
                "Die Variable `mein_name` enthält deinen Namen.",
                "`print` begrüßt dich mit deinem Namen.",
                "Es gibt eine zweite `print`-Zeile.",
            ],
            "starter": '''\
mein_name = "Welt"          # TRAGE HIER DEINEN NAMEN EIN
print("Hallo,", mein_name, "!")
# YOUR CODE HERE – ergaenze eine zweite print-Zeile''',
            "kriterien": [
                "Unter der Zelle erscheint eine Begrüßung mit deinem Namen.",
                "Eine zweite Ausgabezeile ist sichtbar.",
            ],
            "checks": '''\
assert isinstance(mein_name, str) and len(mein_name) > 0, "mein_name muss ein Text sein!"
print("Prüfung bestanden! ✅ Hast du deinen Namen eingetragen und eine zweite Zeile ergänzt?")''',
            "hinweise": [
                "Text in Python kommt immer in Anführungszeichen: `\"Anna\"` – vergiss sie nicht.",
                "Eine zweite Ausgabe beginnt wieder mit `print(...)` in einer neuen Zeile.",
            ],
            "loesung": '''\
mein_name = "Alex"
print("Hallo,", mein_name, "!")
print("Ich lerne gerade, KI-Anwendungen zu bauen.")''',
            "loesung_md": "Text (`\"...\"`) nennt Python einen **String**. `print` gibt alles in den Klammern auf dem Bildschirm aus. "
                          "Mehrere Werte in einem `print` werden mit Leerzeichen verbunden.",
        }),
        ("md", "## 🎓 Dein Fahrplan\n\nDie Lektionen liegen in `notebooks/` – **arbeite sie in der Nummern-Reihenfolge ab.** "
               "Zu jeder Lektion gibt es in `solutions/` ein Lösungs-Notebook zum Vergleichen (erst **nach** deinem eigenen Versuch öffnen!).\n\n"
               "| # | Notebook | Thema |\n|---|---|---|\n"
               "| 01 | `notebooks/01_python/01_setup_und_python.ipynb` | Python-Grundlagen: Variablen, Listen, Dictionarys |\n"
               "| 02 | `notebooks/01_python/02_funktionen_und_umgebung.ipynb` | Funktionen, venv, `.env` & API-Keys |\n"
               "| 03 | `notebooks/02_llm/03_erster_llm_call.ipynb` | Dein erster KI-Aufruf |\n"
               "| 04 | `notebooks/02_llm/04_chatbot_gedaechtnis.ipynb` | Chatbot mit Gedächtnis |\n"
               "| 05 | `notebooks/03_build_1/05_build1_wissensassistent.ipynb` | 🧱 **BUILD 1**: Assistent in reinem Python |\n"
               "| 06 | `notebooks/03_build_1/06_build1_erweiterung_ui.ipynb` | Build 1 erweitern + erste Oberfläche |\n"
               "| 07 | `notebooks/04_langchain/07_langchain_chains.ipynb` | LangChain-Fließbänder |\n"
               "| 08 | `notebooks/04_langchain/08_embeddings_vektor_rag.ipynb` | Embeddings & Vektor-RAG |\n"
               "| 09 | `notebooks/05_build_2/09_build2_rag_assistent.ipynb` | 🔗 **BUILD 2**: RAG-Assistent |\n"
               "| 10 | `notebooks/06_knowledge_graph/10_graphen_in_python.ipynb` | Knowledge Graphs von Hand |\n"
               "| 11 | `notebooks/06_knowledge_graph/11_neo4j_und_cypher.ipynb` | Neo4j & Cypher |\n"
               "| 12 | `notebooks/06_knowledge_graph/12_llm_extraktion_graph.ipynb` | Der Graph füllt sich selbst |\n"
               "| 13 | `notebooks/07_langgraph/13_langgraph_workflows.ipynb` | LangGraph: State, Nodes, Routing |\n"
               "| 14 | `notebooks/07_langgraph/14_hybrid_retrieval.ipynb` | Vektor vs. Graph vs. Hybrid |\n"
               "| 15 | `notebooks/08_build_3/15_build3_hybrid_agent.ipynb` | 🚀 **BUILD 3**: Hybrid-Agent mit Freigabe |\n"
               "| 16 | `notebooks/09_agents/16_tools_und_agenten.ipynb` | Werkzeuge für Agenten |\n"
               "| 17 | `notebooks/09_agents/17_gedaechtnis_und_freigabe.ipynb` | Gedächtnis & Human-in-the-Loop |\n"
               "| 18 | `notebooks/09_agents/18_supervisor_und_parallelitaet.ipynb` | Supervisor & Parallelität |\n"
               "| 19 | `notebooks/10_capstone/19_capstone_systemtest.ipynb` | 🏁 Das große System live testen |\n"
               "| 20 | `notebooks/11_testing/20_testing_und_evaluierung.ipynb` | Testing & Abschluss |\n\n"
               "**Vergleich der drei Builds:** [docs/same-problem-three-architectures.md](docs/same-problem-three-architectures.md)"),
        ("md", "## 📦 Wie installiere ich alles? (falls noch nicht geschehen)\n\n"
               "```bash\npython -m venv .venv\nsource .venv/bin/activate        # Windows: .venv\\\\Scripts\\\\activate\n"
               "pip install -r requirements.txt\npython -m ipykernel install --user --name=lernakademie   # Notebook-Kernel\njupyter lab                       # oder: jupyter notebook\n```\n\n"
               "Dann dieses Notebook öffnen und oben in der Kernel-Auswahl `lernakademie` (bzw. dein `.venv`-Python) wählen. "
               "Details: [docs/notebook-guide.md](docs/notebook-guide.md)"),
    ],
    "weiter": "**Starte jetzt mit Lektion 01:** `notebooks/01_python/01_setup_und_python.ipynb` – dort lernst du, wie Python Daten speichert und verarbeitet.",
}

NB_01 = {
    "pfad": "notebooks/01_python/01_setup_und_python.ipynb",
    "titel": "Lektion 01: Python-Grundlagen – Daten & Struktur",
    "zeit": "~45 Minuten",
    "schwierigkeit": "Anfänger",
    "voraussetzungen": "START_HERE.ipynb",
    "baut": "Eine kleine Datensammlung über dich – und einen Einkaufslisten-Rechner",
    "ziele": [
        "Werte in **Variablen** speichern und wieder verwenden",
        "Texte (**Strings**) mit f-Strings kombinieren",
        "Werte in **Listen** sammeln und mit einer Schleife verarbeiten",
        "Daten in **Dictionarys** als Schlüssel→Wert-Paare ablegen",
        "die drei häufigsten Anfänger-Fehler erkennen und selbst beheben",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Die Variable – ein beschrifteter Kasten\n\n"
               "**WARUM:** Programme müssen sich Dinge merken: deinen Namen, eine Frage, eine Antwort. "
               "Ohne Gedächtnis wäre jedes Programm eine Taschenrechner-Eingabe, die sofort vergisst.\n\n"
               "**WAS:** Eine Variable ist ein **Name für einen Wert**. "
               "Denk an einen beschrifteten Kasten: Du legst etwas hinein (`name = \"Anna\"`) und kannst später jederzeit hineinschauen (`name`).\n\n"
               "**WIE:** Mit `=` – Vorsicht: Das ist keine Mathematik-Gleichung, sondern eine **Zuweisung**: "
               "\"Lege das rechts Stehende in den Kasten links.\""),
        ("code", '''\
name = "Anna"
alter = 30
groesse = 1.68

print(name, "ist", alter, "Jahre alt.")'''),
        ("md", "### 🔎 Was sehen wir hier?\n`\"Anna\"` ist ein **String** (Text), `30` ein **Integer** (ganze Zahl), `1.68` ein **Float** (Dezimalzahl). "
               "Das nennt man **Typen**. Python erkennt sie automatisch – du musst sie nur nicht mischen, ohne es zu merken."),
        ("md", "### 🛑 Fehler sind Freunde (1): TypeError\n\nFühre die nächste Zelle aus – sie **wird absichtlich fehlschlagen**. Das ist gewollt!"),
        ("code", '''\
# Diese Zelle provoziert absichtlich einen Fehler – lies die Meldung genau:
try:
    print("Alter naechstes Jahr: " + alter)
except TypeError as fehler:
    print("TypeError:", fehler)
    print("-> Python weigert sich, Text und Zahl mit + zu verkleben.")'''),
        ("md", "**Was ist passiert?**\n"
               "- `TypeError: can only concatenate str (not \"int\") to str`\n"
               "- **Bedeutung:** Du hast versucht, Text und Zahl mit `+` zu verkleben. Python weigert sich – zu Recht.\n"
               "- **Lösung:** f-Strings! Sie betten Variablen jeden Typs sauber in Text ein:"),
        ("code", '''\
print(f"Alter naechstes Jahr: {alter + 1}")
print(f"{name} ist {groesse} m gross.")'''),
        ("md", "Das `f` vor den Anführungszeichen macht den String zum **f-String**: Alles in `{...}` wird durch den Wert ersetzt – "
               "und dort drin darf sogar gerechnet werden (`{alter + 1}`)."),
        ("md", "## 🧠 Konzept: Liste – die nummerierte Schublade\n\n"
               "**WARUM:** Einzelne Variablen werden unpraktisch, wenn du **viele** Dinge desselben Typs hast: 3 Artikel, 100 Fragen, 500 Dokumente.\n\n"
               "**WAS:** Eine Liste ist eine geordnete Sammlung. Wichtig: Das erste Element hat den Index **0** – zähle wie ein Computer!\n\n"
               "**WIE / TRY:**"),
        ("code", '''\
einkauf = ["Milch", "Brot", "Aepfel"]
print("Komplett:", einkauf)
print("Erstes Element (Index 0):", einkauf[0])
print("Anzahl Elemente:", len(einkauf))

einkauf.append("Butter")   # hinten anhaengen
print("Nach append:", einkauf)'''),
        ("md", "### Schleifen: mit jedem Element etwas tun\n\n"
               "**WARUM:** Bei 500 Dokumenten willst du nicht 500 Zeilen schreiben. Die Schleife sagt: \"Für **jedes** Element: tue Folgendes.\""),
        ("code", '''\
gesamt = 0
for artikel in einkauf:
    print("- Artikel:", artikel)

for zahl in [2, 4, 9]:
    gesamt = gesamt + zahl
print("Summe:", gesamt)'''),
        ("md", "## 🧠 Konzept: Dictionary – das Wörterbuch\n\n"
               "**WARUM:** Listen kennen nur Positionen (\"Element 0\"). Oft willst du mit **Namen** nachschlagen: "
               "Was kostet Milch? Was ist Annas Rolle?\n\n"
               "**WAS:** Ein Dictionary (`dict`) speichert **Schlüssel → Wert**-Paare wie ein Wörterbuch: Stichwort suchen, Erklärung finden.\n\n"
               "**WIE / TRY:**"),
        ("code", '''\
preise = {"Milch": 1.20, "Brot": 2.50, "Aepfel": 3.00}

print("Preis von Milch:", preise["Milch"])
print("Sicher nachschlagen (mit Standardwert):", preise.get("Kaviar", "unbekannt"))

preise["Kaffee"] = 4.99    # neues Paar anlegen
print("Alle Paare:", preise)'''),
        ("md", "### 🛑 Fehler sind Freunde (2): KeyError\n\n"
               "`preise[\"Kaviar\"]` würde mit `KeyError` abstürzen, weil der Schlüssel fehlt. "
               "`.get(schluessel, standardwert)` ist die sichere Variante: Sie liefert nie einen Absturz, sondern den Standardwert. "
               "Merke: **Klammern `[...]` = streng, `.get(...)` = gnädig.**"),
        ("md", "## 🧠 Konzept: Bedingungen – das Programm entscheidet\n\n"
               "**WARUM:** Dein späterer Knowledge Assistant wird entscheiden: \"Das ist eine Verbindungsfrage → nutze den Graphen!\" "
               "Das Grundmuster lernst du jetzt.\n\n"
               "**WIE / TRY:**"),
        ("code", '''\
alter = 30

if alter >= 18:
    print("Volljaehrig")
elif alter > 12:
    print("Jugendlich")
else:
    print("Kind")

# Vergleiche: ==  gleich   !=  ungleich   >  <  >=  <=
print("Ist 30 gleich 30?", 30 == 30)'''),
        ("md", "Das Ergebnis eines Vergleichs ist ein **Boolean**: `True` oder `False` – der ja/nein-Typ, den du später überall brauchst."),
        ("ex", {
            "titel": "Dein Einkaufslisten-Rechner",
            "ziel": "Du kombinierst Liste, Dictionary und Schleife zu einem echten Mini-Programm.",
            "anforderungen": [
                "Erstelle eine Liste `mein_einkauf` mit mindestens 3 Artikeln.",
                "Erstelle ein Dictionary `meine_preise`, das zu jedem Artikel einen Preis (Zahl) speichert.",
                "Berechne in einer Schleife die Summe aller Preise der Liste und speichere sie in `summe`.",
                "Gib die Summe mit zwei Nachkommastellen aus (Tipp: `f\"{summe:.2f}\"`).",
            ],
            "starter": '''\
mein_einkauf = []          # YOUR CODE HERE: mindestens 3 Artikel
meine_preise = {}          # YOUR CODE HERE: Preis pro Artikel
summe = 0                  # YOUR CODE HERE: in einer Schleife aufsummieren

# YOUR CODE HERE: Ausgabe''',
            "kriterien": [
                "`summe` ist eine Zahl und stimmt (rechne per Hand nach!).",
                "Die Ausgabe zeigt die Summe mit 2 Nachkommastellen.",
                "Du hast eine `for`-Schleife verwendet.",
            ],
            "checks": '''\
assert len(mein_einkauf) >= 3, "Die Liste braucht mindestens 3 Artikel."
assert len(meine_preise) >= 3, "Das Dictionary braucht mindestens 3 Preise."
erwartung = sum(meine_preise[a] for a in mein_einkauf if a in meine_preise)
assert abs(summe - erwartung) < 0.001, f"summe sollte {erwartung} sein, ist aber {summe}."
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "In der Schleife: `for artikel in mein_einkauf:` – und dann `summe = summe + meine_preise[artikel]`.",
                "Kürzer geht das Erhöhen mit `summe += meine_preise[artikel]`.",
                "Für zwei Nachkommastellen: `print(f\"Summe: {summe:.2f} Euro\")`.",
            ],
            "loesung": '''\
mein_einkauf = ["Milch", "Brot", "Aepfel"]
meine_preise = {"Milch": 1.20, "Brot": 2.50, "Aepfel": 3.00}

summe = 0
for artikel in mein_einkauf:
    summe += meine_preise[artikel]

print(f"Summe: {summe:.2f} Euro")''',
            "loesung_md": "Die Schleife läuft über die Liste, schlägt pro Artikel den Preis im Dictionary nach und "
                          "erhöht `summe`. Genau dieses Muster (\"über eine Liste iterieren, Werte nachschlagen, "
                          "akkumulieren\") wirst du in Build 1 beim Dokumenten-Scoring wiedersehen!",
            "reflexion": [
                "1. Warum beginnt der Listen-Index bei 0 – und woran merkst du es, wenn du `einkauf[1]` abfragst?",
                "2. Wann würdest du eine Liste, wann ein Dictionary wählen? Nenne je ein Beispiel aus deinem Alltag.",
            ],
            "challenge": ("Hänge einen neuen Artikel (Liste **und** Preis) an und gib danach die Liste mit allen Preisen aus.",
                          '''\
# YOUR CODE HERE (Challenge)
'''),
        }),
    ],
    "weiter": "**Weiter mit Lektion 02:** `notebooks/01_python/02_funktionen_und_umgebung.ipynb` – "
              "aus Einmal-Code wird wiederverwendbarer Code (Funktionen), und du richtest dein Projekt sauber ein (venv, `.env`, API-Keys).",
}

NB_02 = {
    "pfad": "notebooks/01_python/02_funktionen_und_umgebung.ipynb",
    "titel": "Lektion 02: Funktionen, Umgebung & API-Keys",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Anfänger",
    "voraussetzungen": "Lektion 01",
    "baut": "Wiederverwendbare Bausteine (Funktionen) und eine saubere Projektumgebung mit sicheren API-Keys",
    "ziele": [
        "eigene **Funktionen** mit `def` schreiben, Parameter und Rückgabewerte nutzen",
        "den Unterschied zwischen `print` (zeigen) und `return` (zurückgeben) erklären",
        "eine virtuelle Umgebung (venv) anlegen und Packages installieren",
        "API-Keys sicher über `.env` verwalten – ohne sie jemals im Code zu haben",
        "Fehler mit `try/except` abfangen, statt das Programm abstürzen zu lassen",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Funktion – das Rezept mit Namen\n\n"
               "**WARUM:** Ohne Funktionen müsstest du dieselben Zeilen endlos kopieren. "
               "Später in dieser Akademie wirst du **dieselbe** Funktion rufen: einmal schreibst du `beantworte(frage)` – hundertmal benutzt du sie.\n\n"
               "**WAS:** Eine Funktion ist ein benannter, wiederverwendbarer Anweisungsblock. "
               "Wie ein **Kaffeevollautomat**: Knopf drücken (Aufruf), Zutaten wählen (Parameter), Getränk erhalten (**Rückgabewert**).\n\n"
               "**WIE / TRY:**"),
        ("code", '''\
def begruessung(name, stil="hoeflich"):
    """Gibt eine Begruessung zurueck (Docstring = Bedienungsanleitung)."""
    if stil == "locker":
        return f"Na, {name}! Was geht?"
    return f"Guten Tag, {name}."

nachricht = begruessung("Anna")
print(nachricht)
print(begruessung("Ben", stil="locker"))'''),
        ("md", "### 🔎 Was sehen wir hier?\n- `stil=\"hoeflich\"` ist ein **Standardwert** – die Funktion funktioniert auch ohne zweites Argument.\n"
               "- `return` **gibt** einen Wert zurück (das Getränk). `print` würde ihn nur *anzeigen* – die Funktion wäre dann leer.\n\n"
               "**Der wichtigste Unterschied der Lektion:** `return` = zurückgeben (damit andere Code weiterrechnen kann), "
               "`print` = nur auf den Bildschirm. Merksatz: **return rechnet, print plaudert.**"),
        ("code", '''\
def durchschnitt_falsch(zahlen):
    print(sum(zahlen) / len(zahlen))       # nur Anzeige -> Rueckgabewert ist None!

def durchschnitt_richtig(zahlen):
    if not zahlen:                         # leer -> 0 statt Absturz!
        return 0
    return sum(zahlen) / len(zahlen)

ergebnis = durchschnitt_falsch([2, 4])     # gibt 3.0 AUS, aber...
print("ergebnis ist:", ergebnis)          # ...die Variable enthaelt None
print(durchschnitt_richtig([2, 4, 9]))
print(durchschnitt_richtig([]))            # keine DivisionDurchNull-Panik'''),
        ("md", "### 🛑 Fehler sind Freunde (3): ZeroDivisionError & None\n\n"
               "`durchschnitt_falsch([])` würde mit `ZeroDivisionError` abstürzen (Division durch `len([]) = 0`). "
               "Die **Absicherung** (`if not zahlen: return 0`) nennt man *defensive Programmierung*: "
               "Unerwartete Eingaben abfangen, bevor sie Schaden anrichten. Genau das wird dein Assistent später bei Nutzerfragen tun."),
        ("ex", {
            "titel": "Robuste Durchschnitts-Funktion",
            "ziel": "Du schreibst eine Funktion, die **niemals abstürzt** – egal, was hineinkommt.",
            "anforderungen": [
                "Schreibe `durchschnitt(zahlen)`, die den Durchschnitt einer Zahlenliste zurückgibt (`return`!).",
                "Bei einer **leeren** Liste gibt sie `0` zurück (kein Absturz).",
                "Schreibe zusätzlich `ist_arbeitszeit(stunde)`: gibt `True` zurück, wenn die Stunde zwischen 9 und 17 liegt.",
            ],
            "starter": '''\
def durchschnitt(zahlen):
    # YOUR CODE HERE
    pass

def ist_arbeitszeit(stunde):
    # YOUR CODE HERE
    pass''',
            "kriterien": [
                "`durchschnitt([2, 4, 9])` ergibt `5.0`.",
                "`durchschnitt([])` ergibt `0` (kein Crash).",
                "`ist_arbeitszeit(12)` ist `True`, `ist_arbeitszeit(3)` ist `False`.",
                "Beide Funktionen nutzen `return` (nicht nur `print`).",
            ],
            "checks": '''\
assert durchschnitt([2, 4, 9]) == 5.0, "Durchschnitt von [2,4,9] sollte 5.0 sein."
assert durchschnitt([]) == 0, "Leere Liste soll 0 liefern, nicht abstuerzen!"
assert ist_arbeitszeit(12) is True
assert ist_arbeitszeit(3) is False
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Leere Liste prüfst du mit `if not zahlen:` – eine leere Liste ist in Python \"falsy\".",
                "`return` beendet die Funktion sofort – nutze das für den Leerfall zuerst.",
                "Für die Arbeitszeit: `return 9 <= stunde <= 17` (Python kann Ketten vergleichen!).",
            ],
            "loesung": '''\
def durchschnitt(zahlen):
    if not zahlen:
        return 0
    return sum(zahlen) / len(zahlen)

def ist_arbeitszeit(stunde):
    return 9 <= stunde <= 17''',
            "loesung_md": "Erst den Sonderfall (leere Liste) absichern, dann den Normalfall berechnen – dieses "
                          "Muster (\"Erst prüfen, dann rechnen\") zieht sich durch die ganze Akademie. "
                          "`9 <= stunde <= 17` ist eine Python-Kette: sie prüft beide Bedingungen auf einmal.",
        }),
        ("md", "## 🧠 Konzept: Imports & die virtuelle Umgebung\n\n"
               "**WARUM:** Python kann von Natur aus erstaunlich viel – aber LangChain, Mistral-Anbindung & Co. "
               "stammen von anderen Entwicklern. Die holst du als **Packages** dazu. "
               "Damit sich Projekte nicht gegenseitig ihre Versionen überschreiben, bekommt jedes Projekt seinen eigenen **Werkzeugkasten**: die virtuelle Umgebung (venv).\n\n"
               "**WAS:** **Metapher venv:** ein Bauwagen pro Baustelle – jedes Projekt hat seine eigenen Werkzeuge, "
               "kein anderes Projekt kann sie beschädigen. **Metapher Import:** der Kaffeeautomat wird nicht in jedes Zimmer gestellt – "
               "du holst ihn per `import` in den Raum, wenn du ihn brauchst.\n\n"
               "**WIE (im Terminal, nicht im Notebook!):**\n"
               "```bash\npython -m venv .venv\nsource .venv/bin/activate        # Windows: .venv\\\\Scripts\\\\activate\npip install -r requirements.txt\n```\n\n"
               "**TRY (im Notebook):** prüfen wir, ob deine Umgebung alles Wichtige hat:"),
        ("code", '''\
from datetime import datetime       # Standardbibliothek: immer dabei
import random                       # Zufall

print("Aktuelle Stunde:", datetime.now().hour)
print("Wuerfelwurf:", random.randint(1, 6))

try:
    import langchain
    print("langchain-Version:", langchain.__version__)
except ImportError:
    print("langchain fehlt! -> pip install -r requirements.txt")'''),
        ("md", "## 🧠 Konzept: API-Keys & die .env-Datei\n\n"
               "**WARUM:** Ab der nächsten Lektion redet dein Python mit einer echten KI. "
               "Dafür braucht es einen **API-Key** – und der ist wie eine **Kreditkarte**: Wer ihn hat, kann auf deine Kosten bestellen. "
               "Deshalb gehört er **niemals** in den Code (und schon gar nicht in ein Git-Repository – Bots scannen öffentliche Repos in Minuten!).\n\n"
               "**WAS:** Der professionelle Weg: Der Key liegt in einer Datei **`.env`** (nur auf deinem Rechner, wird von Git ignoriert). "
               "Der Code liest ihn zur Laufzeit über Umgebungsvariablen. Wir teilen nur die Vorlage `.env.example` (ohne echte Werte!).\n\n"
               "**WIE & TRY:** In dieser Akademie brauchst du das Schlüssel-Lesen **nicht selbst** zu programmieren – "
               "das übernimmt die zentrale Konfiguration. Aber schau einmal hinter die Kulissen:"),
        ("code", '''\
import os
from dotenv import load_dotenv   # das Package python-dotenv liest .env-Dateien

load_dotenv()                    # .env laden (falls vorhanden)

beispiel_name = os.environ.get("BEISPIEL_NAME", "unbekannt")
print("BEISPIEL_NAME aus .env:", beispiel_name)

key = os.environ.get("MISTRAL_API_KEY", "")
if key:
    # Niemals den ganzen Key ausgeben! Nur ein kurzer Hinweis:
    print("MISTRAL_API_KEY ist gesetzt (beginnt mit", key[:4] + "...)")
else:
    print("Kein Key gesetzt -> die Akademie laeuft im sicheren Offline-Modus.")'''),
        ("md", "### 🛑 Fehler sind Freunde (4): Import & API-Fehler (Vorschau)\n\n"
               "In den nächsten Lektionen begegnest du drei Klassikern:\n"
               "- **`ModuleNotFoundError`** → Package fehlt: `pip install -r requirements.txt` (und: ist die venv aktiv?).\n"
               "- **API-Fehler 401** → Key fehlt oder ist falsch (`.env` prüfen).\n"
               "- **API-Fehler 429** → zu viele Anfragen zu schnell: kurz warten.\n\n"
               "Wir fangen diese Fehler in echtem Code mit `try/except` ab – lerne das Muster jetzt an einem harmlosen Beispiel:"),
        ("code", '''\
def sichere_division(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Division durch Null geht nicht."

print(sichere_division(10, 2))
print(sichere_division(10, 0))'''),
        ("md", "## ✏️ Deine Aufgabe: Die Werkstatt prüfen\n\n"
               "Fast geschafft! Diese kleine Aufgabe verbindet alles: Funktion, Import, Fehlerbehandlung."),
        ("ex", {
            "titel": "Zusammenfassungs-Werkstatt",
            "ziel": "Du schreibst eine Funktion, die eine Liste von Zahlen analysiert – und auch bei Unsinn nicht abstürzt.",
            "anforderungen": [
                "Schreibe `analyse(zahlen)`, das ein Dictionary zurückgibt mit den Schlüsseln `\"anzahl\"`, `\"durchschnitt\"` und `\"maximum\"`.",
                "Bei einer leeren Liste: `{\"anzahl\": 0, \"durchschnitt\": 0, \"maximum\": 0}` – ohne Absturz.",
                "Nutze in der Funktion `try/except` mindestens einmal (z. B. für den Leerfall oder für die Division).",
            ],
            "starter": '''\
def analyse(zahlen):
    # YOUR CODE HERE
    pass

print(analyse([2, 4, 9]))''',
            "kriterien": [
                "`analyse([2, 4, 9])` liefert `anzahl=3`, `durchschnitt=5.0`, `maximum=9`.",
                "`analyse([])` liefert alle Werte als 0 – kein Crash.",
            ],
            "checks": '''\
ergebnis = analyse([2, 4, 9])
assert ergebnis["anzahl"] == 3 and ergebnis["maximum"] == 9
assert abs(ergebnis["durchschnitt"] - 5.0) < 0.001
leer = analyse([])
assert leer == {"anzahl": 0, "durchschnitt": 0, "maximum": 0}
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Baue zuerst das Ergebnis-Dict für den Leerfall und gib es mit `return` zurück.",
                "Für das Maximum gibt es die eingebaute Funktion `max(zahlen)`.",
            ],
            "loesung": '''\
def analyse(zahlen):
    try:
        return {
            "anzahl": len(zahlen),
            "durchschnitt": sum(zahlen) / len(zahlen),
            "maximum": max(zahlen),
        }
    except (ZeroDivisionError, ValueError):   # leere Liste: beide moeglich
        return {"anzahl": 0, "durchschnitt": 0, "maximum": 0}''',
            "loesung_md": "Der `try`-Block enthält den Normalfall; wenn die Liste leer ist, löst `sum/len` bzw. `max` "
                          "einen Fehler aus, den `except` in ein sauberes Ergebnis-Dict übersetzt. Die Funktion kann "
                          "damit **nie** abstürzen – genau das wirst du von deinem Assistenten später auch verlangen.",
            "reflexion": [
                "1. Warum wäre \"der Key steht kurz im Code, ich lösche ihn später\" gefährlich? (Stichwort: Git-Historie!)",
                "2. Was ist der Unterschied zwischen `return` und `print` in einer Funktion – und woran merkst du den Fehler?",
            ],
        }),
    ],
    "weiter": "**🚀 Jetzt wird es spannend – Lektion 03:** `notebooks/02_llm/03_erster_llm_call.ipynb` – "
              "dein Python redet zum ersten Mal mit einer echten KI!",
}

SPECS_A = [START_HERE, NB_01, NB_02]
