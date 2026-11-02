# Aufgabe 2.2 – Build 1b: Orchestrierungsschmerz & erste Oberfläche 🖥️

**Schwierigkeit:** Leicht · **Zeit:** ~45–60 Min · **Kosten:** keine (offline lauffähig)

## Lernziel
Du erweiterst Build 1 um Gesprächs-Verlauf und eine **Streamlit-Chat-Oberfläche** – und dokumentierst ehrlich, wo manuelle Orchestrierung kompliziert wird. Das ist die Motivation für Build 2.

## Warum das wichtig ist
**Das Frontend ist ab jetzt dein ständiger Begleiter:** Du wirst jede Ausbaustufe deines Assistenten sofort sehen und bedienen können – erst minimal (hier), am Ende vollständig (Modul 7). Wichtig: **Du lernst die Konzepte, nicht Frontend-Entwicklung** – die Oberfläche ist fertig gelieferter, kommentierter Code.

## Was du VERSTEHEN sollst (nicht selbst bauen)
- Streamlit läuft bei **jedem Klick** das Skript neu ab → Zustand muss in `st.session_state` leben (dasselbe Problem wie beim LLM-Gedächtnis: der „Notizblock" muss explizit mitgeführt werden!).
- Die Oberfläche ruft hier deinen Assistenten **direkt im selben Prozess** auf – die einfachste Brücke. Warum später eine API-Schicht dazwischen kommt (Modul 7), verstehst du am Vergleich mit dem Build-3-Backend.

## Deine Mission
1. Lies `solutions/chat_ui.py` und starte sie: `streamlit run 02-build1-python-assistent/solutions/chat_ui.py` – chatte mit deinem Build-1-Assistenten!
2. **Verlauf einbauen (Verständnis):** Erkläre dir anhand des Codes, wie `st.session_state.verlauf` das Gespräch über Klicks hinweg erhält. Was passiert ohne `session_state`?
3. **Schmerz-Dokumentation (Core!):** Erweitere `pure_python_assistant.py` um eine zweite Wissensquelle (z. B. Abschnitte aus `data/firmenprofil.md`) und protokolliere in einem Kommentarblock: Welche Funktionen musstest du anpassen? Wie dupliziert sich Logik (Prompt-Bau, Fehlerbehandlung, Scoring)? Was wäre bei 10 Quellen + Verlauf + Zitaten nötig?
4. **Reflexions-Notiz** (3–4 Sätze): Welche 3 Sachen würde ein Framework für dich übernehmen müssen, damit du dich auf das *Produkt* konzentrieren kannst?

## Akzeptanzkriterien
- [ ] Die Oberfläche läuft und antwortet über deinen Build-1-Assistenten.
- [ ] Du kannst in 2 Sätzen erklären, warum `session_state` nötig ist.
- [ ] Deine Schmerz-Dokumentation nennt mindestens 3 konkrete Duplikations-/Wartungspunkte.
- [ ] Die Reflexions-Notiz benennt, was LangChain abnehmen soll (Prompt-Bau? Fehler? Abstraktion?).

## Hinweise
1. Streamlit starten: `streamlit run <datei>` (nicht `python3 <datei>`!)
2. Verlaufs-Boot: `st.session_state.setdefault("verlauf", [])`
3. Bei „.connection refused": Das hier braucht noch **keinen** Server – läuft direkt.

## Reflexionsfragen
1. Was war in Build 1 am mühsamsten – und was davon war *fachlicher* Aufwand (Scoring, Prompts) vs. *technischem* Boilerplate?
2. Warum ist „jedes Mal das Skript neu ausführen" bei Streamlit kein Bug, sondern ein bewusstes Design?
3. Wenn morgen eine zweite Oberfläche (Handy-App) denselben Assistenten nutzen soll – was fehlt in Build 1 dafür?

## Referenzlösung + Walkthrough
→ [`solutions/chat_ui.py`](../solutions/chat_ui.py) (Oberfläche, kommentiert) + [`solutions/pure_python_assistant.py`](../solutions/pure_python_assistant.py) (erweiterte Fassung mit Firmenprofil).

## Weiter
🔗 [`../03-build2-langchain-rag/`](../03-build2-langchain-rag/README.md) – **Build 2**: LangChain ersetzt dein handgebautes Fließband, und semantische Suche ersetzt Wort-Überlappung.
