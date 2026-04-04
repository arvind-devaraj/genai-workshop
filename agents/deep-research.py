import ollama
import numpy as np

# 1. THE SUPPLY CHAIN KB (Distinct Layers)
kb = [
    {
        "layer": "Retail-Consumer", 
        "text": "The price of Organic Tomatoes has spiked 40% this month. Local grocery chains are reporting stockouts."
    },
    {
        "layer": "Logistics-Wholesale", 
        "text": "Regional distributors are struggling with 'Perishable-Transit' delays due to a shortage of refrigerated CO2 canisters."
    },
    {
        "layer": "Agronomy-Industrial", 
        "text": "The 'CO2-Canister' shortage is a byproduct of high natural gas prices, which forced several Ammonia-Fertilizer plants to shut down."
    }
]

def get_vec(text): 
    return np.array(ollama.embed(model='embeddinggemma', input=text)['embeddings'][0])

for item in kb: item['vec'] = get_vec(item['text'])

def research_supply_chain(symptom):
    print(f"🌾 DEEP RESEARCH TRACE: '{symptom}'\n" + "="*60)

    # --- STEP 1: THE RETAIL SYMPTOM ---
    r_vec = get_vec(symptom)
    for item in kb:
        item['score'] = np.dot(r_vec, item['vec']) / (np.linalg.norm(r_vec) * np.linalg.norm(item['vec']))
    
    first_clue = max(kb, key=lambda x: x['score'])
    print(f"[STEP 1] Retail Layer Matches:")
    for item in kb: print(f"  - {item['layer']}: {item['score']:.4f}")
    print(f"👉 MATCHED: {first_clue['layer']} | {first_clue['text']}\n")

    # --- STEP 2: THE PIVOT (Identifying the 'Logistics Link') ---
    pivot_prompt = f"In this market report: '{first_clue['text']}', what is the specific product or logistics constraint? answer in 1-2 words."
    pivot_item = ollama.generate(model='gemma3:4b', prompt=pivot_prompt)['response'].strip()
    print(f"[STEP 2] Pivoting from 'Retail' to 'Logistics': '{pivot_item}'")

    # --- STEP 3: THE DEEP DIVE (The Industrial Root Cause) ---
    p_vec = get_vec(pivot_item)
    for item in kb:
        if item['layer'] != first_clue['layer']:
            item['deep_score'] = np.dot(p_vec, item['vec']) / (np.linalg.norm(p_vec) * np.linalg.norm(item['vec']))
        else:
            item['deep_score'] = 0.0

    root_cause = max(kb, key=lambda x: x['deep_score'])
    print(f"[STEP 3] Deep-Search Scores for '{pivot_item}':")
    for item in kb: print(f"  - {item['layer']}: {item['deep_score']:.4f}")
    print(f"🏭 ROOT CAUSE: {root_cause['layer']} | {root_cause['text']}\n")
    
    # --- STEP 4: FINAL SYNTHESIS ---
    final_prompt = f"Consumer query: {symptom}. Investigation found {first_clue['text']} linked to {root_cause['text']}. Explain the chain reaction."
    print(f"[FINAL_PROMPT]== {final_prompt}")
    return ollama.generate(model='gemma3:4b', prompt=final_prompt)['response']

# --- TEST ---
print("--- FINAL RESEARCH REPORT ---")
print(research_supply_chain("Why can't I find organic tomatoes at the store?"))