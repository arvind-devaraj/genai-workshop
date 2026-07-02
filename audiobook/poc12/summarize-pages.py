import pdfplumber
import ollama

# 1. Read your prompt template from the file
with open("prompt.txt", 'r') as fp:
    prompt_template = fp.read()

# 3. Combine the prompt and the extracted data


def summarize(extracted_text):
    print("Sending to Ollama...")

    final_prompt = f"""
    {prompt_template}

    Here is the text: 
    {extracted_text}
    """

    response = ollama.chat(
        model='qwen2.5:1.5b',
        messages=[{'role': 'user', 'content': final_prompt}]
    )

    # 5. Save the result
    summary = response['message']['content']
    return (summary)


# 2. Extract text from the PDF
# We accumulate the text into a single string variable
full_extracted_text = ""

with pdfplumber.open("books/current.pdf") as pdf:
    # Iterate through pages
    for i, page in enumerate(pdf.pages):
        # Stop after 10 pages (as per your original logic)
        print(f"Extracted Page {i + 1}")
            
        text = page.extract_text()
        result=summarize(text)
        filename = f"data/page{i + 1}.txt"
        with open(filename, 'w', encoding='utf-8') as f_out:
            f_out.write(result)


print(final_prompt)
# 4. Send to Ollama

with open('summary.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(summary)

print("Summary saved to summary.txt")