"""Notebook-Specs Teil C: LangChain + BUILD 2 (Lektion 07-09)."""

NB_07 = {
    "pfad": "notebooks/04_langchain/07_langchain_chains.ipynb",
    "titel": "Lektion 07: LangChain – vom Handbau zum Fließband",
    "zeit": "~45 Minuten",
    "schwierigkeit": "Leicht",
    "voraussetzungen": "Lektion 05–06 (du hast Prompt-Bau & Modell-Call von Hand gebaut!)",
    "baut": "Deine erste Chain – das Fließband, das deinen Build-1-Handarbeit ersetzt",
    "ziele": [
        "erklären, **welche** Handarbeit aus Build 1 LangChain ersetzt",
        "Nachrichten als LangChain-Objekte (`SystemMessage`, `HumanMessage`) nutzen",
        "eine **Chain** mit `|` verketten: Prompt → Modell → Parser",
        "Prompt-Templates mit Platzhaltern füllen",
        "den Validierungsfehler bei vergessenen Platzhaltern als Feature erklären",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Was ersetzt LangChain hier konkret?\n\n"
               "**WARUM:** Erinner dich an Build 1: `baue_prompt` war String-Kleberei, der Client-Call roh, "
               "die Antwort musertest du aus `choices[0].message.content` wühlen – und das **jedes Mal wieder**.\n\n"
               "**WAS:** LangChain liefert standardisierte **Bausteine** mit einer gemeinsamen Schnittstelle (Runnable): "
               "alles hat `.invoke()` und lässt sich mit `|` wie ein Fließband verketten.\n\n"
               "| Build 1 (dein Handbau) | Build 2 (LangChain-Baustein) |\n|---|---|\n"
               "| `baue_prompt` (String-Konkatenation) | `ChatPromptTemplate` |\n"
               "| `client.chat.complete(...)` | Chat-Modell-Objekt |\n"
               "| `antwort.choices[0].message.content` | `StrOutputParser()` |\n\n"
               "**Metapher Chain = Fließband:** Ein Arbeiter schneidet Bleche (Template füllt die Werte), "
               "der nächste lackiert (Modell antwortet), der letzte prüft und verpackt (Parser macht einen sauberen String). "
               "Übergabepunkt ist das Band selbst – die Chain."),
        ("md", "## 🔎 Beispiel: Nachrichten als Objekte\n\n"
               "LangChain spricht nicht mehr mit rohen Dictionaries, sondern mit **Message-Objekten:"),
        ("code", '''\
from langchain_core.messages import HumanMessage, SystemMessage
from lernakademie.llm_client import get_chat_model

modell = get_chat_model(temperature=0.2)

antwort = modell.invoke([
    SystemMessage(content="Du bist ein Python-Tutor fuer absolute Anfaenger."),
    HumanMessage(content="Erklaere in einem Satz, was eine Variable ist."),
])
print("Antwort-Objekt:", antwort)
print("\\nNur der Text (.content):")
print(antwort.content)'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Das Modell-Objekt kennt keine Dictionaries mehr – nur noch typisierte Nachrichten. "
               "Die Antwort ist ein `AIMessage`; der Text steckt in `.content`. "
               "Noch ist es Handarbeit – jetzt kommt das Fließband:"),
        ("md", "## 🧠 Konzept: Prompt-Template & Chain\n\n"
               "**WAS:** Ein `ChatPromptTemplate` ist eine **Vorlage mit Platzhaltern** (`{stil}`, `{text}`). "
               "Statt Strings zu kleben, füllst du beim Aufruf ein Dictionary aus.\n\n"
               "**WIE (das berühmte Einzeiler-Muster):**\n\n"
               "`chain = prompt | modell | parser`  ← das komplette Fließband in einer Zeile."),
        ("code", '''\
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Du fasst Texte praegnant und korrekt zusammen."),
    ("human", "Stil: {stil}. Zusammenfassen: {text}"),
])
chain = prompt | modell | StrOutputParser()

BEISPIELTEXT = ("Python ist eine Programmiersprache, die 1991 veroeffentlicht wurde. "
                "Sie ist bekannt fuer ihre gut lesbare Syntax und wird von der Webentwicklung "
                "bis zur Datenanalyse eingesetzt.")

