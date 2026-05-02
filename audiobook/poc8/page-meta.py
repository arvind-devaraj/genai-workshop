import pdfplumber
import ollama
import re

# 1. Read your prompt template from the file

prompt_template = """

System Role: You are an expert document editor specializing in structural formatting.

Task: Please split the provided text into distinct paragraphs or sections.

Constraints:

Output in JSON format with title and text for each paragraph.

Word Count: Each paragraph must be between 300 and 500 words.

Logic: Do not split in the middle of a sentence. Break the text at the natural end of a thought or sub-topic that falls within the word count range.

Format: Output the result as a numbered list of paragraphs.

Headers: Provide a short, bolded title for each paragraph that summarizes its core concept.

No Omissions: Do not summarize or skip any text. Every word from the original source must be included in the segments.
"""


def page_meta(page_text):
    print("Sending to Ollama...")

    final_prompt = f"""
    {prompt_template}

    Here is the text: 
    {page_text}
    """

    response = ollama.chat(
        model='qwen2.5:1.5b',
        messages=[{'role': 'user', 'content': final_prompt}]
    )

    # 5. Save the result
    result = response['message']['content']
    match = re.search(r'```(?:json)?\s*(.*?)```', result, re.DOTALL)
    if match:
        result = match.group(1).strip()
    return result


if __name__ == '__main__':
    import os

    data_dir = "../data"

    for filename in sorted(os.listdir(data_dir)):
        if not filename.endswith(".txt"):
            continue

        page_num = os.path.splitext(filename)[0]
        out_path = os.path.join("data-meta", f"{page_num}.txt")

        if os.path.exists(out_path):
            print(f"Skipping {filename} (already processed)")
            continue

        print(f"Processing {filename}...")
        with open(os.path.join(data_dir, filename)) as fp:
            contents = fp.read()

        result = page_meta(contents)

        with open(out_path, 'w') as f:
            f.write(result)
        print(f"Saved to {out_path}")
