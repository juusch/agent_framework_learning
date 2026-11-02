# 📖 Glossar – Technikbegriffe auf Deutsch erklärt

**API** *(Application Programming Interface)* – Eine Schnittstelle, über die Programme miteinander reden. **Metapher:** ein Kellner im Restaurant: Du (dein Programm) gibst die Bestellung beim Kellner ab, er bringt sie in die Küche (der Server), und er bringt dir das fertige Gericht zurück. Du siehst nie die Küche – und musst das auch nicht.

**Chain (Kette)** – In LangChain mehrere Verarbeitungsschritte, die wie ein Fließband hintereinandergeschaltet sind: Eingabe → Prompt → Modell → Nachverarbeitung → Ausgabe.

**Chat-Modell** – Eine LLM-Schnittstelle, die mit „Nachrichten" (Rollen: System/User/Assistant) arbeitet, statt mit einem einzelnen Textbaustein.

**Chunk (Chunking)** – Ein kleines, in sich sinnvolles Textstück. Dokumente werden in Chunks zerlegt, damit man gezielt die relevanten Stücke suchen und dem LLM vorlegen kann.

**Dependency (Abhängigkeit)** – Ein fremdes Python-Paket, das dein Projekt benutzt (z. B. `langchain`).

**Dictionary (`dict`)** – Eine Sammlung von „Schlüssel → Wert"-Paaren. **Metapher:** ein Wörterbuch: Du suchst unter einem Stichwort (Schlüssel) und findest die Erklärung (Wert).

