# 🏛️ Architektur der Lernakademie

Diese Seite erklärt, **wie das Repository aufgebaut ist** und wie die technischen Bausteine zusammenwirken – auch für spätere Erweiterungen (Stufe 5–9).

## Verzeichnisstruktur

```
lernakademie/
├── README.md            # Einstiegsseite
├── START_HERE.md         # Gefuehrte Erstinstallation
├── PROGRESS.md           # Fortschritts-Tracker des Lernenden
├── requirements.txt      # Gepinnte Abhaengigkeiten
├── pyproject.toml        # Projekt-Metadaten + pytest-Konfiguration
├── .env.example          # Vorlage fuer Geheimnisse (die echte .env wird nie committet)
│
├── docs/                 # Referenz-Dokumentation
│
├── lernakademie/          # Gemeinsames Hilfs-Paket (s.u.)
│   └── tests/             # Automatische Tests des Hilfs-Pakets
│
├── 00-getting-started/    # Jede Lernstufe folgt demselben Muster:
│   ├── README.md          #   Einfuehrung + Aufgabenuebersicht
│   ├── tasks/             #   Aufgabenbeschreibungen (16-Sektionen-Template)
│   ├── solutions/         #   vollstaendige, lauffaehige Referenzloesungen
│   └── examples/          #   kleine Demo-Skripte zum Ausprobieren
│
├── 01-python-fundamentals/
├── 02-understanding-llms/
├── 03-langchain-fundamentals/
└── 04-rag-and-knowledge/
    └── data/              # Uebungsdokumente (frei erfunden)
```

## Das Hilfs-Paket `lernakademie/`

Damit jede Loesung mit **und ohne** Mistral-API-Key laeuft, gibt es einen zentralen Schalter:

- `lernakademie/config.py`
  - laedt die `.env` (via `python-dotenv`),
  - entscheidet: echter Modus (Key vorhanden, nicht offline erzwungen) oder Offline-Modus.
- `lernakademie/mock_llm.py`
  - ein simuliertes Chat-Modell, das sich in Chains exakt wie ein echtes verhält (gleiche Schnittstelle), aber deterministische, klar mit `[OFFLINE]` markierte Antworten erzeugt. So koennen Lernende **kostenlos und ohne Anmeldung** alle Konzepte ueben und die Automatisierten Tests laufen ohne Credentials in CI.
- `lernakademie/offline_embeddings.py`
  - ein transparentes, schluesselwort-basiertes Embedding-Modell fuer die RAG-Stufe: Es erkennt definierte Schluesselwoerter und bildet daraus Vektoren. Es ist absichtlich simpel, damit Lernende **sehen**, was Embeddings tun – echte Embeddings von Mistral werden im Text erklaert und per Key automatisch verwendet.

### Warum dieses Design?

1. **Lernqualitaet:** Konzepte (Chains, Retrieval) lassen sich ohne Kosten-Sorge erforschen; der Wechsel zum echten Modell ist nur eine Zeile in `.env`.
2. **Testbarkeit:** Alle Tests (`pytest`) laufen ohne Netzwerk und ohne Geheimnisse – Voraussetzung fuer die GitHub-Actions-CI.
3. **Kein Leaking:** API-Keys liegen nur in der nicht versionierten `.env`.

## Versionsstrategie

Wir pinnen Hauptversionen (`langchain>=1.0,<2.0` u.s.w.), weil das LangChain-Ökosystem sich schnell bewegt. Upgrades werden dokumentiert, indem man die Range in `requirements.txt` anpasst und `pytest` laufen laesst.

## Geplante Erweiterungen (Stufen 5–9)

Neue Stufenordner (`05-langgraph-fundamentals/` … `09-production/`) folgen exakt demselben Muster (README + tasks + solutions + examples). LangGraph-bezogene Aufgaben erhalten zusaetzlich einen `diagrams/`-Ordner mit Mermaid-Diagrammen, die der Code- erklaerung vorausgehen.
