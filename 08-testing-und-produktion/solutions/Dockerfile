# Aufgabe 9.3 – Referenzloesung: Dockerfile der Lernakademie
#
# Bauen:   docker build -t lernakademie .
# Starten: docker run --rm -it --env-file .env lernakademie
# (Key kommt zur LAUFZEIT als Umgebungsvariable – nie ins Image!)

FROM python:3.12-slim

WORKDIR /app

# Abhaengigkeiten zuerst kopieren (Cache-Schicht: Code-Aenderungen
# invalidieren die Paket-Installation nicht):
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Dann den Code (siehe solutions/.dockerignore: .env, .venv, Caches fehlen!)
COPY . .

# Startbefehl: der Wissens-Assistent aus Stufe 8
CMD ["python", "08-real-world-projects/solutions/knowledge_assistant.py"]
