# Aufgabe 0.3 – Funktionen, virtuelle Umgebungen & API-Keys 🔧

**Schwierigkeit:** Anfänger · **Zeit:** ~60 Min · **Kosten:** keine

## Lernziel
Code in Funktionen kapseln, ein Projekt mit venv + Paketen aufsetzen und Geheimnisse sicher über `.env` verwalten.

## Warum das wichtig ist
Ab der nächsten Aufgabe rufst du Mistral auf – dafür brauchst du installierte Pakete (venv!) und einen API-Key, der **niemals** im Code landet. **Metaphern:** Funktion = Rezept mit Namen; venv = eigener Werkzeugkasten pro Baustelle; API-Key = Kreditkarte – wer sie hat, zahlt deine Rechnungen.

## Deine Mission
1. **Funktions-Werkstatt:** `begruessung(name, stil="hoeflich")`, `durchschnitt(zahlen)` (leere Liste → 0, kein Crash!), `ist_arbeitszeit(stunde)`. Nutze in `main()` außerdem `datetime` und `random`.
2. **venv anlegen + aktivieren** und `pip install -r requirements.txt`; prüfe mit `pip list`, dass `langchain` erscheint; starte `00-setup/examples/venv_demonstration.py`.
3. **.env:** Kopiere `.env.example` → `.env`, setze `BEISPIEL_NAME`; schreibe `env_demonstration.py`, das `.env` lädt, den Namen begrüßt und prüft, ob ein `MISTRAL_API_KEY` existiert – **ohne den Key jemals komplett auszugeben**. Bonus: zeige mit `git status`, dass `.env` ignoriert wird.

## Akzeptanzkriterien
- [ ] Alle drei Funktionen arbeiten korrekt; `durchschnitt([])` ergibt 0.
- [ ] Der Terminal-Prompt zeigt `(.venv)`; die Demo-Datei läuft.
- [ ] Das Skript liest `.env` und meldet Offline-Modus, wenn kein Key gesetzt ist.
- [ ] `git status` zeigt `.env` **nicht**.

## Hinweise
1. `load_dotenv()` **vor** dem ersten `os.environ.get(...)` aufrufen.
2. Key-Prüfung: `bool(key)` reicht; zum Zeigen nur `key[:4] + "..."`.
3. PowerShell-Skriptblockade: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Reflexionsfragen
1. Warum wäre „der Key steht kurz im Code, ich lösche ihn später" gefährlich? (Tipp: Git-Historie!)
2. Warum teilen wir `.env.example`, aber niemals `.env`?
3. Was bringt die Trennung Rezept (Funktion) und Kochvorgang (Aufruf) für Tests?

## Referenzlösung + Walkthrough
→ [`solutions/funktions_werkstatt.py`](../solutions/funktions_werkstatt.py), [`solutions/env_demonstration.py`](../solutions/env_demonstration.py), [`solutions/venv_checkliste.md`](../solutions/venv_checkliste.md).

## Weiter
🚀 [`01-llms-und-mistral/`](../../01-llms-und-mistral/README.md) – dein Python redet zum ersten Mal mit einer echten KI.
