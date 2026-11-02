"""PyVis-Visualisierung fuer den Graph-Explorer.

Erzeugt interaktives HTML (drag & drop, zoom) aus der API-Antwort.
Bewusst kleine, kommentierte Hilfsbibliothek – kein Lernstoff zum
Selbstschreiben, aber vollstaendig verstaendlich (Stufe 15.3).
"""

from __future__ import annotations

FARBNACH_LABEL = {
    "Person": "#4da6ff",
    "Company": "#ff9f43",
    "Department": "#2ecc71",
    "Project": "#e74c3c",
}


def baue_pyvis_html(nodes: list[dict], edges: list[dict],
                    hoehe: str = "500px") -> str:
    """Baut eine eigenstaendige HTML-Seite mit dem interaktiven Graph."""
    from pyvis.network import Network

    netz = Network(height=hoehe, directed=True, bgcolor="#1a1c23",
                   font_color="white")
    netz.force_atlas_2based(gravity=-50, central_gravity=0.01,
                            spring_length=100, spring_strength=0.08)

    for node in nodes:
        farbe = FARBNACH_LABEL.get(node["label"], "#95a5a6")
        titel = "\n".join(f"{k}: {v}" for k, v in node["properties"].items())
        netz.add_node(node["id"], label=node["name"], title=titel or node["name"],
                      color=farbe, shape="dot", size=18)

    for kante in edges:
        netz.add_edge(kante["von"], kante["zu"], label=kante["typ"],
                      arrows="to", color="#7f8c8d", font={"size": 10})

    # Braucht pyvis >= 0.3: Notebook-/CDN-Modus deaktivieren, damit das HTML
    # in Streamlit-Komponenten laeuft:
    netz.set_options("""
    var options = {
      "interaction": {"hover": true},
      "physics": {"barnesHut": {"gravitationalConstant": -30000}}
    }
    """)
    return netz.generate_html(notebook=False)
