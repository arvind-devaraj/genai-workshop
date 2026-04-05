import ollama
import re

# --- STEP 1: Define the Actual Python Functions (The "Acts") ---
def search_database(query):
    """Simulates a database of state populations."""
    db = {
        "Maharashtra": 123144223, 
        "Karnataka": 61130704,
        "Tamil Nadu": 72147030
    }
    # Clean the input in case the LLM adds extra spaces
    query = query.strip()
    return db.get(query, f"Location '{query}' not found in database.")

def calculator(expression):
    """Evaluates mathematical expressions safely."""
    try:
        # Note: eval is used here for a simple demo; 
        # in production, use a library like 'numexpr' or 'simpleeval'
        return eval(expression, {"__builtins__": None}, {})
    except Exception as e:
        return f"Calculation Error: {str(e)}"

# --- STEP 2: Create the TOOLS Mapping ---
# This dictionary prevents the 'NameError' by linking 
# the LLM's text output to your Python functions.
TOOLS = {
    "search_database": search_database,
    "calculator": calculator
}

# --- STEP 3: The ReAct Engine ---
def run_multitool_agent(user_query, model_name='gemma3:4b'):
    system_prompt = """
    You are a ReAct Research Bot. You solve problems by Reasoning and Acting.
    
    Available Tools: 
    1. search_database(location_name): Returns the population of an Indian state.
    2. calculator(expression): Performs math like "10 + 20" or "500 * 0.15".

    You MUST use this format:
    Thought: [Your reasoning about what to do next]
    Action: [tool_name]("[input]")
    Observation: [The result of the tool - this will be provided to you]
    ... (Repeat if necessary)
    Final Answer: [The definitive final response to the user]
    """

    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": user_query}
    ]

    print(f"TARGET GOAL: {user_query}")
    print("="*50)

    # The Loop: Allows the model to "hop" between different tools
    for i in range(5):  # Limit to 5 hops to prevent infinite loops
        response = ollama.chat(model=model_name, messages=messages)
        content = response['message']['content']
        
        # Print LLM's Thought/Action in Yellow
        print(f"\033[31m{content}\033[0m") 
        
        messages.append({"role": "assistant", "content": content})

        # Check if the LLM wants to provide a Final Answer
        if "Final Answer:" in content:
            print("="*50)
            print("MISSION ACCOMPLISHED.")
            break

        # Parse the Action using Regex
        # Matches: Action: tool_name("input")
        match = re.search(r"Action: (\w+)\(\"(.*?)\"\)", content)
        
        if match:
            tool_name, tool_input = match.groups()
            
            if tool_name in TOOLS:
                # Execute the real Python function
                observation_result = TOOLS[tool_name](tool_input)
                obs_text = f"Observation: {observation_result}"
                
                # Print the Tool Result in Dark Red
                print(f"\033[31m{obs_text}\033[0m\n") 
                
                # Feed the grounded reality back to the LLM
                messages.append({"role": "user", "content": obs_text})
            else:
                error_msg = f"Observation: Error - Tool '{tool_name}' does not exist."
                print(f"\033[31m{error_msg}\033[0m\n")
                messages.append({"role": "user", "content": error_msg})
        else:
            # If the model forgot the format, nudge it back
            nudge = "Observation: Invalid format. Please use Thought: and Action: [tool_name](\"input\")"
            messages.append({"role": "user", "content": nudge})

# --- STEP 4: Run the Agent ---
if __name__ == "__main__":
    query = "What is the combined population of Maharashtra and Karnataka?"
    run_multitool_agent(query)