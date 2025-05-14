from swarm import Swarm
from agents.data_agent import build_data_agent
from agents.conversational_agent import build_conversational_agent
from agents.prompt_engine import prompt_engine
from agents.visualization_agent import visualization_agent
from agents.explanation_agent import explanation_agent
from utils.csv_schema import generate_dataset_schema
from utils.index_builder import build_or_load_index
from utils.executor import execute_code
from utils.llama_helper import extract_semantic_schema_from_index
from langdetect import detect
import os



class SwarmAgentSystem:
    def __init__(self):
        self.client = Swarm()
        self.index = build_or_load_index(dataset_path="datasets", persist_dir="index", force=False)
        self.metadata_prompt = generate_dataset_schema()
        self.semantic_context = extract_semantic_schema_from_index()

        full_schema_prompt = f"""
[INFO] Metadati tecnici dei dataset:
{self.metadata_prompt}

[INFO] Contesto semantico estratto da LlamaIndex:
{self.semantic_context}
"""

        self.conversational_agent = build_conversational_agent(full_schema_prompt)
        self.data_agent = build_data_agent(self.metadata_prompt)

    def process_query(self, user_input, previous_prompt=None):
        user_language = detect(user_input)[:2]  # → 'en' or 'it'
        if previous_prompt:
            combined_input = f"Domanda precedente:\n{previous_prompt}\n\nNuova richiesta:\n{user_input}"
        else:
            combined_input = user_input
        try:
            # Step 1: Prompt strutturato
            response_doc = self.client.run(
                agent=self.conversational_agent,
                messages=[{"role": "user", "content": combined_input}]
            )
            semantic_prompt = response_doc.messages[-1]["content"]

            # Step 2: Prompt naturale
            response_prompt = self.client.run(
                agent=prompt_engine,
                messages=[
                    {"role": "system", "content": f"language: {user_language}"},
                    {"role": "user", "content": f"""
[USER INPUT]:
{user_input}

[STRUCTURED PROMPT]:
{semantic_prompt}
"""}
    ]
    )
            natural_instruction = response_prompt.messages[-1]["content"].strip()
            print("Natural Instruction:", natural_instruction)
            needs_visualization = "grafico" or "visualizza" or "graph" or "visualize" in natural_instruction.lower()

            # Step 3: Codice Python
            response_data = self.client.run(
                agent=self.data_agent,
                messages=[{"role": "user", "content": natural_instruction}]
            )
            generated_code = response_data.messages[-1]["content"].strip()

            if generated_code.startswith("```"):
                generated_code = "\n".join(line for line in generated_code.splitlines() if not line.strip().startswith("```"))

            dataframe_result = execute_code(generated_code)

            #if dataframe_result is None or (hasattr(dataframe_result, 'empty') and dataframe_result.empty):
                #print("Nessun risultato. Riprovo a elaborare nuovamente.")

            #retry_input = f"{user_input}\n\n[NOTA: primo tentativo fallito. Riscrivi la richiesta in forma più generica o semplificata mantenendo il significato.]"
    
            # Conversational Agent rigenera 
            #response_retry = self.client.run(agent=self.conversational_agent, messages=[{"role": "user", "content": retry_input}])
            #structured_retry = response_retry.messages[-1]["content"]

            # Prompt Engine rigenera
            #response_retry_prompt = self.client.run(agent=prompt_engine, messages=[{"role": "user", "content": structured_retry}])
            #natural_retry = response_retry_prompt.messages[-1]["content"]

            # Data Agent rigenera codice
            #response_data_retry = self.client.run(agent=self.data_agent, messages=[{"role": "user", "content": natural_retry}])
            #retry_code = response_data_retry.messages[-1]["content"]
            #dataframe_result = execute_code(retry_code)


            if dataframe_result is None:
                return {"message": "Nessun risultato disponibile. Assicurati di aver formulato bene la domanda o in caso la domanda è stata ben formulata riprova, qualcosa potrebbe essere andato storto.", "type": "text"}

            # Step 4: Visualizzazione (opzionale)
            image_path = None
            viz_code = None
            if needs_visualization:
                os.makedirs("images", exist_ok=True)
                viz_input = f"""
[Prompt utente]:
{natural_instruction}

[Output dati del Data Agent]:
{dataframe_result}

[Codice generato dal Data Agent (solo contesto)]:
{generated_code}
"""
                response_viz = self.client.run(
                    agent=visualization_agent,
                    messages=[{"role": "user", "content": viz_input}]
                )
                viz_code = response_viz.messages[-1]["content"].strip()

                if viz_code.startswith("```"):
                    viz_code = "\n".join(line for line in viz_code.splitlines() if not line.strip().startswith("```"))

                exec(viz_code)
                image_path = "images/output_visualization.png"

            # Step 5: Spiegazione finale
            explain_input = f"""
[Prompt Engine]:
{natural_instruction}

[Output dati del Data Agent]:
{dataframe_result}

[Codice eseguito dal Data Agent (come contesto)]:
{generated_code}

[Codice visualizzazione( come contesto)]:
{viz_code if viz_code else ''}:

[Language]:
{user_language}
"""
            response_exp = self.client.run(
                agent=explanation_agent,
                messages=[
                {"role": "system", "content": f"language: {user_language}"},
                {"role": "user", "content": explain_input}
                ]
            )


            return {
                "message": response_exp.messages[-1]["content"],
                "type": "visualization" if image_path else "text",
                "image_path": image_path
            }

        except Exception as e:
            return {"message": f"Errore: {str(e)}", "type": "text"}

    def run_console(self):
        last_semantic_prompt = None

        while True:
            print("\n-----------------------------------------")
            user_input = input("\n🤖 Inserisci qui la domanda 🤖 : ")

            if last_semantic_prompt:
                combined_input = f"Domanda precedente:\n{last_semantic_prompt}\n\nNuova richiesta:\n{user_input}"
            else:
                combined_input = user_input

            result = self.process_query(combined_input)
            last_semantic_prompt = combined_input

            if result["type"] == "visualization" and result.get("image_path"):
                print("[🖼] Grafico salvato in:", result["image_path"])
            print("\n🧠 Risposta:\n", result["message"])
