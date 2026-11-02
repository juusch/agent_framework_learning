"""Chat-Seite: spricht mit dem Agenten und zeigt Route + Quellen."""

import sys
from pathlib import Path

import requests
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api_config import API_URL

from api_config import API_URL

st.title("💬 Chat mit dem Agenten")
st.caption("Der Agent klassifiziert deine Frage und waehlt die "
           "Retrieval-Route: Vektor (Dokumente), Graph (Beziehungen) oder Hybrid.")

if "verlauf" not in st.session_state:
    st.session_state.verlauf = []

for eintrag in st.session_state.verlauf:
    with st.chat_message(eintrag["role"]):
        st.write(eintrag["content"])
        if eintrag.get("route"):
            st.caption(f"Route: {eintrag['route']} · "
                       f"Doku: {len(eintrag.get('dokumente', []))} · "
                       f"Graph: {len(eintrag.get('graph_fakten', []))}")

frage = st.chat_input("Deine Frage an den Wissens-Agenten ...")
if frage:
    st.session_state.verlauf.append({"role": "user", "content": frage})
    with st.chat_message("user"):
        st.write(frage)

    try:
        antwort = requests.post(
            f"{API_URL}/chat",
            json={"nachricht": frage, "session_id": "streamlit"},
            timeout=30)
    except requests.exceptions.RequestException:
        st.error("Backend nicht erreichbar – siehe Startseite.")
        st.stop()

    if antwort.status_code != 200:
        st.error(f"Backend-Fehler {antwort.status_code}: "
                 f"{antwort.json().get('detail', '?')}")
        st.stop()

    daten = antwort.json()
    st.session_state.verlauf.append({
        "role": "assistant", "content": daten["antwort"],
        "route": daten["route"], "dokumente": daten["dokumente"],
        "graph_fakten": daten["graph_fakten"],
    })
    with st.chat_message("assistant"):
        st.write(daten["antwort"])
        badge = {"vektor": "📄", "graph": "🕸️", "hybrid": "🔀"}.get(
            daten["route"], "❓")
        st.caption(f"{badge} Route: **{daten['route']}** · Modus: {daten['modus']}")

        if daten["dokumente"]:
            with st.expander("📄 Dokument-Fundstellen"):
                for fund in daten["dokumente"]:
                    st.markdown(f"**{fund['quelle']}**")
                    st.write(fund["textstelle"])
        if daten["graph_fakten"]:
            with st.expander("🕸️ Graph-Fakten"):
                for fakt in daten["graph_fakten"]:
                    st.code(fakt, language="text")
