from swarm import Agent
from utils.prompt_loader import load_prompt

def build_conversational_agent(schema_description: str):
    return Agent(
        name="Conversational Agent",
        model="gpt-4.1",
        temperature=0.3,
        instructions=load_prompt("prompts/conversational_prompt.txt"))