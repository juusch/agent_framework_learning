"""Dokumente-Seite: Wissensbasis verwalten (Upload + Liste + Probe-Frage)."""

import sys
from pathlib import Path

import requests
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api_config import API_URL

from api_config import API_URL

st.title("📄 Dokumente & RAG")
st.caption("Hochgeladene Texte landen im Vektor-Index – der Agent findet "
           "danach sinngleiche Stellen (Stufe 4/13).")

# ---- Upload ---------------------------------------------------------------
with st.form("upload", clear_on_submit=True):
    st.subheader("Dokument hochladen")
    titel = st.text_input("Titel", value="meine-notizen")
    inhalt = st.text_area("Inhalt (Text)", height=180,
                          placeholder="Füge hier Wissen ein, z. B. Notizen, "
                          "Zusammenfassungen, Projektinfos ...")
    abgeschickt = st.form_submit_button("Hinzufügen", type="primary")

if abgeschickt:
    if len(titel.strip()) < 1 or len(inhalt.strip()) < 20:
        st.warning("Titel + mindestens 20 Zeichen Inhalt, bitte.")
    else:
        antwort = requests.post(f"{API_URL}/documents", timeout=15,
                                json={"titel": titel.strip(),
                                      "inhalt": inhalt.strip()})
        if antwort.status_code == 200:
            st.success(f"Indexiert: {antwort.json()['neue_chunks']} Chunk(s)")
        else:
            st.error(f"Fehler: {antwort.json().get('detail', '?')}")

# ---- Dokumentliste ----------------------------------------------------------
st.subheader("Indexierte Dokumente")
liste = requests.get(f"{API_URL}/documents", timeout=10).json()["dokumente"]
if liste:
    for dokument in liste:
        st.markdown(f"• **{dokument['titel']}** – {dokument['zeichen']} Zeichen")
else:
    st.info("Noch keine Dokumente indexiert.")

# ---- Probe-Frage -------------------------------------------------------------
st.subheader("Probe-Frage ans RAG")
probe = st.text_input("Frage (Vektor-Route, z. B. 'Was steht über ...?')")
if st.button("Fragen") and probe:
    antwort = requests.post(f"{API_URL}/chat", timeout=30,
                            json={"nachricht": probe, "session_id": "dokumente"})
    daten = antwort.json()
    st.write(daten["antwort"])
    for fund in daten["dokumente"]:
        with st.expander(f"Fundstelle: {fund['quelle']}"):
            st.write(fund["textstelle"])
