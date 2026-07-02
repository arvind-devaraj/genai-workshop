from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="research_agent",
    model="gemini-2.0-flash",
    description="A research agent that fetches real-time information using Google Search before answering.",
    instruction=(
        "You are a helpful research assistant. "
        "Always use the google_search tool to find up-to-date information before answering. "
        "Cite the sources you find and present a clear, concise summary."
    ),
    tools=[google_search],
)
