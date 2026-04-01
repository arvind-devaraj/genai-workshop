import numpy as np
import ollama

def get_vec(text):
    response = ollama.embeddings(model='embeddinggemma', prompt=text)
    return np.array(response['embedding'])

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 1. Generate the base vectors
king = get_vec("king")
man = get_vec("man")
woman = get_vec("woman")
queen = get_vec("queen")

# 2. Perform the arithmetic: King - Man + Woman
# Ideally, this resultant vector should be very close to "Queen"
result_vec = king - man + woman

# 3. Compare the result to "Queen"
score = cosine_similarity(result_vec, queen)

print(f"Similarity of (King - Man + Woman) to 'Queen': {score:.4f}")