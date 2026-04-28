import os
from google import genai
from google.genai import types

# Initialize the client. 
# It will automatically use the GEMINI_API_KEY environment variable.
client = genai.Client()

def call_gemini(prompt: str):
    """Sends a prompt to Gemini and returns the response."""
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Or 'gemini-2.0-pro' for more complex tasks
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7, # Controls randomness (0.0 to 1.0)
            )
        )
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# --- Execution ---
user_prompt = "Explain how photosynthesis works in simple terms."
result = call_gemini(user_prompt)

print(f"Prompt: {user_prompt}")
print(f"Response: {result}")