for stil in ("kurz", "als Bullet Points"):
    ergebnis = chain.invoke({"stil": stil, "text": BEISPIELTEXT})
    print(f"--- Stil: {stil} ---")
    print(ergebnis[:200], "\\n")'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "1. **Dieselbe Chain**, zwei Stile – nur die **Eingabe** (das Dictionary) ändert sich. Das ist Wiederverwendbarkeit.\n"
               "2. Das Ergebnis ist ein **String** (Parser!) – kein `AIMessage`-Objekt mehr.\n"
               "3. Die Chain ist ein Runnable: `.invoke(dict)` links rein, fertiges Ergebnis rechts raus."),
        ("code", '''\
# Was passiert bei einem vergessenen Platzhalter? Fuehre aus – der Fehler ist ein FEATURE:
try:
    chain.invoke({"stil": "kurz"})   # {text} fehlt!
except Exception as fehler:
    print("Fehlerart:", type(fehler).__name__)
    print("Meldung:", str(fehler)[:150])'''),
        ("md", "** Warum das gut ist:** LangChain **validiert** deine Eingabe gegen das Template – "
               "vergessene Werte Crashen nicht mittendrin, sondern gleich am Eingang mit klarer Meldung. "
               "In Build 1 hättest du das selbst programmieren müssen."),
        ("ex", {
            "titel": "Deine eigene Übersetzer-Chain",
            "ziel": "Du baust selbst ein zweites Fließband – mit eigenen Platzhaltern.",
            "anforderungen": [
                "Erstelle `uebersetzer_prompt` mit den Platzhaltern `{text}` und `{zielsprache}` (System-Rolle: „Du übersetzt natürlich und idiomatisch.“).",
                "Verkette eine Chain `uebersetzer = uebersetzer_prompt | modell | StrOutputParser()`.",
                "Übersetze den Beispielsatz nach Englisch und nach Spanisch (zwei `invoke`-Aufrufe, dieselbe Chain).",
            ],
            "starter": '''\
# YOUR CODE HERE: Template bauen

# YOUR CODE HERE: Chain verketten

# YOUR CODE HERE: zwei Aufrufe (Englisch + Spanisch)''',
            "kriterien": [
                "Die Chain liefert Strings (keine `AIMessage`-Objekte).",
                "Beide Sprachen funktionieren über **dieselbe** Chain.",
                "Ein vergessener Platzhalter im `invoke` erzeugt einen Validierungsfehler (Feature!).",
            ],
            "checks": '''\
ergebnis = uebersetzer.invoke({"text": "Guten Morgen", "zielsprache": "Englisch"})
assert isinstance(ergebnis, str) and len(ergebnis) > 0
try:
    uebersetzer.invoke({"text": "Guten Morgen"})   # zielsprache fehlt
    raise AssertionError("Hier haette ein Validierungsfehler kommen muessen!")
except AssertionError:
    raise
except Exception:
    print("Validierung greift ✅")
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Template: `ChatPromptTemplate.from_messages([(\"system\", \"...\"), (\"human\", \"Uebersetze nach {zielsprache}: {text}\")])`",
                "Der Parser importiert aus `langchain_core.output_parsers`.",
            ],
            "loesung": '''\
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

uebersetzer_prompt = ChatPromptTemplate.from_messages([
    ("system", "Du uebersetzt natuerlich und idiomatisch."),
    ("human", "Uebersetze nach {zielsprache}: {text}"),
])
uebersetzer = uebersetzer_prompt | modell | StrOutputParser()

print(uebersetzer.invoke({"text": "Guten Morgen", "zielsprache": "Englisch"})[:120])
print(uebersetzer.invoke({"text": "Guten Morgen", "zielsprache": "Spanisch"})[:120])''',
            "loesung_md": "Template, Modell und Parser sind unverändert – nur die Vorlage ist neu. Genau das ist der Punkt: "
                          "Bausteine austauschen statt Code neu schreiben. Mit echtem Modell übersetzt die Chain wirklich; "
                          "im Offline-Modus siehst du die simulierte Antwort – die Mechanik ist identisch.",
            "reflexion": [
                "1. Zähle: Wie viele Runnables stecken in `prompt | modell | parser`? (Tipp: 3!)",
                "2. Was hat LangChain gegenüber Build 1 **einfacher** gemacht – und was wurde **komplizierter** (neue Begriffe, Abstraktion)?",
            ],
        }),
    ],
    "weiter": "**Weiter mit Lektion 08:** `notebooks/04_langchain/08_embeddings_vektor_rag.ipynb` – "
              "der große Qualitätssprung: **Embeddings** ersetzen deine Wort-Zettel-Suche durch Bedeutung-Suche.",
}

NB_08 = {
    "pfad": "notebooks/04_langchain/08_embeddings_vektor_rag.ipynb",
    "titel": "Lektion 08: Embeddings & Vektor-RAG – Suche nach Bedeutung",
    "zeit": "~60 Minuten",
    "schwierigkeit": "Mittel",
    "voraussetzungen": "Lektion 05–07",
    "baut": "Einen echten Vektor-Index über deine Dokumente – mit Chroma und Retriever",
    "ziele": [
        "erklären, warum Wort-Suche an Grenzen stößt („freie Tage\" vs. „Urlaub\")",
        "beschreiben, was ein **Embedding** ist (Bedeutungs-Koordinaten)",
        "Dokumente **chunken** und in Chroma speichern",
        "mit einem **Retriever** semantisch suchen und Treffer prüfen",
        "Zwischenergebnisse (Chunks, Embeddings, Treffer) **sichtbar inspizieren**",
    ],
    "cells": [
        ("md", "## 🧠 Konzept: Embeddings – die Landkarte der Bedeutung\n\n"
               "**WARUM:** Deine Build-1-Suche findet „Urlaub\" nur, wenn „Urlaub\" wörtlich steht. "
               "**Metapher:** Der Nutzer fragt nach \"freien Tagen\" – dein Wortsucher dreht durch, "
               "weil er nur Wort-Gleichheit kennt.\n\n"
               "**WAS:** Ein **Embedding** übersetzt Text in Zahlenkoordinaten – einen **Vektor**. "
               "Texte mit ähnlicher **Bedeutung** liegen auf dieser Landkarte nah beieinander, "
               "**auch ohne ein gemeinsames Wort**. Eine **Vektor-Datenbank** ist die Bibliothek, "
               "die nach Bedeutung statt nach Alphabet sortiert.\n\n"
               "**Das RAG-Flussbild (merk es dir):**\n\n"
               "```text\nDokumente → Chunks → Embeddings → Vektor-Store\nFrage → Embedding der Frage\n        ↓ (Nachbarschaft auf der Landkarte)\ntop-k Chunks → Kontext → LLM → Antwort + Quellen\n```\n\n"
               "In dieser Akademie nutzt `get_embeddings()` je nach Konfiguration echte Mistral-Embeddings oder "
               "(offline) ein transparentes Schlüsselwort-Modell – die Pipeline bleibt identisch (siehe `docs/local-ai-server.md`)."),
        ("md", "## Schritt 1: Chunking\n\n"
               "**WARUM:** Ganze Dokumente sind zu groß fürs Kontextfenster und zu unpräzise für die Suche. "
               "Wir schneiden sie in **Chunks** (Stückchen).\n\n"
               "**Die zwei Parameter – mit Metapher:**\n"
               "- `chunk_size=600` Zeichen: nicht zu klein (Sinn zerschnitten), nicht zu groß (Suche wird unscharf).\n"
               "- `chunk_overlap=100`: die Schere überlappt – nichts fällt zwischen die Schnitte."),
        ("code", '''\
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)

DOKUMENT = (ROOT / "data" / "mitarbeiter-handbuch.md").read_text(encoding="utf-8")
chunks = splitter.split_text(DOKUMENT)

print(f"{len(chunks)} Chunks aus einer Datei")
print("Chunk 1:", chunks[0][:120], "...")
print("Chunk 2:", chunks[1][:120], "...")'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Der **RecursiveCharacterTextSplitter** schneidet hierarchisch (Absätze → Sätze → Wörter), "
               "sodass Chunks natürlich bleiben. **TRY:** Ändere `chunk_size` auf 50 und beobachte, wie der Sinn zerfällt!"),
        ("md", "## Schritt 2: Embeddings anfassen\n\n"
               "Bevor wir die Black Box nutzen, schauen wir **hinein**. "
               "(Offline-Modus: die Vektoren sind vereinfachte Schlüsselwort-Vektoren – das Prinzip ist dasselbe.)"),
        ("code", '''\
from lernakademie.offline_embeddings import get_embeddings

embeddings = get_embeddings()
print("Embedding-Modell:", type(embeddings).__name__)

fragen = ["Wie viele Urlaubstage habe ich?",
          "Bis wann muss der Urlaubsantrag gestellt werden?",
          "Wie sieht eine sichere Passwort-Regel aus?"]
vektoren = [embeddings.embed_query(f) for f in fragen]

def aehnlichkeit(u, v):
    return sum(a * b for a, b in zip(u, v))   # Punktprodukt ≈ Cosine bei normalisierten Vektoren

print(f"\\nAehnlichkeit Frage1/Question2 (beide Urlaub): {aehnlichkeit(vektoren[0], vektoren[1]):.2f}")
print(f"Aehnlichkeit Frage1/Question3 (Urlaub vs Passwort): {aehnlichkeit(vektoren[0], vektoren[2]):.2f}")'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Themenverwandte Fragen haben **höhere Ähnlichkeit** als fremde – genau darauf baut die Suche. "
               "Die Landkarte existiert wirklich, und du hast sie gerade vermessen."),
        ("md", "## Schritt 3: Der Vektor-Store (Chroma) & der Retriever\n\n"
               "**WAS:** **Chroma** speichert Chunks + Vektoren + **Metadaten** (z. B. die Quelldatei – wichtig für Quellenangaben!). "
               "Der **Retriever** ist der einheitliche Such-Schalter darüber."),
        ("code", '''\
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def baue_vektor_index(k=3):
    """Liest alle data/*.md, chunkt, embedded und liefert einen Retriever."""
    from langchain_community.document_loaders import TextLoader
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    alle_chunks = []
    for datei in sorted((ROOT / "data").glob("*.md")):
        dokumente = TextLoader(str(datei), encoding="utf-8").load()
        alle_chunks.extend(splitter.split_documents(dokumente))
    db = Chroma(collection_name="lektion08", embedding_function=get_embeddings())
    db.add_documents(alle_chunks)
    return db.as_retriever(search_kwargs={"k": k})

retriever = baue_vektor_index()
print("Index gebaut – frage ihn:")'''),
        ("code", '''\
treffer = retriever.invoke("Wie viele Urlaubstage gibt es?")
for dokument in treffer:
    print("Quelle:", dokument.metadata.get("source", "?"))
    print("Auszug:", dokument.page_content.strip().replace("\\n", " ")[:100], "\\n")'''),
        ("ex", {
            "titel": "Der Build-1-Killer-Test",
            "ziel": "Du beweist die Schwäche deiner Build-1-Suche und die Stärke des Retrievers – mit derselben Frage.",
            "anforderungen": [
                "Stelle die Frage: Wie beantrage ich freie Tage? (a) an `suche_relevant` aus Build 1 und (b) an deinen Retriever.",
                "Gib beide Trefferlisten aus (Quelle/Titel bzw. Quelle/Auszug).",
                "Beantworte als Kommentar: Welches Verfahren liefert den relevanten Abschnitt – und warum?",
            ],
            "starter": '''\
from lernakademie.build1 import lade_dokumente, suche_relevant

# YOUR CODE HERE: (a) Build-1-Suche mit der Frage

# YOUR CODE HERE: (b) Retriever mit derselben Frage

# DEINE BEOBACHTUNG: ...''',
            "kriterien": [
                "Beide Ergebnisse sind sichtbar gegenübergestellt.",
                "Deine Beobachtung erklärt den Unterschied (Wortgleichheit vs. Bedeutung).",
            ],
            "checks": '''\
build1_treffer = suche_relevant("Wie beantrage ich freie Tage?", lade_dokumente())
vektor_treffer = retriever.invoke("Wie beantrage ich freie Tage?")
print("Build 1:", [t["titel"] for t in build1_treffer] or "keine Treffer")
print("Retriever:", [d.metadata.get("source", "?") for d in vektor_treffer])
assert vektor_treffer, "Der Retriever sollte Treffer liefern."
print("Vergleich ok ✅ (die inhaltliche Wertung macht dein Kommentar)")''',
            "hinweise": [
                "Für (a): `suche_relevant(\"Wie beantrage ich freie Tage?\", lade_dokumente())`.",
                "Für (b): `retriever.invoke(\"Wie beantrage ich freie Tage?\")`.",
                "Offline-Modus: Der Schlüsselwort-Retriever erkennt „Urlaub“ über seinen Stamm – schau genau hin, was er findet.",
            ],
            "loesung": '''\
from lernakademie.build1 import lade_dokumente, suche_relevant

frage = "Wie beantrage ich freie Tage?"

build1_treffer = suche_relevant(frage, lade_dokumente())
print("Build 1 (Wortsuche):")
for t in build1_treffer:
    print("  -", t["quelle"], "-", t["titel"])

vektor_treffer = retriever.invoke(frage)
print("Retriever (Bedeutungssuche):")
for d in vektor_treffer:
    print("  -", d.metadata.get("source", "?"))

# BEOBACHTUNG: 'freie Tage' steht nicht woertlich in den Handbuechern.
# Die Wort-Ueberlappung findet nur schwache Treffer ('Tag'/'Stellen'-Reste),
# waehrend der Retriever den Urlaubs-Abschnitt findet, weil 'freie Tage'
# und 'Urlaub' auf der Bedeutungs-Landkarte nah beieinander liegen.
# Mit echten Mistral-Embeddings ist der Unterschied noch deutlicher.''',
            "loesung_md": "Genau dieser Vergleich ist der DREHSCHALTER der Akademie: Du hast die Grenze von Build 1 "
                          "mit eigenen Händen gespürt und die Lösung (Bedeutungs-Suche) gleichzeitig erlebt. "
                          "In Lektion 09 baust du daraus den kompletten Build-2-Assistenten.",
            "reflexion": [
                "1. Warum darf man Chunks mit verschiedenen Embedding-Modellen **nie** mischen?",
                "2. Was kostet `k=6` gegenüber `k=3` – Latenz, Tokens, Präzision?",
            ],
        }),
    ],
    "weiter": "**🔗 Lektion 09 schließt BUILD 2 ab:** `notebooks/05_build_2/09_build2_rag_assistent.ipynb` – "
              "Retriever + Chain + Quellen = dein Assistent in neuer Architektur.",
}

