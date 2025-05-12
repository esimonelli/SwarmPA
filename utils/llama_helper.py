from llama_index.core import StorageContext, load_index_from_storage

def extract_semantic_schema_from_index(persist_dir="index"):
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()

    print("🔍 Estrazione semantica avanzata...")
    response = query_engine.query(DEEP_SCHEMA_QUERY)
    return str(response)

DEEP_SCHEMA_QUERY = """
Per ciascun dataset indicizzato, rispondi nel seguente formato strutturato:

---
📂 Dataset: <nome file>.csv

Colonne:
- <colonna_1>: <spiegazione semantica>, tipo: <numerico/categorico/testuale>, es. valori: <valore_1, valore_2,...>, usi: <filtri, aggregazioni, merge, ecc.>
- <colonna_2>: ...
[...]

Relazioni:
- Questo dataset può essere unito a: <altri dataset> tramite la colonna <nome_colonna>
---

REGOLE:
- Se una colonna rappresenta una località (comune, provincia, regione), indicane il livello geografico
- Se esiste una colonna simile in altri dataset, indicalo esplicitamente in "Relazioni"
- Non scrivere testo extra, solo il blocco strutturato come sopra
- Se un dataset non ha colonne utili, indica che non è rilevante

Lo scopo è aiutare un agente a mappare correttamente richieste dell'utente su colonne e dataset reali.
"""

