# voice_assistant/main.py

# Import Module

import logging
import time
from colorama import Fore, init
import voicerss_tts

from voice_assistant.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key

from voice_assistant.config import Config

from voice_assistant.llm import generate_response

from voice_assistant.recording import record_audio, play_audio

from voice_assistant.text_to_speech import text_to_speech

from voice_assistant.transcription import transcribe_audio

from voice_assistant.utils import delete_file

# Configure Logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize colorama

init(autoreset=True)

# File Path for the music player

musice_file = "music.mp3"
eng_file    = "eng.mp3"
cn_file     = "cn.mp3"
piano_file  = "piano.mp3"
rock_file   = "rock.mp3"
comfirm_file = "alert_v2.wav"

reaction    = "reaction_can.wav"
goodbye = "goodbye_can.wav"
help_ack = "acknowledge.wav"

# Voice Rss Configuration

key = '8f7d389a64634ef1a22948f0eb805666'
hl  = 'zh-hk'
v   = 'Jia'
f   = '16khz_16bit_stereo'

# Define the chat bot function

def chat_bot():

    """

    Main function to run the voice assistant.

    """
    
    chat_history = [
        {"role": "assistant", "content": "你是一位樂於助人的助理。你的名字是露娜。只以中文粵語回答，如果是提出建議，當選項多於一個時，只提出其中一項便可。"}
    ]

    counter = None

    while True:
        try:

            # Record audio from the microphone and save it as 'test.wav'
            record_audio(Config.INPUT_AUDIO)

            # Get the API key for transcription
            transcription_api_key = get_transcription_api_key()
            
            # Transcribe the audio file
            user_input = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.INPUT_AUDIO)

            # Check if the transcription is empty and restart the recording if it is. This check will avoid empty requests if vad_filter is used in the fastwhisperapi.
            if not user_input:

                logging.info("No transcription was returned. Starting recording again.")

                continue

            logging.info(Fore.GREEN + "You said: " + user_input + Fore.RESET)

            # Check if the user wants to exit the program
            if "goodbye" in user_input.lower() or "再見" in user_input.lower() or "拜拜" in user_input.lower():

                play_audio(goodbye)

                break

            if "play me some music" in user_input.lower():

                play_audio(musice_file)

                break

            if "play me some chinese music" in user_input.lower():

                play_audio(cn_file)

                break

            if "play me some english music" in user_input.lower():

                play_audio(eng_file)

                break

            if "play me some piano music" in user_input.lower():

                play_audio(piano_file)

                break

            if "play me some rock music" in user_input.lower():

                play_audio(rock_file)

                break

            # Append the user's input to the chat history
            chat_history.append({"role": "user", "content": user_input})

            # Get the API key for response generation
            response_api_key = get_response_api_key()

            # Generate a response
            response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, chat_history)
            
            response_text = response_text.replace('*', '')
            
            response_text = response_text.replace('＊', '')
              
            logging.info(Fore.CYAN + "Response: " + response_text + Fore.RESET)

            # Append the assistant's response to the chat history
            chat_history.append({"role": "assistant", "content": response_text})

            # Determine the output file format based on the TTS model
            if Config.TTS_MODEL == 'openai' or Config.TTS_MODEL == 'elevenlabs' or Config.TTS_MODEL == 'melotts' or Config.TTS_MODEL == 'cartesia':
                output_file = 'output.mp3'
            else:
                output_file = 'output.wav'

            # Get the API key  for TTS
            tts_api_key = get_tts_api_key()

            # play the reaction file for acknowledgement

            play_audio(reaction, wait = 0)

            start = time.time()
            # Convert the response text to speech and save it to the appropriate file
            #text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, output_file)
            
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
            
            end = time.time()
            tts_duration = end - start

            logging.info(tts_duration)
            while (tts_duration < 2.6):
                time.sleep(0.1)
                end = time.time()
                tts_duration = end - start
            # Play the generated speech audio
            play_audio(output_file)
            
            # Clean up audio files
            # delete_file(Config.INPUT_AUDIO)
            # delete_file(output_file)

            time.sleep(1)

        except Exception as e:
            logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
            delete_file(Config.INPUT_AUDIO)
            if 'output_file' in locals():
                delete_file(output_file)
            time.sleep(1)

# Define Emergency Call Function

def emergency_call():

    play_audio(help_ack)

# Define Keyword Trigger Function

def keyword_trigger():

    while True:

        try:    

            # Clean Keyword

            keyword = None

            # Record audio from the microphone and save it as 'test.wav'
            record_audio(Config.INPUT_AUDIO, ready=0, )

            # Get the API key for transcription
            transcription_api_key = get_transcription_api_key()
            
            # Transcribe the audio file
            user_input = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.INPUT_AUDIO)

            # Check if the transcription is empty and restart the recording if it is. This check will avoid empty requests if vad_filter is used in the fastwhisperapi.
            if not user_input:

                logging.info("No transcription was returned. Starting recording again.")

                continue

            logging.info(Fore.GREEN + "You said: " + user_input + Fore.RESET)

            keyword = user_input.lower()

            print(keyword)

            if "luna" in keyword or "露娜" in keyword:

                chat_bot()

            elif "help me" in keyword or "救命" in keyword:

                emergency_call()

            else:
                
                logging.info("Keyword is not right. Run the keyword trigger again.")

                continue


        except Exception as e:
            logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
            delete_file(Config.INPUT_AUDIO)
            time.sleep(1)
            
# Define Main Function

def main():

    while True:
            
        keyword_trigger()

# Call the Main Function While Execute Programm

if __name__ == "__main__":
    main()
