# Aufgabe 13.1 – Vektor-RAG vs. Graph-Retrieval im Vergleich ⚖️

## Schwierigkeit
Mittel · **Kosten: keine** (offline voll übbar)

## Lernziel
Du beantwortest **dieselben Fragen** mit beiden Systemen und siehst messbar, wo welches gewinnt – die Grundlage jeder Architektur-Entscheidung.

## Warum ist das wichtig?
„Welche Retrieval-Art?" ist DIE Design-Frage moderner KI-Systeme. Die Antwort ist nie „immer Vektor" oder „immer Graph" – sie hängt von der **Fragen-Art** ab. Diese Aufgabe macht den Unterschied nicht theoretisch, sondern an vier konkreten Fragen erlebbar.

## Das Konzept einfach erklärt
**Metapher – zwei Büchersucher:**
- **Vektor-Suche** = der Ausleiher, der dich versteht: Du sagst „irgendwas mit Urlaub", er bringt die sinngleichen Kapitel. Er findet aber nur, **was geschrieben wurde** – und er wird unscharf, wenn nach **Verbindungen** gefragt wird.
- **Graph-Suche** = der Archivar mit Fäden: „Wer hängt an Projekt X?" – er folgt exakt den Fäden. Aber er kennt nur, **was als Faden angelegt wurde** – Fließtext liegt ihm nicht.

## Die technische Erklärung
- Beide Systeme nutzen **denselben Wissensbestand** (`data/firmenprofil.md`): einmal als Text für den Vektor-Index (Chroma + Offline-Embeddings, Stufe 4-Muster), einmal als Graph (Extraktion aus demselben Text + manuelle Kanten).
- Vektor-Retrieval: `retriever.invoke(frage)` → Chunks mit Quellen.
- Graph-Retrieval: `cypher_aus_frage` + `fuehre_sicher_aus` (Stufe 12) oder direkte `neighbors`-Traversierung.
- Die **Vergleichs-Notation**: pro Frage notierst du, was jedes System geliefert hat – und bewertest (✓ passt / ✗ daneben / ~ teilweise).

## Voraussetzungen
- Stufe 4 (Vektor-RAG), Stufe 10/12 (Graph, NL→Cypher)

## Deine Mission
Baue `vector_vs_graph.py`:
1. **Beide Systeme aufbauen:** Vektor-Index über `data/firmenprofil.md` (Chunks + Chroma, wie Stufe 4) UND Graph mit dem Firmenprofil-Wissen (Anna→Engineering→AI Assistant, Ben→Data & Analytics→Nutzungsanalysen→AI Assistant …).
2. **Vier Vergleichsfragen** (aus dem Level-README) je an **beide** Systeme stellen.
3. Für jede Frage ausgeben: Vektor-Ergebnis (Text-Fundstelle + Quelle), Graph-Ergebnis (Traversierung), deine Bewertung (welches System gewinnt und warum).
4. **Die Emergenz-Frage:** „Wie hängt Ben mit AI Assistant zusammen?" – der Graph kann es traversieren, obwohl dieser Satz **nicht im Text steht**. Weise es nach!

## Akzeptanzkriterien
- [ ] Beide Systeme liefern für alle vier Fragen Ergebnisse (oder ehrliche „nichts gefunden").
- [ ] Die Bewertungen begründen jeweils in einem Satz.
- [ ] Der Emergenz-Beweis ist sichtbar (Graph findet Verbindung, die im Text nur indirekt beschrieben ist).
- [ ] Du leitest eine Faustregel ab: „Bei Fragen dieser Art nehme ich …".

## Hinweise
1. Für den Vektor-Index: nutze das Stufe-4-Muster (`RecursiveCharacterTextSplitter` + Chroma + `get_embeddings()`); Offline-Embeddings brauchen Schlüsselwörter aus dem Text („Engineering", „AI Assistant", „Ben" …).
2. Der Graph darf auch **manuell** gebaut werden (Stufe 10.1) – Extraktion ist Stufe-12-Thema, hier geht es um den Vergleich.
3. Strukturiere die Ausgabe als Tabelle – du wirst sie öfter ansehen!

## Reflexionsfragen
1. Warum lief Vektor bei „Was steht über Engineering?" ins Leere oder daneben – und was sagt das über die Grenze von Schlüsselwort-Embeddings (vs. echter Embeddings)?
2. Formuliere eine Frage, die **beide** bräuchten – woran erkennst du das bereits an der Frage?
3. Was kostet der Betrieb beider Systeme (doppelter Aufbau, doppelte Pflege) – und wann rechtfertigt das der Nutzen?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| „Beides ist gleich gut" ohne Begründung | Bewerte FRAGEN-TYP, nicht Systeme allgemein |
| Graph-Fragen testen nur Text-Inhalte | wähle bewusst Verbindungs-Fragen („Wie hängt … zusammen?") |
| Vektor-Index leer | Trennzeichen/Pfad prüfen (data/firmenprofil.md) |

## Referenzlösung
→ [`solutions/vector_vs_graph.py`](../solutions/vector_vs_graph.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die Bewertungs-Logik und der Emergenz-Beweis.

## Was haben wir gelernt?
Systematische Vergleichsmethodik, Stärkenprofile beider Retrieval-Arten, Emergenz durch Traversierung.

## Was kommt als Nächstes?
Statt „entweder/oder": Aufgabe 13.2 baut **Hybrid-Retrieval** – beide Quellen in einer Pipeline, mit Quellenangaben, die zeigen, woher jede Information stammt.
