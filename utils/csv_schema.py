import pandas as pd
import os

def generate_dataset_schema():
    datasets_info = {
        "stipendi": "datasets/EntryAccreditoStipendi_202501.csv",
        "redditi": "datasets/EntryAmministratiPerFasciaDiReddito_202501.csv",
        "accessi": "datasets/EntryAccessoAmministrati_202501.csv",
        "pendolarismo": "datasets/EntryPendolarismo_202501.csv"
    }

    schema = "Questi sono i dataset disponibili e le loro colonne:\n\n"
    for name, path in datasets_info.items():
        if os.path.exists(path):
            try:
                df = pd.read_csv(path, nrows=5)
                columns = ", ".join(df.columns)
                schema += f"{name} ({os.path.basename(path)}):\n  - {columns}\n\n"
            except Exception as e:
                schema += f"{name} ({path}): ERRORE LETTURA CSV → {e}\n\n"
        else:
            schema += f"{name} ({path}): FILE NON TROVATO\n\n"
    return schema.strip()
