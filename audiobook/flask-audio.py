import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to generate speech
@app.route('/api/generate-speech', methods=['POST'])
def generate_speech():
    data = request.json
    text = data.get('text')
    print(text)
    api_key = os.getenv('UNREAL_TOKEN')

    API_URL = "https://api.v7.unrealspeech.com/speech"

    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    payload={
        'Text': text,
        'VoiceId': 'Amy',
        'Bitrate': '192k',
        'Speed': '0.1',
        'Pitch': '1',
        'TimestampType': 'sentence'
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        print(response)
        print(response.json().get('OutputUri'))
        response.raise_for_status()
        return jsonify({'audioUrl': response.json().get('OutputUri')})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)