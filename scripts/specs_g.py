"""Notebook-Specs Teil G: Capstone-Systemtest + Testing (Lektion 19-20)."""

NB_19 = {
    "pfad": "notebooks/10_capstone/19_capstone_systemtest.ipynb",
    "titel": "Lektion 19: 🏁 Das große System – live getestet",
    "zeit": "~75 Minuten",
    "schwierigkeit": "Fortgeschritten",
    "voraussetzungen": "Lektion 01–18",
    "baut": "Den kompletten End-to-End-Test deines finalen Assistenten – und den Start der echten Web-Oberfläche",
    "ziele": [
        "das finale System (final-project/) über seine API komplett durchtesten",
        "alle Lektionen im Code des Finale wiedererkennen (Code-Recognition)",
        "den Human-in-the-Loop-Roundtrip über HTTP nachweisen",
        "die finale Streamlit-Oberfläche starten",
        "erklären, wie Notebook-Wissen und finale Anwendung zusammenhängen",
    ],
    "cells": [
        ("md", "## 🏁 Das Finale – was du gebaut hast\n\n"
               "Im Ordner `final-project/knowledge-research-agent/` läuft **dein gesamtes Wissen** als echtes System:\n\n"
               "```text\nBrowser (Streamlit) → FastAPI-Backend → LangGraph-Workflow\n                                        ├─ Vektor-RAG (Lektion 08/09)\n                                        ├─ Knowledge Graph (Lektion 10-12)\n                                        └─ Freigabe-Workflow (Lektion 15/17)\n```\n\n"
               "**Warum über die API testen?** Der TestClient spricht **exakt dieselben Endpunkte** an wie das Frontend – "
               "du testest damit das System, wie der Browser es sieht. Und: alles läuft offline (Simulation), wie gewohnt."),
        ("code", '''\
import sys
from pathlib import Path

FINALE = ROOT / "final-project" / "knowledge-research-agent"
sys.path.insert(0, str(FINALE))

from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)
status = client.get("/status").json()
print("Status:", {k: status[k] for k in ("status", "modus", "anbieter", "modell", "api_key")})
print("Dokumente:", status["dokumente"], "| Graph:", status["graph_knoten"], "Nodes,", status["graph_kanten"], "Kanten")'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Der Status-Endpunkt zeigt dir **ohne Geheimnisse**: Anbieter, Modell, Key-Status („gesetzt\"/„nicht gesetzt\") – "
               "genau wie dein Verbindungstest aus START_HERE. Die zentrale Konfiguration durchzieht ALLES."),
        ("md", "## Test 1: Chat mit Routing (dein Build-3-Agent!)"),
        ("code", '''\
def frage_system(text):
    antwort = client.post("/chat", json={"nachricht": text, "session_id": "notebook-test"})
    antwort.raise_for_status()
    return antwort.json()

for frage in ("Was steht ueber die Abteilung Engineering?",
              "Wer haengt am AI Assistant dran?",
              "Was wissen wir gesamt ueber das Projekt?"):
    daten = frage_system(frage)
    print(f"FRAGE: {frage}")
    print(f"  Route: {daten['route']} | Doku: {len(daten['dokumente'])} | Graph: {len(daten['graph_fakten'])}")
    for fakt in daten["graph_fakten"][:2]:
        print("   Graph-Fakt:", fakt)
    print()'''),
        ("md", "## Test 2: Dokumente hochladen + Verlauf\n\n"
               "Dein Assistent lernt zur Laufzeit dazu – Wissensbasis-Verwaltung wie im Frontend:"),
        ("code", '''\
upload = client.post("/documents", json={
    "titel": "notiz-aus-notebook",
    "inhalt": "Dies ist eine Testnotiz ueber die Weiterbildung im Unternehmen. "
              "Alle Mitarbeitenden haben Zugang zum Lernportal."})
print("Upload:", upload.json())

historie = client.get("/history", params={"session_id": "notebook-test"}).json()
print("Verlauf-Eintraege:", len(historie["eintraege"]))'''),
        ("md", "## Test 3: Der Freigabe-Roundtrip über HTTP\n\n"
               "Jetzt der stärkste Beweis: **Vorschlag → Interrupt → Genehmigung → Graph verändert.** "
               "Genau wie in Lektion 15 – nur dass der Mensch hier \"ein Browser\" wäre:"),
        ("code", '''\
kanten_vorher = client.get("/status").json()["graph_kanten"]

vorschlag = client.post("/facts/propose", json={
    "von": "Clara", "typ": "WORKS_FOR", "zu": "Acme",
    "grund": "Steht implizit im Firmenprofil."}).json()
print("Status:", vorschlag["status"])
print("Interrupt-Frage:", vorschlag["details"]["frage"])
print("Fakt:", vorschlag["details"]["fakt"])

freigabe = client.post("/facts/approve", json={
    "thread_id": vorschlag["thread_id"], "genehmigt": True}).json()
print("Ergebnis:", freigabe["ergebnis"])

kanten_nachher = client.get("/status").json()["graph_kanten"]
print(f"Kanten: {kanten_vorher} -> {kanten_nachher} (+1 = Genehmigung wirkt)")'''),
        ("ex", {
            "titel": "Der Ablehnungs-Beweis (und dein M6)",
            "ziel": "Du beweist, dass Ablehnung den Graph NICHT verändert – und erkennst dein eigenes Wissen im Finale-Code wieder.",
            "anforderungen": [
                "Schlage einen **riskanten** Fakt vor (z. B. `Ben MANAGES Acme`, Grund: „Vermutung ohne Beleg\") und lehne ihn ab (`genehmigt=False`).",
                "Beweis: Die Kantenanzahl ist danach unverändert, der `ABGELEHNT`-Eintrag steht im Audit-Log (`/audit`).",
                "**Code-Recognition:** Öffne `final-project/knowledge-research-agent/backend/graphs/workflow.py` und `backend/agents/approval.py`. "
                "Markiere (als Kommentar hier): mindestens 4 Wiedererkennungen aus deinen Lektionen (z. B. „klassifizieren = Lektion 13\", „interrupt = Lektion 15/17\").",
            ],
            "starter": '''\
# YOUR CODE HERE: riskanter Vorschlag + Ablehnung + Kanten-Beweis

# YOUR CODE HERE: Audit-Log abfragen

# MEINE WIEDERERKENNUNGEN (mindestens 4):
# ...''',
            "kriterien": [
                "Die Kantenanzahl ist nach der Ablehnung unverändert.",
                "Das Audit-Log enthält den ABGELEHNT-Eintrag.",
                "Mindestens 4 Wiedererkennungen sind als Kommentar dokumentiert.",
            ],
            "checks": '''\
audit = client.get("/audit").json()["eintraege"]
assert any("ABGELEHNT" in e for e in audit), "Ablehnung muss im Audit-Log stehen!"
assert client.get("/status").json()["graph_kanten"] == kanten_nachher
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Vorschlag und Freigabe laufen exakt wie in Test 3 – nur mit `genehmigt=False`.",
                "Audit: `client.get(\"/audit\").json()[\"eintraegen\"]`.",
                "Für die Wiedererkennungen: Lies die Dateien mit `Path(...).read_text()` oder öffne sie im Editor.",
            ],
            "loesung": '''\
kanten_vor_ablehnung = client.get("/status").json()["graph_kanten"]

vorschlag = client.post("/facts/propose", json={
    "von": "Ben", "typ": "MANAGES", "zu": "Acme",
    "grund": "Vermutung ohne Beleg."}).json()
freigabe = client.post("/facts/approve", json={
    "thread_id": vorschlag["thread_id"], "genehmigt": False}).json()
print("Ergebnis:", freigabe["ergebnis"])

kanten_nach_ablehnung = client.get("/status").json()["graph_kanten"]
print("Kanten unverändert:", kanten_vor_ablehnung == kanten_nach_ablehnung)
print("Audit:", [e for e in client.get("/audit").json()["eintraege"] if "ABGELEHNT" in e])

# MEINE WIEDERERKENNUNGEN:
# 1. workflow.py: klassifiziere() = meine Router-Logik aus Lektion 13/15
# 2. workflow.py: konditionale Kanten = die Weiche (Lektion 13)
# 3. approval.py: interrupt() vor der Aenderung = Lektion 15 (Freigabe)
# 4. approval.py: AUDIT_LOG = mein Audit aus Lektion 15
# 5. api/main.py: Pydantic-Schemas = strukturierte Ausgaben (Lektion 09)
# 6. retrieval/vector.py: Retriever = Build 2 (Lektion 08/09)''',
            "loesung_md": "Der Ablehnungs-Beweis schließt den Sicherheits-Kreis: Lesen erlaubt der Agent allein "
                          "(Whitelist, Lektion 12), Schreiben nur mit dir (Lektion 15/17) – und das Audit-Log "
                          "macht jede Entscheidung nachvollziehbar. **Du hast dieses System nicht nur benutzt – "
                          "du hast jeden seiner Bausteine selbst gebaut.**",
            "reflexion": [
                "1. Vergleiche mit deinem Build-1-Assistenten aus Lektion 05: Was von deinem damaligen Code steckt konzeptionell noch in diesem System?",
                "2. Warum sitzt der Verlauf im Backend (Sessions) und nicht im Frontend?",
            ],
        }),
        ("md", "## 🖥️ Die finale Oberfläche starten\n\n"
               "Jetzt der Moment: **Dein System als echte Web-App.** Zwei Terminals im Projektordner:\n\n"
               "```bash\n# Terminal 1 – Backend:\ncd final-project/knowledge-research-agent\nuvicorn backend.api.main:app --port 8000\n\n# Terminal 2 – Frontend:\nstreamlit run final-project/knowledge-research-agent/frontend/app.py\n```\n\n"
               "Oder alles auf einmal (inkl. Neo4j, wenn Docker vorhanden): `cd final-project/knowledge-research-agent && docker compose up --build`\n\n"
               "**Probiere im Browser** (http://localhost:8501):\n"
               "- 💬 Chat mit Routen-Badges (vektor/graph/hybrid) und Quellen-Expandern\n"
               "- 🕸️ Graph-Explorer: Nodes klicken, Properties und Verbindungen sehen\n"
               "- 📄 Dokumente hochladen und darüber fragen\n"
               "- 🧪 Prompt-Labor: System-Prompt und Temperature live verändern\n"
               "- ✋ Freigaben: einen Fakt genehmigen UND ablehnen (Audit prüfen!)\n\n"
               "Die Sidebar zeigt dir immer Anbieter, Modell und Endpoint – **niemals** den API-Key."),
        ("code", '''\
from pathlib import Path
for datei in ("frontend/app.py", "backend/api/main.py"):
    p = FINALE / datei
    print("Bereit:", datei, "|", p.exists())
print("\\nStartbefehle stehen im Markdown oben. Viel Erfolg mit DEINEM System! 🚀")'''),
    ],
    "weiter": "**Letzte Lektion:** `notebooks/11_testing/20_testing_und_evaluierung.ipynb` – "
              "du lernst, dein System zu prüfen wie eine Ingenieurin – und schreibst deine Abschluss-Reflexion.",
}

