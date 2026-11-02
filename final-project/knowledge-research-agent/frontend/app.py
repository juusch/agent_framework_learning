"""Knowledge & Research Agent – Streamlit-Frontend (Hauptoberflaeche).

Start (Backend muss zuerst laufen, siehe README):
    streamlit run "final-project/knowledge-research-agent/frontend/app.py"

Lern-Hinweis: Das Frontend ist FERTIGER CODE zum Benutzen und
konzeptionellen Verstehen (Aufgabe 15.3). Es enthaelt bewusst KEINE
Geheimnisse und KEINE Geschaeftslogik – alles laeuft ueber die API.
"""

import sys
from pathlib import Path

import requests
import streamlit as st

# Die Seiten liegen im Unterordner pages/:
sys.path.insert(0, str(Path(__file__).resolve().parent))

from api_config import API_URL

st.set_page_config(page_title="Knowledge & Research Agent",
                   page_icon="🎓", layout="wide")


@st.cache_data(ttl=5)
def api_status() -> dict | None:
    """Lebenszeichen des Backends (kurz cachen, damit die Sidebar ruhig bleibt)."""
    try:
        antwort = requests.get(f"{API_URL}/status", timeout=3)
        return antwort.json() if antwort.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None


# ---- Sidebar: Status + Navigation ------------------------------------------
status = api_status()
with st.sidebar:
    st.title("🎓 Knowledge Agent")
    if status:
        # Nicht-sensible Konfigurationsanzeige (NIE der API-Key selbst!):
        farbe = {"mistral": "🟢", "openai_compatible": "🟢",
                "offline": "🟡"}.get(status.get("modus"), "🟡")
        st.success(f"{farbe} Backend erreichbar")
        st.markdown(f"**Anbieter:** {status.get('anbieter', status['modus'])}")
        if status.get("modell"):
            st.markdown(f"**Modell:** `{status['modell']}`")
        if status.get("endpoint"):
            st.markdown(f"**Endpoint:** `{status['endpoint']}`")
        st.caption(f"{status['dokumente']} Dokumente | "
                   f"{status['graph_knoten']} Graph-Knoten | "
                   f"{status['graph_kanten']} Kanten")
        if status.get("modus") == "offline":
            st.caption("Offline: Retrieval/Graph/Workflow sind echt – "
                       "nur LLM-Formulierungen simuliert. Andere KI-Quelle? "
                       "Siehe .env.example + docs/local-ai-server.md")
    else:
        st.error("Backend nicht erreichbar!")
        st.code("uvicorn backend.api.main:app --port 8000",
                language="bash")
        st.caption("(aus dem Ordner final-project/knowledge-research-agent)")
    st.divider()
    st.caption("Lernsystem der LangChain-&-LangGraph-Akademie – "
               "offline nutzbar, siehe README.")

# ---- Startseite -------------------------------------------------------------
st.title("Personal Knowledge & Research Agent")
st.markdown(
    "Dein Abschlussprojekt: ein Agent mit **zwei Wissenssystemen** – "
    "Vektor-Datenbank (Dokumente) und Knowledge Graph (Beziehungen) – "
    "gesteuert durch einen LangGraph-Workflow."
)

spalten = st.columns(3)
with spalten[0]:
    st.page_link("pages/1_Chat.py", label="💬 Chat mit dem Agenten", icon="💬")
    st.page_link("pages/2_Graph_Explorer.py", label="🕸️ Knowledge Graph", icon="🕸️")
with spalten[1]:
    st.page_link("pages/3_Dokumente.py", label="📄 Dokumente & RAG", icon="📄")
    st.page_link("pages/4_Prompt_Labor.py", label="🧪 Prompt-Labor", icon="🧪")
with spalten[2]:
    st.page_link("pages/5_Freigaben.py", label="✋ Freigaben", icon="✋")
    st.page_link("pages/6_Verlauf.py", label="📜 Verlauf", icon="📜")

st.divider()
st.subheader("Beispiel-Fragen zum Ausprobieren")
st.markdown(
    "• *Was wissen wir gesamt über das AI-Assistant-Projekt?* → Hybrid-Route\n"
    "• *Wer hängt am AI Assistant dran?* → Graph-Route (Traversierung)\n"
    "• *Was steht über die Abteilung Engineering?* → Vektor-Route\n"
    "• *Wie hängt Ben mit dem Projekt zusammen?* → Graph-Emergenz"
)

if status and status["modus"] == "offline":
    st.info(
        "Offline-Modus aktiv: Retrieval, Graph, Workflow und Freigaben sind "
        "echt – nur die Sprachformulierung des Modells ist simuliert. "
        "Andere KI-Quelle (Mistral, lokaler Server, jeder OpenAI-kompatible "
        "Endpoint): nur .env aendern – siehe docs/local-ai-server.md."
    )
