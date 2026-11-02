"""Simulierte Modelle fuer den Offline-Modus der Lernakademie.

Warum gibt es das?
- Lernende koennen JEDE Aufgabe ohne API-Key und ohne Kosten ausueben.
- Die automatisierten Tests (CI) benoetigen keine Geheimnisse.

Alle simulierten Antworten beginnen mit "[OFFLINE]", damit jederzeit
klar ist: Das ist kein echtes Sprachmodell.

Die Klasse MockChatModel verhaelt sich gegenueber LangChain-Chains wie ein
echtes Chat-Modell (gleiche Runnable-Schnittstelle: .invoke, |, bind etc.).
"""

from __future__ import annotations

from typing import Any, List, Sequence

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel

from lernakademie.config import get_model_name, has_mistral_key, is_offline_mode

OFFLINE_PREFIX = "[OFFLINE]"

# Maximal so viele Zeichen des Nutzer-Texts, die die Simulation aufgreift.
_MAX_ECHO_CHARS = 220


def _extract_last_user_text(messages: Sequence[BaseMessage]) -> str:
    """Liefert den Text der letzten User-/Human-Nachricht (oder '')."""
    for message in reversed(list(messages)):
        if message.type in ("human", "user"):
            content = message.content
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                return " ".join(
                    part.get("text", "") for part in content if isinstance(part, dict)
                )
    return ""


def _mock_answer_text(messages: Sequence[BaseMessage]) -> str:
    """Erzeugt eine deterministische, klar gekennzeichnete Schein-Antwort."""
    user_text = " ".join(_extract_last_user_text(messages).split())
    if not user_text:
        user_text = "(keine Nutzereingabe erkannt)"
    if len(user_text) > _MAX_ECHO_CHARS:
        user_text = user_text[:_MAX_ECHO_CHARS] + " ..."
    return (
        f"{OFFLINE_PREFIX} Simulierte Antwort (kein echtes Modell, keine Kosten). "
        f"Ein echtes Modell wuerde jetzt auf folgenden Text reagieren: „{user_text}“"
    )


class MockChatModel(BaseChatModel):
    """Offline-Stand-In fuer ein LangChain-Chat-Modell.

    Verhaelt sich in Chains wie ein echtes Modell, liefert aber
    deterministische, klar markierte Platzhalter-Antworten.
    """

    @property
    def _llm_type(self) -> str:
        return "lernakademie-offline-model"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Any = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        message = AIMessage(content=_mock_answer_text(messages))
        return ChatResult(generations=[ChatGeneration(message=message)])

    def with_structured_output(self, schema: Any, **kwargs: Any):
        """Offline-Variante: fuellt das Pydantic-Schema mit Platzhaltern.

        So bleiben Chains mit strukturiertem Output ohne Key lauffaehig
        und testbar.
        """
        if not (isinstance(schema, type) and issubclass(schema, BaseModel)):
            raise ValueError(
                "Im Offline-Modus wird fuer with_structured_output ein "
                "Pydantic-Modell (Basisklasse BaseModel) benoetigt."
            )

        def _fill(_: Any) -> Any:
            fields: dict[str, Any] = {}
            for name, field in schema.model_fields.items():
                annotation = field.annotation

                if annotation is int:
                    fields[name] = 1
                elif annotation is float:
                    fields[name] = 1.0
                elif _is_list_annotation(annotation):
                    fields[name] = []
                elif annotation is str:
                    fields[name] = f"{OFFLINE_PREFIX} {name} (simuliert)"
                else:
                    fields[name] = None
            return schema(**fields)

        @staticmethod
        def _is_list_annotation(annotation: Any) -> bool:
            origin = getattr(annotation, "__origin__", None)
            return annotation is list or origin is list


        return RunnableLambda(_fill)

    def bind(self, **kwargs: Any) -> "MockChatModel":
        """Akzeptiert bind-Parameter (z. B. tools) und ignoriert sie offline."""
        return self


def get_chat_model(temperature: float = 0.7) -> Any:
    """Liefert das Chat-Modell je nach Modus.

    - Echter Modus: ChatMistralAI (Mistral AI als primarer Provider).
    - Offline-Modus: MockChatModel (kein Key, keine Kosten).
    """
    if is_offline_mode():
        return MockChatModel()
    from langchain_mistralai import ChatMistralAI

    return ChatMistralAI(
        model=get_model_name(),
        temperature=temperature,
        api_key=__import__("os").environ["MISTRAL_API_KEY"],
    )


# ---------------------------------------------------------------------------
# Mock-Client fuer Stufe 2 (direkte Mistral-API ohne LangChain)
# ---------------------------------------------------------------------------


class _MockMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class _MockChoice:
    def __init__(self, content: str) -> None:
        self.message = _MockMessage(content)


class _MockChatResponse:
    def __init__(self, content: str) -> None:
        self.choices = [_MockChoice(content)]


class MockMistralClient:
    """Simuliert den minimalen Chat-Teil des mistralai-Clients."""

    def __init__(self) -> None:
        class _Chat:
            @staticmethod
            def complete(**kwargs: Any) -> _MockChatResponse:
                messages = kwargs.get("messages", [])
                last_user = ""
                for message in reversed(messages):
                    if message.get("role") == "user":
                        last_user = message.get("content", "")
                        break
                text = " ".join(last_user.split())
                if len(text) > _MAX_ECHO_CHARS:
                    text = text[:_MAX_ECHO_CHARS] + " ..."
                return _MockChatResponse(
                    f"{OFFLINE_PREFIX} Simulierte Antwort (Offline-Modus) auf: „{text}“"
                )

        self.chat = _Chat()


def get_mistral_client() -> Any:
    """Liefert einen Mistral-Client: echt (mit Key) oder simuliert (offline)."""
    if is_offline_mode():
        return MockMistralClient()
    from mistralai import Mistral

    return Mistral(api_key=__import__("os").environ["MISTRAL_API_KEY"])


__all__ = [
    "OFFLINE_PREFIX",
    "MockChatModel",
    "MockMistralClient",
    "get_chat_model",
    "get_mistral_client",
    "has_mistral_key",
    "is_offline_mode",
]
