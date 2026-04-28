# Long endpoint: /synthesisTasks
# - Up to 500,000 characters
# - Asynchronous, takes ~1s per 800 chars
# - Returns a TaskId (use to check status)

import requests
import sys

fp=open("contents.txt")
sample_text= fp.read()
print(sample_text)

response = requests.post(
  'https://api.v7.unrealspeech.com/speech',
  headers = {
    'Authorization' : 'Bearer J4AmBk60TbnT49slRIKYW1LyoCoyVsKYwQQjp6mGJHpsip6VVwYCsD'
  },
  json = {
    'Text': sample_text, # Up to 500,000 characters
    'VoiceId': 'Amy', # Dan, Will, Scarlett, Liv, Amy
    'Bitrate': '192k', # 320k, 256k, 192k, ...
    'Speed': '0.15', # -1.0 to 1.0
    'Pitch': '1', # -0.5 to 1.5
    'TimestampType': 'sentence', # word or sentence
   #'CallbackUrl': '<URL>', # pinged when ready
  }
)

print(response.text)