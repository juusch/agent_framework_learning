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
