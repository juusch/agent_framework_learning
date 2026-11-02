# Aufgabe 9.1 – Testing & Evaluierung 🧪

## Schwierigkeit
Mittel · **Kosten: keine** (alles offline)

## Lernziel
Du kannst KI-Anwendungen **automatisiert** prüfen: Unit-/Integrationstests für die Logik und einfache Evaluierung für Antwortqualität.

## Warum ist das wichtig?
KI-Verhalten ist nicht deterministisch – „Ich habe es einmal probiert und es ging" ist **kein** Test. Die Rettung: Trenne **deterministische Logik** (normal testbar) von **LLM-Verhalten** (evaluiert man mit Kriterien und Beispielen). Genau nach diesem Muster ist diese Akademie gebaut: `lernakademie/tests/` und `tests/` laufen komplett offline in CI.

## Das Konzept einfach erklärt
**Metapher:** Zwei Prüfungsarten: Ein **Unittest** ist eine Rechenaufgabe mit eindeutiger Lösung (30 Urlaubstage == 30). Eine **Eval** ist eine Bewertung mit Bewertungsraster („Enthält die Antwort die richtige Zahl? Nennt sie eine Quelle?"): Sie prüft nicht Identität, sondern **Eigenschaften**.

## Die technische Erklärung
- **Unit-Tests (pytest):** prüfen reine Funktionen – Chunker, Parser, Weichen, Tools. Das Offline-Konzept der Akademie macht sogar LLM-Verkettungen testbar (deterministische Mock-Antworten).
- **Integrationstests:** ganze Graphen/Chains mit definierten Eingaben – wie `tests/test_agents.py`.
- **Evaluierung von LLM-Antworten:** mit `assert "30" in antwort` prüfst du Fakten; für Qualität nutzt man Kriterien-Listen („erwähnt Quelle", „unter N Wörtern") oder LLM-as-Judge (ein Modell bewertet die Antwort – Stichwort LangSmith Evals).

## Deine Mission
1. **Unit:** Schreibe Tests für eine Stufe-5-Lösung (z. B. `routing_graph.klassifizieren`): drei Kategorien + Grenzfall (leere Eingabe).
2. **Integration:** Schreibe einen Test, der `loop_graph.baue_graph()` startet und prüft: endet immer (auch mit max_versuche=0-konfiguration? denke nach!), Historie wächst pro Runde.
3. **Eval:** Baue `evaluation.py`: definiere 4 Testfragen mit **erwarteten Eigenschaften** (enthaelt "30"/"VPN"/Quelle/nichts-gefunden) und bewerte die Wissens-Assistent-Antworten (offline-ehrlich!). Gib eine Erfolgsquote aus.
4. Lasse alles laufen: `pytest` (auch die bestehenden 15+ Tests müssen grün bleiben).

## Akzeptanzkriterien
- [ ] Neue Unit-Tests für Stufe-5-Logik, grün.
- [ ] Integrationstest prüft, dass der Loop **immer terminiert**.
- [ ] `evaluation.py` liefert eine Erfolgsquote über 0 % und unter 100 % wäre verdächtig präzise – verstehe warum sie 100 % sein kann (deterministisch offline!).
- [ ] `pytest` insgesamt grün.

## Hinweise
1. Tests für Unterordner-Dateien: Modul per `importlib` laden wie in `tests/test_solutions.py`.
2. Eval-Eigenschaften bewusst einfach halten – das Muster zählt, nicht die Perfektion.
3. Niemand verhindert dich, **deine** Evaluierungskriterien zu erweitern.

## Reflexionsfragen
1. Warum können Mock-basierte Tests die *Mechanik*, aber nicht die *Qualität* echter LLM-Antworten prüfen? Was kostet dich das in CI – und was in Produktion?
2. Was ist ein „Regressionstest" im KI-Kontext (Stichwort: Prompt geändert → Evals laufen lassen)?
3. Warum ist eine Erfolgsquote als Zahl gefährlich, wenn die Testfragen zu einfach sind?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Tests brauchen Netz/Key | Offline-Modus (`ACADEMY_OFFLINE=1`) nutzen |
| Tests erreichen nie die Lösungsfunktionen | importlib-Muster aus `tests/test_solutions.py` kopieren |
| Eval testet nur das Echo | Eigenschaften wählen, die wirklich aus dem Retrieval kommen |

## Referenzlösung
→ [`solutions/evaluation.py`](../solutions/evaluation.py) plus die bestehenden Tests in [`tests/`](../../tests/)

## Was haben wir gelernt?
Testpyramide für KI-Apps, Eval-Muster, CI-fähige Offline-Tests.

## Was kommt als Nächstes?
9.2: Sicherheit (Keys!), Kosten (Budget!) und Observability (Logging, LangSmith).
