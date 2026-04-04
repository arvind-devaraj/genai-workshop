import ollama
import numpy as np

# 1. THE BRAIN: Security Knowledge Base
kb = [
    {"pattern": "string formatting in execute()", "fix": "Use parameterized queries to prevent SQL Injection."},
    {"pattern": "md5() or sha1() for passwords", "fix": "Use argon2 or bcrypt for secure hashing."},
    {"pattern": "open(user_input)", "fix": "Sanitize file paths with os.path.basename to prevent traversal."}
]

def get_vec(text):
    """Converts text into a mathematical vector."""
    res = ollama.embed(model='embeddinggemma', input=text)
    return np.array(res['embeddings'][0])

# Pre-embed the rules for speed
for item in kb: 
    item['vec'] = get_vec(item['pattern'])

# 2. THE AUDIT: Semantic Search + LLM Reasoning
def security_agent(user_code):
    # STEP 1: Search (Retrieve relevant rule)
    code_vec = get_vec(user_code)
    
    # Calculate Cosine Similarity using np.dot
    # (dot product of normalized vectors = cosine similarity)
    def similarity(v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    # Find rules that match the code "smell" (Threshold > 0.6)
    matches = [i['fix'] for i in kb if similarity(code_vec, i['vec']) > 0.6]

    # STEP 2: Reason (Generate the Review)
    prompt = f"Code:\n{user_code}\n\nRules Found: {matches}\n\nTask: Provide a 1-sentence fix."
    return ollama.generate(model='gemma3:4b', prompt=prompt)['response']

# --- TEST ---
print(security_agent("cursor.execute(f'SELECT * FROM users WHERE id={id}')"))