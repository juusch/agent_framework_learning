"""Beispiel: jede Grundbauform einmal im Blick (fuer Aufgabe 0.x zum Ausprobieren)."""

# 1) print – Ausgabe
print("1) print gibt Text aus.")

# 2) Variablen – beschriftete Kisten
obst = "Apfel"
anzahl = 3
print(f"2) Variablen: {anzahl}x {obst}")

# 3) Rechnen mit Zahlen
gesamt_preis = 0.5 * anzahl
print(f"3) Rechnen: {anzahl} Aepfel kosten {gesamt_preis} Euro")

# 4) Liste – nummerierte Schublade
einkauf = ["Milch", "Brot"]
einkauf.append("Butter")
print(f"4) Liste: {einkauf}")

# 5) Dictionary – Woerterbuch (Schluessel -> Wert)
preise = {"Milch": 1.20, "Brot": 2.50}
print(f"5) Dictionary: Milch kostet {preise['Milch']} Euro")
