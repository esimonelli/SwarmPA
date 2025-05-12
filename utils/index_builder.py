import os
from pathlib import Path
import pandas as pd
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    SimpleDirectoryReader,
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.schema import Document

def load_csvs_as_nodes(dataset_path="datasets"):
    parser = SimpleNodeParser()
    documents = []

    for path in Path(dataset_path).glob("*.csv"):
        df = pd.read_csv(path)
        csv_text = f"Dataset: {path.name}\n\nColonne:\n"
        for col in df.columns:
            sample = df[col].dropna().astype(str).unique()[:3]
            preview = ", ".join(sample)
            csv_text += f"- {col}: es. {preview}\n"
        doc = Document(text=csv_text, metadata={"file_name": path.name})
        nodes = parser.get_nodes_from_documents([doc])
        documents.extend(nodes)

    return documents

def build_semantic_index(dataset_path="datasets", persist_dir="index"):
    print("⚙️ Indicizzazione dei CSV in corso...")
    nodes = load_csvs_as_nodes(dataset_path)
    index = VectorStoreIndex(nodes)
    index.storage_context.persist(persist_dir=persist_dir)
    print(f"✅ Indice creato e salvato in '{persist_dir}' ({len(nodes)} nodi)")
    return index

def build_or_load_index(dataset_path="datasets", persist_dir="index", force=False):
    required_files = [
        "docstore.json",
        "index_store.json",
        "default__vector_store.json"
    ]
    index_path = Path(persist_dir)
    index_exists = all((index_path / f).exists() for f in required_files)

    if index_exists and not force:
        print(f"🔁 Caricamento indice esistente da '{persist_dir}'...")
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)
        print("✅ Indice caricato correttamente.")
        return index
    else:
        print("🔄 Creazione nuovo indice semantico (forzata o assente)...")
        return build_semantic_index(dataset_path, persist_dir)
