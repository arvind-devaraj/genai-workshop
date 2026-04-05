import ollama
import numpy as np

def get_vector(word_text):
    # 1. Ask Ollama to turn the word into a list of numbers
    response = ollama.embed(model='embeddinggemma', input=word_text)
    vector_list = response['embeddings'][0]
    
    # 2. Convert to a NumPy array so we can do math (+ and -)
    return np.array(vector_list)

def calculate_similarity(vector1, vector2):
    # This formula calculates how 'close' two vectors are.
    # 1.0 means identical, 0.0 means completely different.
    dot_product = np.dot(vector1, vector2)
    norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    return dot_product / norm_product

def solve_analogy(word_a, word_b, word_c, list_of_candidates):
    # Logic: "A is to B" (Relationship) applied to "C"
    # Example: "Man is to King" applied to "Woman"
    
    # Get the vectors for our three starting words
    vector_a = get_vector(word_a)
    vector_b = get_vector(word_b)
    vector_c = get_vector(word_c)
    
    # THE MATH: Subtract A from B to get the 'difference' (the concept of royalty)
    # Then add that difference to C
    target_vector = (vector_b - vector_a) + vector_c
    
    best_word = ""
    highest_score = -1.0
    
    # Loop through our choices to find the best fit
    for candidate in list_of_candidates:
        candidate_vector = get_vector(candidate)
        score = calculate_similarity(target_vector, candidate_vector)
        
        # If this word is a better match than the last one, save it
        if score > highest_score:
            highest_score = score
            best_word = candidate
            
    return best_word

# --- Try it out! ---

# Example 1: Royalty
result1 = solve_analogy("man", "king", "woman", ["queen", "princess", "nurse"])
print("Man: King :: Woman: ", result1)

# Example 2: Countries
result2 = solve_analogy("France", "Paris", "Japan", ["Tokyo", "Kyoto", "China"])
print("France: Paris :: Japan: ", result2)

# Example 3: Verbs
result3 = solve_analogy("eat", "ate", "sleep", ["slept", "sleeping", "bed"])
print("Eat: Ate :: Sleep: ", result3)