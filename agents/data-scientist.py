import pandas as pd
from smolagents import CodeAgent, LiteLLMModel, tool

# 1. Setup the Local Model via Ollama
# We use LiteLLMModel as the bridge to Ollama's API
model = LiteLLMModel(
    model_id="ollama_chat/gemma3:4b",
    api_base="http://localhost:11434"
)

# 2. Define the Tool with the required @tool decorator
@tool
def load_sales_data() -> pd.DataFrame:
    """
    A tool that returns a DataFrame of recent sales for analysis.
    
    Returns:
        pd.DataFrame: Contains 'Product', 'Revenue', and 'Month' columns.
    """
    data = {
        "Product": ["Laptops", "Monitors", "Keyboards", "Laptops", "Monitors", "Keyboards"],
        "Revenue": [1200, 500, 150, 1500, 450, 200],
        "Month": ["January", "January", "January", "February", "February", "February"]
    }
    return pd.DataFrame(data)

# 3. Initialize the Agent
agent = CodeAgent(
    tools=[load_sales_data],
    model=model,
    # The agent needs permission to use these libraries in its generated code
    additional_authorized_imports=["pandas", "numpy"]
)

# 4. Run the Specific Query
# Gemma 3 will write the Python/Pandas code to filter and find the Max value
query = "Which product had the highest revenue in February?"
result = agent.run(query)

print(f"\n" + "="*30)
print(f"QUERY: {query}")
print(f"RESULT: {result}")
print("="*30)