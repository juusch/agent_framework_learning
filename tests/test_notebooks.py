"""Notebook-Validierung: Struktur, Syntax, Lernpfad-Integritaet – offline in CI.

Unterscheidet klar (Anforderung 'nicht schummeln'):
- Loesungs-Notebooks: wurden vom Build-Skript KOMPLETT AUSGEGEFUEHRT (offline).
- Lern-Notebooks: hier werden Struktur + Syntax + Workspace-Regeln geprueft
  (die Ausfuehrung der Lern-Notebooks erwartet # YOUR CODE HERE-Zellen, die
  bewusst NICHT funktionieren – das ist der Sinn des Arbeitsblatts).
"""

import re
import sys
from pathlib import Path

import nbformat
import pytest

PROJEKT = Path(__file__).resolve().parents[1]
ALLE_LERN = sorted((PROJEKT / "notebooks").glob("**/*.ipynb"))
ALLE_LOESUNGEN = sorted((PROJEKT / "solutions").glob("*.ipynb"))
START = PROJEKT / "START_HERE.ipynb"


def _code_zellen(nb) -> list:
    return [z for z in nb.cells if z.cell_type == "code"]


def test_notebook_inventar():
    """21 Lern-Notebooks (START_HERE + 20 Lektionen) + 20 Loesungen."""
    assert START.exists(), "START_HERE.ipynb fehlt im Projektursprung!"
    assert len(ALLE_LERN) == 20, f"Erwartet 20 Lektions-Notebooks, gefunden: {len(ALLE_LERN)}"
    assert len(ALLE_LOESUNGEN) == 20, f"Erwartet 20 Loesungen, gefunden: {len(ALLE_LOESUNGEN)}"


@pytest.mark.parametrize("nb_pfad", [START] + ALLE_LERN + ALLE_LOESUNGEN,
                         ids=lambda p: p.name)
def test_notebooks_parse_und_syntax(nb_pfad):
    """Jedes Notebook ist valides nbformat; jede Code-Zelle kompiliert."""
    nb = nbformat.read(str(nb_pfad), as_version=4)
    for index, zelle in enumerate(_code_zellen(nb)):
        compile(zelle.source, f"{nb_pfad.name}[zelle {index}]", "exec")


def test_loesungen_wurden_ausgefuehrt():
    """Build-Pflicht: Loesungs-Notebooks enthaelten echte Outputs (Erwartungen)."""
    ohne_output = []
    for loesung in ALLE_LOESUNGEN:
        nb = nbformat.read(str(loesung), as_version=4)
        outputs = sum(len(z.get("outputs", [])) for z in _code_zellen(nb))
        if outputs == 0:
            ohne_output.append(loesung.name)
    assert not ohne_output, f"Loesungen ohne Ausfuehrung: {ohne_output}"


def test_lernpfad_reihenfolge_und_links():
    """Die 20 Lektionen sind nummeriert 01-20 und 'weiter'-Verweise existieren."""
    nummern = [int(p.stem.split("_")[0]) for p in ALLE_LERN]
    assert nummern == list(range(1, 21)), f"Erwartet 1..20: {nummern}"


def test_start_here_fuehrt_zur_ersten_lektion():
    """Der Einstieg verweist auf Lektion 01 und erklaert die Konfiguration."""
    text = START.read_text(encoding="utf-8")
    assert "01_setup_und_python" in text
    assert "local-ai-server" in text          # Konfigurations-Doku verlinkt


@pytest.mark.parametrize("nb_pfad", ALLE_LERN, ids=lambda p: p.name)
def test_lektionen_haben_standardstruktur(nb_pfad):
    """Jede Lektion: Titel, Zeit, Lernziele, Setup-Zelle, Aufgabe(n), Weiter."""
    nb = nbformat.read(str(nb_pfad), as_version=4)
    text = "\n".join(z.source for z in nb.cells if z.cell_type == "markdown")
    code = "\n".join(z.source for z in _code_zellen(nb))
    assert "# Lektion" in text, "Titel fehlt"
    assert "Zeit" in text, "Zeitangabe fehlt"
    assert "Nach dieser Lektion kannst du" in text, "Lernziele fehlen"
    assert "llm_zusammenfassung" in code, "zentrale Konfigurations-Zelle fehlt"
    assert "Deine Aufgabe" in text, "Aufgabenstellung fehlt"
    assert "Richtig, wenn" in text, "Akzeptanzkriterien fehlen"
    if nb_pfad.stem != "20_testing_und_evaluierung":
        assert "Weiter" in text, "'Weiter'-Verweis fehlt"


def test_workspace_zellen_sind_ersichtlich():
    """Lern-Notebooks enthalten sichtbare YOUR-CODE-HIER-Marker."""
    for nb_pfad in ALLE_LERN:
        code = "\n".join(z.source for z in
                         _code_zellen(nbformat.read(str(nb_pfad), as_version=4)))
        assert "YOUR CODE HERE" in code, f"{nb_pfad.name}: Workspace-Marker fehlt"


def test_pruefzellen_existieren():
    """Jede Lektion enthaelt automatische Pruefzellen (assert-basiert)."""
    for nb_pfad in ALLE_LERN:
        code = "\n".join(z.source for z in
                         _code_zellen(nbformat.read(str(nb_pfad), as_version=4)))
        assert "assert" in code, f"{nb_pfad.name}: keine Pruefzelle (assert) gefunden"
