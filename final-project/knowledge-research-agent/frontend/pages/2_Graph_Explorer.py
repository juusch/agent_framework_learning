"""Knowledge-Graph-Explorer: interaktive Visualisierung mit PyVis.

Fertig gelieferter Code (Stufe 15-Konzept): Die Visualisierung ist
Werkzeug – verstanden wird sie in Aufgabe 15.3 und Stufe 10.4.
"""

import sys
from pathlib import Path

import requests
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from components.graph_viz import baue_pyvis_html  # noqa: E402

from api_config import API_URL

st.title("🕸️ Knowledge-Graph-Explorer")
st.caption("Nodes anklicken und ziehen; Auswahl unten zeigt Properties "
           "und Nachbarn.")

antwort = requests.get(f"{API_URL}/graph", timeout=10)
if antwort.status_code != 200:
    st.error("Backend nicht erreichbar.")
    st.stop()

graph = antwort.json()

# ---- Interaktive Visualisierung (PyVis -> HTML-Embed) ----------------------
html = baue_pyvis_html(graph["nodes"], graph["edges"])
st.components.v1.html(html, height=520, scrolling=False)

# ---- Suche + Detail-Ansicht ------------------------------------------------
st.subheader("Entity-Suche und Inspektion")
namen = sorted(node["name"] for node in graph["nodes"])
auswahl = st.selectbox("Node auswählen", namen)

gewaehlt = next(n for n in graph["nodes"] if n["name"] == auswahl)
links, rechts = st.columns(2)
with links:
    st.markdown("**Properties**")
    for schluessel, wert in gewaehlt["properties"].items():
        st.write(f"`{schluessel}`: {wert}")
with rechts:
    st.markdown("**Verbindungen (Kanten mit diesem Node)**")
    for kante in graph["edges"]:
        von_name = next(n["name"] for n in graph["nodes"]
                        if n["id"] == kante["von"])
        zu_name = next(n["name"] for n in graph["nodes"]
                       if n["id"] == kante["zu"])
        if gewaehlt["id"] in (kante["von"], kante["zu"]):
            st.code(f"{von_name} --{kante['typ']}--> {zu_name}", language="text")

st.caption("Neue Fakten legst du ueber die Seite ✋ Freigaben an – "
           "der Graph aendert sich NUR nach deiner Genehmigung.")
