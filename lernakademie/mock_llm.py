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

import re
from typing import Any, Dict, List, Optional, Sequence  # noqa: F401

from langchain_core.callbacks import CallbackManagerForLLMRun  # noqa: F401  (Typ-Hint der _generate-Signatur)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, PrivateAttr


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


def _normalize_for_match(text: str) -> str:
    """Vergleichstext: klein, Unterstriche/Minus als Leerzeichen, Umlaute normalisiert."""
    lowered = text.lower().replace("_", " ").replace("-", " ")
    for original, replacement in (("ü", "ue"), ("ä", "ae"), ("ö", "oe"), ("ß", "ss")):
        lowered = lowered.replace(original, replacement)
    return lowered


def _tool_name(werkzeug: Any) -> str:
    """Name eines Tools (BaseTool oder schlichte Funktion)."""
    name = getattr(werkzeug, "name", None) or getattr(werkzeug, "__name__", None)
    if not name:
        raise ValueError("Tool ohne Namen an bind_tools uebergeben.")
    return name


def _tool_parameter(werkzeug: Any) -> Dict[str, Dict[str, Any]]:
    """Parameter-Schema als {name: {beschreibung, typ}} (Angaben optional)."""
    args = getattr(werkzeug, "args", None)
    if isinstance(args, dict):
        schema = {}
        for name, info in args.items():
            if isinstance(info, dict):
                schema[name] = {
                    "beschreibung": info.get("description", ""),
                    "typ": info.get("type", ""),
                }
            else:
                schema[name] = {"beschreibung": "", "typ": ""}
        return schema

    import inspect

    schema = {}
    for name, parameter in inspect.signature(werkzeug).parameters.items():
        annotation = parameter.annotation
        typ = "integer" if annotation is int else (
            "number" if annotation is float else (
                "boolean" if annotation is bool else ""))
        schema[name] = {"beschreibung": "", "typ": typ}
    return schema


def _baue_tool_args(werkzeug: Any, user_text: str) -> Dict[str, Any]:
    """Fuellt die Tool-Argumente heuristisch fuer die Offline-Simulation.

    - Rechenausdruecke ('zahl op zahl') fuer Parameter wie expression/rechnung
    - Zahlen aus dem Text fuer int/number-Parameter (min -> erste, max -> letzte)
    - True/False fuer bool-Parameter mit 'ja/nein'-Erkennung
    - sonst: der Nutzettext (uebliche Faelle: query, text, frage, ...)
    """
    args: Dict[str, Any] = {}
    zahlen = re.findall(r"-?\d+(?:\.\d+)?", user_text)
    for name, info in _tool_parameter(werkzeug).items():
        name_klein = name.lower()
        typ = str(info.get("typ", "")).lower()

        if name_klein in ("expression", "rechnung", "formel", "aufgabe"):
            match = re.search(r"-?\d+(?:\.\d+)?\s*[+\-*/]\s*-?\d+(?:\.\d+)?", user_text)
            args[name] = match.group(0) if match else user_text
        elif typ == "integer" or (typ == "number" and not name_klein.startswith("text")):
            if "max" in name_klein or "bis" in name_klein or "ober" in name_klein:
                args[name] = zahlen[-1] if zahlen else 0
            else:
                args[name] = zahlen[0] if zahlen else 0
        elif typ == "boolean":
            args[name] = any(wort in user_text.lower()
                             for wort in ("ja", "true", "wahr", "yes"))
        else:
            args[name] = user_text
    return args


def _finde_passendes_tool(messages: Sequence[BaseMessage], werkzeuge) -> Optional[Any]:
    """Waehlt das Tool, dessen Name im Nutzertext vorkommt."""
    user_text = _normalize_for_match(_extract_last_user_text(messages))
    if not user_text:
        return None
    for werkzeug in werkzeuge:
        name = _normalize_for_match(_tool_name(werkzeug))
        if name and name in user_text:
            return werkzeug
    return None


class MockChatModel(BaseChatModel):
    """Offline-Stand-In fuer ein LangChain-Chat-Modell.

    Verhaelt sich in Chains wie ein echtes Modell, liefert aber
    deterministische, klar markierte Platzhalter-Antworten.

    Zusaetzlich simuliert es einfaches TOOL CALLING:
    - bind_tools(tools) merkt sich die Tools.
    - Enthaelt der Nutzertext einen Tool-Namen, liefert das Modell einen
      passenden tool_call (damit laufen auch Agenten-Loops offline).
    - Liegt bereits ein ToolMessage-Ergebnis vor, wird eine finale
      Antwort formuliert (der Agent-Loop endet).
    """

    _tools: List[Any] = PrivateAttr(default_factory=list)

    @property
    def _llm_type(self) -> str:
        return "lernakademie-offline-model"

    def bind_tools(self, tools: Any, **kwargs: Any) -> "MockChatModel":
        """Merkt sich die Tools fuer die Offline-Tool-Call-Simulation."""
        gebunden = MockChatModel()
        gebunden._tools = list(tools)
        return gebunden

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Any = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Fall 1: Ein Tool hat bereits geliefert -> finale Antwort formulieren
        tool_nachrichten = [m for m in messages if isinstance(m, ToolMessage)]
        if tool_nachrichten:
            inhalt = str(tool_nachrichten[-1].content)
            if len(inhalt) > _MAX_ECHO_CHARS:
                inhalt = inhalt[:_MAX_ECHO_CHARS] + " ..."
            message = AIMessage(
                content=f"{OFFLINE_PREFIX} Finale Antwort auf Basis der "
                f"Tool-Ergebnisse: {inhalt}"
            )
            return ChatResult(generations=[ChatGeneration(message=message)])

        # Fall 2: Tools gebunden und Treffer im Nutzertext -> tool_call simulieren
        if self._tools:
            werkzeug = _finde_passendes_tool(messages, self._tools)
            if werkzeug is not None:
                message = AIMessage(
                    content="",
                    tool_calls=[{
                        "name": _tool_name(werkzeug),
                        "args": _baue_tool_args(werkzeug, _extract_last_user_text(messages)),
                        "id": "tool_call_offline_1",
                        "type": "tool_call",
                    }],
                )
                return ChatResult(generations=[ChatGeneration(message=message)])

        # Fall 3: normale Platzhalter-Antwort
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

                if annotation is bool:
                    fields[name] = False
                elif annotation is int:
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


__all__ = [
    "OFFLINE_PREFIX",
    "MockChatModel",
    "MockMistralClient",
]