NB_20 = {
    "pfad": "notebooks/11_testing/20_testing_und_evaluierung.ipynb",
    "titel": "Lektion 20: Testing, Evaluierung & dein Abschluss",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Mittel",
    "voraussetzungen": "Lektion 01–19",
    "baut": "Eigene Tests für dein System, eine kriterienbasierte Evaluierung – und deine Abschluss-Reflexion",
    "ziele": [
        "Unit- und Integrationstests für deine Bausteine schreiben",
        "erklären, warum Mocks die *Mechanik*, aber nicht die *Qualität* echter LLM-Antworten prüfen",
        "eine kriterienbasierte **Evaluierung** (Erfolgsquote) durchführen",
        "Kosten-Regeln benennen (Loop-Limits, kleine Modelle, Caching)",
        "die drei Architekturen mit eigenen Worten vergleichen (Abschluss!)",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: „Ich habe es einmal probiert\" ist kein Test\n\n"
               "**WARUM:** KI-Verhalten ist nicht deterministisch – einmal laufen lassen beweist gar nichts. "
               "Und wenn du später einen Prompt änderst: Wer merkt, dass die Antwortqualität eingebrochen ist?\n\n"
               "**WAS – die zwei Prüfarten:**\n"
               "- **Unittest** = Rechenaufgabe mit eindeutiger Lösung (`30 Urlaubstage == 30`). Prüft **Logik**.\n"
               "- **Eval** = Bewertungsraster („Enthält die Antwort die richtige Quelle?\"). Prüft **Eigenschaften** von Antworten.\n\n"
               "**Metapher:** Mocks prüfen, ob der Motor sich dreht (Mechanik). Evals prüfen, ob das Auto gut fährt (Qualität) – "
               "letzteres braucht mit echtem Modell mehr als eine Probefahrt."),
        ("code", '''\
# Unit-Test-Stil: wir pruefen Logik, die wir selbst gebaut haben.
import sys
from pathlib import Path
sys.path.insert(0, str(ROOT))
from lernakademie.build1 import lade_dokumente, suche_relevant

def test_suche_findet_urlaub():
    abschnitte = lade_dokumente()
    treffer = suche_relevant("Wie viele Urlaubstage gibt es?", abschnitte)
    assert treffer, "Urlaubsfrage muss Treffer liefern"
    assert treffer[0]["titel"] == "Urlaub", f"Erster Treffer: {treffer[0]['titel']}"

def test_suche_leer_bei_unbekannt():
    assert suche_relevant("Weihnachtsgeld Hoehe Bonus?", lade_dokumente()) == []

for test in (test_suche_findet_urlaub, test_suche_leer_bei_unbekannt):
    test()          # im Notebook einfach aufrufen – rot = AssertionError
    print("PASS:", test.__name__)'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Ein `assert` ist ein Test: Stimmt die Behauptung nicht, **crasht** die Zelle mit AssertionError – "
               "das ist der Witz, nicht der Fehler! Diese zwei Tests laufen (neben 40+ weiteren) in der **CI** des Repositories "
               "(`.github/workflows/tests.yml`) bei jedem Push automatisch – offline, ohne Kosten."),
        ("ex", {
            "titel": "Deine eigenen zwei Tests",
            "ziel": "Du schreibst Tests für Funktionen, die DU gebaut hast – und zwar für Grenzfälle.",
            "anforderungen": [
                "Schreibe zwei Test-Funktionen (mit `assert`) für Bausteine aus deinen Lektionen – z. B.: Build-2-Quellen korrekt (Lektion 09), GraphStore-Nachbarn (Lektion 10) oder die Klassifikation (Lektion 13/15).",
                "Jeder Test prüft mindestens einen **Grenzfall** (leere Liste, unbekannte Frage, andere thread_id …).",
                "Rufe beide auf – beide müssen PASS drucken.",
            ],
            "starter": '''\
def test_1():
    # YOUR CODE HERE: eine Behauptung ueber deinen Assistenten pruefen
    pass

def test_2():
    # YOUR CODE HERE: Grenzfall!
    pass

test_1(); print("PASS: test_1")
test_2(); print("PASS: test_2")''',
            "kriterien": [
                "Beide Tests laufen grün (kein AssertionError).",
                "Mindestens ein Grenzfall ist geprüft.",
                "Die Tests nutzen Bausteine aus deinen Lektionen (nicht nur `assert True`).",
            ],
            "checks": '''\
test_1()
test_2()
print("Alle Prüfungen bestanden! ✅ (Deine Tests laufen jetzt – das ist echte Ingenieursarbeit.)")''',
            "hinweise": [
                "Beispiele: `assert lade_dokumente()` / `assert suche_relevant(...) == []` bei Unsinn / "
                "`assert store.find_node(\"Person\", name=\"Anna\") is not None`.",
                "Ein guter Testname beschreibt die Behauptung: `test_suche_leer_bei_unbekannt`.",
            ],
            "loesung": '''\
from lernakademie.build2 import beantworte

def test_build2_quellen_korrekt():
    ergebnis = beantworte("Wie viele Urlaubstage gibt es?")
    assert "mitarbeiter-handbuch.md" in ergebnis["quellen"], ergebnis["quellen"]

def test_build2_grenzfall_ehrlich():
    ergebnis = beantworte("Wie hoch ist das Weihnachtsgeld?")
    assert ergebnis["quellen"] == [], "Ohne Treffer: keine Quellen erfinden!"
    assert "leider nicht" in ergebnis["antwort"]

test_1 = test_build2_quellen_korrekt
test_2 = test_build2_grenzfall_ehrlich
test_1(); print("PASS: test_build2_quellen_korrekt")
test_2(); print("PASS: test_build2_grenzfall_ehrlich")''',
            "loesung_md": "Genau diese beiden Tests existieren (in ähnlicher Form) in `tests/` des Repositories – "
                          "du hast gerade reproduziert, wie die CI dein Projekt bei jedem Push prüft. "
                          "Der Grenzfall („ehrlich leer\") ist der wichtigste: Er verhindert, dass dein Assistent "
                          "Quellen erfindet.",
            "reflexion": [
                "1. Was ist ein Regressionstest im KI-Kontext? (Stichwort: Prompt geändert → Tests/Evals laufen lassen.)",
                "2. Warum ist eine 100%-Erfolgsquote bei zu einfachen Eval-Fragen gefährlich?",
            ],
        }),
        ("md", "## 🧠 Konzept: Evaluierung – die Antwort-Qualität messen\n\n"
               "**WAS:** Eine Eval definiert **Testfragen mit erwarteten Eigenschaften** (nicht mit erwartetem Volltext!). "
               "Offline ist alles deterministisch – die Quote ist reproduzierbar (Feature!)."),
        ("code", '''\
from lernakademie.build2 import beantworte

EVAL_Faelle = [   # (frage, erwartete Eigenschaft als Funktion)
    ("Wie viele Urlaubstage gibt es?",
     lambda e: "mitarbeiter-handbuch.md" in e["quellen"]),
    ("Wie richte ich VPN ein?",
     lambda e: "it-handbuch.md" in e["quellen"]),
    ("Was gilt fuer Passwoerter?",
     lambda e: e["gefundene_stellen"] >= 1),
    ("Wie hoch ist das Weihnachtsgeld?",
     lambda e: e["quellen"] == [] and "leider nicht" in e["antwort"]),
]

treffer = 0
for frage, pruefung in EVAL_Faelle:
    ergebnis = beantworte(frage)
    bestanden = pruefung(ergebnis)
    treffer += int(bestanden)
    print(f"{'PASS' if bestanden else 'FAIL'} | {frage}")
print(f"\\nErfolgsquote: {treffer}/{len(EVAL_Faelle)} = {100 * treffer / len(EVAL_Faelle):.0f}%")'''),
        ("md", "## 🧠 Konzept: Kosten & Betrieb in einem Bild\n\n"
               "Die drei Betreiber-Regeln, die die Akademie von Anfang an eingebaut hat:\n"
               "1. **Bremsen:** Loop-Limits (Lektion 13/18), `max_runden` beim Supervisor, Historien-Kürzung (Lektion 04).\n"
               "2. **Geheimnisse:** nur `.env`, niemals im Code, Keys maskiert in Logs.\n"
               "3. **Nachvollziehbarkeit:** strukturierte Logs, Audit-Log (Lektion 15/19) – und optional LangSmith "
               "(reine Umgebungsvariablen, kein Codeumbau).\n\n"
               "**Was vor echter Veröffentlichung noch fehlt:** Login/Auth, HTTPS, Rate-Limits – Ausblick, kein Teil dieser Akademie."),
        ("md", "## 🎓 Deine Abschluss-Reflexion (der letzte Auftrag)\n\n"
               "Beantworte schriftlich (in der nächsten Zelle) – **in deinen eigenen Worten**:\n\n"
               "1. **Wann würdest du heute welche der drei Architekturen bauen?** Nenne je ein konkretes Beispiel aus deinem Leben: "
               "ein Fall für Build 1 (reines Python), Build 2 (LangChain + RAG), Build 3 (LangGraph + Graph + Agent).\n"
               "2. **Warum kann dein Build-3-Assistent Fragen beantworten, die Build 1 und 2 zusammen nicht konnten?** "
               "(Stichwort: Emergenz aus Lektion 10/14.)\n"
               "3. **Was bedeutet \"anbieter-unabhängig\" konkret?** Was musst du ändern, um von Mistral zu einem lokalen Server zu wechseln – und was NICHT?\n\n"
               "Vergleich zum Nachschauen: [docs/same-problem-three-architectures.md](../../docs/same-problem-three-architectures.md)"),
        ("code", '''\
# MEINE ABSCHLUSST-REFLEXION:
# 1. Build 1 wuerde ich fuer ... bauen, weil ...
#    Build 2 passt auf ..., Build 3 brauchte ich, wenn ...
# 2. ...
# 3. ...
'''),
        ("md", "## 🏆 Geschafft!\n\n"
               "Du hast den Weg von **\"Was ist ein Terminal?\"** bis **\"Ich habe ein getestetes Multi-Quellen-Wissenssystem "
               "gebaut und über ein Frontend bedient\"** zurückgelegt – in 20 Lektionen, drei Builds und einem Finale.\n\n"
               "**Dein nächstes Projekt:** Nutze die Bausteine (`lernakademie/`), deine `data/` und das Finale als Vorlage – "
               "und bau den Assistenten für **dein** Wissen. Die Werkzeuge hast du jetzt.\n\n"
               "*(Deinen Fortschritt kannst du in `PROGRESS.md` abhaken – und der Vergleich der Architekturen lebt in "
               "[docs/same-problem-three-architectures.md](../../docs/same-problem-three-architectures.md).)*"),
    ],
    "weiter": None,
}

SPECS_G = [NB_19, NB_20]
