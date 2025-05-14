from swarm import Agent
from utils.prompt_loader import load_prompt

explanation_agent = Agent(
    name="Explain Agent",
    model="gpt-4.1",
    temperature=0.5,
    instructions=load_prompt("prompts/explanation_prompt.txt"))
