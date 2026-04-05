import os
from PIL import Image
from smolagents import CodeAgent, LiteLLMModel, tool

# 1. Setup Qwen3-VL via Ollama
# We use LiteLLM to bridge to the local Ollama endpoint
model = LiteLLMModel(
    model_id="ollama_chat/qwen3-vl", # or "ollama_chat/qwen3-vl:8b"
    api_base="http://localhost:11434",
    flatten_messages_as_text=False  # Required for Multimodal/Vision
)

# 2. Define the Audit Tool
@tool
def calculate_caloric_integrity(fat: float, carbs: float, protein: float, reported: float) -> str:
    """
    Calculates if the reported calories match the macronutrient sum.
    Args:
        fat: Grams of total fat.
        carbs: Grams of total carbohydrates.
        protein: Grams of protein.
        reported: The calories printed on the label.
    """
    calculated = (fat * 9) + (carbs * 4) + (protein * 4)
    variance = abs(calculated - reported)
    score = (1 - (variance / reported)) * 100
    
    return f"Calculated: {calculated} kcal. Reported: {reported} kcal. Integrity: {score:.2f}%"

# 3. Initialize Agent
agent = CodeAgent(
    tools=[calculate_caloric_integrity], 
    model=model,
    add_base_tools=True
)

# 4. Execute with Local Image
image_path = "product-label.jpg"

if os.path.exists(image_path):
    with Image.open(image_path) as img:
        # Qwen3-VL benefits from RGB normalization
        label_img = img.convert("RGB")
        
        task = """
        1. Look at the image and identify 'Total Fat', 'Total Carbohydrate', 'Protein', and 'Calories'.
        2. Call 'calculate_caloric_integrity' with these exact numbers.
        3. Provide a final_answer with the audit result.
        """
        
        print("--- Qwen3-VL: Local Multimodal Audit ---")
        print(agent.run(task, images=[label_img]))
else:
    print(f"File {image_path} not found.")