"""Notebook-Baukasten: erzeugt Lern- und Loesungs-Notebooks aus kompakten Specs.

Struktur pro Notebook (Abschnitt 1-3 + Standards des Prompts):
  Willkommen (Titel, Zeit, Schwierigkeit, Voraussetzungen, was gebaut wird)
  Lernziele (beobachtbar/testbar)
  Setup-Zelle (Projektwurzel, zentrale Konfiguration – NIE eigene .env-Leserei)
  Inhalt: md/code-Zellen + "ex"-Einheiten (Aufgabe mit Workspace, Kriterien,
  Checks, Hinweise als <details>, Reflexion)
  Weiter-Verweis am Ende
Loesungs-Notebook: identisch, aber Workspace enthaelt die Loesung + Erklaerung.
"""
from __future__ import annotations

from pathlib import Path

import nbformat as nbf

SETUP_CODE = '''\
import sys
from pathlib import Path

# Projektwurzel finden (dort liegt der Ordner "lernakademie")
ROOT = Path.cwd()
while not (ROOT / "lernakademie").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
if not (ROOT / "lernakademie").exists():
    raise RuntimeError("Projektwurzel nicht gefunden – starte das Notebook im Repo-Ordner.")
sys.path.insert(0, str(ROOT))

from lernakademie.config import llm_zusammenfassung

_info = llm_zusammenfassung()  # zeigt NIE den API-Key selbst
print("KI-Konfiguration:", _info["anbieter"], "| Modell:", _info["modell"],
      "| Key:", _info["api_key"])
if _info["anbieter"] == "offline":
    print("Offline-Modus: alles laeuft – Antworten sind Simulationen ([OFFLINE]).")
'''


def _md(text: str):
    return nbf.v4.new_markdown_cell(text)


def _code(code: str):
    zelle = nbf.v4.new_code_cell(code)
    zelle["execution_count"] = None
    return zelle


def _ex_zellen(ex: dict, loesung: bool) -> list:
    """Baut eine Aufgabeneinheit: Aufgabe -> Workspace -> Kriterien -> Checks -> Hinweise."""
    zellen = [_md(f"## ✏️ Deine Aufgabe: {ex['titel']}\n\n{ex.get('ziel', '')}\n\n"
                  f"**Anforderungen:**")]
    for anforderung in ex.get("anforderungen", []):
        zellen.append(_md(f"- {anforderung}"))
    zellen.append(_md("**Schreibe deinen Code in die folgende Zelle:**"))
    if loesung:
        zellen.append(_code(ex["loesung"]))
        if ex.get("loesung_md"):
            zellen.append(_md(f"**💡 Warum diese Loesung funktioniert:**\n\n{ex['loesung_md']}"))
    else:
        zellen.append(_code(ex["starter"]))
    if ex.get("kriterien"):
        zellen.append(_md("### ✅ Richtig, wenn:"))
        for kriterium in ex["kriterien"]:
            zellen.append(_md(f"- [ ] {kriterium}"))
    if ex.get("checks"):
        zellen.append(_md("**🧪 Fuehre die folgende Zelle aus, um dein Ergebnis zu pruefen:**"))
        zellen.append(_code(ex["checks"]))
    for stufe, hinweis in enumerate(ex.get("hinweise", []), start=1):
        zellen.append(_md(
            f"<details><summary>💡 Hinweis {stufe} (oeffnen, wenn du nicht weiterkommst)</summary>\n\n"
            f"{hinweis}\n</details>"))
    if ex.get("reflexion"):
        zellen.append(_md("## 📝 Reflexion\n\nBeantworte in deinen eigenen Worten:"))
        for frage in ex["reflexion"]:
            zellen.append(_md(f"{frage}"))
    if ex.get("challenge"):
        challenge_md, challenge_code = ex["challenge"]
        zellen.append(_md(f"## 🧩 Challenge (freiwillig)\n\n{challenge_md}"))
        zellen.append(_code(challenge_code))
    return zellen


