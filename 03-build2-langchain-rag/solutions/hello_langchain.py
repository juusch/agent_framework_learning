"""Aufgabe 3.1 – Referenzloesung: Hello LangChain.

Kernpunkte:
- Chat-Modell als OBJEKT (get_chat_model: Mistral oder Offline-Simulation)
- Nachrichten als Message-Objekte (SystemMessage, HumanMessage, AIMessage)
- Antworttext steckt in .content
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from lernakademie.llm_client import get_chat_model, is_offline_mode


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Das Modell ist eine Simulation.\n")

    # Chat-Modell-Objekt holen (mit Key: ChatMistralAI, ohne: MockChatModel)
    model = get_chat_model(temperature=0.2)

    # Nachrichten als Objekte statt Dictionaries
    system = SystemMessage(content="Du bist ein Python-Tutor fuer absolute Anfaenger.")
    human = HumanMessage(content="Erkläre in einem Satz, was eine Variable ist.")

    antwort = model.invoke([system, human])
    print("Modell-Antwort:", antwort.content)

    # Experiment: Historie mitReisen – wir simulieren einen bisherigen
    # Gespraechsverlauf, indem wir eine (fingierte) Assistenten-Antwort
    # in die Liste aufnehmen und danach eine Rueckfrage stellen.
    verlauf = [
        system,
        human,
        AIMessage(content="Eine Variable ist wie eine beschriftete Kiste."),
        HumanMessage(content="Und was ist dann eine Liste?"),
    ]
    antwort2 = model.invoke(verlauf)
    print("\nAntwort mit Historie:", antwort2.content)


if __name__ == "__main__":
    main()
