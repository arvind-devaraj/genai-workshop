import ollama
import json

# Configuration
MODEL = "gemma3:4b"

def run_gemma_task(task_name, prompt, system_prompt="You are a helpful NLP assistant."):
    print(f"\n--- Running Task: {task_name} ---")
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ]
        )
        print(response['message']['content'])
    except Exception as e:
        print(f"Error: Ensure Ollama is running and {MODEL} is pulled. {e}")

# 1. Named Entity Recognition (NER)
ner_text = "Apple CEO Tim Cook visited Mumbai on April 18, 2026."
run_gemma_task("NER", f"Extract (Person, Org, Location, Date) as JSON from: {ner_text}")

# 2. Summarization
long_text = "The evolution of generative AI has reached a turning point with multimodal models. These models can process text, images, and audio simultaneously, allowing for more natural human-computer interaction than ever before."
run_gemma_task("Summarization", f"Summarize this in one sentence: {long_text}")


# 3. Intent Classification
user_msg = "I need to reset my password, I forgot it."
run_gemma_task("Intent Classification", f"Classify this into [Support, Sales, Billing]: {user_msg}")

# 4. Translation
run_gemma_task("Translation", "Translate 'Where is the nearest train station?' into French and Spanish.")

# 5. Zero-Shot Classification
news = "The local team won the championship after a double-overtime thriller."
run_gemma_task("Zero-Shot Class", f"Label this text as 'Politics', 'Sports', or 'Weather': {news}")

# 6. Structured Data Extraction
raw_data = "I bought a coffee for $5.50 and a muffin for $3.75 at Starbucks."
run_gemma_task("Data Extraction", f"Turn this into a JSON list of items and prices: {raw_data}")

# 7. Synthetic Data Generation ---
# Useful for seeding databases without using real customer data (PII).
synthetic_prompt = """
Generate 3 rows of synthetic user data in a JSON array. 
Each object should contain: 
- 'user_id' (UUID)
- 'full_name' 
- 'email' (use a fake @dev-test.local domain)
- 'last_login' (ISO timestamp)
- 'account_status' (Active, Suspended, or Pending)
Ensure the data looks realistic but is entirely fictional.
"""
run_gemma_task("Synthetic Data Generation", synthetic_prompt)

# 8. PII Redaction (Data Masking) ---
# Essential for security compliance (GDPR/SOC2) before processing logs.
raw_log_data = """
2026-04-05 14:22:01 INFO: User 'sarah.jenkins@gmail.com' successfully authenticated from IP 192.168.1.104.
2026-04-05 14:23:45 ERROR: Connection timed out for customer record associated with phone +1-555-0199.
2026-04-05 14:25:12 DEBUG: Session started for 'm.rossi@company.it'.
"""

redaction_prompt = f"""
Identify and redact all Personal Identifiable Information (PII) from the following log entries. 
Replace emails, IP addresses, and phone numbers with '[REDACTED]'. 
Keep the log structure (timestamps and levels) exactly as they are.

LOGS:
{raw_log_data}
"""
run_gemma_task("PII Redaction", redaction_prompt)

print("\n" + "="*40)
print("All tasks completed.")