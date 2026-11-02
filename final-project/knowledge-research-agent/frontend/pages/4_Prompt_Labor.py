"""Prompt-Labor: Experimentier-Werkstatt fuer Prompts + Temperature."""

import sys
from pathlib import Path

import requests
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api_config import API_URL

from api_config import API_URL

st.title("🧪 Prompt-Labor")
st.caption("Stufe 2.3/3.2 interaktiv: Was passiert, wenn du System-Prompt "
           "oder Temperature aenderst? Sofort sichtbar – ohne Codeumbau.")

links, rechts = st.columns(2)
with links:
    system_prompt = st.text_area(
        "System-Prompt", value="Du bist ein freundlicher Erklärbär.",
        height=100)
with rechts:
    user_prompt = st.text_area(
        "User-Prompt", value="Erkläre in einem Satz, was ein Embedding ist.",
        height=100)
    temperatur = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)

if st.button("Abschicken", type="primary"):
    antwort = requests.post(
        f"{API_URL}/prompt-labor",
        json={"system_prompt": system_prompt,
              "user_prompt": user_prompt,
              "temperature": temperatur},
        timeout=30)
    daten = antwort.json()
    st.subheader("Antwort")
    st.write(daten["antwort"])
    st.caption(f"Modus: {daten['modus']} – offline sind Antworten "
               "deterministisch; mit Key siehst du echte Effekte "
               "(Stufe 2.3).")

st.divider()
st.markdown(
    "**Was du hier lernst (ohne zu programmieren):** System-Prompts formen "
    "die Rolle, Temperature steuert die Kreativitaet – und der Modus-Schalter "
    "zeigt dir jederzeit, ob du im Offline- oder Mistral-Modus experimentierst."
)
