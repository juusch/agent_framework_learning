"""Beispiel fuer Aufgabe 1.3: zeigt, dass Pakete in der venv installiert sind."""

import importlib.metadata as md

from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Installierte Pakete in deiner Umgebung")
table.add_column("Paket")
table.add_column("Version", justify="right")

for paket in ["langchain", "langchain-core", "langgraph", "rich"]:
    try:
        table.add_row(paket, md.version(paket))
    except Exception:
        table.add_row(paket, "NICHT INSTALLIERT")

console.print(table)
console.print(
    "[green]Alles bereit![/green] Wenn hier Versionen stehen, "
    "laeuft deine virtuelle Umgebung korrekt."
)
