"""Der LLM-Provider-Layer der Lernakademie.

EINE Anlaufstelle fuer alle Anwendungen:

    .env / Umgebung
        -> lernakademie.config (zentrale Konfiguration)
            -> lernakademie.llm_client (dieses Modul)
                -> ChatMistralAI | ChatOpenAI (OpenAI-kompatibel) | MockChatModel
                    -> LangChain / LangGraph / Aufgaben / Frontend

Die Aufgaben rufen NUR get_chat_model() bzw. get_api_client() auf –
ob dahinter Mistral Cloud, ein lokaler Server (z. B. LM Studio, Ollama,
vLLM, LocalAI, llama.cpp) oder die Offline-Simulation steckt, entscheidet
ausschliesslich die .env. Keine Aufgabe liest selbst Umgebungsvariablen.
"""

from __future__ import annotations

from typing import Any

from lernakademie import config
from lernakademie.config import (  # Re-Exports: ein Import fuer die Aufgaben
    PROVIDER_MISTRAL, PROVIDER_OFFLINE, PROVIDER_OPENAI, get_model_name,
    is_offline_mode, llm_zusammenfassung, maske_geheimnis,
)
from lernakademie.mock_llm import OFFLINE_PREFIX, MockChatModel, MockMistralClient

_DUMMY_KEY = "not-required"  # manche Clients verlangen einen nicht-leeren Key


def get_chat_model(temperature: float = 0.7) -> Any:
    """Liefert das konfigurierte LangChain-Chat-Modell.

    - Offline-Modus: MockChatModel (Simulation, keine Kosten)
    - mistral: ChatMistralAI (offizielle Mistral-Integration)
    - openai_compatible: ChatOpenAI mit eigener Base-URL
      (jeder Server, der die OpenAI-kompatible API anbietet)
    """
    provider = config.get_provider()
    modell = config.get_model_name()

    if provider == PROVIDER_OFFLINE:
        return MockChatModel()

    if provider == PROVIDER_MISTRAL:
        from langchain_mistralai import ChatMistralAI

        key = config.get_api_key()
        if not key:
            raise ValueError(
                "LLM_PROVIDER=mistral benoetigt einen API-Key "
                "(MISTRAL_API_KEY oder LLM_API_KEY) in deiner .env."
            )
        return ChatMistralAI(model=modell, api_key=key, temperature=temperature)

    # openai_compatible – Key ist optional (lokale Server brauchen oft keinen)
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=modell,
        base_url=config.get_base_url(),
        api_key=config.get_api_key() or _DUMMY_KEY,
        temperature=temperature,
    )


# ---------------------------------------------------------------------------
# Direkter API-Client (fuer Build 1 / Modul 1: OHNE LangChain)
# ---------------------------------------------------------------------------


class OpenAICompatClient:
    """Minimal-Client fuer OpenAI-kompatible Server (reines requests).

    Gleiche schlanke Schnittstelle wie der Mistral-SDK-Client:
        client.chat.complete(model=..., messages=[...]) -> response
        response.choices[0].message.content -> Antworttext
    """

    def __init__(self, base_url: str, api_key: str, timeout: int = 60) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout
        self.chat = self._Chat(self)

    class _Chat:
        def __init__(self, client: "OpenAICompatClient") -> None:
            self._client = client

        def complete(self, model: str, messages: list[dict],
                     temperature: float = 0.0, **_: Any) -> Any:
            import requests

            header = {"Content-Type": "application/json"}
            if self._client._api_key:
                header["Authorization"] = f"Bearer {self._client._api_key}"
            antwort = requests.post(
                f"{self._client._base_url}/chat/completions",
                headers=header,
                json={"model": model, "messages": messages,
                      "temperature": temperature},
                timeout=self._client._timeout,
            )
            if antwort.status_code == 404:
                raise ConnectionError(
                    f"Endpunkt nicht gefunden: {self._client._base_url}/chat/completions "
                    "– pruefe LLM_BASE_URL (meist mit /v1 am Ende)."
                )
            if antwort.status_code in (401, 403):
                raise ConnectionError(
                    "Zugriff verweigert (401/403) – pruefe LLM_API_KEY."
                )
            antwort.raise_for_status()
            daten = antwort.json()
            # OpenAI-Format in die schlanke SDK-Form bringen:
            class _Nachricht:
                def __init__(self, content: str) -> None:
                    self.content = content

            class _Wahl:
                def __init__(self, content: str) -> None:
                    self.message = _Nachricht(content)

            class _Antwort:
                def __init__(self, content: str) -> None:
                    self.choices = [_Wahl(content)]

            return _Antwort(daten["choices"][0]["message"]["content"])


def get_api_client() -> Any:
    """Direkter Client ohne LangChain – provider-unabhaengig.

    - offline: MockMistralClient (Simulation)
    - mistral: offizieller Mistral-SDK-Client
    - openai_compatible: OpenAICompatClient (reines requests)
    """
    provider = config.get_provider()
    if provider == PROVIDER_OFFLINE:
        return MockMistralClient()
    if provider == PROVIDER_MISTRAL:
        from mistralai import Mistral

        key = config.get_api_key()
        if not key:
            raise ValueError(
                "LLM_PROVIDER=mistral benoetigt einen API-Key "
                "(MISTRAL_API_KEY oder LLM_API_KEY) in deiner .env."
            )
        return Mistral(api_key=key)
    return OpenAICompatClient(config.get_base_url(), config.get_api_key())


def sende_nachricht(messages: list[dict], temperature: float = 0.0) -> str:
    """Bequemlichkeit: kompletter direkter Aufruf -> Antworttext."""
    client = get_api_client()
    antwort = client.chat.complete(
        model=config.get_model_name(), messages=messages,
        temperature=temperature)
    return antwort.choices[0].message.content
