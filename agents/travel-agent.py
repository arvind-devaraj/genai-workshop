from smolagents import CodeAgent, LiteLLMModel, tool

# --- STEP 1: Define Tools with Docstrings (smolagents uses these for reasoning) ---

@tool
def search_flights(origin: str, destination: str, date: str) -> str:
    """
    Searches for flights between Indian cities.
    Args:
        origin: Departure city (e.g., 'Mumbai')
        destination: Arrival city (e.g., 'Delhi')
        date: Date of travel in YYYY-MM-DD format.
    """
    flights = {
        "Mumbai-Delhi": [{"flight": "6E-2012", "price": 4500, "time": "06:00 AM"},
                         {"flight": "AI-802", "price": 5200, "time": "09:00 AM"}],
        "Bangalore-Goa": [{"flight": "QP-1102", "price": 3200, "time": "11:00 AM"}]
    }
    key = f"{origin}-{destination}"
    return str(flights.get(key, "No flights found for this route."))

@tool
def get_hotel_recommendation(city: str, budget_level: str) -> str:
    """
    Provides hotel recommendations based on city and budget.
    Args:
        city: The city to stay in.
        budget_level: One of 'luxury', 'mid', or 'budget'.
    """
    hotels = {
        "Delhi": {"luxury": "The Leela Palace", "mid": "FabHotel Prime", "budget": "Zostel Delhi"},
        "Goa": {"luxury": "Taj Exotica", "mid": "Lemon Tree", "budget": "Old Quarter Hostel"}
    }
    return hotels.get(city, {}).get(budget_level, "No specific recommendation found.")

# --- STEP 2: Setup the Model and Agent ---

model = LiteLLMModel(
    model_id="ollama/gemma3:4b", 
    api_base="http://localhost:11434" # Points to your local Ollama
)

# CodeAgent automatically handles the ReAct loop and multi-hop reasoning
agent = CodeAgent(
    tools=[search_flights, get_hotel_recommendation], 
    model=model,
    add_base_tools=True # Adds useful tools like a python_interpreter
)

# --- STEP 3: Execution ---

user_query = "I want to travel from Mumbai to Delhi on May 10th. I have a mid-range budget. Suggest a flight and a hotel."

# Running this will print the Thought/Action/Observation traces automatically to your console
agent.run(user_query)