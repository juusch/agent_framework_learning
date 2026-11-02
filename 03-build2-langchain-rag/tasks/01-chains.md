# Aufgabe 3.1 – Chains: vom Handbau zum Fließband 🔗

**Schwierigkeit:** Leicht · **Zeit:** ~45 Min · ⚠️ **Kosten:** nur mit Key

## Lernziel
Du kennst die LangChain-Grundbausteine – Chat-Modelle, Prompt-Templates, Output-Parser – und verkettest sie mit `|` zur **Chain** (Runnable-Schnittstelle).

## Warum das wichtig ist
Erinnerung an Build 1: Prompt von Hand bauen, Client callen, Antwort extrahieren, Fehler behandeln – jedes Mal dasselbe. **Metapher – das Fließband:** Ein Arbeiter schneidet (Template füllt), der nächste lackiert (Modell antwortet), der letzte prüft (Parser macht aus der `AIMessage` einen sauberen String). `prompt | modell | parser` – das ist die ganze Magie.

## Deine Mission
1. **Hello LangChain:** Chat-Modell holen (`lernakademie.get_chat_model()`), Nachrichten als Objekte (`SystemMessage`, `HumanMessage`), `.invoke()`, Antwort über `.content`.
2. **Summarizer-Chain:** `ChatPromptTemplate` mit `{stil}` und `{text}` → Modell → `StrOutputParser`; teste denselben Text mit zwei Stilen – **dieselbe Chain, nur die Eingabe ändert sich**.
3. **Bonus:** Mini-Übersetzer-Chain (`{text}`, `{zielsprache}`), wiederverwendet dasselbe Modell-Objekt.

## Akzeptanzkriterien
- [ ] Die Chain ist in einer Variablen definiert und mehrfach per `.invoke({...})` aufrufbar.
- [ ] Vergessene Platzhalter im `invoke`-Dict erzeugen einen **Validierungsfehler** – du verstehst ihn als Feature.
- [ ] Die Ausgabe ist ein String (Parser!), kein `AIMessage`-Objekt.

## Hinweise
1. Aktuelle Imports: `from langchain_core.prompts import ChatPromptTemplate`, `from langchain_core.output_parsers import StrOutputParser`
2. Chain: `chain = prompt | modell | StrOutputParser()`
3. `lernakademie.llm_client.get_chat_model()` liefert das **konfigurierte** Modell – Mistral, dein lokaler Server oder offline die Simulation. Die Chain merkt keinen Unterschied: genau das ist Provider-Unabhängigkeit.

## Reflexionsfragen
1. Zähle: Wie viele Runnables stecken in `prompt | modell | parser`? (3!)
2. Was genau hat LangChain gegenüber Build 1 ersetzt – und was ist **neu** dazugekommen (Abstraktion = neue Begriffe)?
3. Warum ist `with_structured_output` (Pydantic) die logische Fortsetzung des Parser-Gedankens? (→ 3.3)

## Referenzlösung + Walkthrough
→ [`solutions/hello_langchain.py`](../solutions/hello_langchain.py), [`solutions/summarizer_chain.py`](../solutions/summarizer_chain.py)

## Weiter
3.2 – der große Qualitätssprung: **Embeddings** ersetzen deine Wortsuche.
