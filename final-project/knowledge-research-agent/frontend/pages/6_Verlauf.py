"""Verlauf: alle Fragen, Routen und Quellen einer Session nachlesen."""

import sys
from pathlib import Path

import requests
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api_config import API_URL

from api_config import API_URL

st.title("📜 Ausführungshistorie")
st.caption("Der Verlauf lebt im Backend (Stufe 15.3-Konzept) – hier "
           "liest du nach, welche Route der Agent wählte und woher "
           "jede Information kam.")

antwort = requests.get(f"{API_URL}/history",
                       params={"session_id": "streamlit"}, timeout=10)
eintraege = antwort.json()["eintraege"]

if not eintraege:
    st.info("Noch keine Fragen gestellt – geht auf die Chat-Seite!")
else:
    for eintrag in eintraege:
        with st.expander(f"❓ {eintrag['frage'][:60]} "
                         f"(Route: {eintrag['route']})"):
            st.write(eintrag["antwort"])
            if eintrag["dokumente"]:
                st.markdown(f"**📄 Dokumente:** {len(eintrag['dokumente'])}")
                for fund in eintrag["dokumente"]:
                    st.caption(f"{fund['quelle']}: {fund['textstelle'][:100]}...")
            if eintrag["graph_fakten"]:
                st.markdown(f"**🕸️ Graph-Fakten:** "
                            f"{len(eintrag['graph_fakten'])}")
                for fakt in eintrag["graph_fakten"]:
                    st.code(fakt, language="text")
