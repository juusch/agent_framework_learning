"""Notebook-Specs Teil B: LLM-Grundlagen + BUILD 1 (Lektion 03-06)."""

NB_03 = {
    "pfad": "notebooks/02_llm/03_erster_llm_call.ipynb",
    "titel": "Lektion 03: Dein erster LLM-Aufruf",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Leicht",
    "voraussetzungen": "Lektion 01–02 (Funktionen, .env)",
    "baut": "Deine erste echte Konversation zwischen Python und einer KI",
    "ziele": [
        "erklären, was ein LLM ist – und was es NICHT ist",
        "erklären, was ein API-Call technisch tut (Nachrichten, Rollen, Antwort)",
        "aus Python eine Nachricht an das konfigurierte Modell senden",
        "die Antwort korrekt auslesen",
        "das Verhalten mit System-Nachricht und **Temperature** steuern",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Das LLM – eine sehr belesene, manchmal unzuverlässige Assistentin\n\n"
               "**WARUM:** Bis jetzt konnte dein Programm nur das, was du exakt hineingeschrieben hast. "
               "Ein **LLM** (Large Language Model, z. B. Mistral) kann **freie Sprache** verstehen und beantworten – "
               "das öffnet völlig neue Arten von Programmen: Chatbots, Zusammenfasser, Suchassistenten.\n\n"
               "**WAS:** Ein LLM ist eine gigantische **Textfortsetzungs-Maschine**: Es hat aus riesigen Textmengen gelernt, "
               "welches Wort wahrscheinlich als Nächstes kommt. Deshalb: Es \"weiß\" nichts – es **sagt** nur wahrscheinliche, "
               "meist sinnvolle Sätze. Manchmal erfindet es überzeugend klingende Dinge (**Halluzination**) – das prägt dein ganzes weiteres Bauen.\n\n"
               "**Metapher API:** Stell dir ein **Restaurant** vor: Dein Programm ist der Gast, die **API** ist der Kellner, "
               "das Modell ist die Küche. Du gibst dem Kellner eine Bestellung (dein Prompt), die Küche kocht, "
               "der Kellner bringt das Gericht (die Antwort). Der **API-Key** ist deine Mitgliedskarte – "
               "und `docs/local-ai-server.md` zeigt dir, wie du das ganze Restaurant auch auf **deinen eigenen Rechner** holst (LM Studio, Ollama, …)."),
        ("md", "## 🧠 Konzept: Nachrichten & Rollen\n\n"
               "Ein Gespräch mit einem LLM ist eine **Liste von Nachrichten** (du kennst Listen aus Lektion 01!). "
               "Jede Nachricht hat eine **Rolle**:\n\n"
               "| Rolle | Wer spricht? | Beispiel |\n|---|---|---|\n"
               "| `system` | Du als Programmierer (Anweisung an den Assistenten) | \"Du bist ein freundlicher Erklärbbär.\" |\n"
               "| `user` | Der Nutzer | \"Was ist eine API?\" |\n"
               "| `assistant` | Das Modell (frühere Antworten) | \"Eine API ist …\" |\n\n"
               "Die System-Nachricht ist wie ein **Flüstern zum Kellner vor Servicebeginn**: "
               "\"Behandle alle Gäste höflich und erkläre kinderleicht.\""),
        ("md", "## 🔎 Beispiel: Die erste Nachricht\n\n"
               "Wir nutzen `lernakademie.llm_client.get_api_client()` – je nach `.env` spricht der Client mit Mistral Cloud, "
               "einem lokalen Server **oder** der Offline-Simulation (dann siehst du `[OFFLINE]`-Antworten – der Ablauf ist identisch, nur kostenlos)."),
        ("code", '''\
from lernakademie.llm_client import get_api_client, get_model_name

client = get_api_client()
antwort = client.chat.complete(
    model=get_model_name(),
    messages=[
        {"role": "system", "content": "Du bist ein freundlicher Erklaerbaer fuer Technik-Anfaenger."},
        {"role": "user", "content": "Erklaere in zwei Saetzen, was eine API ist."},
    ],
)
print("Rohe Antwort des Servers:", antwort)'''),
        ("md", "### Was sehen wir hier?\n"
               "Der Server schickt ein Objekt mit `choices` – einer **Liste** von Antwortmöglichkeiten (normalerweise genau einer). "
               "Der eigentliche Text steckt in `antwort.choices[0].message.content`. Diese Verschachtelung verstehen zu können, "
               "ist dein erste **Datenauslese-Training** – gleich machst du es selbst."),
        ("code", '''\
inhalt = antwort.choices[0].message.content
print("Nur der Text:")
print(inhalt)'''),
        ("md", "## 🧠 Konzept: Temperature – Kreativitäts-Regler\n\n"
               "**WAS:** `temperature` steuert, wie **vorhersehbar** das Modell antwortet.\n"
               "**Metapher:** ein Jazz-Saxofonist: Bei `0.0` spielt er die Noten exakt wie geschrieben. "
               "Bei `0.9` improvisiert er frei – meist stimmig, manchmal überraschend.\n\n"
               "**Faustregel (merk dir das!):** Fakten & Struktur → niedrig (0.0–0.2) · Ideen & Kreatives → hoch (0.7+).\n\n"
               "**TRY:** Führe die Zelle mehrfach aus und vergleiche:"),
        ("code", '''\
for temperatur in (0.0, 0.9):
    print(f"--- temperature={temperatur} ---")
    antwort = client.chat.complete(
        model=get_model_name(),
        messages=[{"role": "user",
                   "content": "Nenne ein kreatives Geschenk fuer eine Person, die Kaffee liebt."}],
        temperature=temperatur,
    )
    print(antwort.choices[0].message.content[:200])'''),
        ("md", "## 🧠 Konzept: Tokens & Kosten\n\n"
               "LLMs rechnen nicht in Buchstaben oder Wörtern, sondern in **Tokens** (kleine Textstücke, oft 3–4 Zeichen). "
               "Faustregel für Deutsch: **`zeichen // 4` ≈ Anzahl Tokens**. Warum das zählt:\n"
               "- Das **Kontextfenster** (wie viel das Modell auf einmal lesen kann) wird in Tokens gemessen – wie ein Schreibtisch, auf den nur begrenzt Blätter passen.\n"
               "- Die **Kosten** pro Anfrage zählen Tokens.\n\n"),
        ("code", '''\
text = "Erklaere in zwei Saetzen, was eine API ist."
print("Geschaetzte Tokens:", len(text) // 4)'''),
        ("md", "## 🛑 Fehler sind Freunde (5): API-Fehler verstehen\n\n"
               "Die drei Klassiker und ihre Bedeutung:\n"
               "- **401 (unauthorized):** Key fehlt oder ist falsch → `.env` prüfen.\n"
               "- **429 (rate limit):** zu viele Anfragen zu schnell → kurz warten.\n"
               "- **Connection error:** Server nicht erreichbar → läuft er überhaupt? URL prüfen (`LLM_BASE_URL`).\n\n"
               "TRY: Hier simulieren wir einen toten Endpunkt und fangen den Fehler **freundlich** ab:"),
        ("code", '''\
import requests

def frage_server(url, frage):
    """Sendet eine Frage an einen OpenAI-kompatiblen Endpoint – mit klaren Fehlermeldungen."""
    try:
        antwort = requests.post(url, json={
            "model": "egal", "messages": [{"role": "user", "content": frage}]},
            timeout=5)
        antwort.raise_for_status()
        return antwort.json()["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "Verbindung fehlgeschlagen: laeuft der Server? Stimmt die URL (meist mit /v1)?"
    except requests.exceptions.HTTPError as fehler:
        return f"Server-Fehler {fehler.response.status_code}: Key oder Modellname pruefen."

print(frage_server("http://localhost:59999/v1", "Test"))'''),
        ("ex", {
            "titel": "Deine eigene Frage-Funktion",
            "ziel": "Du kapselst den kompletten LLM-Aufruf in EINE wiederverwendbare Funktion – dein erster Baustein für den Knowledge Assistant!",
            "anforderungen": [
                "Schreibe `frage_modell(frage, temperature=0.0)`, das eine Frage (String) entgegennimmt.",
                "Die Funktion sendet die Frage an das konfigurierte Modell (mit der Rolle `user`).",
                "Sie gibt **nur den Antworttext** als String zurück (`return`, nicht `print`).",
                "Zusatz: bei einem leeren Frage-String gibt sie einen Hinweis-Text zurück (kein Absturz).",
            ],
            "starter": '''\
from lernakademie.llm_client import get_api_client, get_model_name

def frage_modell(frage, temperature=0.0):
    # YOUR CODE HERE
    pass

print(frage_modell("Was ist Python?"))''',
            "kriterien": [
                "`frage_modell(\"...\")` gibt einen String zurück (auch im Offline-Modus!).",
                "Der Rückgabewert enthält nicht `choices` oder Rohdaten – nur den Text.",
                "Ein leerer String stürzt nicht ab.",
            ],
            "checks": '''\
ergebnis = frage_modell("Was ist Python?")
assert isinstance(ergebnis, str) and len(ergebnis) > 0, "Es soll ein nicht-leerer String zurueckkommen!"
assert "choices" not in ergebnis, "Nur der Text zurueckgeben, nicht die Rohdaten!"
leer = frage_modell("   ")
assert isinstance(leer, str), "Auch der Leerfall muss einen String liefern."
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Basis: `client = get_api_client()` und dann `client.chat.complete(model=get_model_name(), messages=[...], temperature=temperature)`.",
                "Den Text holst du mit `antwort.choices[0].message.content`.",
                "Für den Leerfall: `if not frage.strip(): return \"Bitte stelle eine echte Frage.\"` am Anfang.",
            ],
            "loesung": '''\
from lernakademie.llm_client import get_api_client, get_model_name

def frage_modell(frage, temperature=0.0):
    if not frage.strip():
        return "Bitte stelle eine echte Frage."
    client = get_api_client()
    antwort = client.chat.complete(
        model=get_model_name(),
        messages=[{"role": "user", "content": frage}],
        temperature=temperature,
    )
    return antwort.choices[0].message.content

print(frage_modell("Was ist Python?"))''',
            "loesung_md": "Erst die Eingabe prüfen (leer = höflicher Hinweis), dann den Client holen, senden und nur den "
                          "relevanten Teil zurückgeben. Diese Funktion ist der Urvater ALLER späteren Bausteine – "
                          "in Build 1 wirst du sie zu einem Wissens-Assistenten ausbauen.",
            "reflexion": [
                "1. Warum sind die drei Rollen (system/user/assistant) getrennt – was könntest du mit der System-Rolle steuern?",
                "2. Welchen Temperature-Wert würdest du für einen Rechtschreibkorrektor wählen – und warum?",
            ],
            "challenge": ("Erweitere `frage_modell` um einen Parameter `system_prompt` (Standard: „Du bist ein hilfreicher Assistent.“) "
                          "und teste, wie sich die Antwort ändert.",
                          '''\
# YOUR CODE HERE (Challenge)'''),
        }),
    ],
    "weiter": "**Weiter mit Lektion 04:** `notebooks/02_llm/04_chatbot_gedaechtnis.ipynb` – "
              "aus einem einzelnen Aufruf wird ein **Gespräch mit Gedächtnis**. (Spoiler: Das Gedächtnis ist eine Liste – Lektion 01 lässt grüßen!)",
}

