"""Zentrale Konfiguration der Lernakademie – EINE Stelle fuer alle Einstellungen.

Das Wichtigste auf einen Blick (die "Wo/Wie/Welche"-Metapher):

    LLM_BASE_URL  -> WO lebt dein KI-Server?   (z. B. http://localhost:1234/v1)
    LLM_API_KEY   -> WIE darfst du zugreifen?  (optional bei lokalen Servern!)
    LLM_MODEL     -> WELCHES Modell soll antworten? (z. B. mistral-small-latest)

Drei Anbieter-Modi (LLM_PROVIDER), automatisch erkannt, wenn nicht gesetzt:

    mistral            -> Mistral Cloud (Standard-Beispiel der Akademie)
    openai_compatible  -> jeder OpenAI-kompatible Server (Ollama, LM Studio,
                          vLLM, LocalAI, llama.cpp, andere Cloud-Endpoints)
    offline            -> Simulation ohne Kosten und ohne Key (Lern-Modus)

Die Loesungen lesen NIE selbst .env-Werte – sie fragen dieses Modul.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PROVIDER_OFFLINE = "offline"
PROVIDER_MISTRAL = "mistral"
PROVIDER_OPENAI = "openai_compatible"
_GUELTIGE_PROVIDER = {PROVIDER_OFFLINE, PROVIDER_MISTRAL, PROVIDER_OPENAI}

# Mistral-Standardwerte (Convenient-Preset, siehe .env.example)
MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
MISTRAL_MODELL = "mistral-small-latest"


def _env(name: str) -> str:
    return os.environ.get(name, "").strip()


def maske_geheimnis(wert: str) -> str:
    """Zeigt von einem Geheimnis nur die ersten 4 Zeichen – nie mehr."""
    if not wert:
        return ""
    return wert[:4] + "***" if len(wert) > 4 else "***"


def get_provider() -> str:
    """Liefert den aktiven Anbieter (offline | mistral | openai_compatible).

    Reihenfolge:
    1. ACADEMY_OFFLINE=1 erzwingt den Offline-Modus (z. B. fuer Demos/CI).
    2. LLM_PROVIDER explizit gesetzt -> wird geprüft und verwendet.
    3. Automatik: MISTRAL_API_KEY -> mistral; LLM_BASE_URL -> openai_compatible;
       sonst -> offline (Simulation, keine Kosten).
    """
    if _env("ACADEMY_OFFLINE") == "1":
        return PROVIDER_OFFLINE

    gewuenscht = _env("LLM_PROVIDER").lower()
    if gewuenscht:
        if gewuenscht not in _GUELTIGE_PROVIDER:
            raise ValueError(
                f"LLM_PROVIDER='{gewuenscht}' ist ungueltig. Erlaubt: "
                f"{', '.join(sorted(_GUELTIGE_PROVIDER))} (oder leer lassen "
                "fuer automatische Erkennung)."
            )
        return gewuenscht

    if _env("MISTRAL_API_KEY") or _env("LLM_API_KEY"):
        return PROVIDER_MISTRAL
    if _env("LLM_BASE_URL"):
        return PROVIDER_OPENAI
    return PROVIDER_OFFLINE


def is_offline_mode() -> bool:
    return get_provider() == PROVIDER_OFFLINE


def has_mistral_key() -> bool:
    """Abwärtskomfortabel: prüft die Mistral-Variablen (Preset A)."""
    return bool(_env("MISTRAL_API_KEY"))


def get_api_key() -> str:
    """API-Key – darf leer sein (viele lokale Server brauchen keinen!)."""
    if get_provider() == PROVIDER_MISTRAL:
        return _env("LLM_API_KEY") or _env("MISTRAL_API_KEY")
    return _env("LLM_API_KEY")


def get_base_url() -> str:
    """Wo lebt der Server? Muss bei openai_compatible gesetzt sein."""
    provider = get_provider()
    if provider == PROVIDER_MISTRAL:
        return _env("LLM_BASE_URL") or MISTRAL_BASE_URL
    if provider == PROVIDER_OPENAI:
        base_url = _env("LLM_BASE_URL")
        if not base_url:
            raise ValueError(
                "LLM_PROVIDER=openai_compatible benoetigt LLM_BASE_URL "
                "(z. B. http://localhost:1234/v1). Ergaenze es in deiner .env."
            )
        return base_url.rstrip("/")
    return ""  # Offline-Modus: kein echter Server


def get_model_name() -> str:
    """Welches Modell soll antworten? Wird immer durchgereicht – nie hartcodiert."""
    provider = get_provider()
    if provider == PROVIDER_MISTRAL:
        return (_env("LLM_MODEL") or _env("MISTRAL_MODEL")
                or MISTRAL_MODELL)
    if provider == PROVIDER_OPENAI:
        modell = _env("LLM_MODEL")
        if not modell:
            raise ValueError(
                "LLM_PROVIDER=openai_compatible benoetigt LLM_MODEL "
                "(der Modellname, den dein Server meldet – z. B. "
                "'qwen2.5-7b-instruct'). Ergaenze es in deiner .env."
            )
        return modell
    return "offline-simulation"  # Offline-Modus: Modellname ohne Bedeutung


def llm_zusammenfassung() -> dict:
    """Nicht-sensible Konfigurationsübersicht (fuer Status-Anzeigen/Tests).

    Enthaelt NIE den echten Key – nur ob einer konfiguriert ist.
    """
    provider = get_provider()
    base_url = get_base_url() if provider != PROVIDER_OFFLINE else ""
    return {
        "anbieter": provider,
        "base_url": base_url,
        "modell": get_model_name(),
        "api_key": "gesetzt" if get_api_key() else "nicht gesetzt (optional)",
    }
