import ollama
import numpy as np

# 1. THE AGENT'S "FILESYSTEM" (Simulated codebase)
codebase = [
    {"file": "auth.py", "content": "def login(user): return f'Welcome {user}'"},
    {"file": "utils.py", "content": "def calculate_tax(price): return price * 0.15"},
    {"file": "db.py", "content": "def save_user(name): connect_db(); print('Saved')"}
]

def get_embedding(text):
    return np.array(ollama.embed(model='embeddinggemma', input=text)['embeddings'][0])

# Pre-embed the file contents so the agent can "search" them
for f in codebase:
    f['vec'] = get_embedding(f['content'])

def find_guilty_file(error_msg):
    """Semantic search to find which file is most related to the error."""
    error_vec = get_embedding(error_msg)
    # Match error message to file content using Cosine Similarity
    best_file = max(codebase, key=lambda f: np.dot(error_vec, f['vec']) / (np.linalg.norm(error_vec) * np.linalg.norm(f['vec'])))
    return best_file

# 2. THE AGENTIC DIAGNOSIS
def bug_hunter_agent(error_log):
    print(f"🚨 Received Error: {error_log}")
    
    # Step 1: Investigation (Retrieval)
    target_file = find_guilty_file(error_log)
    print(f"🔍 Investigation points to: {target_file['file']}")

    # Step 2: Resolution (Generation)
    system_prompt = f"""
    You are a debugger. You found a bug in {target_file['file']}.
    File Content: {target_file['content']}
    Error Reported: {error_log}
    
    Rewrite the file content to fix the bug. Output ONLY the fixed code.
    """
    
    response = ollama.generate(model='gemma3:4b', system=system_prompt, prompt="Fix the bug.")
    return response['response'].strip()

# --- TEST ---
# The error mentions 'connect_db' is not defined. 
# The agent should find 'db.py' because it contains that string.
error = "NameError: name 'connect_db' is not defined in save_user"

print("\n--- Fixed Code ---")
print(bug_hunter_agent(error))