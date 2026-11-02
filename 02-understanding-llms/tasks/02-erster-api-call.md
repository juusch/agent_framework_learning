# Aufgabe 2.2 – Dein erster API-Call an Mistral 🚀

## Schwierigkeit
Anfänger · ⚠️ **Kosten:** nur mit echtem API-Key; ohne Key läuft die Lösung automatisch (und kostenlos) im Offline-Modus.

## Lernziel
Du verstehst, was bei einem API-Call technisch passiert, und kannst aus Python heraus eine Anfrage an ein Mistral-Modell senden.

## Warum ist das wichtig?
Jede LangChain-Anwendung (Stufe 3), jeder Chatbot, jede RAG-Pipeline gipfelt in genau diesem Moment: Text losschicken, Antwort empfangen. Wenn du *das* verstehst, ist der Rest der Akademie nur noch elegante Verpackung.

## Das Konzept einfach erklärt
**Metapher – die Restaurant-Kette:** Dein Programm ist der Gast, die **API** der Kellner, das Modell die Küche. Du gibst dem Kellner eine Bestellung (dein Prompt + dein API-Key als Mitgliedskarte), die Küche „kocht" eine Antwort, der Kellner bringt sie zurück. Du siehst die Küche nie – aber du merkst sofort, wenn sie geschlossen ist (Fehlermeldung) oder überlastet (429).

## Die technische Erklärung
1. Dein Skript baut ein **HTTP-Request** an `https://api.mistral.ai/v1/chat/completions`.
2. Im Header steckt dein API-Key (Authentifizierung).
3. Im Body (JSON) stehen: `model` (z. B. `mistral-small-latest`) und `messages` – die Liste der Nachrichten mit **Rollen**:
   - `system`: Verhaltensanweisung an den Assistenten („Du bist ein...").
   - `user`: die Frage des Nutzers.
   - `assistant`: frühere Antworten des Modells (für Gesprächsverlauf).
4. Wir nutzen das offizielle Python-SDK (`mistralai`) statt roher HTTP-Aufrufe – es erledigt Header, JSON und Fehlerformate für uns.
5. Die Antwort steckt in `response.choices[0].message.content`.

## Voraussetzungen
- Aufgabe 1.4 (`.env` mit `MISTRAL_API_KEY`, venv aktiv)
- Optional: `python3 02-understanding-llms/examples/token_zaehler.py` zeigt dir vorher, wie Text in Tokens übergeht.

## Deine Mission
Schreibe `first_api_call.py`, das:
1. den Mistral-Client initialisiert (mit Key aus `.env` – **nie** den Key in den Code schreiben!),
2. eine Nachricht an das Modell sendet: System-Rolle „Du bist ein freundlicher Erklärbär für Technik-Anfänger." + User-Rolle „Erkläre in zwei Sätzen, was eine API ist.",
3. die Antwort des Modells ausgibt,
4. Fehler abfängt: kein Netz? Rate-Limit (429)? Falscher Key (401)? → jeweils eine verständliche deutsche Meldung statt eines Tracebacks.

**Offline-Hinweis:** Die Referenzlösung nutzt `lernakademie.get_mistral_client()`. Ohne Key bekommst du eine `[OFFLINE]`-Antwort – der *Code-Ablauf* ist identisch, nur die „Küche" ist eine Simulation.

## Akzeptanzkriterien
- [ ] Das Skript läuft ohne Key (Offline-Antwort) **und** mit Key (echte Antwort).
- [ ] Der API-Key steht **nirgendwo** im Quellcode.
- [ ] Bei 401/429/Netzwerkfehlern erscheint eine klare Meldung, kein Traceback.
- [ ] Du kannst die drei Nachrichten-Rollen benennen.

## Hinweise
1. Client: `from mistralai import Mistral; client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])`
2. Aufruf: `client.chat.complete(model="mistral-small-latest", messages=[...])` – jede Nachricht ist ein Dictionary `{"role": ..., "content": ...}`.
3. Antwort: `response.choices[0].message.content`.
4. Fehler fangen: `except Exception as fehler:` und `str(fehler)` prüfen („401", „429", Connection...).

## Reflexionsfragen
1. Warum steht der Key im Header und nicht im Code?
2. Was wäre passiert, wenn du statt der SDK-Bibliothek eine funktionierende Kreditkarte als Key verwendest? (Freiwillige Zusatzfrage: Was sind „Rate-Limits" und warum existieren sie?)
3. Wo im Ablauf „Request → Küche → Response" würde ein langsames Netz sichtbar?

## Häufige Fehler
| Fehler | Bedeutung | Lösung |
|---|---|---|
| 401 unauthorized | Key fehlt/falsch | `.env` prüfen, `load_dotenv()` |
| 429 rate limit | zu viele Aufrufe | kurze Pause, seltener aufrufen |
| `Connection error` | kein Netz / URL falsch | Netz prüfen; Modellname prüfen |
| Antwort beginnt mit `[OFFLINE]` | kein Key gesetzt – kein Fehler | Key eintragen, wenn online üben |

## Referenzlösung
→ [`solutions/first_api_call.py`](../solutions/first_api_call.py)

## Code-Walkthrough
Zeile für Zeile kommentiert in der Lösungsdatei – besonders die Funktion `erstelle_client()` und die Fehleranalyse.

## Was haben wir gelernt?
API-Grundprinzip, Nachrichten-Rollen, SDK-Nutzung, Fehlerbehandlung.

## Was kommt als Nächstes?
Du hast **eine** Nachricht geschickt. Aufgabe 2.3 zeigt, wie System-Nachrichten das Verhalten formen und wie Temperature zwischen „brav" und „kreativ" umschaltet.
