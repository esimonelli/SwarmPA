from swarm import Swarm
from swarm_interface import SwarmAgentSystem
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
from dotenv import load_dotenv
load_dotenv()

#benvenuto in questo sistema multi-agente

#TRIPLE 3 è un sistema di agenti multi-agente progettato per analizzare i dati della Pubblica Amministrazione in linguaggio naturale. 
#È in grado di elaborare domande relative a stipendi, redditi, accessi e spostamenti, fornendo risposte dettagliate e visualizzazioni grafiche.


# - Saluti, Overfitted Stallions

if __name__ == "__main__":
    system = SwarmAgentSystem()
    system.run_console()


