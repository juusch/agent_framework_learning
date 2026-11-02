# 🖥️ Lokale AI-Server & OpenAI-kompatible Endpoints

> **Das Wichtigste zuerst:** Du kannst in dieser Akademie entscheiden, **wo deine KI läuft** – ohne eine einzige Zeile Python zu ändern. Alles wird über die Datei `.env` konfiguriert. Verbindung testen:
>
> ```bash
> python -m tools.test_llm_connection
> ```

## 1. Was ist ein lokaler AI-Server?

Ein Programm auf **deinem** Computer, das KI-Modelle bereitstellt – ähnlich wie Mistral Cloud, nur bei dir zu Hause. Bekannte Vertreter: **LM Studio**, **Ollama**, **vLLM**, **LocalAI**, **llama.cpp**-Server.

**Warum möchte jemand einen nutzen?**
- **Kosten:** nach dem Herunterladen des Modells kostet jeder Aufruf nichts.
- **Privatsphäre:** deine Prompts verlassen deinen Computer nicht.
- **Geschwindigkeit:** keine Internet-Rundreise.
- **Experimentierfreude:** verschiedene Modelle ausprobieren (Llama, Qwen, Mistral-Open-Weight …).

**Der Preis:** du brauchst einen entsprechend starken Computer (je nach Modell viel RAM/GPU), die Modelle sind oft kleiner/schwächer als große Cloud-Modelle, und manche Fähigkeiten (siehe Abschnitt „Fähigkeiten") fehlen je nach Modell.

## 2. Was heißt „OpenAI-kompatibel"?

Die meisten Server „sprechen" dieselbe Standardsprache für KI-Anfragen – die **OpenAI-API**. Das ist wie ein **gemeinsamer Stecker**: Ob der Fernseher von Sony, Samsung oder Philips kommt – der HDMI-Stecker passt überall. Solange dein Server diesen Stecker anbietet (meist unter `/v1/chat/completions`), kann die Akademie mit ihm reden.

⚠️ **Wichtig:** „kompatibel" heißt nicht „identisch". Ob Tool-Calling, JSON-Mode oder Embeddings wirklich funktionieren, hängt von **Server UND Modell** ab. Prüfe immer die Dokumentation deines Servers für:
- die **tatsächliche API-URL** (oft `http://localhost:PORT/v1`, aber nicht immer),
- die **genauen Modellnamen**, die der Server meldet.

## 3. Die „Wo / Wie / Welche"-Regel

Drei Werte konfigurierst du – mehr nicht:

| Variable | Beantwortet | Beispiel |
|---|---|---|
| `LLM_BASE_URL` | **WO** lebt dein KI-Server? | `http://localhost:1234/v1` |
| `LLM_API_KEY` | **WIE** darfst du zugreifen? | oft leer (`LLM_API_KEY=`) |
| `LLM_MODEL` | **WELCHES** Modell soll antworten? | `qwen2.5-7b-instruct` |

**Metapher:** Die URL ist die **Adresse des Restaurants**, der API-Key deine **Mitgliedskarte** (bei manchen Lokalen braucht man keine – dann leer lassen!), und der Modellname das **Gericht**, das du bestellst.

## 4. Konfigurieren (Beispiele)

Kopiere `.env.example` → `.env` und wähle eine Variante:

**Variante A – Mistral Cloud (Standard der Akademie):**
```env
MISTRAL_API_KEY=dein-mistral-key
MISTRAL_MODEL=mistral-small-latest
```

**Variante B – LM Studio oder ein anderer Server auf Port 1234:**
```env
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=
LLM_MODEL=dein-lokales-modell
```

**Variante B2 – generischer Server auf Port 8000 (z. B. vLLM/LocalAI):**
```env
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=http://localhost:8000/v1
LLM_API_KEY=
LLM_MODEL=my-model
```

**Variante B3 – Server im lokalen Netzwerk (z. B. auf einem anderen Computer):**
```env
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=http://192.168.1.50:1234/v1
LLM_API_KEY=
LLM_MODEL=my-model
```

> 🔧 Das sind **Konfigurationsbeispiele**, keine garantierten Server-Anleitungen. Prüfe die Doku deines Servers für die echte URL und den Modellnamen!

**Zurückschalten zu Mistral:** Variante-B-Zeilen auskommentieren/löschen und `MISTRAL_API_KEY` eintragen – fertig. Oder `LLM_PROVIDER=mistral` setzen. **Keine Codeänderung.**

## 5. Der API-Key darf leer sein

Viele lokale Server prüfen keine Zugangsdaten. Deshalb gilt:

```env
LLM_API_KEY=
```

ist eine **vollständige, gültige Konfiguration**. Die Anwendung stürzt nicht ab, weil kein Key gesetzt ist – sie schickt dann einfach keine Authentifizierung mit. (Meldet der Server trotzdem `401`/`403`, braucht *dein* Server doch einen Key → eintragen.)

**Die drei Eisernen Regeln für Keys:**
1. Niemals in den Quellcode schreiben.
2. Niemals committen (`.env` steht in `.gitignore`).
3. Niemals ausdrucken/loggen – auch der Verbindungstest zeigt nur „gesetzt"/„nicht gesetzt", nie den Key selbst.

## 6. Verbindung testen

```bash
python -m tools.test_llm_connection
```

Der Test zeigt Anbieter, Server-URL, Modell und Key-Status (ohne Geheimnisse), sendet eine Mini-Anfrage und druckt bei Fehlern **konkrete Prüfschritte**. Beispiel-Ausgabe:

```
AI-Verbindungstest
------------------
Anbieter: OpenAI-kompatibler Server
Server:   http://localhost:1234/v1
Modell:   qwen2.5-7b-instruct
API-Key:  nicht gesetzt (optional)

Verbinde...
✓ Verbindung erfolgreich!
✓ Modell hat geantwortet (Antwort: OK)
```

## 7. Häufige Fehler

| Fehlermeldung | Ursache | Lösung |
|---|---|---|
| `Connection refused` | Server läuft nicht (oder falscher Port) | Server starten; Port in der Server-Doku prüfen |
| `404 ... /chat/completions` | URL passt nicht | Meist fehlt/sitzt ein falsches `/v1` am Ende → `LLM_BASE_URL` korrigieren |
| `401 / 403` | Server erwartet einen Key | `LLM_API_KEY` setzen |
| `model not found` | Modellname falsch | Exakten Namen aus der Server-Doku/-Oberfläche übernehmen (`LLM_MODEL`) |
| Antwort ist Unsinn oder leer | Modell zu schwach für die Aufgabe | Größeres Modell wählen; Fähigkeiten-Tabelle unten prüfen |
| Konfigurations-`ValueError` | `openai_compatible` ohne `LLM_BASE_URL`/`LLM_MODEL` | Fehlende Variable in `.env` ergänzen (Meldung sagt welche) |

Mehr: [`troubleshooting.md`](troubleshooting.md).

## 8. ⚠️ Sicherheit: dein Server im Netzwerk

- **Standard-Einstellung: nur dein eigener Computer.** `http://localhost:...` ist privat – das ist der sichere Normalfall.
- **Anderer Computer im Heimnetzwerk** (`http://192.168.x.x:...`): der Server ist dann für **jedes Gerät im Netzwerk** erreichbar. Aktiviere die Authentifizierung deines Servers (Key setzen und in `.env` eintragen)!
- **Niemals einen Server ohne Authentifizierung ins offene Internet expose** – sonst kann jeder deine Rechenleistung (und damit deinen Strom/ deine Hardware) nutzen.
- Für echte Fernzugriffe: **HTTPS** und **starke Authentifizierung** nutzen (Reverse-Proxy, VPN).
- Gilt für alle Varianten: **Keys privat halten**, nie in Screenshots, Chats oder Repos.

## 9. Fähigkeiten: nicht jedes Modell kann alles

Die Akademie kennzeichnet Aufgaben mit benötigter Modell-Fähigkeit. Grundfähigkeiten (Chat, System-/User-Nachrichten, Text) kann praktisch jedes Modell. Fortgeschrittene hängen von Server **und** Modell ab:

| Fähigkeit | Wofür in der Akademie | Risiko bei nicht-geeignetem Modell |
|---|---|---|
| **Tool-Calling** | Modul 6: Agenten wählen Werkzeuge | Agent ruft Tools nicht auf → Wechsel auf tool-fähiges Modell |
| **Structured Output / JSON** | Modul 3.3/5.3: Pydantic-Schemata, Graph-Extraktion | Validierung schlägt fehl → kleineres Modell ersetzen oder Aufgabe im Offline-Modus üben (Simulation liefert immer gültige Strukturen) |
| **Embeddings** | Modul 3/5: semantische Suche | Die Akademie fällt automatisch auf Schlüsselwort-Embeddings zurück (RAG bleibt übbar); für echte semantische Suche: Mistral oder `EMBEDDINGS=openai_compatible` mit embeddings-fähigem Server |
| **Streaming / Vision / Reasoning** | nicht Teil des Kerncurriculums | entfällt |

**💡 Praktischer Tipp:** Im Zweifel im **Offline-Modus** üben (alles läuft, deterministisch, gratis) und für echte LLM-Antworten ein Modell wählen, das die geforderte Fähigkeit laut Server-Doku beherrscht.

## 10. 💡 Lektion: Dein KI-Modell ist austauschbar

Der vielleicht wichtigste Architektur-Gedanke der Akademie:

```
Anwendung (Aufgaben, Graphen, Frontend)
        ↓
Modell-Schnittstelle (lernakademie.llm_client)
        ↓
Anbieter (Mistral | lokaler Server | jeder OpenAI-kompatible Endpoint)
```

ist etwas **grundlegend anderes** als:

```
Anwendung → Mistral-hardcodierte Implementierung
```

**Warum das in echten Projekten entscheidend ist:**
- **Preise ändern sich** – der Wechsel zu einem günstigeren Anbieter ist dann eine `.env`-Änderung, kein Umbau.
- **Modelle verbessern sich** – neues Modell ausprobieren = neue Zeile in `.env`.
- **Datenprivatsphäre** – sensible Daten? Dann läuft dasselbe System gegen deinen lokalen Server.
- **Unabhängigkeit** – kein Lock-in bei einem Anbieter.

Genau deshalb **liest keine Aufgabe selbst Umgebungsvariablen**: Konfiguration zentral (`lernakademie/config.py`), Anbieter-Layer zentral (`lernakademie/llm_client.py`), und LangChain/LangGraph/LangGraph-Knoten **bekommen ein fertig konfiguriertes Modell** – der Graph interessiert sich nicht dafür, ob dahinter Mistral oder dein lokaler Server steckt. Ob du diesen Lernpfad einmal **architektonisch** nachvollziehen willst: Öffne `lernakademie/config.py` und `lernakademie/llm_client.py` – beide sind bewusst klein und komplett lesbar.
