"""Aufgabe 6.3 – Referenzloesung: Wissens-Agent (RAG als Tool).

Muster: Der Index wird EINMAL gebaut; das Tool greift ueber eine
Closure darauf zu. Der Agent entscheidet, wann Nachschlagen noetig ist.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain.agents import create_agent
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lernakademie.llm_client import get_chat_model, is_offline_mode
from lernakademie.offline_embeddings import get_embeddings, hat_bezug

DATA = Path(__file__).resolve().parents[2] / "data"


def baue_retriever(k: int = 3):
    """Index einmalig bauen: laden -> splitten -> Chroma -> Retriever."""
    from langchain_community.document_loaders import TextLoader

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    alle_chunks = []
    for datei in sorted(DATA.glob("*.md")):
        alle_chunks.extend(splitter.split_documents(
            TextLoader(str(datei), encoding="utf-8").load()))
    db = Chroma(collection_name="handbuch_agent", embedding_function=get_embeddings())
    db.add_documents(alle_chunks)
    return db.as_retriever(search_kwargs={"k": k})


def baue_such_tool(retriever):
    """Fabrik: erzeugt das Such-Tool MIT Zugriff auf den Retriever (Closure)."""

    @tool
    def handbuch_suche(suchbegriff: str) -> str:
        """Schlaegt im Mitarbeiter- und IT-Handbuch nach und liefert passende Textstellen mit Quellenangabe."""
        if is_offline_mode() and not hat_bezug(suchbegriff):
            return "Keine passenden Stellen gefunden. Formuliere die Suche mit Begriffen aus den Handbuechern."
        dokumente = retriever.invoke(suchbegriff)
        if not dokumente:
            return "Keine passenden Stellen gefunden."
        treffer = []
        for dokument in dokumente:
            quelle = Path(dokument.metadata["source"]).name
            auszug = dokument.page_content.strip().replace("\n", " ")
            treffer.append(f"[{quelle}] {auszug}")
        return "\n\n".join(treffer)

    return handbuch_suche


@tool
def uhrzeit() -> str:
    """Liefert die aktuelle Uhrzeit im Format HH:MM."""
    return f"Es ist {datetime.now().strftime('%H:%M')} Uhr."


def benutzte_tools(ergebnis: dict) -> list[str]:
    return [
        call["name"]
        for nachricht in ergebnis["messages"]
        for call in (getattr(nachricht, "tool_calls", None) or [])
    ]


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Retrieval ist echt, Antwort formuliert simuliert.\n")

    retriever = baue_retriever()          # Index: EINMAL bauen
    such_tool = baue_such_tool(retriever)  # Tool mit Closure-Zugriff

    agent = create_agent(
        model=get_chat_model(temperature=0.0),
        tools=[such_tool, uhrzeit],
        system_prompt=("Du bist ein Firmen-Assistent. Fuer Fragen zu Urlaub, "
                       "Gehalt, VPN, Passwort & Co. schlage im Handbuch nach "
                       "(handbuch_suche). Alltagsfragen beantwortest du direkt."),
    )

    anfragen = [
        "Was steht im Handbuch zum Thema Urlaub? Nutze die handbuch_suche.",
        "Wie richte ich VPN ein? Nutze die handbuch_suche.",
        "Wie spät ist es? Nutze die uhrzeit.",  # sollte NICHT nachschlagen
    ]
    for anfrage in anfragen:
        ergebnis = agent.invoke({"messages": [{"role": "user", "content": anfrage}]})
        print(f"Anfrage: {anfrage}")
        print(f"  Tools   : {benutzte_tools(ergebnis) or 'keines'}")
        print(f"  Antwort : {ergebnis['messages'][-1].content[:200]}\n")


if __name__ == "__main__":
    main()
