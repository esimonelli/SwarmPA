from swarm import Swarm
from dotenv import load_dotenv
from agents.data_agent import build_data_agent
from agents.conversational_agent import build_conversational_agent
from utils.executor import execute_code
from utils.csv_schema import generate_dataset_schema
from utils.llama_helper import extract_semantic_schema_from_index
from utils.index_builder import build_or_load_index
from agents.prompt_engine import prompt_engine
from agents.visualization_agent import visualization_agent
from agents.explanation_agent import explanation_agent
import os

load_dotenv()
client = Swarm()

# Carica o crea l'indice una sola volta
index = build_or_load_index(dataset_path="datasets", persist_dir="index", force=False)

# Costruzione del prompt semantico
metadata_prompt = generate_dataset_schema()
print("[INFO] Output di schema_description / metadata_prompt:")
print(metadata_prompt)

semantic_context = extract_semantic_schema_from_index()

full_schema_prompt = f"""
[INFO] Metadati tecnici dei dataset:
{metadata_prompt}

[INFO] Contesto semantico estratto da LlamaIndex:
{semantic_context}
"""
print("[INFO] Prompt system completo passato al Conversational Agent:\n")
print(full_schema_prompt)

# Costruzione del Conversational Agent con contesto semantico
conversational_agent = build_conversational_agent(full_schema_prompt)

while True:
    print("\n-----------------------------------------")
    user_input = input("\n🤖 Inserisci qui la domanda 🤖 : ")

    # Step 1 – Comprensione della richiesta
    response_doc = client.run(
        agent=conversational_agent,
        messages=[{
            "role": "user",
            "content": user_input
        }]
    )
    semantic_prompt = response_doc.messages[-1]["content"]
    print("[INFO] Prompt strutturato generato dal Document Agent:\n", semantic_prompt)

    # Step 2 – Traduzione in prompt naturale
    response_prompt = client.run(
        agent=prompt_engine,
        messages=[{
            "role": "user",
            "content": f"""
[USER INPUT]:
{user_input}

[STRUCTURED PROMPT]:
{semantic_prompt}
"""
        }]
    )
    natural_instruction = response_prompt.messages[-1]["content"].strip()
    print("[INFO] Prompt testuale generato dal Prompt Engine:\n", natural_instruction)

    needs_visualization = "grafico" in natural_instruction.lower()

    # Step 3 – Codice Python dal Data Agent
    data_agent = build_data_agent(metadata_prompt)
    response_data = client.run(
        agent=data_agent,
        messages=[{
            "role": "user",
            "content": natural_instruction
        }]
    )
    generated_code = response_data.messages[-1]["content"]

    if generated_code.startswith("```"):
        generated_code = "\n".join(
            line for line in generated_code.splitlines()
            if not line.strip().startswith("```")
        )

    print("\n[INFO] Codice generato dal Data Agent:\n")
    print(generated_code)

    try:
        dataframe_result = execute_code(generated_code)
        print("[DEBUG] Valore dataframe_result:", repr(dataframe_result))
    except Exception as e:
        print(f"[ERRORE] durante l'esecuzione del codice dati: {e}")
        continue

    # Step 4 – Visualizzazione (se richiesta)
    viz_code = None
    if needs_visualization:
        print("[INFO] Attivo il Visualization Agent per generare il grafico...")
        os.makedirs("images", exist_ok=True)

        viz_input = f"""
[Prompt utente]:
{natural_instruction}

[Output dati del Data Agent]:
{dataframe_result}

[Codice generato dal Data Agent]:
{generated_code}
"""

        response_viz = client.run(
            agent=visualization_agent,
            messages=[{
                "role": "user",
                "content": viz_input
            }]
        )

        viz_code = response_viz.messages[-1]["content"]

        if viz_code.startswith("```"):
            viz_code = "\n".join(
                line for line in viz_code.splitlines()
                if not line.strip().startswith("```")
            )

        print("\n[INFO] Codice generato dal Visualization Agent:\n")
        print(viz_code)

        try:
            exec(viz_code)
            print("[INFO] ✅ Grafico generato e salvato in ./images/output_visualization.png")
        except Exception as e:
            print(f"[ERRORE] durante l'esecuzione del codice di visualizzazione: {e}")
            continue

    # Step 5 – Spiegazione finale integrata
    viz_section = f"[Codice visualizzazione]:\n{viz_code}" if viz_code else ""
    explain_input = f"""
[Prompt utente]:
{natural_instruction}

[Output dati del Data Agent]:
{dataframe_result}

[Codice eseguito dal Data Agent]:
{generated_code}

{viz_section}
"""

    response_exp = client.run(
        agent=explanation_agent,
        messages=[{
            "role": "user",
            "content": explain_input
        }]
    )

    print("\n🧠 Spiegazione finale:\n")
    print(response_exp.messages[-1]["content"])


# Integrare anche una mappatura comune → regione da CSV esterno, se vuoi migliorare la copertura logica in questi casi.
