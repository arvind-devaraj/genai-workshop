import ollama

# 1. Define available tools
def get_weather(city):
    # Imagine this calls a real API
    return "22°C and Sunny"

# 2. The ReAct Prompt
prompt = """
You are a ReAct assistant. You have access to a tool: get_weather(city).
Follow this pattern:
Thought: [Your reasoning about what to do]
Action: [The tool to call]
Observation: [The result of the tool]
Final Answer: [The final response to the user]

Question: What should I wear in Tokyo today?
"""

# 3. Execution (Conceptual)
# The model outputs: "Thought: I need to know the weather in Tokyo. Action: get_weather('Tokyo')"
response = ollama.chat(model='gemma3:4b', messages=[{'role': 'user', 'content': prompt}])

# You (the developer) parse the "Action", call the function, 
# and feed the "Observation" back to the model.
observation = get_weather("Tokyo")

final_prompt = prompt + response['message']['content'] + f"\nObservation: {observation}"
final_response = ollama.chat(model='gemma3:4b', messages=[{'role': 'user', 'content': final_prompt}])

print(final_response['message']['content'])