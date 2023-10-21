from gtts import gTTS
import os

# https://gtts.readthedocs.io/en/latest/index.html
# https://ss64.com/osx/afplay.html

def text_to_speech(text, output_filename, lang='en', tld='co.za', playback_rate=1.25):
    # Initialize gTTS with the text to convert
    speech = gTTS(text, lang=lang, tld=tld)

    # Save the audio file to a temporary file
    speech_file = f'{output_filename}.mp3'
    speech.save(speech_file)

    # Play the audio file
    os.system('afplay ' + speech_file + f' -r {playback_rate}')


# Example
## text = "Global warming is the long-term rise in the average temperature of the Earth's climate system"
## text_to_speech(text, 'sample_speech')
