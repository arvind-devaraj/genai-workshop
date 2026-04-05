from smolagents import CodeAgent, LiteLLMModel, tool

@tool
def get_weather(city: str) -> float:
    """
    Returns the current temperature in Celsius for a given city.
    Args:
        city: The name of the city.
    """
    # Mock data logic
    data = {"tokyo": 22.0, "new york": 15.0}
    return data.get(city.lower(), 20.0)

model = LiteLLMModel(model_id="ollama/gemma3:4b", api_base="http://localhost:11434")

# We use CodeAgent because it's great at 'multi-hop' logic 
# (it can even do the math itself in Python!)
agent = CodeAgent(tools=[get_weather], model=model, add_base_tools=True)

agent.run("Is it warmer in Tokyo or New York right now, and what is the difference?")