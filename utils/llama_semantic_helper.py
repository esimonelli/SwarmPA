from llama_index.core import Document

# Creazione dei blocchi di testo dettagliati per l'indicizzazione semantica perfetta
doc_stipendi = Document(
    text="""
📂 Dataset: EntryAccreditoStipendi_202501.csv

Colonne:
- comune_della_sede: comune della sede lavorativa dell'amministrato, tipo: testuale, es. valori: Milano, Roma, Napoli, usi: filtro, aggregazione, merge geografico
- amministrazione: tipo di amministrazione pubblica (es. Ministero, Comune, INPS), tipo: categorico, es. valori: Comune, Ministero, INPS, usi: filtro, aggregazione
- eta_min: età minima della fascia anagrafica, tipo: numerico, es. valori: 18, 35, 50, usi: filtro, aggregazione
- eta_max: età massima della fascia anagrafica, tipo: numerico, es. valori: 34, 49, 64, usi: filtro, aggregazione
- sesso: sesso dell’amministrato, tipo: categorico, es. valori: M, F, usi: filtro, aggregazione, confronto
- modalita_pagamento: modalità con cui lo stipendio viene accreditato, tipo: categorico, es. valori: BONIFICO, LIBRETTO, usi: filtro, distribuzione
- numero: numero di accrediti registrati per quella combinazione, tipo: numerico, es. valori: 1, 100, 3000, usi: aggregazione, somma, media

Relazioni:
- Questo dataset può essere unito a: EntryPendolarismo_202501.csv tramite comune_della_sede
- Questo dataset può essere unito a: EntryAmministratiPerFasciaDiReddito_202501.csv tramite sesso, eta_min, eta_max
- Questo dataset può essere unito a: EntryAccessoAmministrati_202501.csv tramite sesso, eta_min, eta_max
""",
    metadata={"file_name": "EntryAccreditoStipendi_202501.csv"}
)

doc_redditi = Document(
    text="""
📂 Dataset: EntryAmministratiPerFasciaDiReddito_202501.csv

Colonne:
- comparto: settore di appartenenza dell’amministrato (es. Scuola, Sanità), tipo: categorico, es. valori: SCUOLA, SANITÀ, usi: filtro, aggregazione
- regione_residenza: regione di residenza dell’amministrato, tipo: geografico, es. valori: Lazio, Lombardia, Sicilia, usi: filtro, confronto regionale
- sesso: sesso dell’amministrato, tipo: categorico, es. valori: M, F, usi: filtro, aggregazione, confronto
- eta_min: età minima della fascia, tipo: numerico, es. valori: 18, 35, 50, usi: filtro, aggregazione
- eta_max: età massima della fascia, tipo: numerico, es. valori: 34, 49, 64, usi: filtro, aggregazione
- aliquota_max: aliquota massima applicata per fascia, tipo: numerico (percentuale), es. valori: 23, 38, usi: confronto, analisi fiscale
- fascia_reddito_min: inizio della fascia reddituale (testuale), tipo: testuale, es. valori: Fino a 28000, Oltre i 28000, usi: filtro descrittivo
- fascia_reddito_max: limite superiore della fascia reddituale (testuale), tipo: testuale, es. valori: Fino a 50000, Oltre i 50000, usi: filtro descrittivo
- numerosita: numero di amministrati in quella fascia, tipo: numerico, es. valori: 10, 150, 10000, usi: aggregazione, distribuzione

Relazioni:
- Questo dataset può essere unito a: EntryAccreditoStipendi_202501.csv tramite sesso, eta_min, eta_max
- Questo dataset può essere unito a: EntryAccessoAmministrati_202501.csv tramite sesso, eta_min, eta_max
""",
    metadata={"file_name": "EntryAmministratiPerFasciaDiReddito_202501.csv"}
)

doc_accessi = Document(
    text="""
📂 Dataset: EntryAccessoAmministrati_202501.csv

Colonne:
- regione_residenza_domicilio: regione di residenza dell’amministrato, tipo: geografico, es. valori: Lazio, Puglia, Toscana, usi: filtro, confronto regionale
- amministrazione_appartenenza: amministrazione in cui lavora l’amministrato, tipo: testuale/categorico, es. valori: INPS, COMUNE DI MILANO, usi: filtro, aggregazione
- sesso: sesso dell’amministrato, tipo: categorico, es. valori: M, F, usi: filtro, aggregazione
- eta_max: età massima della fascia anagrafica, tipo: numerico, es. valori: 34, 49, 64, usi: filtro, aggregazione
- eta_min: età minima della fascia anagrafica, tipo: numerico, es. valori: 18, 35, 50, usi: filtro, aggregazione
- modalita_autenticazione: modalità con cui l’utente accede al portale (es. SPID, CIE), tipo: categorico, es. valori: SPID, CIE, CNS, usi: filtro, distribuzione
- numero_occorrenze: numero di accessi con quella modalità, tipo: numerico, es. valori: 5, 100, 20000, usi: aggregazione, somma

Relazioni:
- Questo dataset può essere unito a: EntryAmministratiPerFasciaDiReddito_202501.csv tramite sesso, eta_min, eta_max
- Questo dataset può essere unito a: EntryAccreditoStipendi_202501.csv tramite sesso, eta_min, eta_max
- Questo dataset può essere unito a: EntryPendolarismo_202501.csv tramite amministrazione_appartenenza ⇄ ente
""",
    metadata={"file_name": "EntryAccessoAmministrati_202501.csv"}
)

doc_pendolarismo = Document(
    text="""
📂 Dataset: EntryPendolarismo_202501.csv

Colonne:
- provincia_della_sede: provincia della sede lavorativa, tipo: geografico, es. valori: Milano, Roma, Torino, usi: filtro, confronto geografico
- comune_della_sede: comune della sede lavorativa, tipo: geografico, es. valori: Bologna, Napoli, Bari, usi: filtro, merge geografico
- stesso_comune: indica se l’amministrato lavora nello stesso comune di residenza, tipo: categorico (SI/NO), es. valori: SI, NO, usi: filtro, analisi pendolarismo
- ente: tipo di ente in cui lavora l’amministrato, tipo: testuale/categorico, es. valori: MINISTERO, COMUNE DI MILANO, usi: filtro, aggregazione
- numero_amministrati: numero di amministrati per quella combinazione, tipo: numerico, es. valori: 5, 200, 10000, usi: somma, media
- distance_min_KM: distanza minima casa-lavoro in chilometri, tipo: testuale/numerico, es. valori: 0, 10, 30, usi: filtro, aggregazione
- distance_max_KM: distanza massima casa-lavoro in chilometri, tipo: testuale/numerico, es. valori: 5, 20, 50, usi: filtro, aggregazione

Relazioni:
- Questo dataset può essere unito a: EntryAccreditoStipendi_202501.csv tramite comune_della_sede
- Questo dataset può essere unito a: EntryAccessoAmministrati_202501.csv tramite ente ⇄ amministrazione_appartenenza
""",
    metadata={"file_name": "EntryPendolarismo_202501.csv"}
)

from llama_index.core.node_parser import SimpleNodeParser

parser = SimpleNodeParser()
nodes = parser.get_nodes_from_documents([
    doc_stipendi,
    doc_redditi,
    doc_accessi,
    doc_pendolarismo
])
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex(nodes)
index.storage_context.persist(persist_dir="index_perfetto")


len(nodes)
