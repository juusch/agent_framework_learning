"""Sitzungsverwaltung: Verlauf pro Session im Backend.

Genauso wie der Chatbot in Stufe 2.4 seinen Verlauf als Liste gepflegt
hat, tut das der Server hier – nur fuer mehrere Sessions gleichzeitig.
"""

from __future__ import annotations

from threading import Lock
from typing import Any, Dict, List

_LOCK = Lock()
_SESSIONS: Dict[str, List[Dict[str, Any]]] = {}
_MAX_EINTRAEGE = 100


def verlauf_holen(session_id: str) -> List[Dict[str, Any]]:
    with _LOCK:
        return list(_SESSIONS.get(session_id, []))


def verlauf_anhaengen(session_id: str, eintrag: Dict[str, Any]) -> None:
    with _LOCK:
        eintraege = _SESSIONS.setdefault(session_id, [])
        eintraege.append(eintrag)
        if len(eintraege) > _MAX_EINTRAEGE:  # Budget-Kontrolle (Stufe 2.4)
            del eintraege[: len(eintraege) - _MAX_EINTRAEGE]