**Embedding** – Eine Liste von Zahlen (ein „Vektor"), die die *Bedeutung* eines Textes darstellt. Texte mit ähnlicher Bedeutung haben ähnliche Vektoren.

**Funktion (`def`)** – Ein benannter, wiederverwendbarer Anweisungsblock. **Metapher:** ein Rezept: einmal aufgeschrieben, immer wieder kochbar.

**Halluzination** – Wenn ein LLM überzeugend klingende, aber falsche Informationen erfindet. Deshalb: Quellen prüfen und RAG verwenden.

**Kontextfenster (Context Window)** – Die maximale Textmenge (in Tokens), die ein LLM gleichzeitig „lesen" kann. **Metapher:** ein Schreibtisch, auf den nur begrenzt Blätter passen.

**LLM (Large Language Model)** – Ein Sprachmodell, das aus riesigen Textmengen gelernt hat, wahrscheinliche, meist sinnvolle Antworten zu erzeugen. **Metapher:** ein sehr belesener, aber manchmal unzuverlässiger Assistent.

**Node (LangGraph)** – Ein einzelner Arbeitsschritt in einem Graphen. **Metapher:** eine Person mit genau einer klaren Aufgabe.

**Offline-Modus** – In dieser Akademie: Übungen laufen ohne API-Key mit einem klar gekennzeichneten simulierten Modell (`[OFFLINE]`). So kannst du kostenlos und ohne Anmeldung alles üben.

**Paket (Package)** – Installierbare Sammlung von Python-Code anderer Leute (z. B. via `pip install`).

**Prompt** – Die Anweisung/Frage, die du dem LLM gibst. **Metapher:** ein Arbeitsauftrag an einen neuen Mitarbeiter – je klarer, desto besser das Ergebnis.

**Prompt-Template** – Eine Vorlage mit Platzhaltern (`{thema}`), die du immer wieder mit anderen Inhalten füllen kannst.

**Pydantic** – Eine Bibliothek, mit der man Datenstrukturen definiert und automatisch prüft, ob Daten dem erwarteten Format entsprechen.

**RAG (Retrieval-Augmented Generation)** – Muster: erst relevante Dokumentstellen *suchen* (retrieval), dann dem LLM als Kontext *mitgeben*, dann die Antwort *erzeugen* (generation). **Metapher:** ein Assistent, der vor der Antwort kurz im Handbuch nachschlägt.

**Runnable** – Die einheitliche LangChain-Schnittstelle: alles, was man mit `.invoke()` aufrufen kann (Prompt, Modell, Parser, ganze Chain).

**State (LangGraph)** – Der gemeinsame „Notizblock" eines Workflows, den alle Arbeitsschritte lesen und aktualisieren können.

**Temperatur** – Einstellung, wie „kreativ" (hoch, z. B. 0.7) oder wie „vorhersehbar" (niedrig, z. B. 0.0) ein LLM antwortet.

**Token** – Ein Textstück, das das LLM als Einheit verarbeitet (oft 3–4 Zeichen oder ca. ¾ eines Wortes). Rechnung: 1000 deutsche Wörter ≈ 1300–1800 Tokens.

**Vektor-Datenbank** – Speichert Embeddings und findet „sinngleiche" Texte. **Metapher:** eine Bibliothek, die Bücher nicht nach Alphabet, sondern nach *Bedeutung* sortiert.

**Virtuelle Umgebung (venv)** – Ein isolierter Paket-Speicher pro Projekt. **Metapher:** ein eigener Werkzeugkasten pro Baustelle, damit sich Werkzeuge verschiedener Projekte nicht in die Quere kommen.

**.env-Datei** – Eine lokale Datei mit Umgebungsvariablen (z. B. API-Keys). Sie wird **nie** committet (steht in `.gitignore`).

**Umgebungsvariable (Environment Variable)** – Eine Einstellung, die dein Betriebssystem an Programme weitergibt – der klassische Weg, geheime Schlüssel zu übergeben, ohne sie im Code zu schreiben.

**Knowledge Graph (Wissensgraph)** – Wissen als Entitäten (Nodes) und deren Verbindungen (Relationships). **Metapher:** das Ermittlungsbrett: Fotos + rote Fäden. Während Text-RAG "sinngleiche Stellen" findet, traversiert der Graph **exakte Verbindungen** – und beantwortet Fragen, die nirgends wörtlich stehen ("Wie hängt A mit B zusammen?").

**Node (Graph)** – Eine Entität im Graphen mit Label (Typ) und Properties (Attribute). **Metapher:** Karteikarte mit Farbkodierung und Notizen.

**Label (Graph)** – Der Typ eines Nodes (:Person, :Company) – Filterkriterium für Abfragen; ein Node kann mehrere haben.

**Relationship (Graph-Beziehung)** – Gerichtete, benannte Verbindung zwischen zwei Nodes (WORKS_FOR) mit optionalen Properties (seit: 2021). **Die Daten erster Klasse** – der Unterschied zu relationalen DBs.

**Cypher** – Abfragesprache von Neo4j: "ASCII-Art für Graphen" – das Suchmuster wird wörtlich gezeichnet: `MATCH (a:Person)-[:WORKS_FOR]->(c) RETURN a, c`.

**Traversierung (Traversal)** – Kanten folgen, um Muster oder Pfade zu finden. Die Grundbewegung der Graph-Suche; Antworten entstehen oft erst durch Verkettung (Emergenz).

**Entity Resolution** – Erkennen, ob zwei Funde dieselbe Entität sind ("Acme" = "ACME"?), damit der Graph keine Duplikate enthält. Der Türsteher vor dem Node-Anlegen.

**GraphRAG** – Retrieval-Muster: Vektor-Suche (sinngleiche Texte) und Graph-Traversierung (exakte Verbindungen) kombinieren – jede Antwort weist ihre Quelle aus.

**Whitelist (bei generierten Abfragen)** – Deterministische Prüfung LLM-generierter Cypher/SQL vor Ausführung: nur lesende Muster erlaubt. Schutz gegen Halluzination UND Prompt-Injection – als Python-Code, nie als LLM.

**FastAPI** – Python-Framework für HTTP-APIs mit automatischer Validierung (Pydantic) und Doku (/docs). Im Capstone die Mittelschicht zwischen Frontend und Agent.

**Streamlit** – Frontend-Framework in reinem Python (kein HTML/JS): Skript wird bei Interaktion neu ausgeführt, Zustand lebt in `st.session_state`. Gewählt für die Akademie, weil Lernende ohne Web-Ausbildung sofort Oberflächen bauen können.

**Lokaler AI-Server** – Ein Programm auf deinem eigenen Computer, das KI-Modelle bereitstellt (LM Studio, Ollama, vLLM, LocalAI, llama.cpp …). Vorteile: kostenlos nach dem Download, privat, schnell. **Metapher:** dein eigenes Restaurant nebenan statt des Cloud-Restaurants.

**OpenAI-kompatibel** – Ein Server „spricht" dieselbe Anfrage-Sprache wie die OpenAI-API (gemeinsamer Stecker/HDMI-Prinzip). Solange dein Server `/v1/chat/completions` anbietet, kann die Akademie mit ihm reden – ob lokal oder in der Cloud.

**Base-URL** – Die Adresse deines KI-Servers (`LLM_BASE_URL`): **WO** die KI lebt. Beispiele: `http://localhost:1234/v1` (eigener Rechner), `http://192.168.1.50:1234/v1` (Heimnetzwerk), `https://api.mistral.ai/v1` (Cloud).

**API-Endpunkt** – Eine Adresse + Methode am Server (POST /chat), an die Clients JSON schicken und JSON zurückerhalten. **Metapher:** ein Schalter im eigenen Restaurant – der Kellner (FastAPI) nimmt Bestellungen dagegen an.
