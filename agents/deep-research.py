import ollama
import numpy as np

# 1. THE RESEARCH REPOSITORY (Your 'Local Library' of PDFs/Articles)
research_vault = [
    {"topic": "Solid State Batteries", "content": "Solid-state batteries use ceramic electrolytes instead of liquid, significantly reducing fire risk and increasing energy density."},
    {"topic": "Anode Materials", "content": "Silicon anodes can hold more lithium than graphite but suffer from expansion issues during charging cycles."},
    {"topic": "Manufacturing Scale", "content": "The primary barrier to solid-state adoption is the high cost of thin-film ceramic deposition at scale."},
    {"topic": "Thermal Management", "content": "Ceramic electrolytes are more stable at high temperatures, allowing for smaller cooling systems in EVs."}
]

def get_vec(text):
    return np.array(ollama.embed(model='embeddinggemma', input=text)['embeddings'][0])

# Pre-index the vault
for entry in research_vault:
    entry['vec'] = get_vec(entry['content'])

# 2. THE DEEP RESEARCH LOOP
def deep_research_agent(main_query):
    print(f"🔬 Starting Deep Research on: {main_query}\n")

    # STEP 1: DECOMPOSITION (Breaking the topic down)
    plan_prompt = f"Break this research topic into 3 specific technical sub-questions: {main_query}"
    plan_res = ollama.generate(model='gemma3:4b', prompt=plan_prompt)
    sub_questions = plan_res['response'].strip().split('\n')
    
    final_report = []

    # STEP 2: RECURSIVE RETRIEVAL
    for question in sub_questions:
        if not question.strip(): continue
        print(f"  → Investigating: {question.strip()}")
        
        # Use Embedding-Gemma to find the best 'fact' in the vault
        q_vec = get_vec(question)
        best_fact = max(research_vault, key=lambda x: np.dot(q_vec, x['vec']) / (np.linalg.norm(q_vec) * np.linalg.norm(x['vec'])))
        
        # STEP 3: ANALYSIS
        # Gemma analyzes the fact in the context of the sub-question
        analysis = ollama.generate(
            model='gemma3:4b', 
            prompt=f"Context: {best_fact['content']}\nQuestion: {question}\nProvide a concise technical summary."
        )
        final_report.append(analysis['response'])

    # STEP 4: SYNTHESIS
    print("\n✍️ Synthesizing Final Report...")
    summary_prompt = f"Combine these findings into a professional technical brief: {' '.join(final_report)}"
    final_res = ollama.generate(model='gemma3:4b', prompt=summary_prompt)
    
    return final_res['response']

# --- RUN ---
report = deep_research_agent("The future of solid-state battery commercialization")
print("\n--- FINAL RESEARCH BRIEF ---")
print(report)