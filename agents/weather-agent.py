from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, tool

# 1. Define the tool with a docstring (smolagents uses this for instructions)
@tool
def get_weather(city: str) -> str:
    """
    Tells you the current weather in a specific city.
    Args:
        city: The name of the city.
    """
    # Imagine this calls a real API
    return "22°C and Sunny"

# 2. Setup the model (pointing to your local Ollama instance)
model = LiteLLMModel(
    model_id="ollama/gemma3:4b", 
    api_base="http://localhost:11434"
)

# 3. Initialize the Agent
agent = CodeAgent(tools=[get_weather], model=model)

# 4. Run it
agent.run("What should I wear in Tokyo today?")