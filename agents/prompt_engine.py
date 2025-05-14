from swarm import Agent
from utils.prompt_loader import load_prompt

prompt_engine = Agent(
    name="Prompt Engine",
    model="gpt-4.1",
    temperature=0.2,
    instructions=load_prompt("prompts/engine_prompt.txt")
)
