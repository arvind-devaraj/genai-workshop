from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool

# 1. Initialize the Ollama model via LiteLLM
# Use the 'ollama_chat/' prefix followed by your local model name
model = LiteLLMModel(
    model_id="ollama_chat/gemma3:4b", 
    api_base="http://localhost:11434", # Default Ollama port
    num_ctx=8192                       # Recommended: increase context for agents
)

# 2. Setup the Agent
# add_base_tools=True gives the agent a Python interpreter (for math/logic)
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()], 
    model=model,
    add_base_tools=True 
)

# 3. Run a task
agent.run("Search for the current price of Ethereum and tell me how much 2.5 ETH is worth in USD.")