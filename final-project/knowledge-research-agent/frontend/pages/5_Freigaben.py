"""Freigaben: Human-in-the-Loop fuer neue Graph-Fakten (Stufe 14.2 live)."""

import sys
from pathlib import Path

import requests
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api_config import API_URL

from api_config import API_URL

st.title("✋ Freigaben – Fakten in den Knowledge Graph")
st.caption("Destruktive Operationen NUR mit deiner Zustimmung: Vorschlag "
           "prüfen → genehmigen oder ablehnen → Audit-Log führt Buch.")

links, rechts = st.columns(2)
with links:
    st.subheader("Neuen Fakt vorschlagen")
    von = st.text_input("Von (Entity-Name)", value="Clara")
    typ = st.selectbox("Beziehungstyp",
                       ["WORKS_FOR", "LEADS", "CONTRIBUTES_TO", "WORKS_ON",
                        "BELONGS_TO", "PROVIDES_DATA_FOR"])
    zu = st.text_input("Zu (Entity-Name)", value="Engineering")
    grund = st.text_input("Grund / Beleg", value="Steht im Firmenprofil.")

    if st.button("Vorschlag prüfen", type="primary"):
        antwort = requests.post(f"{API_URL}/facts/propose", timeout=15,
                                json={"von": von.strip(), "typ": typ,
                                      "zu": zu.strip(), "grund": grund})
        daten = antwort.json()
        st.session_state.vorschlag = daten
        st.write(f"**{daten['details']['frage']}**")
        st.code(daten["details"]["fakt"], language="text")
        st.caption(f"Grund des Vorschlags: {daten['details']['grund']}")

with rechts:
    st.subheader("Über laufenden Vorschlag entscheiden")
    vorschlag = st.session_state.get("vorschlag")
    if not vorschlag or vorschlag.get("status") != "wartet_auf_freigabe":
        st.info("Links einen Fakt vorschlagen – dann erscheint hier "
                "die Entscheidung.")
    else:
        st.code(vorschlag["details"]["fakt"], language="text")
        if st.button("✅ Genehmigen", type="primary"):
            ergebnis = requests.post(
                f"{API_URL}/facts/approve", timeout=15,
                json={"thread_id": vorschlag["thread_id"],
                      "genehmigt": True}).json()
            st.success(ergebnis["ergebnis"])
            st.session_state.vorschlag = None
        if st.button("❌ Ablehnen"):
            ergebnis = requests.post(
                f"{API_URL}/facts/approve", timeout=15,
                json={"thread_id": vorschlag["thread_id"],
                      "genehmigt": False}).json()
            st.warning(ergebnis["ergebnis"])
            st.session_state.vorschlag = None

st.divider()
st.subheader("Audit-Log")
audit = requests.get(f"{API_URL}/audit", timeout=10).json()["eintraege"]
if audit:
    for eintrag in audit:
        st.write(f"• {eintrag}")
else:
    st.caption("Noch keine Entscheidungen getroffen.")
