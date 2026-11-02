"""Tests fuer die zentrale LLM-Konfiguration und den Provider-Layer.

Alle Tests laufen OHNE echten Server – offline bzw. mit gemockten
Verbindungen (CI-faehig).
"""

import os

import pytest

# Sicherstellen, dass keine echte .env die Tests verfaelscht:
_RELEVANT = ["LLM_PROVIDER", "LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL",
             "MISTRAL_API_KEY", "MISTRAL_MODEL", "ACADEMY_OFFLINE",
             "EMBEDDINGS", "EMBEDDINGS_MODEL"]


@pytest.fixture(autouse=True)
def saubere_env(monkeypatch):
    for name in _RELEVANT:
        monkeypatch.delenv(name, raising=False)
    yield


def test_auto_erkennung_offline():
    from lernakademie import config

    assert config.get_provider() == config.PROVIDER_OFFLINE
    assert config.is_offline_mode() is True
    assert config.llm_zusammenfassung()["api_key"] == "nicht gesetzt (optional)"


def test_auto_erkennung_mistral(monkeypatch):
    from lernakademie import config

    monkeypatch.setenv("MISTRAL_API_KEY", "test-key-12345678")
    assert config.get_provider() == config.PROVIDER_MISTRAL
    assert config.get_base_url() == "https://api.mistral.ai/v1"
    assert config.get_model_name() == "mistral-small-latest"  # Standard


def test_auto_erkennung_openai_compatible(monkeypatch):
    from lernakademie import config

    monkeypatch.setenv("LLM_BASE_URL", "http://localhost:1234/v1")
    monkeypatch.setenv("LLM_MODEL", "qwen2.5-7b-instruct")
    assert config.get_provider() == config.PROVIDER_OPENAI
    assert config.get_base_url() == "http://localhost:1234/v1"
    assert config.get_model_name() == "qwen2.5-7b-instruct"
    assert config.get_api_key() == ""  # Key optional!


def test_mistral_preset_modell(monkeypatch):
    from lernakademie import config

    monkeypatch.setenv("MISTRAL_API_KEY", "k")
    monkeypatch.setenv("MISTRAL_MODEL", "mistral-medium-latest")
    assert config.get_model_name() == "mistral-medium-latest"


def test_openai_compatible_ohne_base_url_fehler(monkeypatch):
    from lernakademie import config

    monkeypatch.setenv("LLM_PROVIDER", "openai_compatible")
    with pytest.raises(ValueError, match="LLM_BASE_URL"):
        config.get_base_url()


def test_openai_compatible_ohne_modell_fehler(monkeypatch):
    from lernakademie import config

    monkeypatch.setenv("LLM_PROVIDER", "openai_compatible")
    monkeypatch.setenv("LLM_BASE_URL", "http://localhost:1234/v1")
    with pytest.raises(ValueError, match="LLM_MODEL"):
        config.get_model_name()


def test_mistral_explicit_ohne_key_fehler(monkeypatch):
    """Explizit mistral ohne Key -> klarer Fehler (statt Absturz irgendwo)."""
    from lernakademie.llm_client import get_chat_model

    monkeypatch.setenv("LLM_PROVIDER", "mistral")
    with pytest.raises(ValueError, match="API-Key"):
        get_chat_model()


def test_ungueltiger_provider_fehler(monkeypatch):
    from lernakademie import config

    monkeypatch.setenv("LLM_PROVIDER", "gibtsnicht")
    with pytest.raises(ValueError, match="ungueltig"):
        config.get_provider()


def test_offline_erzwungen_trotz_key(monkeypatch):
    from lernakademie import config

    monkeypatch.setenv("MISTRAL_API_KEY", "echter-key")
    monkeypatch.setenv("ACADEMY_OFFLINE", "1")
    assert config.get_provider() == config.PROVIDER_OFFLINE


def test_geheimnis_maskierung():
    from lernakademie.config import maske_geheimnis

    assert maske_geheimnis("abcdefghijklmnop") == "abcd***"
    assert maske_geheimnis("kurz") == "***"
    assert maske_geheimnis("") == ""
    # Niemals der komplette Key:
    assert "abcdefghijklmnop" not in maske_geheimnis("abcdefghijklmnop")


def test_zusammenfassung_ohne_secrets(monkeypatch):
    from lernakademie import config

    monkeypatch.setenv("MISTRAL_API_KEY", "super-geheimer-key-987654321")
    info = config.llm_zusammenfassung()
    assert "super-geheimer-key" not in str(info)
    assert info["api_key"] == "gesetzt"


def test_chat_model_offline_ist_mock():
    from lernakademie.llm_client import get_chat_model
    from lernakademie.mock_llm import MockChatModel

    assert isinstance(get_chat_model(), MockChatModel)


def test_chat_model_openai_compatible(monkeypatch):
    """ChatOpenAI mit konfigurierter Base-URL (kein echter Call!)."""
    from langchain_openai import ChatOpenAI

    from lernakademie.llm_client import get_chat_model

    monkeypatch.setenv("LLM_PROVIDER", "openai_compatible")
    monkeypatch.setenv("LLM_BASE_URL", "http://localhost:9999/v1")
    monkeypatch.setenv("LLM_MODEL", "mini-modell")
    modell = get_chat_model(temperature=0.2)
    assert isinstance(modell, ChatOpenAI)
    assert modell.model_name == "mini-modell"
    assert str(modell.openai_api_base).endswith("localhost:9999/v1")
    # Ohne Key kein Crash – Dummy-Key wird intern gesetzt:
    assert modell.openai_api_key is not None


def test_api_client_offline_ist_simulation():
    from lernakademie.llm_client import get_api_client
    from lernakademie.mock_llm import MockMistralClient

    client = get_api_client()
    assert isinstance(client, MockMistralClient)
    antwort = client.chat.complete(model="x",
                                   messages=[{"role": "user", "content": "hi"}])
    assert antwort.choices[0].message.content


def test_verbindungstest_offline_erfolgreich(capsys):
    """Der Verbindungstest laeuft im Offline-Modus mit klarer Ausgabe."""
    from tools import test_llm_connection

    test_llm_connection.main()
    ausgabe = capsys.readouterr().out
    assert "Offline-Modus" in ausgabe
    assert "Verbindung erfolgreich" in ausgabe
    assert "API-Key" in ausgabe


def test_verbindungstest_fehler_mit_hinweisen(monkeypatch, capsys):
    """Bei nicht erreichbarem Server: konkrete Troubleshooting-Schritte."""
    from tools import test_llm_connection

    monkeypatch.setenv("LLM_PROVIDER", "openai_compatible")
    monkeypatch.setenv("LLM_BASE_URL", "http://localhost:59999/v1")
    monkeypatch.setenv("LLM_MODEL", "testmodell")
    test_llm_connection.main()
    ausgabe = capsys.readouterr().out
    assert "fehlgeschlagen" in ausgabe
    assert "LLM_BASE_URL" in ausgabe  # Loesungshinweis vorhanden
