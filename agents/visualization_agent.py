from swarm import Agent
from utils.prompt_loader import load_prompt

visualization_agent = Agent(
    name="Visualization Agent",
    model="gpt-4.1",
    temperature=0.4,
    instructions=load_prompt("prompts/visualization_prompt.txt"))
