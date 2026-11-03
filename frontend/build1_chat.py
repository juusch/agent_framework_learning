"""BUILD 1 – Streamlit-Oberflaeche fuer den Pure-Python-Assistenten.

FERTIG GELIEFERT (Lektion 06): Start im Terminal mit
    streamlit run frontend/build1_chat.py

Lern-Konzept dahinter (kein Bauauftrag): Streamlit fuehrt das Skript bei
jedem Klick komplett neu aus -> der Verlauf lebt nur in st.session_state
(dasselbe Problem wie beim LLM-Gedaechtnis: der Notizblock muss explizit
mitgefuehrt werden).
"""

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lernakademie.build1 import beantworte, lade_dokumente  # noqa: E402

st.set_page_config(page_title="Build 1 – Knowledge Assistant", page_icon="🧱")
st.title("🧱 Build 1 – dein Pure-Python-Assistent")
st.caption("Wort-Ueberlappungssuche + handgebauter Prompt – alles aus Lektion 05.")

if "abschnitte" not in st.session_state:      # Index EINMAL bauen
    st.session_state.abschnitte = lade_dokumente()
if "verlauf" not in st.session_state:          # Verlauf ueberlebt Klicks
    st.session_state.verlauf = []

for eintrag in st.session_state.verlauf:
    with st.chat_message(eintrag["role"]):
        st.write(eintrag["content"])
        if eintrag.get("quellen"):
            st.caption("Quellen: " + " | ".join(eintrag["quellen"]))

frage = st.chat_input("Frag deinen Assistenten ...")
if frage:
    st.session_state.verlauf.append({"role": "user", "content": frage})
    with st.chat_message("user"):
        st.write(frage)

    ergebnis = beantworte(frage, st.session_state.abschnitte)
    st.session_state.verlauf.append({
        "role": "assistant", "content": ergebnis["antwort"],
        "quellen": ergebnis["quellen"]})
    with st.chat_message("assistant"):
        st.write(ergebnis["antwort"])
        if ergebnis["quellen"]:
            st.caption("Quellen: " + " | ".join(ergebnis["quellen"]))
