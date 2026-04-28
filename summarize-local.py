import ollama

with open('contents.txt', 'r', encoding='utf-8') as file:
    data = file.read()
    #print(data)


prompt = f"""

Rewrite the text below into a clean, spoken-word summary for an audio recording. Follow these constraints strictly:

NO STAGE DIRECTIONS: Do not include any parentheticals, sound descriptions, mood cues, or stage directions (e.g., "(gentle voice)", "(music plays)").

NO FORMATTING LABELS: Do not use headers like "Intro," "Summary," or "Audio Cues."

NO PREAMBLE: Start the output immediately with the first word of the content. Do not say "Here is the summary."

Start with the line "this page"

 Here is the text: {data} """
response = ollama.chat(
    model='gemma3:270m',
    messages=[{'role': 'user', 'content': prompt}]
)

summary=response['message']['content']

with open('summary.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(summary)