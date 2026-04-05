from smolagents import CodeAgent, LiteLLMModel, tool

# 1. Setup the Brain
model = LiteLLMModel(
    model_id="ollama_chat/gemma3:4b", 
    api_base="http://localhost:11434"
)

@tool
def get_chip_specs(chip_name: str) -> dict:
    """
    Retrieves hardware specifications.
    Args:
        chip_name: The name of the chip (e.g., 'H100' or 'MI300X').
    """
    specs = {
        "H100": {"model": "NVIDIA H100", "memory_gb": 80, "tdp_watts": 700, "teraflops": 3958},
        "MI300X": {"model": "AMD MI300X", "memory_gb": 192, "tdp_watts": 750, "teraflops": 5300}
    }
    return specs.get(chip_name.upper(), {"error": "Not found"})

# 2. Initialize Agent
agent = CodeAgent(
    tools=[get_chip_specs], 
    model=model,
    add_base_tools=True
)

# 3. The "Strict" Task
# We add a hint to the prompt to force the correct format for smaller models.
task = """
Find the specs for H100 and MI300X. 
Calculate which has better teraflops per watt.
YOU MUST CALL THE TOOLS USING PYTHON CODE BLOCKS.
Final answer must be delivered via the final_answer tool.
"""

# 4. Execute
print("--- Executing with Format Guardrails ---")
try:
    # We can also wrap the run in a specific instruction for the local model
    result = agent.run(task)
    print(f"\nFinal Result: {result}")
except Exception as e:
    print(f"\nError encountered: {e}")