NB_04 = {
    "pfad": "notebooks/02_llm/04_chatbot_gedaechtnis.ipynb",
    "titel": "Lektion 04: Chatbot mit Gedächtnis",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Leicht",
    "voraussetzungen": "Lektion 03",
    "baut": "Einen funktionierenden Chatbot, der sich an das Gespräch erinnert",
    "ziele": [
        "erklären, warum LLMs **gedächtnislos** sind – und was das für deine Architektur bedeutet",
        "einen Gesprächsverlauf als Nachrichten-Liste pflegen",
        "eine Budget-Bremse einbauen (Historie begrenzen)",
        "mit Temperature experimentieren und die Wirkung dokumentieren",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Das Gedächtnis-Geheimnis\n\n"
               "**WARUM:** Jeder API-Aufruf ist ein **isolierter Moment**. "
               "Das Modell erinnert sich an NICHTS zwischen zwei Aufrufen – dein Chatbot aus Lektion 03 hat \"vergessen\", "
               "was du eine Sekunde vorher gefragt hast.\n\n"
               "**DAS Geheimnis:** Chatbots mit \"Gedächtnis\" schicken einfach **die ganze bisherige Liste** wieder mit. "
               "**Metapher:** Der Assistent hat Goldfisch-Gedächtnis. **Du** als Programmierer bist die Lösung: "
               "Du führst das Protokoll (die `messages`-Liste) und legst es bei jeder Frage **komplett wieder auf den Tisch**.\n\n"
               "Schau genau hin – das ist buchstäblich eine Liste aus Lektion 01:"),
        ("code", '''\
from lernakademie.llm_client import get_api_client, get_model_name

client = get_api_client()
verlauf = [
    {"role": "system", "content": "Du bist ein freundlicher Lern-Coach fuer Python-Anfaenger."},
]

def sage(text):
    """Ein Gespraechszug: Frage anhängen, senden, Antwort merken."""
    verlauf.append({"role": "user", "content": text})
    antwort = client.chat.complete(model=get_model_name(), messages=verlauf)
    inhalt = antwort.choices[0].message.content
    verlauf.append({"role": "assistant", "content": inhalt})
    return inhalt

sage("Hallo! Ich heisse Alex und lerne Python.")
antwort = sage("Wie heisse ich noch mal?")   # <-- Erinnerungstest!
print("Antwort auf die Erinnerungsfrage:")
print(antwort)'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Beim zweiten `sage(...)` enthält `verlauf` **vier** Nachrichten: System, Name-Nennung, Modell-Antwort, neue Frage. "
               "Das Modell \"sieht\" den ganzen Tisch – deshalb kann es auf Alex antworten. "
               "**Gedächtnis ist hier kein Zauber, sondern Listen-Management.**"),
        ("code", '''\
for nachricht in verlauf:
    print(f"[{nachricht['role']:9s}] {nachricht['content'][:60]}")'''),
        ("md", "## 🧠 Konzept: Die Budget-Bremse\n\n"
               "**WARUM:** Jede Nachricht kostet Tokens (Lektion 03!) – ein endlos wachsender Verlauf wird **teuer** und "
               "irgendwann größer als das Kontextfenster (der Schreibtisch voll).\n\n"
               "**WIE:** Wir kürzen die Historie regelmäßig. **Aber:** die System-Nachricht (Index 0) muss IMMER bleiben – "
               "sonst vergisst dein Bot, wer er ist!"),
        ("code", '''\
def kuerze_historie(verlauf, max_nachrichten=20):
    """Behaelt die System-Nachricht (Index 0) und die letzten Nachrichten."""
    if len(verlauf) <= max_nachrichten:
        return verlauf
    return [verlauf[0]] + verlauf[-(max_nachrichten - 1):]

langer_verlauf = [{"role": "system", "content": "Ich bleibe!"}] + \\
    [{"role": "user", "content": f"Nachricht {i}"} for i in range(30)]
gekuerzt = kuerze_historie(langer_verlauf)
print("Vorher:", len(langer_verlauf), "| Nachher:", len(gekuerzt))
print("System bleibt:", gekuerzt[0]["content"] == "Ich bleibe!")'''),
        ("md", "## 🔎 Beispiel: Ein kompletter Chatbot\n\n"
               "Jetzt kombinieren wir alles: Verlauf, Senden, Merken, Kürzen – in **einer** sauberen Funktion:"),
        ("code", '''\
from lernakademie.llm_client import get_api_client, get_model_name

PERSONA = "Du bist ein freundlicher Lern-Coach. Antworte kurz und ohne Fachchinesisch."

def baue_chatbot(persona=PERSONA, max_nachrichten=20):
    client = get_api_client()
    verlauf = [{"role": "system", "content": persona}]

    def sage(text):
        verlauf.append({"role": "user", "content": text})
        antwort = client.chat.complete(model=get_model_name(), messages=verlauf)
        inhalt = antwort.choices[0].message.content
        verlauf.append({"role": "assistant", "content": inhalt})
        if len(verlauf) > max_nachrichten:               # Budget-Bremse
            verlauf[:] = [verlauf[0]] + verlauf[-(max_nachrichten - 1):]
        return inhalt

    return sage

bot = baue_chatbot()
for frage in ("Hallo, ich heisse Kim und arbeite im Marketing.",
              "Wie heisse ich noch mal?",
              "Was ist eine Variable?"):
    print("FRAGE:", frage)
    print("BOT  :", bot(frage)[:120], "\\n")'''),
        ("ex", {
            "titel": "Dein eigener Chatbot",
            "ziel": "Du baust einen Chatbot mit Gedächtnis UND einer sauberen, testbaren Struktur.",
            "anforderungen": [
                "Schreibe `baue_chatbot(persona=..., max_nachrichten=...)`, das eine Funktion `sage(text)` zurückgibt.",
                "Jeder Aufruf von `sage` hängt die Frage an den Verlauf an, sendet die **gesamte** Liste und merkt sich die Antwort.",
                "Der Verlauf wird auf `max_nachrichten` gekürzt – die System-Nachricht bleibt immer.",
                "Leere Eingaben geben einen Hinweis zurück und landen NICHT im Verlauf.",
            ],
            "starter": '''\
def baue_chatbot(persona="Du bist ein Assistent.", max_nachrichten=20):
    # YOUR CODE HERE
    def sage(text):
        # YOUR CODE HERE
        pass
    return sage

bot = baue_chatbot()
bot("Hallo, ich heisse Sam!")''',
            "kriterien": [
                "Zwei aufeinanderfolgende `sage`-Aufrufe teilen sich das Gedächtnis (Erinnerungstest!).",
                "Der Verlauf wächst nie über `max_nachrichten`.",
                "Leere Eingaben craschen nicht.",
            ],
            "checks": '''\
bot = baue_chatbot(max_nachrichten=10)
bot("Hallo, ich heisse Sam!")
zweiter = bot("Wie heisse ich?")
assert isinstance(zweiter, str) and len(zweiter) > 0
for i in range(15):
    bot(f"Nachricht {i}")
assert True  # kein Absturz nach vielen Nachrichten = Budget-Bremse laeuft
leer = bot("   ")
assert isinstance(leer, str)
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Kopiere das Muster aus dem Beispiel oben – aber schreib es selbst,和理解 kommt vom Tippen!",
                "Für den Leerfall: `if not text.strip(): return \"...\"` ganz am Anfang von `sage`.",
                "Das Kürzen geht in einem Schritt: `verlauf[:] = [verlauf[0]] + verlauf[-(max_nachrichten-1):]`.",
            ],
            "loesung": '''\
from lernakademie.llm_client import get_api_client, get_model_name

def baue_chatbot(persona="Du bist ein Assistent.", max_nachrichten=20):
    client = get_api_client()
    verlauf = [{"role": "system", "content": persona}]

    def sage(text):
        if not text.strip():
            return "Bitte schreib mir eine echte Nachricht."
        verlauf.append({"role": "user", "content": text})
        antwort = client.chat.complete(model=get_model_name(), messages=verlauf)
        inhalt = antwort.choices[0].message.content
        verlauf.append({"role": "assistant", "content": inhalt})
        if len(verlauf) > max_nachrichten:
            verlauf[:] = [verlauf[0]] + verlauf[-(max_nachrichten - 1):]
        return inhalt

    return sage

bot = baue_chatbot()
print(bot("Hallo, ich heisse Sam!")[:120])''',
            "loesung_md": "Der Verlauf lebt in der äußeren Funktion (`closure`) – deshalb \"überlebt\" er mehrere `sage`-Aufrufe. "
                          "Das Muster \"Daten im Closure + kleine Funktion zurückgeben\" begegnet dir in Build 2 erneut "
                          "(Retriever-Tools!). Die Budget-Bremse greift erst, wenn der Verlauf zu lang wird – die System-Nachricht "
                          "wird mit `[verlauf[0]]` explizit gerettet.",
            "reflexion": [
                "1. Was würde passieren, wenn du beim Kürzen die System-Nachricht vergisst?",
                "2. Warum kostet ein längeres Gespräch pro Nachricht MEHR als ein kurzes – und wo liegt die Grenze (Stichwort: Kontextfenster)?",
            ],
        }),
    ],
    "weiter": "**🧱 BUILD 1 beginnt – Lektion 05:** `notebooks/03_build_1/05_build1_wissensassistent.ipynb` – "
              "dein Chatbot bekommt **echtes Wissen**: Dokumente, eigene Suche, selbst gebauter Prompt. Ganz ohne Framework!",
}

