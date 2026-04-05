import ollama

model_name = 'mapler/gpt2'
prompt = "In a shocking discovery, scientists found that"

def run_experiment(label, options):
    print(f"\n--- EXPERIMENT: {label} ---")
    response = ollama.generate(
        model=model_name,
        prompt=prompt,
        options=options
    )
    print(response['response'].strip())

# 1. TOP-K (The Filter)
# Limits the model to the top 'K' most likely next words.
# Low K (e.g., 5) makes it very focused/boring; High K (e.g., 100) allows for rare words.
run_experiment("Low Top-K (Conservative)", {
    'top_k': 5,
    'num_predict': 40
})

# 2. TOP-P / Nucleus Sampling (The Dynamic Filter)
# Chooses from the smallest set of words whose cumulative probability adds up to P.
# This is more "human-like" because it shrinks the pool when the model is certain 
# and expands it when it's uncertain.
run_experiment("High Top-P (Creative/Diverse)", {
    'top_p': 0.95,
    'temperature': 0.8,
    'num_predict': 40
})

# 3. REPEAT PENALTY (The Anti-Loop)
# Prevents the model from saying the same phrase over and over.
# GPT-2 is notorious for getting stuck in loops; 1.1 or 1.2 helps break them.
run_experiment("High Repeat Penalty", {
    'repeat_penalty': 1.5,
    'num_predict': 40
})

# 4. THE "DREAMER" (Balanced Creativity)
# Combining parameters for a high-quality, creative output.
run_experiment("The Dreamer (Balanced)", {
    'temperature': 0.85,
    'top_k': 40,
    'top_p': 0.9,
    'repeat_penalty': 1.1,
    'num_predict': 50
})