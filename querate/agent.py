from google.adk.agents import Agent, SequentialAgent, ParallelAgent

from querate.sub_agents.music_agent import music_agent
from querate.sub_agents.fashion_agent import fashion_agent
from querate.sub_agents.film_agent import film_agent
from querate.prompt import CURATOR_INSTRUCTION

music_agent.output_key = "music_analysis"
fashion_agent.output_key = "fashion_analysis"
film_agent.output_key = "film_analysis"

taste_gatherer = ParallelAgent(
    name="taste_gatherer",
    sub_agents=[music_agent, fashion_agent, film_agent],
)

curator_agent = Agent(
    model="gemini-2.5-flash",
    name="curator_agent",
    description="Synthesizes music, film, and fashion analysis into a unified aesthetic portrait.",
    instruction=CURATOR_INSTRUCTION,
)

root_agent = SequentialAgent(
    name="querate",
    sub_agents=[taste_gatherer, curator_agent],
)
