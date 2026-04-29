import json
import hashlib
import requests
import timeout_decorator
import os

API_URL = "https://api.v7.unrealspeech.com/speech"

API_TOKEN = os.environ.get('UNREAL_TOKEN')

prefix=len("https://unreal-expire-in-90-days.s3-us-west-2.amazonaws.com/")
suffix=len(".mp3")



#@timeout_decorator.timeout(7)
def create_audio(content):
    response = requests.post(
                    API_URL,
                    headers={
                        'Authorization': f'Bearer {API_TOKEN}'
                    },
                    json={
                        'Text': content,
                        'VoiceId': 'Amy',
                        'Bitrate': '192k',
                        'Speed': '0.1',
                        'Pitch': '1',
                        'TimestampType': 'sentence'
                    }
                )

    json_response=response.json()
    #print(json_response)
    # Return the API response to the user
    return json_response['OutputUri']



with open('data/page29.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    print(text)

if __name__ == '__main__':
    
        print(create_audio(text))

