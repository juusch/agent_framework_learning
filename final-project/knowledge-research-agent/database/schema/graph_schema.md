# Graph-Schema des Knowledge Graph (Capstone)

Dieses Dokument beschreibt die Modellierung des Knowledge Graph –
die "Ontologie" der Anwendung (vgl. Stufe 10.2).

## Labels (Node-Typen)

| Label | Bedeutung | Properties (Beispiel) |
|---|---|---|
| `:Person` | Mitarbeitende | `name`, `rolle` |
| `:Department` | Abteilungen | `name` |
| `:Company` | Unternehmen | `name`, `branche` |
| `:Project` | Projekte | `name`, `status` |

## Beziehungstypen (Relationships)

| Typ | Bedeutung | von → zu |
|---|---|---|
| `WORKS_FOR` | arbeitet bei | Person → Company |
| `BELONGS_TO` | gehört zu | Person → Department |
| `LEADS` | leitet | Person → Department |
| `WORKS_ON` | arbeitet an | Department → Project |
| `CONTRIBUTES_TO` | trägt bei zu | Person → Project |
| `PROVIDES_DATA_FOR` | liefert Daten für | Department → Project |

## Regeln

1. Beziehungen verbinden **IDs**, nie Namen (Stufe 10.1).
2. Neue Fakten nur über den **Freigabe-Workflow** (interrupt/resume,
   Stufe 14.2) – niemals direkt schreibend.
3. Lesende Abfragen durchlaufen die **Whitelist** (`ist_sicher`,
   Stufe 12.3).
4. Entity Resolution vor jedem Anlegen (`find_node`, Stufe 12.2).

## Offline-Betrieb

Die Anwendung nutzt den In-Memory-`GraphStore` der Akademie. Für
Persistenz und echte Neo4j-Abfragen: `docker compose up` startet Neo4j;
die Brücke zeigt `04-knowledge-graphs/solutions/python_neo4j_bridge.py`,
ein optionaler Seeder liegt unter `database/seed/seed_to_neo4j.py`.
