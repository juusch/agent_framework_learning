"""Aufgabe 6.1 – Referenzloesung: Agent mit erstem Tool.

Der Docstring des Tools ist die "Bedienungsanleitung", anhand derer
das Modell entscheidet, ob es das Werkzeug benutzt.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain.agents import create_agent
from langchain_core.tools import tool

from lernakademie.mock_llm import get_chat_model, is_offline_mode


@tool
def wortzaehler(text: str) -> str:
    """Zaehlt die Woerter eines Texts."""
    return f"Der Text enthaelt {len(text.split())} Woerter."


def zeige_nachrichtentypen(ergebnis: dict) -> None:
    """Macht den Agenten-Loop sichtbar: Human -> AI(tool_call) -> Tool -> AI."""
    for nachricht in ergebnis["messages"]:
        info = f"type={type(nachricht).__name__}"
        if getattr(nachricht, "tool_calls", None):
            info += f" tool_calls={[c['name'] for c in nachricht.tool_calls]}"
        print(f"  {info}")


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Tool-Auswahl wird simuliert "
              "(Tool-Namen in der Frage erwaehnen).\n")

    agent = create_agent(
        model=get_chat_model(temperature=0.0),
        tools=[wortzaehler],
        system_prompt="Du bist ein Assistent fuer Text-Statistiken.",
    )

    frage = ("Wie viele Woerter hat der Satz 'LangGraph macht Workflows "
             "steuerbar'? Nutze den wortzaehler.")
    ergebnis = agent.invoke({"messages": [{"role": "user", "content": frage}]})
    print("Frage:", frage)
    print("Antwort:", ergebnis["messages"][-1].content, "\n")
    zeige_nachrichtentypen(ergebnis)

    kontrollfrage = "Erkläre in einem Satz, was ein Embedding ist."
    ergebnis2 = agent.invoke({"messages": [{"role": "user", "content": kontrollfrage}]})
    print("\nKontrollfrage:", kontrollfrage)
    print("Antwort:", ergebnis2["messages"][-1].content)


if __name__ == "__main__":
    main()
