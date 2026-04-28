# Long endpoint: /synthesisTasks
# - Up to 500,000 characters
# - Asynchronous, takes ~1s per 800 chars
# - Returns a TaskId (use to check status)

import requests


sample_text="""“Everyone holds his fortune in his own hands, like a sculptor the raw material he will fashion into a figure. But it’s the same with that type of artistic activity as with all others: We are merely born with the capability to do it. The skill to mold the material into what we want must be learned and attentively cultivated.” —JOHANN WOLFGANG VON GOETHE

That’s what this book is about, sculpting your mind and your life in the pursuit of mastery. Becoming the best in a craft, emulating the best practicioners in all fields throughout history.

“We imagine that creativity and brilliance just appear out of nowhere, the fruit of natural talent, or perhaps of a good mood, or an alignment of the stars. It would be an immense help to clear up the mystery— to name this feeling of power, to examine its roots, to define the kind of intelligence that leads to it, and to understand how it can be manufactured and maintained. Let us call this sensation mastery— the feeling that we have a greater command of reality, other people, and ourselves. Although it might be something we experience for only a short while, for others— Masters of their field— it becomes their way of life, their way of seeing the world. (Such Masters include Leonardo da Vinci, Napoleon Bonaparte, Charles Darwin, Thomas Edison, and Martha Graham, among many others.) And at the root of this power is a simple process that leads to mastery— one that is accessible to all of us.”

Then Greene gives a high level overview of the process:

We enter a new field with excitement, but also fear about how much there is to learn ahead of us. The greatest danger here is boredom, impatience, fear, and confusion. Once we stop observing and learning, the process towards mastery comes to a halt.
But if we manage these emotions and keep pushing forward, we start to gain fluency, and we master the basic skills allowing us to take on bigger and better challenges.
Eventually, we move from student to practicioner. We use our own ideas and experiments, getting feedback in the process. We start to use our own style
Then as we continue for years we make the leap to mastery. We develop an intuitive sense of the skill and have mastered it to the point of being able to innovate and break the rules.

"""
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