def baue_notebook(spec: dict, loesung: bool) -> object:
    """Erzeugt ein nbformat-Notebook aus einer Spec."""
    zellen = []

    # --- Abschnitt 1: Willkommen ------------------------------------------
    zellen.append(_md(
        f"# {spec['titel']}\n\n{spec.get('begruessung', '')}\n\n"
        f"| | |\n|---|---|\n"
        f"| **Zeit** | {spec['zeit']} |\n"
        f"| **Schwierigkeit** | {spec['schwierigkeit']} |\n"
        f"| **Voraussetzungen** | {spec['voraussetzungen']} |\n"
        f"| **Du baust** | {spec['baut']} |"))

    # --- Abschnitt 2: Lernziele -------------------------------------------
    zellen.append(_md("## 🎯 Nach dieser Lektion kannst du:"))
    for ziel in spec["ziele"]:
        zellen.append(_md(f"- {ziel}"))

    # --- Setup (zentrale Konfiguration, fresh-kernel-faehig) ---------------
    zellen.append(_md(
        "## ⚙️ Setup – einmal pro Notebook ausführen\n\n"
        "Diese Zelle findet die Projektwurzel und lädt die **zentrale KI-Konfiguration** "
        "aus deiner `.env` (siehe `docs/local-ai-server.md`). Du musst nie Notebook-Code "
        "ändern, um den Anbieter zu wechseln."))
    zellen.append(_code(SETUP_CODE))

    # --- Inhalt ------------------------------------------------------------
    for eintrag in spec["cells"]:
        if eintrag[0] == "md":
            zellen.append(_md(eintrag[1]))
        elif eintrag[0] == "code":
            zelle = _code(eintrag[1])
            if len(eintrag) > 2:
                zelle["outputs"] = []
            zellen.append(zelle)
        elif eintrag[0] == "ex":
            zellen.extend(_ex_zellen(eintrag[1], loesung))
        else:
            raise ValueError(f"Unbekannter Zelltyp: {eintrag[0]}")

    # --- Weiter -------------------------------------------------------------
    if spec.get("weiter"):
        zellen.append(_md(f"## ➡️ Weiter\n\n{spec['weiter']}"))

    nb = nbf.v4.new_notebook(cells=zellen)
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    }
    return nb


def schreibe_notebooks(spec: dict, projekt: Path, mit_ausfuehrung: bool = True) -> None:
    """Schreibt Lern-Notebook (ohne Outputs) + Loesungs-Notebook (mit Outputs)."""
    import nbclient

    lern_pfad = projekt / spec["pfad"]
    lern_pfad.parent.mkdir(parents=True, exist_ok=True)
    nb_lern = baue_notebook(spec, loesung=False)
    if spec.get("fuehre_lernnotebook_aus") and mit_ausfuehrung:
        import nbclient
        nbclient.NotebookClient(nb_lern, timeout=300, kernel_name="python3",
                                resources={"metadata": {"path": str(projekt)}}
                                ).execute()
    nbf.write(nb_lern, str(lern_pfad))
    print("geschrieben:", lern_pfad)

    if not spec.get("hat_loesung", True):
        return

    loesungs_pfad = projekt / "solutions" / (
        Path(spec["pfad"]).stem + "_loesung.ipynb")
    loesungs_pfad.parent.mkdir(parents=True, exist_ok=True)
    nb = baue_notebook(spec, loesung=True)
    if mit_ausfuehrung:
        # Loesungs-Notebook einmal komplett ausfuehren -> erwartete Outputs
        # bleiben fuer Lernende sichtbar (ehrlich: offline simuliert bzw.
        # mit der konfigurierten KI):
        nbclient.NotebookClient(nb, timeout=300, kernel_name="python3",
                                resources={"metadata": {"path": str(projekt)}}
                                ).execute()
    nbf.write(nb, str(loesungs_pfad))
    print("geschrieben:", loesungs_pfad, "(ausgefuehrt)" if mit_ausfuehrung else "")
