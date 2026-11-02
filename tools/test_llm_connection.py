"""AI-Verbindungstest – prueft deine .env in 10 Sekunden.

Aufruf (im Akademie-Hauptordner):
    python -m tools.test_llm_connection

Der Test:
  1. laedt die zentrale Konfiguration,
  2. zeigt Anbieter, Server-URL, Modell und Key-Status (NIE den Key selbst!),
  3. sendet eine minimale Testanfrage,
  4. druckt bei Fehlern konkrete Loesungshinweise.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lernakademie import config
from lernakademie.llm_client import get_api_client

ANBIETER_NAME = {
    "mistral": "Mistral Cloud",
    "openai_compatible": "OpenAI-kompatibler Server",
    "offline": "Offline-Modus (Simulation)",
}


def main() -> None:
    print("AI-Verbindungstest")
    print("------------------")
    try:
        info = config.llm_zusammenfassung()
    except ValueError as fehler:
        print(f"\n✗ Konfigurationsfehler:\n  {fehler}")
        print("\nHinweis: Pruefe deine .env – Vorlage: .env.example")
        return

    print(f"Anbieter: {ANBIETER_NAME.get(info['anbieter'], info['anbieter'])}")
    print(f"Server:   {info['base_url'] or '(kein echter Server – Offline-Modus)'}")
    print(f"Modell:   {info['modell']}")
    print(f"API-Key:  {info['api_key']}")
    print("\nVerbinde...")

    try:
        client = get_api_client()
        antwort = client.chat.complete(
            model=config.get_model_name(),
            messages=[{"role": "user",
                       "content": "Antworte ausschliesslich mit dem Wort: OK"}],
            temperature=0.0,
        )
        text = antwort.choices[0].message.content
    except ValueError as fehler:
        print(f"\n✗ Konfigurationsfehler:\n  {fehler}")
        return
    except Exception as fehler:
        print(f"\n✗ Verbindung fehlgeschlagen: {fehler}")
        print("\nHaeufige Ursachen (der Reihe nach pruefen):")
        print("  1. Laeuft dein AI-Server? (z. B. LM Studio/Ollama starten)")
        print("  2. Stimmt LLM_BASE_URL? Meist mit /v1 am Ende,")
        print("     z. B. http://localhost:1234/v1 – pruefe die Doku deines Servers.")
        print("  3. Stimmt LLM_MODEL? Der Name muss exakt dem Server-matchen")
        print("     (z. B. 'qwen2.5-7b-instruct', nicht 'Qwen').")
        print("  4. Bei 401/403: braucht der Server einen Key? Dann LLM_API_KEY setzen.")
        print("  5. Ohne Key/Server: .env leer lassen -> Offline-Modus (alles lauffaehig).")
        print("\nDetails: docs/local-ai-server.md und docs/troubleshooting.md")
        return

    print("✓ Verbindung erfolgreich!")
    print(f"✓ Modell hat geantwortet (Antwort: {text.strip()[:40]})")
    if config.is_offline_mode():
        print("\nHinweis: Du befindest dich im OFFLINE-Modus – die Antwort ist eine")
        print("Simulation. Fuer echte Antworten: Mistral-Key ODER lokalen")
        print("Server in .env konfigurieren (siehe .env.example).")
    print("\nDu bist bereit, weiterzumachen. 🚀")


if __name__ == "__main__":
    main()
