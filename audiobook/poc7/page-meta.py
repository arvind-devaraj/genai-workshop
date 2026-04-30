import pdfplumber
import ollama

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
    summary = response['message']['content']
    return (summary)


if __name__ == '__main__':
    fp = open("../data/page102.txt")
    contents=fp.read()
    print(page_meta(contents))