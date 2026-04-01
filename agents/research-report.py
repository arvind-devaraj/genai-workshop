import os
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, tool

# 1. Define a tool to save files locally
@tool
def save_report(content: str, filename: str) -> str:
    """
    Saves a text string into a local file.
    Args:
        content: The text content to write to the file.
        filename: The name of the file (e.g., 'report.txt').
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully saved report to {os.path.abspath(filename)}"

# 2. Setup Ollama (using Qwen2.5-Coder for best results)
model = LiteLLMModel(
    model_id="ollama_chat/gemma3:4b", 
    api_base="http://localhost:11434"
)

# 3. Initialize Agent with Search + our Custom File Tool
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(), save_report], 
    model=model,
    add_base_tools=True 
)

# 4. Run the task
agent.run(
    "Search for the 3 latest breakthroughs in Quantum Computing from 2024-2025. "
    "Summarize them in bullet points and save the summary to a file named 'quantum_news.txt'."
)