"""
https://images.sampletemplates.com/wp-content/uploads/2018/04/Detailed-Grocery-Payment-Receipt-Samples.jpg
"""


import pytesseract
import requests
from PIL import Image, ImageOps, ImageEnhance
from io import BytesIO
from smolagents import CodeAgent, LiteLLMModel, tool


# 1. Setup Gemma 3 4B (Local via Ollama)
# Run 'ollama pull gemma3:4b' first!
model = LiteLLMModel(
    model_id="ollama_chat/gemma3:4b", 
    api_base="http://localhost:11434"
)

# 2. Robust OCR Tool
@tool
def perform_ocr(image_url: str) -> str:
    """
    Downloads an image, enhances it for better readability, and extracts text.
    Args:
        image_url: The direct link to the image to scan.
    """
    # Download
    response = requests.get(image_url, timeout=10)
    img = Image.open(BytesIO(response.content))
    
    # Pre-processing for higher accuracy:
    # Convert to Grayscale -> Increase Contrast -> Auto-Level colors
    img = img.convert('L')
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageOps.autocontrast(img)
    
    raw_text = pytesseract.image_to_string(img)
    return f"--- OCR RESULTS ---\n{raw_text}\n--- END ---"

# 3. Initialize the Agent
agent = CodeAgent(
    tools=[perform_ocr], 
    model=model,
    add_base_tools=True # Gives the agent the 'Calculator' (Python Interpreter)
)

# 4. The Test Task
target_url = "https://images.sampletemplates.com/wp-content/uploads/2018/04/Detailed-Grocery-Payment-Receipt-Samples.jpg"

prompt = (
    f"Please scan this receipt: {target_url}\n"
    "1. Extract the Merchant Name, Date, and the Grand Total.\n"
    "2. Calculate a 12% tax on that total and tell me the final amount.\n"
    "3. Format your answer as a clean summary."
)

agent.run(prompt)