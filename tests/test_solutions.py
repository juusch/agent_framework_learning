"""Tests fuer die Referenzloesungen der Lernstufen 1 und 4.

Die Loesungen liegen in Unterordnern ohne Paketstruktur; wir laden sie
deshalb per importlib direkt aus ihrem Dateipfad.
"""

import importlib.util
import os
from pathlib import Path

import pytest

os.environ.setdefault("ACADEMY_OFFLINE", "1")

PROJEKT = Path(__file__).resolve().parents[1]


def lade_modul(relativer_pfad: str):
    datei = PROJEKT / relativer_pfad
    spec = importlib.util.spec_from_file_location(datei.stem, datei)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


@pytest.fixture(scope="module")
def einkaufsliste():
    return lade_modul("01-python-fundamentals/solutions/einkaufsliste.py")


@pytest.fixture(scope="module")
def werkstatt():
    return lade_modul("01-python-fundamentals/solutions/funktions_werkstatt.py")


@pytest.fixture(scope="module")
def assistant():
    return lade_modul("01-python-fundamentals/solutions/personal_assistant.py")


@pytest.fixture(scope="module")
def document_qa():
    return lade_modul("04-rag-and-knowledge/solutions/document_qa.py")


# ---- Stufe 1 -------------------------------------------------------------

def test_einkaufsliste_summe(einkaufsliste):
    einkauf = ["Milch", "Brot"]
    preise = {"Milch": 1.2, "Brot": 2.5}
    assert einkaufsliste.berechne_summe(einkauf, preise) == pytest.approx(3.7)


def test_einkaufsliste_ergaenzen(einkaufsliste):
    einkauf, preise = [], {}
    einkaufsliste.ergaenze(einkauf, preise, "Kaffee", 4.99)
    assert "Kaffee" in einkauf and preise["Kaffee"] == 4.99


def test_funktions_werkstatt(werkstatt):
    assert werkstatt.begruessung("Anna") == "Guten Tag, Anna. Schoen, Sie zu sehen."
    assert werkstatt.begruessung("Ben", stil="locker") == "Na, Ben! Was geht?"
    assert werkstatt.durchschnitt([2, 4, 9]) == 5.0
    assert werkstatt.durchschnitt([]) == 0.0
    assert werkstatt.ist_arbeitszeit(12) is True
    assert werkstatt.ist_arbeitszeit(3) is False


def test_assistent_antworten(assistant):
    assert assistant.finde_antwort("fertig") == "__ENDE__"
    assert "Uhr" in assistant.finde_antwort("Wie ist die Uhrzeit?")
    einkauf_antwort = assistant.finde_antwort("zeige einkauf")
    assert "Milch" in einkauf_antwort
    unverstanden = assistant.finde_antwort("xyz unpassend")
    assert "nicht verstanden" in unverstanden


# ---- Stufe 4 (RAG, offline) ----------------------------------------------

def test_document_qa_retrieval_quellen(document_qa):
    retriever = document_qa.baue_retriever(k=3)
    ergebnis = document_qa.beantworte(
        "Wie viele Urlaubstage gibt es?", retriever)
    assert ergebnis["quellen"] == ["mitarbeiter-handbuch.md"]


def test_document_qa_kein_treffer(document_qa):
    retriever = document_qa.baue_retriever(k=3)
    ergebnis = document_qa.beantworte("Wie hoch ist das Weihnachtsgeld?", retriever)
    assert ergebnis["antwort"] == document_qa.NICHT_GEFUNDEN
    assert ergebnis["quellen"] == []
