"""Zentrale Konfiguration der Lernakademie.

Entscheidet, ob Loesungen im OFFLINE-Modus (simuliertes Modell,
keine Kosten, kein Key noetig) oder im echten Mistral-Modus laufen.

Regel:
- ACADEMY_OFFLINE=1 in .env erzwingt den Offline-Modus.
- Sonst: echten Modus verwenden, wenn MISTRAL_API_KEY gesetzt ist.
- Sonst: Offline-Modus.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def has_mistral_key() -> bool:
    """True, wenn ein Mistral-API-Key in den Umgebungsvariablen liegt."""
    return bool(os.environ.get("MISTRAL_API_KEY", "").strip())


def is_offline_mode() -> bool:
    """True, wenn die Loesungen ohne echte API-Aufrufe laufen sollen."""
    if os.environ.get("ACADEMY_OFFLINE", "").strip() == "1":
        return True
    return not has_mistral_key()


def get_model_name() -> str:
    """Liefert den konfigurierten Mistral-Modellnamen (Standard: mistral-small-latest)."""
    return os.environ.get("ACADEMY_MODEL", "mistral-small-latest").strip() or "mistral-small-latest"
