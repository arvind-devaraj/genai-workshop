import ollama

# The "Domain" - A technical SOP (Standard Operating Procedure)
technical_sop = """
SERVICE: 'payment-gateway-v2'
1. Architecture: Runs on K8s in 'finance' namespace. Depends on 'auth-srv' and 'redis-cache'.
2. Environment Variables:
   - DB_MAX_CONN: Default 20. Increase to 50 during peak load.
   - TIMEOUT_MS: Critical. Must be lower than 500ms to prevent cascading failure.
3. Health Checks: Endpoint /health returns 200. If 503, check 'redis-cache' connectivity.
4. Emergency Rollback:
   - Command: `kubectl rollout undo deployment/payment-gateway-v2 -n finance`
   - Requirement: Must notify #incident-response on Slack before executing.
5. Known Issues: 'Error 401' usually means the 'auth-srv' secret has expired.
"""

# The "Incident" Question
# The user wants to know what to do about a specific error code.
question = "I'm seeing a 401 error in the logs and the service is sluggish. What is the likely cause, and what command do I run if I need to revert to the previous version?"

prompt = f"""
Act as a Senior DevOps Engineer. Use ONLY the provided SOP to answer the question.
If the SOP doesn't cover a part of the question, say "Instruction not found in SOP."

SOP:
{technical_sop}

QUESTION:
{question}
"""

print("--- Analyzing System Incident ---")
response = ollama.chat(
    model='gemma3:4b',
    messages=[{'role': 'user', 'content': prompt}]
)

print(response['message']['content'])