import requests
import os

# Updated URL for the stream endpoint
API_URL = "https://api.v7.unrealspeech.com/stream"
API_TOKEN = os.environ.get('UNREAL_TOKEN')

def create_audio_stream(content, output_filename="output.mp3"):
    """
    Calls the stream API and saves the binary content to a local file.
    """
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'Text': content,
        'VoiceId': 'Amy', # Note: Ensure your tier supports this voice
        'Bitrate': '192k',
        'Speed': '0',     # 0 is default/normal speed in the stream API
        'Pitch': '1'
    }

    # Use stream=True to handle large data chunks efficiently
    response = requests.post(API_URL, headers=headers, json=payload, stream=True)

    if response.status_code == 200:
        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return f"Success: Saved to {output_filename}"
    else:
        return f"Error {response.status_code}: {response.text}"

if __name__ == '__main__':
    # Load your text
    text="""
Inference Optimization: Making Models Faster and Cheaper

New models come and go, but one thing remains constant: continually improving them to be better, cheaper, and faster. Until now, the book has explored various methods for enhancing model performance. This chapter shifts focus towards optimizing these models for speed and cost efficiency.

"""    
    print(len(text))
    print("Processing stream...")
    result = create_audio_stream(text)
    print(result)
