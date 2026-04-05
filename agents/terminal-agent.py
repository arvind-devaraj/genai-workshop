from smolagents import CodeAgent, LiteLLMModel, tool
import subprocess

# 1. Define the Terminal Tool
@tool
def execute_shell(command: str) -> str:
    """
    Executes a shell command in the local terminal.
    Args:
        command: The bash/shell command to run.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Failed to execute command: {str(e)}"

# 2. Configure the Model to use Ollama
# We point LiteLLM to the local Ollama endpoint
model = LiteLLMModel(
    model_id="ollama_chat/gemma3", 
    api_base="http://localhost:11434", # Default Ollama port
    num_ctx=8192
)

# 3. Initialize the Agent
agent = CodeAgent(
    tools=[execute_shell],
    model=model
)

# 4. Interact in English
agent.run("Create a file named test.txt with contents 'hello world', then list the files in the directory.")