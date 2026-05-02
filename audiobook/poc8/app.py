from flask import Flask, render_template, request, send_file, jsonify
import requests
import os
import io
import json
import hashlib

app = Flask(__name__)

API_URL = "https://api.v7.unrealspeech.com/stream"
API_TOKEN = os.environ.get('UNREAL_TOKEN')

PARAGRAPHS_FILE = os.path.join(os.path.dirname(__file__), 'paragraphs.json')
CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

@app.route('/')
def index():
    with open(PARAGRAPHS_FILE) as f:
        data = json.load(f)
    return render_template('index.html', segments=data)

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    # This strictly handles the POST request from the JavaScript
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'Text': data['text'],
        'VoiceId': 'Amy',
        'Bitrate': '192k',
        'Speed': '0.1',
        'Pitch': '1'
    }

    text = data['text']
    text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
    cache_path = os.path.join(CACHE_DIR, f"{text_hash}.mp3")

    if os.path.exists(cache_path):
        return send_file(cache_path, mimetype="audio/mpeg")

    try:
        print("external api")
        response = requests.post(API_URL, headers=headers, json=payload, stream=True)
        if response.status_code == 200:
            audio_bytes = response.content
            with open(cache_path, 'wb') as f:
                f.write(audio_bytes)
            return send_file(cache_path, mimetype="audio/mpeg")
        else:
            return jsonify({"error": f"API returned {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Make sure port 5001 isn't being used by another process
    app.run(debug=True, port=5001)