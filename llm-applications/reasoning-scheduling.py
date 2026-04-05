import ollama

# 1. Define the complex scheduling data
log_data = """
PARTICIPANTS:
- Alice (PST): Free 9:00 AM - 11:00 AM.
- Bob (GMT): Free 2:00 PM - 4:00 PM.
- Charlie (EST): Free 10:00 AM - 12:00 PM.

CONSTRAINTS:
- The meeting must be exactly 45 minutes.
- Bob needs a 15-minute buffer after his 1:30 PM GMT call.
- All times must be converted to a unified UTC format for comparison.
"""

# 2. Construct the prompt for a reasoning-capable model
prompt = f"""
Solve this scheduling puzzle step-by-step:
1. Normalize all participant availability to UTC.
2. Account for Bob's 15-minute buffer (he is actually free starting at 1:45 PM GMT).
3. Identify the intersection where ALL three participants are available.
4. If no intersection exists, propose the 'best fit' and explain who needs to move their schedule.

Context:
{log_data}

Return the result in a clear, formatted summary.
"""

# 3. Call the model
# Note: Ensure you have pulled the model first via: ollama pull gemma3:4b
try:
    response = ollama.chat(
        model='gemma3:4b',
        messages=[{'role': 'user', 'content': prompt}]
    )

    # 4. Output the reasoning and the result
    print("--- Scheduling Analysis ---")
    print(response['message']['content'])

except Exception as e:
    print(f"An error occurred: {e}")