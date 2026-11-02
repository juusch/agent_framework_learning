"""Aufgabe 9.2 – Loesung: Logging, Tracing, Key-Maskierung, Kostenschaetzung.

Betreiber-Grundlagen in einer Datei:
- strukturiertes Logging mit Zeitstempel
- @verfolge-Decorator -> sichtbarer Trace mit Dauer je Funktion
- maske_geheimnisse() -> Keys/Token werden zu ***
- schaetze_kosten() -> Budget-Bewusstsein
"""

import functools
import logging
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.mock_llm import is_offline_mode

LOGGING_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"

# Grundstein fuer Geheimnis-Sicherheit: alles Token-aehnliche maskieren
_GEHEIMNIS_MUSTER = re.compile(r"([A-Za-z0-9_-]{8}[A-Za-z0-9_-]{8,})")


def maske_geheimnisse(text: str) -> str:
    """Maskiert Token/Key-artige Strings (>= 16 Zeichen ohne Leerzeichen)."""
    return _GEHEIMNIS_MUSTER.sub("***", text)


def richte_logging_ein() -> logging.Logger:
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
    return logging.getLogger("lernakademie.pipeline")


def verfolge(funktion):
    """Decorator: protokolliert Start/Ende/Dauer -> Trace in der Konsole."""
    logger = logging.getLogger(f"lernakademie.trace.{funktion.__name__}")

    @functools.wraps(funktion)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        logger.info("START %s", funktion.__name__)
        try:
            ergebnis = funktion(*args, **kwargs)
        except Exception as fehler:
            # Fehler protokollieren, aber KEINE Geheimnisse durchsickern lassen:
            logger.error("FEHLER %s: %s", funktion.__name__,
                          maske_geheimnisse(str(fehler)))
            raise
        dauer_ms = (time.perf_counter() - start) * 1000
        logger.info("ENDE  %s (%.1f ms)", funktion.__name__, dauer_ms)
        return ergebnis

    return wrapper


def schaetze_kosten(zeichen_input: int, zeichen_output: int,
                    preis_pro_1k_tokens: float = 0.001) -> float:
    """Faustregel aus Stufe 2: 4 Zeichen ~= 1 Token."""
    tokens = (zeichen_input + zeichen_output) / 4
    return tokens / 1000 * preis_pro_1k_tokens


# ---------------- Demo-Pipeline --------------------------------------------


@verfolge
def schritt_laden(text: str) -> str:
    time.sleep(0.01)
    return text


@verfolge
def schritt_verarbeiten(text: str) -> str:
    time.sleep(0.02)
    return text.upper()


@verfolge
def schritt_antworten(text: str) -> str:
    time.sleep(0.01)
    return f"Antwort auf Basis von: {text}"


def main() -> None:
    logger = richte_logging_ein()
    if is_offline_mode():
        logger.info("OFFLINE-Modus: Demo laeuft ohne API-Kosten")

    # 1) Trace einer Mini-Pipeline
    ergebnis = schritt_antworten(schritt_verarbeiten(schritt_laden("hallo welt")))
    print("\nErgebnis:", ergebnis)

    # 2) Geheimnis-Maskierung (der Klassiker: versehentlich geloggter Key)
    Gefaehrliche_Log_Zeile = "Nutzer hat key_a1b2c3d4e5f6g7h8i9j0 eingegeben"
    maskiert = maske_geheimnisse(Gefaehrliche_Log_Zeile)
    assert "***" in maskiert and "a1b2c3d4" not in maskiert
    print("Maskiert:", maskiert)

    # 3) Kostenschaetzung: drei Szenarien (1000 Zeichen in, 500 out je Frage)
    for name, fragen in (("1 Frage", 1), ("100 Fragen", 100),
                         ("Loop ohne Limit (!)", 100)):
        kosten = schaetze_kosten(fragen * 1000, fragen * 500)
        print(f"{name}: ~{kosten:.3f} EUR")
    print("\nErkenntnis: 1 Frage kostet Cent-Bruchteile – ein UNBEGRENZTER "
          "Loop multipliziert das mit jedem Durchgang. Deshalb: max_runden!")


if __name__ == "__main__":
    main()
