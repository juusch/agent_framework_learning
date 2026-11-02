"""Tests fuer die Agenten-Loesungen (Stufe 6) – komplett offline."""

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


def test_toolbox_agent_tools():
    toolbox = lade_modul("06-agents-und-tools/solutions/toolbox_agent.py")
    assert "84" in toolbox.taschenrechner.invoke({"expression": "12 * 7"})
    assert "Ungueltiger Ausdruck" in toolbox.taschenrechner.invoke({"expression": "abc"})
    assert "Fehler" in toolbox.zufallszahl.invoke({"minimum": 9, "maximum": 3})
    assert "Zufallszahl" in toolbox.zufallszahl.invoke({"minimum": 1, "maximum": 6})


def test_knowledge_agent_retrieval_tool():
    know = lade_modul("06-agents-und-tools/solutions/knowledge_agent.py")
    retriever = know.baue_retriever(k=3)
    such_tool = know.baue_such_tool(retriever)
    treffer = such_tool.invoke({"suchbegriff": "Wie viele Urlaubstage gibt es?"})
    assert "mitarbeiter-handbuch.md" in treffer
    leer = such_tool.invoke({"suchbegriff": "Weihnachtsgeld Hoehe"})
    assert "Keine passenden" in leer or "keine passenden" in leer


def test_memory_approval_agent_flow():
    mem = lade_modul("06-agents-und-tools/solutions/memory_approval_agent.py")
    agent = mem.baue_agent()
    config = {"configurable": {"thread_id": "test-thread"}}

    from langchain_core.messages import HumanMessage
    from langgraph.types import Command

    ergebnis = agent.invoke(
        {"messages": [HumanMessage(content="Lege die geheime Notiz 'X' an.")]},
        config,
    )
    interrupts = ergebnis.get("__interrupt__")
    assert interrupts is not None  # Lauf pausiert VOR der Aktion
    assert not mem.ANGELEGTE_NOTIZEN  # noch nichts angelegt

    fortsetzung = agent.invoke(Command(resume=True), config)
    assert "[GEHEIM]" in mem.ANGELEGTE_NOTIZEN[0]  # Freigabe -> ausgefuehrt
    assert "Freigabe erteilt" in fortsetzung["messages"][-1].content