NB_05 = {
    "pfad": "notebooks/03_build_1/05_build1_wissensassistent.ipynb",
    "titel": "Lektion 05: 🧱 BUILD 1 – Der Wissensassistent in reinem Python",
    "zeit": "~75 Minuten",
    "schwierigkeit": "Mittel",
    "voraussetzungen": "Lektion 01–04",
    "baut": "Die erste Version deines Personal Knowledge Assistant – komplett von Hand, ohne jedes KI-Framework",
    "ziele": [
        "Dokumente laden und in Abschnitte zerlegen",
        "eine eigene Suchfunktion (Wort-Überlappung) schreiben",
        "den Prompt **von Hand** bauen und das Modell damit füttern",
        "die manuelle Orchestrierung komplett erklären können",
        "erleben, wo diese Architektur an ihre Grenzen stößt",
    ],
    "cells": [
        ("md", "## 🧱 Willkommen zu BUILD 1!\n\n"
               "Das ist der erste Meilenstein der Akademie. Du baust jetzt den **Personal Knowledge Assistant** "
               "zum **ersten** Mal – und zwar bewusst **komplett von Hand**:\n\n"
               "- **KEIN** LangChain\n- **KEIN** Framework\n- Nur: Python, dein Wissen aus Lektion 01–04, und der direkte Modell-Aufruf\n\n"
               "**WARUM so anstrengend?** Weil du erst **verstehen** sollst, was unter der Haube passiert, "
               "bevor dir ein Framework die Arbeit abnimmt. **Metapher:** Bevor du ein Fertighaus kaufst, baust du einmal einen Schuppen aus Holz. "
               "Danach weißt du, was LangChain (Build 2) wirklich für dich tut – und was es nur **versteckt**.\n\n"
               "**Die Build-1-Architektur:**\n\n"
               "```text\nDokumente (data/*.md)\n   ↓  laden + in Abschnitte schneiden\nFrage\n   ↓  eigene Suche: Wort-Uebereinstimmung\nbeste Abschnitte\n   ↓  Prompt von Hand zusammenbauen\nLLM-Aufruf\n   ↓\nAntwort + Quellen\n```"),
        ("md", "## Schritt 1: Dokumente laden\n\n"
               "Im Ordner `data/` liegen drei erfundene \"Firmen-Handbücher\". "
               "Wir zerlegen jeden Text an seinen `## `-Überschriften in **Abschnitte** – jedes Mal ein Dictionary mit Quelle, Titel und Text "
               "(Lektion 01: Dictionarys!)."),
        ("code", '''\
from pathlib import Path

DATA = ROOT / "data"

def lade_dokumente():
    """Liest alle data/*.md und schneidet sie an ## -Ueberschriften."""
    abschnitte = []
    for datei in sorted(DATA.glob("*.md")):
        text = datei.read_text(encoding="utf-8")
        teile = text.split("## ")
        for teil in teile[1:]:                # teile[0] ist der Dokumentkopf
            titel, *rest = teil.split("\\n", 1)
            inhalt = rest[0].strip() if rest else ""
            if inhalt:
                abschnitte.append({
                    "quelle": datei.name,
                    "titel": titel.strip(),
                    "text": inhalt,
                })
    return abschnitte

abschnitte = lade_dokumente()
print(f"{len(abschnitte)} Abschnitte aus {len({a['quelle'] for a in abschnitte})} Dokumenten")
print("Beispiel:", abschnitte[0]["quelle"], "-", abschnitte[0]["titel"])'''),
        ("md", "## Schritt 2: Die eigene Suche\n\n"
               "**WARUM:** Der Assistent soll NUR aus den Dokumenten antworten. "
               "Dazu müssen wir die **relevantesten** Abschnitte finden – ohne irgendeine KI, nur mit Python.\n\n"
               "**WAS (unser simples Verfahren):** Wort-Überlappung. Wir zählen, wie viele Wörter Frage und Abschnitt gemeinsam haben. "
               "**Metapher:** Wir vergleichen Wort-Zettel – wenn genug gleiche Zettel in Frage und Text stecken, passt der Abschnitt wahrscheinlich.\n\n"
               "**TRY:** Schau dir das Scoring einmal roh an:"),
        ("code", '''\
def _woerter(text):
    """Saeubert: klein, Umlaute normalisieren, Fuellwoerter (<4 Zeichen) raus."""
    text = text.lower().replace("ü", "ue").replace("ä", "ae").replace("ö", "oe")
    return {w.strip(".,?!:;\\\"'()") for w in text.split() if len(w) >= 4}

frage = "Wie viele Urlaubstage gibt es?"
print("Fragewörter:", sorted(_woerter(frage)))
print()
for abschnitt in abschnitte[:3]:
    treffer = _woerter(frage) & _woerter(abschnitt["text"])
    print(f"{abschnitt['titel']:20s} | Treffer: {sorted(treffer)}")'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Jede Frage wird zur **Wortmenge** (ein `set` – Mengen kennen keine Duplikate). "
               "Der Schnitt (`&`) zweier Mengen zeigt die gemeinsamen Wörter. "
               "Das ist der komplette \"Geheimcode\" unserer Build-1-Suche – mehr steckt nicht dahinter."),
        ("ex", {
            "titel": "Die Funktion `suche_relevant`",
            "ziel": "Du schreibst das Herz der Build-1-Suche: eine Funktion, die zu einer Frage die besten Abschnitte liefert.",
            "anforderungen": [
                "Schreibe `suche_relevant(frage, abschnitte, top=2)`.",
                "Score = Anzahl gemeinsamer (gesäuberter) Wörter zwischen Frage und Abschnittstext.",
                "Nur Abschnitte mit Score > 0 kommen in die Ergebnisliste.",
                "Die Liste ist nach Score absteigend sortiert und maximal `top` lang.",
            ],
            "starter": '''\
def suche_relevant(frage, abschnitte, top=2):
    # YOUR CODE HERE
    pass

ergebnisse = suche_relevant("Wie viele Urlaubstage gibt es?", abschnitte)
for a in ergebnisse:
    print(a["quelle"], "-", a["titel"])''',
            "kriterien": [
                "Für die Urlaubsfrage liefert die Funktion den Abschnitt `mitarbeiter-handbuch.md – Urlaub` an erster Stelle.",
                "Fragen ohne Treffer ergeben eine **leere Liste**.",
                "Die Ausgabe ist eine Liste von Dictionaries (kein Score-Verlust in die Antwort!).",
            ],
            "checks": '''\
treffer = suche_relevant("Wie viele Urlaubstage gibt es?", abschnitte)
assert treffer, "Die Urlaubsfrage sollte Treffer liefern!"
assert treffer[0]["titel"] == "Urlaub", f"Erster Treffer sollte 'Urlaub' sein, ist '{treffer[0]['titel']}'"
assert suche_relevant("Weihnachtsgeld Hoehe Bonus?", abschnitte) == [], "Ohne Treffer: leere Liste!"
assert len(suche_relevant("Urlaub Gehalt Passwort VPN", abschnitte, top=2)) <= 2
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Baue eine Liste `(score, abschnitt)`, sortiere sie mit `sortiert = sorted(liste, key=lambda paar: paar[0], reverse=True)`.",
                "Die Bereinigung erledigt die Hilfsfunktion `_woerter` aus der Zelle oben (du darfst sie benutzen!).",
                "Vergiss nicht: nur Score > 0 mitnehmen – sonst kämen bei jeder Frage alle Abschnitte durch.",
            ],
            "loesung": '''\
def suche_relevant(frage, abschnitte, top=2):
    frage_woerter = _woerter(frage)
    scored = []
    for abschnitt in abschnitte:
        score = len(frage_woerter & _woerter(abschnitt["text"]))
        if score > 0:
            scored.append((score, abschnitt))
    scored.sort(key=lambda paar: paar[0], reverse=True)
    return [abschnitt for _, abschnitt in scored[:top]]

for a in suche_relevant("Wie viele Urlaubstage gibt es?", abschnitte):
    print(a["quelle"], "-", a["titel"])''',
            "loesung_md": "Jeder Abschnitt bekommt einen Punktwert (Score). Nach dem Sortieren schneiden wir die `top`-Besten ab. "
                          "Die Funktion ist **deterministisch** – gleiche Frage, gleiche Treffer – deshalb konnte die Prüfung "
                          "sie auch exakt testen. Determinismus ist Gold wert (Lektion 20 zeigt dir, wie man das systematisch nutzt).",
            "reflexion": [
                "1. Deine Suche findet \"Urlaub\" – aber wie gut findet sie **\"freie Tage\"**? Wo liegt die Schwäche (und was wird Build 2 dagegen tun)?",
                "2. Was passiert bei einer Frage voller kleiner Wörter (\"Wie ist das mit dem?\") – und warum haben wir Wörter < 4 Zeichen aussortiert?",
            ],
        }),
        ("md", "## Schritt 3: Der Prompt von Hand\n\n"
               "**WARUM:** Das Modell soll **nur aus den gefundenen Abschnitten** antworten – sonst halluziniert es. "
               "Deshalb bauen wir den Kontext **mit Anweisung** in einen Text.\n\n"
               "**Genau diese String-Arbeit** wird in Build 2 `ChatPromptTemplate` übernehmen – merk dir, wie sie von Hand aussieht:"),
        ("code", '''\
def baue_prompt(frage, abschnitte_liste):
    kontext = "\\n\\n".join(
        f"[{a['quelle']} - {a['titel']}]\\n{a['text']}" for a in abschnitte_liste)
    return (
        "Du bist ein Assistent fuer Firmenhandbuecher. Antworte NUR auf Basis "
        "des folgenden Kontexts. Wenn die Antwort nicht im Kontext steht, sage: "
        "'Das steht in den Dokumenten leider nicht.'\\n\\n"
        f"Kontext:\\n{kontext}\\n\\nFrage: {frage}"
    )

beispiel = baue_prompt("Urlaub?", abschnitte[:2])
print(beispiel[:300] + "...")'''),
        ("md", "## Schritt 4: Alles orchestrieren\n\n"
               "Jetzt der **Dirigent**: Suche → Prompt → Modell → Antwort + Quellen. "
               "Das ist die komplette manuelle Orchestrierung deines Assistenten:"),
        ("code", '''\
from lernakademie.llm_client import get_api_client, get_model_name

NICHT_GEFUNDEN = "Dazu habe ich in den Dokumenten leider nichts gefunden."

def beantworte(frage, abschnitte):
    relevante = suche_relevant(frage, abschnitte)
    if not relevante:
        return {"antwort": NICHT_GEFUNDEN, "quellen": []}
    prompt = baue_prompt(frage, relevante)
    client = get_api_client()
    try:
        antwort = client.chat.complete(
            model=get_model_name(),
            messages=[{"role": "user", "content": prompt}])
        text = antwort.choices[0].message.content
    except Exception as fehler:
        return {"antwort": f"Technisches Problem: {fehler}", "quellen": []}
    quellen = [f"{a['quelle']} - {a['titel']}" for a in relevante]
    return {"antwort": text, "quellen": quellen}

for frage in ("Wie viele Urlaubstage gibt es?",
              "Was gilt fuer Passwoerter?",
              "Wie hoch ist das Weihnachtsgeld?"):
    ergebnis = beantworte(frage, abschnitte)
    print("FRAGE  :", frage)
    print("ANTWORT:", ergebnis["antwort"][:120])
    print("QUELLEN:", ergebnis["quellen"], "\\n")'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "1. Die Urlaubsfrage findet den richtigen Abschnitt (Quelle: `mitarbeiter-handbuch.md – Urlaub`).\n"
               "2. Die Passwort-Frage findet den IT-Abschnitt.\n"
               "3. Die Weihnachtsgeld-Frage ist ein **Beweis für Ehrlichkeit**: kein Treffer → keine erfundene Antwort.\n\n"
               "**Dieselbe Version läuft jetzt als wiederverwendbares Modul** (`lernakademie/build1.py`) – "
               "genau das ist der \"Level 3\"-Schritt aus dem Notebook-Guide: Konzept erst von Hand verstehen, "
               "dann als Abstraktion nutzen. Importieren wir sie:"),
        ("code", '''\
from lernakademie.build1 import beantworte as beantworte_modul, lade_dokumente

ergebnis = beantworte_modul("Wie viele Urlaubstage gibt es?", lade_dokumente())
print("Antwort:", ergebnis["antwort"][:150])
print("Quellen:", ergebnis["quellen"])'''),
        ("md", "## 🧩 Challenge (freiwillig): Die Grenze erleben\n\n"
               "Stelle die Frage **\"Wie beantrage ich freie Tage?\"** – es steht kein Wort davon wörtlich in den Dokumenten. "
               "Beobachte, was deine Wort-Suche tut. Schreib deine Beobachtung als Kommentar in die Zelle. "
               "Genau diese Schwäche wird Build 2 mit **Embeddings** (Bedeutungs-Suche) beheben!"),
        ("code", '''\
ergebnis = beantworte("Wie beantrage ich freie Tage?", abschnitte)
print("ANTWORT:", ergebnis["antwort"][:150])
print("QUELLEN:", ergebnis["quellen"])
# DEINE BEOBACHTUNG: ...
'''),
    ],
    "weiter": "**Weiter mit Lektion 06:** `notebooks/03_build_1/06_build1_erweiterung_ui.ipynb` – "
              "du erweiterst Build 1 um eine zweite Wissensquelle, dokumentierst den Wartungsschmerz und startest deine erste Web-Oberfläche.",
}

NB_06 = {
    "pfad": "notebooks/03_build_1/06_build1_erweiterung_ui.ipynb",
    "titel": "Lektion 06: 🧱 BUILD 1 – Erweiterung, Wartungsschmerz & erste Oberfläche",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Mittel",
    "voraussetzungen": "Lektion 05",
    "baut": "Build 1 mit zwei Wissensquellen, ein Gesprächs-Verlauf – und der Start deiner ersten Streamlit-Oberfläche",
    "ziele": [
        "eine zweite Wissensquelle einbinden und den Wartungsaufwand messen",
        "erklären, warum manuelle Orchestrierung bei Wachstum schmerzt",
        "Gesprächs-Verlauf in den Assistenten integrieren",
        "die fertige Streamlit-Oberfläche starten und mit deinem eigenen Assistenten bedienen",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Der Wartungsschmerz (der Punkt dieser Lektion!)\n\n"
               "Build 1 funktioniert – **für zwei Dokumente**. Aber was passiert bei Wachstum? "
               "Das wirst du jetzt **selbst erleben**, nicht nur lesen.\n\n"
               "**Metapher:** Ein Schuppen ist schnell gezimmert. Aber jeder Anbau bedeutet: "
               "Werkzeug nachkaufen, Pläne anpassen, alles neu prüfen. Irgendwann sehnst du dich nach einem System, das mitwächst."),
        ("code", '''\
from lernakademie.build1 import lade_dokumente, suche_relevant, baue_prompt, beantworte

# Der Firmenprofil-Abschnitt ist bereits dabei (data/ enthaelt drei Dateien):
abschnitte = lade_dokumente()
quellen = {a["quelle"] for a in abschnitte}
print("Aktuelle Quellen:", sorted(quellen))

ergebnis = beantworte("Was macht die Abteilung Engineering?", abschnitte)
print("ANTWORT:", ergebnis["antwort"][:150])
print("QUELLEN:", ergebnis["quellen"])'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Drei Quellen, eine Frage zum Firmenprofil – und dein Assistent findet die Antwort. "
               "**Aber:** In unserem Startpunkt (Lektion 05) hattest du nur zwei Dateien geladen. "
               "Wir mussten **nichts an der Logik ändern** – die `glob(\"*.md\")`-Schleife hat automatisch mitgewachsen. "
               "Das ist der eine MUTMASSLICHE Vorteil. Jetzt der Preis:"),
        ("ex", {
            "titel": "Den Wartungsschmerz messen",
            "ziel": "Du erweiterst den Assistenten und protokollierst ehrlich, was das kostet.",
            "anforderungen": [
                "Füge eine vierte Wissensquelle hinzu: Erstelle eine neue Datei `data/meine_notizen.md` mit einem `## `-Abschnitt über ein Thema, das dich interessiert (mindestens 4 Sätze).",
                "Lade die Abschnitte neu und stelle eine Frage an deine eigene Datei – der Assistent soll sie finden.",
                "Beantworte als Kommentar in der letzten Zelle: (a) Welche Funktionen hast du NICHT ändern müssen? (b) An wie vielen Stellen müsstest du ansetzen, wenn du pro Quelle ein anderes Scoring wolltest? (c) Was bräuchtest du zusätzlich für: Verlauf, Zitiergenauigkeit bis Zeile, 10x mehr Dokumente?",
            ],
            "starter": '''\
from pathlib import Path

# YOUR CODE HERE: eigene Notizdatei schreiben (Path(...).write_text)
# Tipp: Path(ROOT / "data" / "meine_notizen.md").write_text(..., encoding="utf-8")

# YOUR CODE HERE: Abschnitte neu laden und eine Frage an deine Notiz stellen''',
            "kriterien": [
                "Die Datei `data/meine_notizen.md` existiert mit einem `## `-Abschnitt.",
                "Eine Frage dazu liefert deine Quelle in `quellen`.",
                "Deine drei Schmerz-Antworten stehen als Kommentar.",
            ],
            "checks": '''\
datei = ROOT / "data" / "meine_notizen.md"
assert datei.exists(), "Lege die Datei data/meine_notizen.md an!"
inhalt = datei.read_text(encoding="utf-8")
assert "## " in inhalt and len(inhalt) > 150, "Braucht eine ## -Ueberschrift und Substanz (mind. 150 Zeichen)."
print("Alle Prüfungen bestanden! ✅ (Deine Schmerz-Notizen sind dein echter Lohn hier.)")''',
            "hinweise": [
                "Datei schreiben: `datei.write_text(\"# Notizen\\n\\n## Mein Thema\\n\\nHier steht dein Text...\", encoding=\"utf-8\")`.",
                "Danach einfach `lade_dokumente()` erneut aufrufen – die neue Datei fließt automatisch ein.",
                "Für die Schmerz-Analyse: zähle die Stellen in `baue_prompt`, `beantworte`, `suche_relevant`, die pro Quelle angefasst werden müssten.",
            ],
            "loesung": '''\
from pathlib import Path

meine_datei = ROOT / "data" / "meine_notizen.md"
meine_datei.write_text(
    "# Meine Notizen\\n\\n"
    "## Mein Lerntagebuch\\n\\n"
    "In dieser Akademie baue ich einen Wissensassistenten dreimal. "
    "Build 1 hat mich gelehrt, dass Suchen, Prompts und Orchestrierung "
    "zusammenhaengen. Ich notiere hier meine Erkenntnisse, um sie spaeter "
    "wiederzufinden. Diese Notiz dient als vierte Wissensquelle.",
    encoding="utf-8",
)

abschnitte = lade_dokumente()
ergebnis = beantworte("Was steht im Lerntagebuch?", abschnitte)
print("ANTWORT:", ergebnis["antwort"][:130])
print("QUELLEN:", ergebnis["quellen"])

# Schmerzprotokoll:
# (a) Nicht geaendert: lade_dokumente, suche_relevant, baue_prompt, beantworte
#     -> die glob-Schleife laesst neue Dateien automatisch einfliessen.
# (b) Eigenes Scoring pro Quelle: mindestesns 3 Stellen
#     (suche_relevant-Schleife, ggf. baue_prompt-Formatierung, beantworte-Quellenliste).
# (c) Verlauf: eigene Struktur + Anhängen der Historie in baue_prompt (2 Stellen);
#     Zitate bis Zeile: Abschnitt-Format aendern + Prompt-Regeln (2 Stellen);
#     10x Dokumente: Scoring wird langsam -> Caching/Index noetig (neues Problem!).''',
            "loesung_md": "Der Clou: `glob(\"*.md\")` macht Erweiterungen leicht – aber die Schmerzpunkte liegen woanders: "
                          "individuelle Scoring-Regeln, Verlauf, Zitiergenauigkeit und Skalierung. **Genau diese vier Schmerzen** "
                          "lösen Build 2 (Embeddings, Templates, Retriever) und Build 3 (State, Graph) – deshalb lernt du sie!",
            "reflexion": [
                "1. Welcher Teil deiner Arbeit war *Fachlogik* (Scoring, Prompt-Regeln) und welcher reiner *Boilerplate*?",
                "2. Nenne die drei Sachen, die ein Framework für dich übernehmen müsste, damit du dich aufs Produkt konzentrieren kannst.",
            ],
        }),
        ("md", "## 🧠 Konzept: Verlauf für den Assistenten\n\n"
               "Aus Lektion 04 kennst du das Muster. Jetzt kombinieren wir es mit dem Assistenten – "
               "der Assistent **erinnert sich an die vorherige Frage**:"),
        ("code", '''\
from lernakademie.build1 import beantworte as b1

def baue_assistent_mit_gedaechtnis(abschnitte, max_runden=5):
    verlauf = []   # Liste von (frage, antwort)-Paaren

    def frage(stellen):
        ergebnis = b1(stellen, abschnitte)
        verlauf.append((stellen, ergebnis["antwort"]))
        if len(verlauf) > max_runden:
            del verlauf[0]
        return ergebnis

    def kontext():
        return " | ".join(f"Frage: {f[:40]} -> Antwort: {a[:40]}" for f, a in verlauf)
    return frage, kontext

frage, kontext = baue_assistent_mit_gedaechtnis(abschnitte)
frage("Wie viele Urlaubstage gibt es?")
frage("Und wann verfaellt Resturlaub?")
print("Gespraechskontext:\\n", kontext())'''),
        ("md", "## 🖥️ Deine erste Oberfläche (fertig gebaut – du startest sie!)\n\n"
               "Der Assistent soll nicht nur im Notebook leben. Es gibt eine **fertige kleine Streamlit-Oberfläche**, "
               "die genau deinen Build-1-Assistenten bedient (Code: `frontend/build1_chat.py`).\n\n"
               "**Wichtig:** Streamlit läuft als eigenes Programm (nicht im Notebook). "
               "Öffne ein **Terminal im Projektordner** und führe aus:\n\n"
               "```bash\nsource .venv/bin/activate        # Windows: .venv\\\\Scripts\\\\activate\nstreamlit run frontend/build1_chat.py\n```\n\n"
               "Der Browser öffnet sich automatisch. Tipp: Mit `# YOUR CHAT` kannst du dort deinem Assistenten Fragen stellen.\n\n"
               "**Was du hier gelernt hast (Konzept, kein Frontend-Bau):** Streamlit läuft bei jedem Klick das Skript komplett neu – "
               "deshalb lebt der Gesprächsverlauf in `st.session_state`. Das kennst du schon: **der Notizblock muss explizit mitgeführt werden** "
               "– exakt wie beim LLM-Gedächtnis in Lektion 04!"),
        ("code", '''\
# Hier im Notebook: nur der Beweis, dass die Datei existiert und nutzbar ist.
from pathlib import Path
app = ROOT / "frontend" / "build1_chat.py"
print("Oberflaeche gefunden:", app.exists())
print("Start im Terminal:  streamlit run frontend/build1_chat.py")'''),
    ],
    "weiter": "**🔗 BUILD 2 wartet – Lektion 07:** `notebooks/04_langchain/07_langchain_chains.ipynb` – "
              "LangChain übernimmt dein handgebautes Fließband: Prompts, Modelle, Parser. Und du weißt genau, was es tut!",
}

SPECS_B = [NB_03, NB_04, NB_05, NB_06]
