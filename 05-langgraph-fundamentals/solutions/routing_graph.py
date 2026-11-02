"""Aufgabe 5.3 – Referenzloesung: konditionales Routing (Support-Router).

Trennung der Verantwortlichkeiten:
- klassifizieren  = schreibende Station (Regel-Logik)
- weiche          = lesende Funktion (entscheidet nur)
- antwort_*       = drei Fachstellen
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class TicketZustand(TypedDict):
    eingabe: str
    kategorie: str
    antwort: str


def klassifizieren(state: TicketZustand) -> dict:
    """Regel-Logik (Stufe-2-Wissen): Kategorie aus dem Text ableiten."""
    text = state["eingabe"].lower()
    if "rechnung" in text or "betrag" in text:
        kategorie = "rechnung"
    elif any(wort in text for wort in ("funktioniert", "fehler", "absturz")):
        kategorie = "technisch"
    else:
        kategorie = "allgemein"
    return {"kategorie": kategorie}


def weiche(state: TicketZustand) -> str:
    """Fahrdienstleiter: liest nur und nennt den Namen des naechsten Nodes."""
    return state["kategorie"]


def antwort_rechnung(state: TicketZustand) -> dict:
    return {"antwort": "Ihre Anfrage geht an die Buchhaltung. "
                      "Rechnungen werden innerhalb von 5 Werktagen geprueft."}


def antwort_technisch(state: TicketZustand) -> dict:
    return {"antwort": "Unser Technik-Team nimmt sich dem Problem an. "
                      "Bitte nennen Sie Geraet und Fehlermeldung."}


def antwort_allgemein(state: TicketZustand) -> dict:
    return {"antwort": "Vielen Dank! Unser allgemeines Team "
                      "beantwortet Ihre Frage in Kuerze."}


def baue_graph():
    graph = StateGraph(TicketZustand)
    graph.add_node("klassifizieren", klassifizieren)
    graph.add_node("antwort_rechnung", antwort_rechnung)
    graph.add_node("antwort_technisch", antwort_technisch)
    graph.add_node("antwort_allgemein", antwort_allgemein)

    graph.add_edge(START, "klassifizieren")
    graph.add_conditional_edges(
        "klassifizieren",          # von diesem Node...
        weiche,                    # ...entscheidet diese Funktion...
        {                          # ...ueber dieses Mapping:
            "rechnung": "antwort_rechnung",
            "technisch": "antwort_technisch",
            "allgemein": "antwort_allgemein",
        },
    )
    for node in ("antwort_rechnung", "antwort_technisch", "antwort_allgemein"):
        graph.add_edge(node, END)
    return graph.compile()


def main() -> None:
    app = baue_graph()
    eingaben = [
        "Meine letzte Rechnung enthaelt einen falschen Betrag.",
        "Die App funktioniert seit heute nicht mehr und stuerzt ab.",
        "Wo kann ich meine Arbeitszeiten einsehen?",
    ]
    for eingabe in eingaben:
        ergebnis = app.invoke({"eingabe": eingabe, "kategorie": "", "antwort": ""})
        print(f"Eingabe : {eingabe}")
        print(f"Kategorie: {ergebnis['kategorie']}")
        print(f"Antwort : {ergebnis['antwort']}\n")


if __name__ == "__main__":
    main()
