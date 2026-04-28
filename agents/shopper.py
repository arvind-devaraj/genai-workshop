import os
import subprocess
from smolagents import CodeAgent, LiteLLMModel

# 1. Setup Gemma 3 4B via Ollama
# LiteLLM acts as the bridge between smolagents and your local Ollama instance
model = LiteLLMModel(
    model_id="ollama_chat/gemma3:4b", 
    api_base="http://localhost:11434", # Default Ollama port
    num_ctx=8192,                      # Gemma 3 supports large context
    temperature=0.1                    # Low temperature for precise refactoring
)

# 2. Define the Refactoring Tools
@tool 
def read_file(path: str) -> str:
    """Reads a file's content."""
    with open(path, "r") as f: return f.read()

@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file."""
    with open(path, "w") as f: f.write(content)
    return f"Updated {path}"

@tool
def run_pytest(file_path: str) -> str:
    """Runs pytest on a specific file to check for regressions."""
    result = subprocess.run(["pytest", file_path], capture_output=True, text=True)
    return f"Exit Code: {result.returncode}\n{result.stdout}\n{result.stderr}"

# 3. Initialize the Agent
agent = CodeAgent(
    tools=[read_file, write_file, run_pytest],
    model=model,
    add_base_tools=True,
    additional_authorized_imports=["re", "json", "os"]
)


# 4. Define the Refactoring Logic
def execute_refactor(target_file: str, instructions: str):
    prompt = f"""
    You are an expert Senior Software Engineer. 
    Your task is to refactor the file: {target_file}
    
    Goal: {instructions}
    
    Strict Workflow:
    1. Read the file content.
    2. Identify areas for improvement (DRY, SOLID, naming, performance).
    3. Apply the refactor by writing back to the file.
    4. Run the linter to ensure syntax is correct.
    5. Run tests (e.g., 'pytest {target_file}') to ensure behavior is preserved.
    6. If tests fail, fix the code and repeat until it passes.
    """
    refactor_agent.run(prompt)

# Example Usage
if __name__ == "__main__":
    execute_refactor("legacy_app.py", "Simplify the nested if-statements and add type hints.")
    pass