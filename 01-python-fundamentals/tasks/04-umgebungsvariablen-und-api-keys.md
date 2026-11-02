# Aufgabe 1.4 – Umgebungsvariablen & API-Keys 🔑

## Schwierigkeit
Anfänger

## Lernziel
Du kannst geheime Werte (API-Keys) sicher über `.env` verwalten und weißt, warum sie **niemals** in den Quellcode gehören.

## Warum ist das wichtig?
Ein API-Key ist wie eine Kreditkarte: Wer ihn hat, kann auf deine Kosten Anfragen senden. Sobald er auf GitHub landet (auch „nur kurz"), können ihn Bots binnen Minuten missbrauchen. Der Standardweg: **Umgebungsvariablen** – Werte außerhalb des Codes, die dein Programm zur Laufzeit liest.

## Das Konzept einfach erklärt
**Metapher:** Der Quellcode ist ein offenes Kochbuch, das jeder lesen darf. Geheimzutaten notierst du deshalb auf einem Zettel in deiner Schublade (`.env`) statt ins Kochbuch. Nur du öffnest die Schublade; das Kochbuch bleibt harmlos.

**Was ist eine API?** (jetzt wird's relevant) Eine *Programmierschnittstelle*: dein Programm „bestellt" bei einem Dienst (z. B. Mistral) eine Antwort, wie ein Kellner die Bestellung in die Küche bringt. Der API-Key ist dein Mitgliedsausweis für dieses Bestellen.

## Die technische Erklärung
- `os.environ.get("NAME")` liest eine Umgebungsvariable (liefert `None`, wenn sie fehlt).
- `python-dotenv` lädt die Datei `.env` in `os.environ`: `from dotenv import load_dotenv; load_dotenv()`
- `.env` **steht in `.gitignore`** – git ignoriert sie; die Vorlage `.env.example` (ohne echte Werte!) wird geteilt.
- Guter Stil: nie `os.environ["KEY"]` (crasht ohne Key), sondern `.get()` + freundliche Fehlermeldung.

## Voraussetzungen
- Aufgabe 1.3 (venv aktiv, Pakete installiert – `python-dotenv` ist in `requirements.txt`)

## Deine Mission
1. Kopiere `.env.example` → `.env` (im Projektordner) und setze `BEISPIEL_NAME` auf deinen Namen.
2. Schreibe `env_demonstration.py`, das:
   - `.env` lädt,
   - `BEISPIEL_NAME` und `MISTRAL_API_KEY` liest,
   - den Namen begrüßt,
   - prüft, ob ein Mistral-Key vorhanden ist, und eine klare Meldung gibt („Online-Modus möglich" / „Offline-Modus – auch gut!").
3. **Bonus:** Prüfe mit `git status`, dass `.env` **nicht** als zu committende Datei erscheint.

## Akzeptanzkriterien
- [ ] Das Skript begrüßt dich mit dem Namen aus `.env`.
- [ ] Ohne Key erscheint eine klare Meldung, kein Absturz.
- [ ] `git status` zeigt `.env` **nicht** (nur `.env.example` wurde geteilt).
- [ ] Der Key (falls vorhanden) wird **niemals komplett ausgegeben** – höchstens die ersten 4 Zeichen.

## Hinweise
1. Kopieren im Terminal: `cp .env.example .env` (Windows PowerShell: `copy .env.example .env`).
2. Lesen: `os.environ.get("BEISPIEL_NAME", "unbekannt")`.
3. Key nie loggen! Zum Prüfen reicht `bool(key)` bzw. `key[:4] + "..."`.

## Reflexionsfragen
1. Warum ist „der Key steht kurzfristig im Code, ich lösche ihn nachher" trotzdem gefährlich? (Tipp: Git-Historie!)
2. Warum teilen wir `.env.example` statt `.env`?
3. Was ist die Aussage der Meldung „Offline-Modus" in dieser Akademie (siehe README)?

## Häufige Fehler
| Problem | Lösung |
|---|---|
| Skript liest `.env` nicht | `load_dotenv()` vor dem ersten Lesen aufrufen; Skript aus dem Projektordner starten |
| `.env`-Werte mit Anführungszeichen | In der Regel weglassen: `BEISPIEL_NAME=Anna` |
| `.env` taucht in `git status` auf | `.gitignore` prüfen (sie enthält `.env`) |

## Referenzlösung
→ [`solutions/env_demonstration.py`](../solutions/env_demonstration.py)

## Code-Walkthrough
In der Lösungsdatei; sie nutzt genau das Muster, das auch das Akademie-Paket `lernakademie` intern verwendet.

## Was haben wir gelernt?
Sicheres Key-Management, `os.environ`, `python-dotenv`, Git-Hygiene bei Geheimnissen.

## Was kommt als Nächstes?
Abschlusstest der Stufe: Du kombinierst alles (Variablen, Sammlungen, Funktionen, `.env`) in deinem ersten Mini-Projekt – einem regelbasierten „persönlichen Assistenten". Danach lernt in Stufe 2 eine echte KI das Antworten übernehmen.
