# voice_assistant/main.py

# Import Module

import logging
import time
from colorama import Fore, init
import voicerss_tts

# import voice assistant script

from voice_assistant.api_key_manager import get_tts_api_key

from voice_assistant.config import Config

from voice_assistant.recording import play_audio

from voice_assistant.text_to_speech import text_to_speech

# Configure Logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize colorama

init(autoreset=True)

# Voice Rss Configuration

key = '8f7d389a64634ef1a22948f0eb805666'
hl  = 'zh-hk'
v   = 'Jia'
f   = '16khz_16bit_stereo'

# Define text to speech function

def tts():

    """
    
    Main functuin to run text to speech 
    
    """

    #tts_input = "Goodbye! See You Next Time!"
    
    response_text = "拜拜... 期待再次與你聊天..."

    # Determine the output file format based on the TTS model
    if Config.TTS_MODEL == 'openai' or Config.TTS_MODEL == 'elevenlabs' or Config.TTS_MODEL == 'melotts' or Config.TTS_MODEL == 'cartesia':
                output_file = 'output.mp3'
    else:
                output_file = 'output.wav'

    # Get the API key for TTS
    tts_api_key = get_tts_api_key()

    # Convert the response text to speech and save it to the appropriate file

    voice = voicerss_tts.speech({
                'key'   : key,
                'hl'    : hl,
                'src'   : response_text,
                'v'     : v,
                'r'     : '0',
                'c'     : 'wav',
                'f'     : '44khz_16bit_stereo',
                'ssml'  : 'false',
                'b64'   : 'false'
            })

    new_file = open("output.wav", "wb")
    new_file.write(voice['response'])
    new_file.close
            
    # Play the generated speech audio
    play_audio(output_file)


# Call the Main Function While Execute Programm

if __name__ == "__main__":
    
    tts()
