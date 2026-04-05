import ollama

# The prompt for our experiment
prompt = "The secret ingredient in the potion was"

# The "Mad Scientist" setup
response = ollama.generate(
    model='mapler/gpt2',
    prompt=prompt,
    options={
        'temperature': 1.8,  # High chaos
        'top_p': 0.9,        # Nucleus sampling
        'num_predict': 50    # Max length
    }
)

print(f"--- Chaos Output (Temp 1.8) ---\n")
print(response['response'])

# Let's compare it to a "Sane" version in the same script
sane_response = ollama.generate(
    model='mapler/gpt2',
    prompt=prompt,
    options={
        'temperature': 0.2,  # Very focused
        'num_predict': 50
    }
)

print(f"\n--- Sane Output (Temp 0.2) ---\n")
print(sane_response['response'])