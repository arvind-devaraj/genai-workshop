import os
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google import GeminiEmbedding

# 1. API Setup
#os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

# 2. Optimized Configuration (April 2026 Standard)
# LLM: Use Flash-Lite for speed (The "Brain")
Settings.llm = GoogleGenAI(model="models/gemini-3.1-flash-lite-preview")

# EMBEDDING: Use the dedicated embedding model (The "Search")
# Using 'gemini-embedding-001' which is stable and supported for embedContent
Settings.embed_model = GeminiEmbedding(
    model_name="models/gemini-embedding-001",
    embed_batch_size=100  # Sends multiple items in one go to save time
)

# 3. Simple Array Knowledge Base
kb_array = [
    "The 2025 Tokyo Protocol mandates a global coal phase-out by 2035.",
    "NASA's Artemis IV landed a pressurized rover on Mars in January 2026.",
    "The March 2026 AI Act requires digital watermarking on all AI media.",
    "The SF 49ers won Super Bowl LX in February 2026 against the Chiefs."
]

# 4. Build and Query
documents = [Document(text=item) for item in kb_array]

# This will now work without the 404 error
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

print("\n--- Response ---")
print(query_engine.query("What are the new AI rules for 2026?"))