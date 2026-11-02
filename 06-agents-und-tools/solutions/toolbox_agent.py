"""Aufgabe 6.2 – Referenzloesung: Agent mit Werkzeugkasten.

Sicherheit zuerst: Der Taschenrechner parst einfache Ausdruecke selbst
(statt eval zu verwenden) und Tools fangen Fehler ab – so bleibt der
Agent auch bei Muell-Eingaben handlungsfaehig.
"""

import random
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain.agents import create_agent
from langchain_core.tools import tool

from lernakademie.llm_client import get_chat_model, is_offline_mode

_RECHNUNG = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)\s*$")


@tool
def taschenrechner(expression: str) -> str:
    """Berechnet einen einfachen mathematischen Ausdruck der Form 'zahl operator zahl' (z.B. '12 * 7')."""
    match = _RECHNUNG.match(expression)
    if not match:
        return ("Ungueltiger Ausdruck. Bitte im Format 'zahl operator zahl' "
                "angeben, z.B. '12 * 7'.")
    links, operator, rechts = float(match.group(1)), match.group(2), float(match.group(3))
    try:
        if operator == "+":
            ergebnis = links + rechts
        elif operator == "-":
            ergebnis = links - rechts
        elif operator == "*":
            ergebnis = links * rechts
        elif operator == "/":
            ergebnis = links / rechts
    except ZeroDivisionError:
        return "Division durch Null ist nicht moeglich."
    zahl = int(ergebnis) if ergebnis == int(ergebnis) else round(ergebnis, 6)
    return f"Ergebnis von {expression} = {zahl}"


@tool
def uhrzeit() -> str:
    """Liefert die aktuelle Uhrzeit im Format HH:MM."""
    return f"Es ist {datetime.now().strftime('%H:%M')} Uhr."


@tool
def zufallszahl(minimum: int, maximum: int) -> str:
    """Zieht eine Zufallszahl zwischen minimum und maximum (inklusive)."""
    if minimum > maximum:
        return "Fehler: minimum muss kleiner oder gleich maximum sein."
    return f"Zufallszahl zwischen {minimum} und {maximum}: {random.randint(minimum, maximum)}"


def benutzte_tools(ergebnis: dict) -> list[str]:
    """Liest aus dem State ab, welche Tools der Agent aufgerufen hat."""
    namen = []
    for nachricht in ergebnis["messages"]:
        for call in getattr(nachricht, "tool_calls", None) or []:
            namen.append(call["name"])
    return namen


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Tool-Auswahl simuliert "
              "(Tool-Namen in den Fragen erwaehnen).\n")

    agent = create_agent(
        model=get_chat_model(temperature=0.0),
        tools=[taschenrechner, uhrzeit, zufallszahl],
        system_prompt="Du bist ein Alltags-Assistent und nutzt deine "
                      "Werkzeuge, wann immer exakte Antworten noetig sind.",
    )

    anfragen = [
        "Was ergibt 12 * 7? Nutze den taschenrechner.",
        "Wie spät ist es? Nutze die uhrzeit.",
        "Gib mir eine zufallszahl zwischen 1 und 6.",
        "Erkläre in einem Satz, was eine Kette (Chain) ist.",  # ohne Tool
    ]
    for anfrage in anfragen:
        ergebnis = agent.invoke({"messages": [{"role": "user", "content": anfrage}]})
        tools = benutzte_tools(ergebnis)
        print(f"Anfrage: {anfrage}")
        print(f"  Tools : {tools if tools else 'keines'}")
        print(f"  Antwort: {ergebnis['messages'][-1].content}\n")

    # Fehlerfall: ungültige Rechnung – das Tool meldet freundlich
    fehler = agent.invoke({"messages": [{"role": "user", "content":
                             "Was ergibt abc? Nutze den taschenrechner."}]})
    print("Fehlereingabe 'abc':", fehler["messages"][-1].content)


if __name__ == "__main__":
    main()