NB_09 = {
    "pfad": "notebooks/05_build_2/09_build2_rag_assistent.ipynb",
    "titel": "Lektion 09: 🔗 BUILD 2 – Der RAG-Assistent mit Quellen",
    "zeit": "~75 Minuten",
    "schwierigkeit": "Mittel",
    "voraussetzungen": "Lektion 07–08",
    "baut": "Die Build-2-Version deines Knowledge Assistant: semantische Suche + Chain + ehrliche Quellenangaben + strukturierte Ausgaben",
    "ziele": [
        "Retriever-Ergebnisse **in eine Chain** einschleusen (RunnablePassthrough/RunnableLambda)",
        "Antworten mit **Quellen aus den Metadaten** liefern (nicht vom Modell zitieren lassen!)",
        "das ehrliche „Weiß ich nicht\" bei Trefferlosigkeit garantieren",
        "strukturierte Ausgaben mit **Pydantic** erzwingen",
        "Build 1 vs. Build 2 sachlich vergleichen",
    ],
    "cells": [
        ("md", "## 🔗 Willkommen zu BUILD 2!\n\n"
               "Gleiche Anwendung, bessere Architektur. Der große Unterschied zu Build 1:\n\n"
               "```text\nFrage → Retriever (Bedeutungssuche!) → top-k Chunks + Metadaten\n     → Prompt mit {context} → Modell → Parser → Antwort\n     → Quellenliste separat aus den Metadaten\n```\n\n"
               "**Warum die Quellen NICHT vom Modell kommen:** Das Modell kann zitieren, was es will – "
               "wir nehmen die Wahrheit aus den **Metadaten** der gefundenen Chunks. Das ist Determinismus statt Hoffnung."),
        ("code", '''\
# Index einmal bauen (aus Lektion 08 – als wiederverwendbares Muster):
from lernakademie.offline_embeddings import get_embeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def baue_retriever(k=3):
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    alle_chunks = []
    for datei in sorted((ROOT / "data").glob("*.md")):
        alle_chunks.extend(splitter.split_documents(
            TextLoader(str(datei), encoding="utf-8").load()))
    db = Chroma(collection_name="build2", embedding_function=get_embeddings())
    db.add_documents(alle_chunks)
    return db.as_retriever(search_kwargs={"k": k})

retriever = baue_retriever()
print("Retriever bereit.")'''),
        ("md", "## 🧠 Konzept: Kontext in die Chain einschleusen\n\n"
               "**Das Problem:** Die Chain erwartet `{{context}}` und `{{question}}` – aber der Retriever liefert Documents, kein Dictionary. "
               "Die Brücke: **`RunnablePassthrough().assign(context=RunnableLambda(...))`** – "
               "es reichert die Eingabe um das Context-Feld an, **ohne** die Frage zu verlieren."),
        ("code", '''\
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from lernakademie.llm_client import get_chat_model
from lernakademie.offline_embeddings import hat_bezug

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Du beantwortest Fragen NUR auf Basis des gegebenen Kontexts. "
     "Wenn die Antwort nicht im Kontext steht, antworte exakt mit: "
     "'Das steht in den Dokumenten leider nicht.'"),
    ("human", "Kontext:\\n{context}\\n\\nFrage: {question}"),
])

NICHT_GEFUNDEN = "Das steht in den Dokumenten leider nicht."

def baue_rag_chain(retriever):
    modell = get_chat_model(temperature=0.0)

    def _kontext_holen(eingabe):
        frage = eingabe["question"]
        if not hat_bezug(frage):        # offline: ehrlich statt beliebige Treffer
            return ""
        dokumente = retriever.invoke(frage)
        return "\\n\\n---\\n\\n".join(d.page_content for d in dokumente)

    def _relevante_docs(frage):
        """Nur Treffer mit echtem Bezug (offline: Aehnlichkeit > 0)."""
        from lernakademie.config import is_offline_mode
        dokumente = retriever.invoke(frage)
        if is_offline_mode():
            frage_vektor = get_embeddings().embed_query(frage)
            dokumente = [d for d in dokumente
                          if any(a * b for a, b in zip(
                              frage_vektor, get_embeddings().embed_query(d.page_content)))]
        return dokumente

    def _quellen(eingabe):
        frage = eingabe["question"]
        if not hat_bezug(frage):
            return []
        return sorted({Path(d.metadata["source"]).name
                       for d in _relevante_docs(frage)})

    chain = (
        RunnablePassthrough().assign(context=RunnableLambda(_kontext_holen))
        | PROMPT | modell | StrOutputParser()
    )
    return chain, _quellen

chain, quellen_fuer = baue_rag_chain(retriever)'''),
        ("ex", {
            "titel": "Die Funktion `beantworte` (Build 2)",
            "ziel": "Du vollendest den Build-2-Assistenten: Antwort + Quellen in einem strukturierten Dictionary.",
            "anforderungen": [
                "Schreibe `beantworte(frage)`, das `{{\"antwort\": ..., \"quellen\": [...], \"gefundene_stellen\": int}}` zurückgibt.",
                "Bei leerem Kontext: `antwort=NICHT_GEFUNDEN`, `quellen=[]`, `gefundene_stellen=0` (kein Modell-Call nötig!).",
                "Nutze die fertige `chain` und `quellen_fuer` aus den Zellen oben.",
                "Teste die drei Standardfragen: Urlaubstage / Passwörter / Weihnachtsgeld (ehrlich leer!).",
            ],
            "starter": '''\
def beantworte(frage):
    # YOUR CODE HERE
    pass

print(beantworte("Wie viele Urlaubstage gibt es?"))''',
            "kriterien": [
                "Die Urlaubsfrage liefert eine Antwort und `mitarbeiter-handbuch.md` in den Quellen.",
                "Die Weihnachtsgeld-Frage liefert das ehrliche NICHT_GEFUNDEN mit `quellen=[]`.",
                "Der Rückgabewert ist immer ein Dictionary mit den drei Schlüsseln.",
            ],
            "checks": '''\
urlaub = beantworte("Wie viele Urlaubstage gibt es?")
assert "mitarbeiter-handbuch.md" in urlaub["quellen"], f"Quelle fehlt: {urlaub['quellen']}"
assert urlaub["gefundene_stellen"] >= 1
weihnachten = beantworte("Wie hoch ist das Weihnachtsgeld?")
assert weihnachten["quellen"] == [] and "leider nicht" in weihnachten["antwort"]
print("Alle Prüfungen bestanden! ✅")''',
            "hinweise": [
                "Early-Exit: `if not hat_bezug(frage): return {...leer...}` ganz am Anfang (spart Modell-Calls!).",
                "Antwort holen: `chain.invoke({\"question\": frage})`.",
                "Quellen: `quellen_fuer({\"question\": frage})` liefert die sortierte Liste.",
            ],
            "loesung": '''\
def beantworte(frage):
    if not hat_bezug(frage):
        return {"antwort": NICHT_GEFUNDEN, "quellen": [], "gefundene_stellen": 0}
    antwort = chain.invoke({"question": frage})
    quellen = quellen_fuer({"question": frage})
    if not quellen:
        return {"antwort": NICHT_GEFUNDEN, "quellen": [], "gefundene_stellen": 0}
    return {"antwort": antwort, "quellen": quellen,
            "gefundene_stellen": len(quellen)}

for frage in ("Wie viele Urlaubstage gibt es?",
              "Was gilt fuer Passwoerter?",
              "Wie hoch ist das Weihnachtsgeld?"):
    ergebnis = beantworte(frage)
    print("FRAGE:", frage)
    print("  ->", ergebnis["antwort"][:100])
    print("  Quellen:", ergebnis["quellen"], "\\n")''',
            "loesung_md": "Der Early-Exit verhindert sinnlose Modell-Aufrufe (und im Offline-Modell ehrlich-beliebige Treffer). "
                          "Quellen kommen aus Metadaten, nie aus der Modell-Antwort. Damit ist Build 2 komplett – "
                          "vergleiche unten mit Build 1!",
            "reflexion": [
                "1. Warum ist „Antworte nur aus dem Kontext\" Eindämmung, aber KEINE Garantie gegen Halluzination?",
                "2. Welche Frage bleibt unbeantwortet, obwohl die Information im System steckt? (→ Verbindungsfragen – dein Einstieg in die Knowledge-Graph-Lektionen!)",
            ],
        }),
        ("md", "## 🧠 Konzept: Strukturierte Ausgaben (Pydantic)\n\n"
               "**WARUM:** Dein Assistent soll manchmal **Daten** liefern, nicht Fließtext: Thema, Stichpunkte, Zahlen. "
               "**Pydantic** erzwingt ein **Formular** – das Modell muss liefern, was dein Code erwartet (Validierung inklusive)."),
        ("code", '''\
from pydantic import BaseModel, Field

class Kurzanalyse(BaseModel):
    thema: str = Field(description="Thema des Texts in wenigen Wortern")
    stichpunkte: list[str] = Field(description="3-5 Kernaussagen als Stichpunkte")
    schaetzwortzahl: int = Field(description="Geschaetzte Wortzahl")

analysator = get_chat_model(temperature=0.0).with_structured_output(Kurzanalyse)
ergebnis = analysator.invoke((ROOT / "data" / "firmenprofil.md").read_text(encoding="utf-8")[:1500])
print("Typ:", type(ergebnis).__name__)
print("Thema:", ergebnis.thema)
print("Stichpunkte:", ergebnis.stichpunkte[:3])'''),
        ("md", "### 🔎 Was sehen wir hier?\n"
               "Kein String, sondern ein **echtes Objekt** mit Attribut-Zugriff (`ergebnis.thema`). "
               "Die `description`-Texte sind Teil der Anweisung an das Modell!\n\n"
               "## 📊 Der große Vergleich: Build 1 vs. Build 2\n\n"
               "| Kriterium | 🧱 Build 1 | 🔗 Build 2 |\n|---|---|---|\n"
               "| Suche | Wort-Überlappung | semantisch (Embeddings) |\n"
               "| \"freie Tage\"-Frage | ❌ schwach | ✅ findet Urlaubs-Abschnitt |\n"
               "| Prompt | eigene String-Kleberei | `ChatPromptTemplate` (validiert!) |\n"
               "| Antwort | Text aus `choices[0]...` | Chain + Parser + optional Pydantic |\n"
               "| Quellen | eigene Logik | aus Metadaten des Retrievers |\n"
               "| **Restproblem** | alles manuell, keine Synonyme | **keine Beziehungen** (\"Wer arbeitet woran?\") – → Knowledge Graph! |"),
        ("md", "Auch Build 2 existiert als Modul (`lernakademie/build2.py`) – gleiche Architektur wie in diesem Notebook:"),
        ("code", '''\
from lernakademie.build2 import beantworte as b2
ergebnis = b2("Wie viele Urlaubstage gibt es?")
print("Antwort:", ergebnis["antwort"][:120])
print("Quellen:", ergebnis["quellen"])'''),
    ],
    "weiter": "**🕸️ Neue Welt – Lektion 10:** `notebooks/06_knowledge_graph/10_graphen_in_python.ipynb` – "
              "warum „Wer arbeitet woran?\" keine Textfrage ist, sondern eine **Beziehungsfrage**.",
}

SPECS_C = [NB_07, NB_08, NB_09]
