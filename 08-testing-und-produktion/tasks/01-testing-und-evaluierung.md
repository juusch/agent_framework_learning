# Aufgabe 8.1 – Testing & Evaluierung 🧪

**Schwierigkeit:** Mittel · **Zeit:** ~60 Min · **Kosten:** keine

## Lernziel
Du prüfst KI-Anwendungen **automatisiert**: Unit-/Integrationstests für die Logik, kriterienbasierte Evaluierung für Antwortqualität.

## Warum das wichtig ist
„Ich habe es einmal probiert und es ging" ist **kein** Test. **Metapher:** Unittest = Rechenaufgabe mit eindeutiger Lösung (30 Urlaubstage == 30). Eval = Bewertungsraster („Enthält die Antwort die richtige Zahl? Nennt sie eine Quelle?") – prüft Eigenschaften, nicht Identität. Die Akademie lebt nach diesem Muster: alle Tests laufen offline in CI.

## Deine Mission
1. **Unit-Tests:** schreibe Tests für eine Modul-5-Lösung (`routing_graph.klassifizieren`: 3 Kategorien + Grenzfall) und den Build-1-Assistenten (`suche_relevant`: Treffer, Sortierung, leerer Fall) – mit dem importlib-Muster aus `tests/test_solutions.py`.
2. **Integrationstest:** ein Test, der `loop_graph.baue_graph()` startet und **Terminierung** prüft (auch bei Grenzkonfiguration); und ein Test für den Build-2-Retriever (Quellen korrekt?).
3. **Eval:** `solutions/evaluation.py` studieren und erweitern: eine neue Testfrage mit erwarteter Eigenschaft für den Build-2-Assistenten; Erfolgsquote ausgeben.
4. **Regression verstehen:** Ändere absichtlich einen Prompt/Parameter in einer Lösung → Tests laufen lassen → welches Verhalten „merkt" sich der Test?

## Akzeptanzkriterien
- [ ] Deine Unit-Tests sind grün und deckten Grenzfälle ab.
- [ ] Der Integrationstest beweist Terminierung.
- [ ] Deine Eval-Frage ist dokumentiert und die Quote nachvollziehbar.
- [ ] `pytest` insgesamt grün (auch die bestehenden 40+ Tests).

## Hinweise
1. Dateien in Unterordnern: per `importlib.util.spec_from_file_location` laden (Vorlage in `tests/`).
2. Offline-Modus macht alles deterministisch – die Quote ist reproduzierbar (Feature!).
3. Trau dich, bestehende Tests zu lesen – sie sind ihre eigene Dokumentation.

## Reflexionsfragen
1. Warum können Mock-Tests die *Mechanik*, aber nicht die *Qualität* echter LLM-Antworten prüfen – was kostet dich das in CI vs. Produktion?
2. Was ist ein Regressionstest im KI-Kontext (Stichwort: Prompt geändert → Evals laufen)?
3. Warum ist eine 100%-Quote bei zu einfachen Testfragen gefährlich?

## Referenzlösung + Walkthrough
→ [`solutions/evaluation.py`](../solutions/evaluation.py), [`tests/`](../../tests/), [`final-project/knowledge-research-agent/tests/`](../../final-project/knowledge-research-agent/tests/)

## Weiter
8.2 – Sicherheit, Kosten, Logging, Docker – und dein Abschluss.
