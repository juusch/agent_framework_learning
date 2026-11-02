"""Aufgabe 15.2 – Referenzloesung: Streamlit-Chat mit Backend-Bruecke.

Start-Reihenfolge:
    1) uvicorn --app-dir 07-finale-app/solutions api_server:app --reload
    2) streamlit run 07-finale-app/solutions/chat_app.py

Konzept-Unterscheidung fuer Lernende:
- VERSTEHEN: session_state, requests-Bruecke, Fehler-UX
- GEBAUT: diese ~70 Zeilen (bewusst minimal)
- FERTIG GELIEFERT: das Capstone-Frontend (Graph-Explorer, Playground, ...)
"""

import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Lernakademie Chat", page_icon="🎓")
st.title("🎓 Lernakademie – Chat mit deinem Agenten")

# ---- Sidebar: Live-Status des Backends ------------------------------------
with st.sidebar:
    st.header("Backend-Status")
    try:
        status = requests.get(f"{API_URL}/status", timeout=3).json()
        st.success(f"Erreichbar – Modus: **{status['modus']}**")
        if status["modus"] == "offline":
            st.caption("Ohne API-Key: Antworten sind [OFFLINE]-Simulationen.")
    except requests.exceptions.ConnectionError:
        st.error("Backend nicht erreichbar!")
        st.caption("Starte es mit: uvicorn --app-dir 07-finale-app/solutions api_server:app")
    st.divider()
    temperatur = st.slider("Temperature (Bonus-Widget)", 0.0, 1.0, 0.0, 0.1)
    st.caption("Wird als Payload mitgeschickt – die UI steuert Backend-Verhalten.")


# ---- Session-State als Gedaechtnis ----------------------------------------
if "verlauf" not in st.session_state:
    st.session_state.verlauf = [
        {"role": "assistant", "content": "Hallo! Frag mich etwas – "
         "ich rede mit deinem FastAPI-Backend."}
    ]

for nachricht in st.session_state.verlauf:
    with st.chat_message(nachricht["role"]):
        st.write(nachricht["content"])

# ---- Eingabe -> POST ans Backend -> Antwort in den Verlauf ---------------
frage = st.chat_input("Deine Frage ...")
if frage:
    st.session_state.verlauf.append({"role": "user", "content": frage})
    with st.chat_message("user"):
        st.write(frage)

    try:
        antwort = requests.post(
            f"{API_URL}/chat",
            json={"nachricht": frage, "session_id": "streamlit",
                  "temperature": temperatur},
            timeout=30,
        )
        if antwort.status_code == 200:
            text = antwort.json()["antwort"]
        else:
            text = f"Backend-Fehler ({antwort.status_code}): {antwort.json().get('detail', '?')}"
    except requests.exceptions.ConnectionError:
        text = ("Backend nicht erreichbar. Hast du uvicorn gestartet? "
                "(siehe Sidebar)")
    except requests.exceptions.Timeout:
        text = "Zeitueberschreitung – das Backend brauchte zu lange."

    st.session_state.verlauf.append({"role": "assistant", "content": text})
    with st.chat_message("assistant"):
        st.write(text)
