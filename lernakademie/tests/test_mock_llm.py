"""Tests fuer das Hilfs-Paket (laufen ohne API-Key)."""

import os

os.environ.setdefault("ACADEMY_OFFLINE", "1")

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel

from lernakademie.mock_llm import (
    OFFLINE_PREFIX,
    MockChatModel,
    get_chat_model,
    get_mistral_client,
)
from lernakademie.offline_embeddings import OfflineKeywordEmbeddings


class RezeptIdee(BaseModel):
    titel: str
    zutaten: list[str]
    dauer_minuten: int


def test_mock_model_is_offline_and_deterministic():
    model = MockChatModel()
    messages = [SystemMessage(content="Du bist ein Kuechenassistent."),
                HumanMessage(content="Nenne ein Rezept mit Nudeln.")]
    first = model.invoke(messages)
    second = model.invoke(messages)
    assert first.content == second.content
    assert OFFLINE_PREFIX in first.content
    assert "Nudeln" in first.content


def test_mock_model_in_chain():
    model = get_chat_model()
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Du bist ein Zusammenfassungs-Assistent."),
         ("human", "{text}")]
    )
    chain = prompt | model | StrOutputParser()
    result = chain.invoke({"text": "Hallo Welt"})
    assert OFFLINE_PREFIX in result


def test_structured_output_offline():
    model = get_chat_model()
    structured = model.with_structured_output(RezeptIdee)
    result = structured.invoke("Pasta mit Tomaten!")
    assert isinstance(result, RezeptIdee)
    assert result.dauer_minuten == 1
    assert result.zutaten == []
    assert OFFLINE_PREFIX in result.titel


def test_mock_mistral_client():
    client = get_mistral_client()
    response = client.chat.complete(
        messages=[{"role": "user", "content": "Wie geht es dir?"}]
    )
    assert OFFLINE_PREFIX in response.choices[0].message.content


def test_offline_embeddings_similarity():
    embeddings = OfflineKeywordEmbeddings()
    doc = embeddings.embed_query("Wie viele Urlaubstage habe ich im ersten Jahr?")
    query = embeddings.embed_query("Urlaubsantrag stellen")
    empty = embeddings.embed_query("ganz anderes Thema")
    assert sum(a * b for a, b in zip(doc, query)) > 0
    assert sum(a * b for a, b in zip(doc, empty)) == 0


def test_mock_tool_calling_react_agent():
    """Der Offline-Mock simuliert Tool-Calling so, dass create_react_agent funktioniert."""
    from langchain_core.tools import tool
    from langchain.agents import create_agent
    from lernakademie.mock_llm import get_chat_model

    @tool
    def wortzaehler(text: str) -> str:
        """Zaehlt die Woerter eines Texts."""
        return f"Der Text enthaelt {len(text.split())} Woerter."

    agent = create_agent(
        model=get_chat_model(),
        tools=[wortzaehler],
        system_prompt="Du bist ein Zaehlassistent.",
    )
    ergebnis = agent.invoke(
        {"messages": [{"role": "user", "content": "Bitte nutze den wortzaehler fuer diesen Satz"}]}
    )
    letzte = ergebnis["messages"][-1]
    assert "Tool-Ergebnisse" in letzte.content
    assert "7 Woerter." in letzte.content
