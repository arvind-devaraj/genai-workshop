import ollama
import json

# --- STEP 1: Define the Tools (The 'Act' part) ---
def search_flights(origin, destination, date):
    """Simulates a flight search API for Indian carriers (IndiGo, Air India, etc.)"""
    # In a real app, you'd use Amadeus or Skyscanner API here
    flights = {
        "Mumbai-Delhi": [{"flight": "6E-2012", "price": 4500, "time": "06:00 AM"},
                         {"flight": "AI-802", "price": 5200, "time": "09:00 AM"}],
        "Bangalore-Goa": [{"flight": "QP-1102", "price": 3200, "time": "11:00 AM"}]
    }
    key = f"{origin}-{destination}"
    return flights.get(key, "No flights found for this route.")

def get_hotel_recommendation(city, budget_level):
    """Simulates a hotel database lookup"""
    hotels = {
        "Delhi": {"luxury": "The Leela Palace", "mid": "FabHotel Prime", "budget": "Zostel Delhi"},
        "Goa": {"luxury": "Taj Exotica", "mid": "Lemon Tree", "budget": "Old Quarter Hostel"}
    }
    return hotels.get(city, {}).get(budget_level, "No specific recommendation found.")

# --- STEP 2: The ReAct Engine ---
def run_concierge(user_request):
    system_prompt = """
    You are an Indian Travel Concierge. You use a ReAct (Reason + Act) framework.
    Available Tools:
    - search_flights(origin, destination, date)
    - get_hotel_recommendation(city, budget_level)

    Format your response exactly like this:
    Thought: [Your reasoning about what is missing or what to do next]
    Action: [tool_name](args)
    Observation: [The result of the tool - this will be provided to you]
    ... (repeat if needed)
    Final Answer: [Your complete travel plan]
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request}
    ]

    # --- The ReAct Loop (Simplified) ---
    # First Pass: Model Reasons and decides to Act
    response = ollama.chat(model='gemma3:4b', messages=messages)
    content = response['message']['content']
    print(f"\n--- Model's Internal Monologue ---\n{content}")

    # Logic to parse the "Action" and execute the Python function
    if "search_flights" in content:
        # For demo purposes, we manually trigger the observation 
        # In production, use regex to extract (origin, destination, date)
        obs = search_flights("Mumbai", "Delhi", "2026-05-10")
        
        # Feed observation back for final reasoning
        messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": f"Observation: {obs}"})
        
        final_response = ollama.chat(model='gemma3:4b', messages=messages)
        return final_response['message']['content']

# --- STEP 3: Execution ---
user_query = "I want to travel from Mumbai to Delhi on May 10th. I have a mid-range budget. Suggest a flight and a hotel."
result = run_concierge(user_query)

print("\n--- Final Concierge Response ---")
print(result)