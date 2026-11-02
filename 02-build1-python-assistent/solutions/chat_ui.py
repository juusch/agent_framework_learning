"""BUILD 1b – Erste Chat-Oberflaeche fuer deinen Pure-Python-Assistenten.

FERTIG GELIEFERERTER CODE (Konzept-Verstaendnis, kein Bau-Auftrag):
- ruft den Assistenten DIREKT im selben Prozess auf (einfachste Bruecke;
  die API-Schicht folgt in Modul 7)
- st.session_state haelt den Verlauf ueber Klicks hinweg (Streamlit
  fuehrt das Skript bei jeder Interaktion komplett neu aus!)

Start:   streamlit run 02-build1-python-assistent/solutions/chat_ui.py
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pure_python_assistant import beantworte, lade_dokumente  # noqa: E402

st.set_page_config(page_title="Build 1 – Knowledge Assistant", page_icon="🧱")
st.title("🧱 Build 1 – dein Pure-Python-Assistent")
st.caption("Erste Oberflaeche: direkter Aufruf im selben Prozess – "
           "ohne API-Schicht, ohne Frameworks.")

# Verlauf ueberlebt die Skript-Neu-Ausfuehrung nur im session_state:
if "verlauf" not in st.session_state:
    st.session_state.verlauf = []
if "abschnitte" not in st.session_state:  # Index EINMAL bauen (Stufe-6.3-Sache)
    st.session_state.abschnitte = lade_dokumente()

for eintrag in st.session_state.verlauf:
    with st.chat_message(eintrag["role"]):
        st.write(eintrag["content"])
        if eintrag.get("quellen"):
            st.caption("Quellen: " + " | ".join(eintrag["quellen"]))

frage = st.chat_input("Frag deinen Assistenten ... (offline nutzbar)")
if frage:
    st.session_state.verlauf.append({"role": "user", "content": frage})
    with st.chat_message("user"):
        st.write(frage)

    ergebnis = beantworte(frage, st.session_state.abschnitte)

    st.session_state.verlauf.append({
        "role": "assistant",
        "content": ergebnis["antwort"],
        "quellen": ergebnis["quellen"],
    })
    with st.chat_message("assistant"):
        st.write(ergebnis["antwort"])
        if ergebnis["quellen"]:
            st.caption("Quellen: " + " | ".join(ergebnis["quellen"]))
