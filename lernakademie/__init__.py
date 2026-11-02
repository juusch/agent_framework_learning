"""Gemeinsames Hilfs-Paket der Lernakademie.

Stellt den Offline-/Echt-Modus bereit, damit alle Loesungen
mit und ohne MISTRAL_API_KEY lauffaehig sind.
"""

from lernakademie.config import is_offline_mode, has_mistral_key, get_model_name

__all__ = ["is_offline_mode", "has_mistral_key", "get_model_name"]
