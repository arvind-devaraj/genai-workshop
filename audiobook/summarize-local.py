import ollama

with open('contents.txt', 'r', encoding='utf-8') as file:
    data = file.read()
    #print(data)


prompt = f"""
Act as an experienced podcast scriptwriter.  Rewrite the following text into a single paragraph. Start with the rewritten text without any introductions or preamble(e.g here is the summary)

Guidelines:

Conversational Tone: Like a podcast or audiobook, use natural, spoken language. Use "we," "you," and "I" to engage the listener.

Add Transitions: Use smooth verbal transitions between sections (e.g., "Moving on to," "Next up is," "Think of this like...").

Maintain Structure: Keep the main points organized logically, but ensure the formatting is appropriate for a script (e.g., headings that act as signposts).

Preserve Integrity: Keep the technical facts accurate; do not lose the meaning, just change the delivery.


 Here is the text: {data}  """
response = ollama.chat(
    model='qwen2.5:1.5b',
    messages=[{'role': 'user', 'content': prompt}]
)

summary=response['message']['content']

with open('summary.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(summary)