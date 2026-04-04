import ollama
import numpy as np

# 1. THE VULNERABILITY DATABASE (The 'Red Flags')
# In a real app, this would be thousands of CVE entries or OWASP guidelines.
security_kb = [
    {"issue": "SQL Injection", "pattern": "string formatting in execute()", "fix": "Use parameterized queries."},
    {"issue": "Insecure Hashing", "pattern": "md5() or sha1() for passwords", "fix": "Use argon2 or bcrypt."},
    {"issue": "Path Traversal", "pattern": "open(user_input)", "fix": "Sanitize file paths with os.path.basename."}
]

def get_embedding(text):
    return np.array(ollama.embed(model='embeddinggemma', input=text)['embeddings'][0])

# Pre-embed the 'Red Flags'
for entry in security_kb:
    entry['vec'] = get_embedding(entry['pattern'])

def audit_code(new_code):
    """Scan code for security smells using semantic similarity."""
    code_vec = get_embedding(new_code)
    
    # Calculate similarity to known bad patterns
    similarities = [
        (np.dot(code_vec, entry['vec']) / (np.linalg.norm(code_vec) * np.linalg.norm(entry['vec'])), entry)
        for entry in security_kb
    ]
    
    # Filter for high-probability matches (Threshold > 0.6)
    potential_issues = [entry for score, entry in similarities if score > 0.6]
    return potential_issues

# 2. THE AGENTIC REVIEW
def pr_reviewer_agent(submitted_code):
    print("🛡️ Starting Security Audit...")
    
    # Step 1: Detect Risks
    risks = audit_code(submitted_code)
    
    risk_context = ""
    if risks:
        print(f"⚠️ Found {len(risks)} potential vulnerability!")
        risk_context = "\n".join([f"- {r['issue']}: {r['fix']}" for r in risks])
    
    # Step 2: Generate the Review
    system_prompt = f"""
    You are a Security Engineer. Review the submitted code. 
    If these risks were found, highlight them: {risk_context}
    Suggest the exact code fix. Be concise.
    """
    
    response = ollama.generate(model='gemma3:4b', system=system_prompt, prompt=submitted_code)
    return response['response']

# --- TEST ---
# This code uses string formatting in a SQL query—a classic SQL injection risk.
user_submission = """
def get_user_data(username):
    query = f"SELECT * FROM users WHERE name = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()
"""

print("\n--- PR Review Report ---")
print(pr_reviewer_agent(user_submission))