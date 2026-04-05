import ollama
import numpy as np

def get_vector(text):
    """Fetches and normalizes the vector for a given string."""
    res = ollama.embed(model='embeddinggemma', input=text)
    vec = np.array(res['embeddings'][0])
    # Normalizing makes vector math more reliable in high-dimensional spaces
    return vec / np.linalg.norm(vec)

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def solve_generic_analogy(a, b, c, candidates):
    """
    Solves the analogy: A is to B as C is to [Result]
    Formula: Result ≈ (B - A) + C
    """
    v_a = get_vector(a)
    v_b = get_vector(b)
    v_c = get_vector(c)
    
    # Calculate the 'relationship vector' (B - A) and apply it to C
    target_vector = (v_b - v_a) + v_c
    # Re-normalize the target
    target_vector = target_vector / np.linalg.norm(target_vector)
    
    results = []
    for word in candidates:
        v_word = get_vector(word)
        score = cosine_similarity(target_vector, v_word)
        results.append((word, score))
    
    # Sort by closest match
    results.sort(key=lambda x: x[1], reverse=True)
    return results[0]

# --- Examples of Generic Use Cases ---

# 1. Family/Gender
print(f"Man:King :: Woman:? -> {solve_generic_analogy('man', 'king', 'woman', ['queen', 'princess', 'staff'])[:1]}")

# 2. Science/States of Matter
print(f"Ice:Water :: Water:? -> {solve_generic_analogy('ice', 'water', 'water', ['steam', 'gas', 'cloud'])[:1]}")

# 3. Verb Tense
print(f"Walk:Walked :: Swim:? -> {solve_generic_analogy('walk', 'walked', 'swim', ['swam', 'swum', 'swimming'])[:1]}")

# 4. Tech/Company
print(f"Google:Search :: Apple:? -> {solve_generic_analogy('Google', 'Search', 'Apple', ['iPhone', 'Fruit', 'Job'])[:1]}")