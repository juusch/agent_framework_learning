"""Beispiel fuer Aufgabe 2.2: Wie viele TOKENS hat ein Text ungefaehr?

LLMs lesen und rechnen nicht in Buchstaben oder Worten, sondern in Tokens
(kleine Textstuecke, oft 3-4 Zeichen). Faustregel fuer Deutsch:
1 Token ~= 3.5-4 Zeichen bzw. 1000 Woerter ~= 1300-1800 Tokens.

Wichtig zu verstehen:
- Das Kontextfenster (wie viel das Modell auf einmal lesen kann) wird in
  Tokens gemessen.
- Die Kosten werden pro Token berechnet.
- Eine grobe Schaetzung kennst du ab sofort aus dem Handgelenk.
"""


def schaetze_tokens(text: str) -> int:
    """Grobe Schaetzung: Laenge in Zeichen / 4."""
    return max(1, len(text) // 4)


def main() -> None:
    beispiele = [
        "Hallo Welt",
        "Erkläre in zwei Saetzen, was eine API ist.",
        "Python ist eine vielseitige Programmiersprache, die besonders "
        "fuer Einsteiger gut geeignet ist, weil sie wie Englisch liest "
        "und viele Fehler freundlich meldet.",
    ]
    for text in beispiele:
        print(f"{schaetze_tokens(text):4d} Tokens | {text[:60]}")


if __name__ == "__main__":
    main()
