"""Gemeinsame API-Konfiguration fuer alle Frontend-Seiten.

API_URL ist ueberschreibbar (Docker: http://backend:8000) – ein kleines
Beispiel dafuer, dass das Frontend austauschbar/umgebungsfaehig bleibt.
"""

import os

API_URL = os.environ.get("API_URL", "http://localhost:8000")
