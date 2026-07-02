import os

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()

# 1. The model the agent will reason with.
# parallel_tool_calls=False makes the model wait for a tool's result before
# deciding what to do next -- without it, this model calls the search tool
# and writes its final answer in the same turn, before it has read the
# search results, and ends up making sources up.
model = OpenAIChatModel(
    model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    provider=OpenAIProvider(
        base_url="https://api.together.xyz/v1",
        api_key=os.environ["TOGETHER_API_KEY"],
    ),
    settings=ModelSettings(parallel_tool_calls=False),
)


# 2. The shape we want the final answer in.
class Answer(BaseModel):
    summary: str
    sources: list[str]


# 3. A tool is anything the model can call to fetch information it doesn't
# already know. pydantic_ai ships this one -- it wraps a web search API
# behind a function the model can invoke, and shows up as another item
# in the `tools` list.
agent = Agent(model=model, output_type=Answer, tools=[duckduckgo_search_tool(max_results=5)])


if __name__ == "__main__":
    question = "What is the current industry consensus on using GRPO over PPO for model alignment?"
    
    result = agent.run_sync(question)

    print(result.output.summary)
    print("\nSources:")
    for source in result.output.sources:
        print(f"- {source}")
