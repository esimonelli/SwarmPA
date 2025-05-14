from swarm import Agent
from utils.prompt_loader import load_prompt

def build_data_agent(schema_description: str):
    return Agent(
        name="Data Agent",
        model="gpt-4.1",
        temperature=0.1,
        instructions=load_prompt("prompts/data_prompt.txt"))