"""Tests fuer die wiederverwendbaren Build-Module (lernakademie/).

Die Notebook-Loesungen wurden komplett ausgefuehrt (siehe test_notebooks.py);
hier pruefen wir die Produktions-Abstraktionen, auf denen Capstone & Frontend
aufbauen – deterministisch, offline.
"""

import os

os.environ.setdefault("ACADEMY_OFFLINE", "1")

from lernakademie.build1 import lade_dokumente, suche_relevant, beantworte as b1
from lernakademie.build2 import beantworte as b2


def test_build1_suche():
    abschnitte = lade_dokumente()
    treffer = suche_relevant("Wie viele Urlaubstage gibt es?", abschnitte)
    assert treffer and treffer[0]["titel"] == "Urlaub"
    assert suche_relevant("Weihnachtsgeld Hoehe Bonus?", abschnitte) == []


def test_build1_ehrlichkeit():
    ergebnis = b1("Wie hoch ist das Weihnachtsgeld?", lade_dokumente())
    assert ergebnis["quellen"] == []
    assert "nichts gefunden" in ergebnis["antwort"]


def test_build2_quellen_und_ehrlichkeit():
    ergebnis = b2("Wie viele Urlaubstage gibt es?")
    assert "mitarbeiter-handbuch.md" in ergebnis["quellen"]
    leer = b2("Wie hoch ist das Weihnachtsgeld?")
    assert leer["quellen"] == [] and "leider nicht" in leer["antwort"]
