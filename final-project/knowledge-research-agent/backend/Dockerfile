# Dockerfile fuer Backend UND Frontend des Capstone (siehe docker-compose.yml).
# Build-Kontext ist die AKADEMIE-WURZEL (wegen des lernakademie-Pakets):
#   docker build -f final-project/knowledge-research-agent/backend/Dockerfile .

FROM python:3.12-slim

WORKDIR /app

# Abhaengigkeiten zuerst (Cache-Schicht, Stufe 9.3):
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Komplette Akademie kopieren (dockerignore schliesst .env/.venv aus):
COPY . .

WORKDIR /app/final-project/knowledge-research-agent

# Geheimnisse NIEMALS ins Image – Keys kommen zur Laufzeit als
# Umgebungsvariablen (docker compose liest .env des Hosts).
EXPOSE 8000 8501
