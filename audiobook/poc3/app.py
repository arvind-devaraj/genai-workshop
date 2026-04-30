from flask import Flask, render_template, request, send_file, jsonify
import requests
import os
import io
import json

app = Flask(__name__)

API_URL = "https://api.v7.unrealspeech.com/stream"
API_TOKEN = os.environ.get('UNREAL_TOKEN')

PARAGRAPHS_FILE = os.path.join(os.path.dirname(__file__), 'paragraphs.json')

@app.route('/')
def index():
    with open(PARAGRAPHS_FILE) as f:
        data = json.load(f)
    return render_template('index.html', title=data['title'], segments=data['segments'])

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
        'Speed': '0',
        'Pitch': '1'
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, stream=True)
        if response.status_code == 200:
            # Return the raw audio bytes back to the frontend
            return send_file(
                io.BytesIO(response.content),
                mimetype="audio/mpeg"
            )
        else:
            return jsonify({"error": f"API returned {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Make sure port 5001 isn't being used by another process
    app.run(debug=True, port=5001)