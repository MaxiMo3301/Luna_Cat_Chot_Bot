# voice_assistant/recording.py

# Importing Module

import speech_recognition as sr
import pygame
import time
import logging
import pydub

from io import BytesIO
from pydub import AudioSegment

# Audio path

meow = "alert.wav"

# Playing Audio Function

def play_audio(file_path, wait = 1):

    """

    Play am audio file using pygame.

    Args:

    file_path(str): The Path to the Audio file to play.

    """

    try:

        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        if (wait):
            while pygame.mixer.music.get_busy():

                time.sleep(0.1)

            pygame.mixer.quit()
        
    except pygame.error as e:

        logging.error(f"Failed to play audio: {e}")

    except Exception as e:

        logging.error(f"An unexpected error occurred while playing audio: {e}")

# Recording Audio Function

def record_audio(file_path, timeout=10, phrase_time_limit=None, retries=3, energy_threshold=2000, pause_threshold=1, phrase_threshold=0.1, dynamic_energy_threshold=True, calibration_duration=1, ready = 1):

    """

    Record audio from the microphone and save it as an MP3 file.
    
    Args:

    file_path (str): The path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    retries (int): Number of retries if recording fails.
    energy_threshold (int): Energy threshold for considering whether a given chunk of audio is speech or not.
    pause_threshold (float): How much silence the recognizer interprets as the end of a phrase (in seconds).
    phrase_threshold (float): Minimum length of a phrase to consider for recording (in seconds).
    dynamic_energy_threshold (bool): Whether to enable dynamic energy threshold adjustment.
    calibration_duration (float): Duration of the ambient noise calibration (in seconds).

    """

    # Config Speech Recognizer

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = energy_threshold
    recognizer.pause_threshold = pause_threshold
    recognizer.phrase_threshold = phrase_threshold
    recognizer.dynamic_energy_threshold = dynamic_energy_threshold

    # Config Recording Setting

    with sr.Microphone() as source:

        logging.info("Calibrating for ambient noise...")

        recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)

    # Recording

    for attempt in range(retries):
        try:

            # play the signal for recording
            if ready == 1:
                
                play_audio(meow)

            
            with sr.Microphone() as source:

                # Listen for the first phrase and extract it into audio data

                logging.info("Recording Start")

                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info("Recording complete")

                # Convert the recorded audio data to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = pydub.AudioSegment.from_wav(BytesIO(wav_data))
                mp3_data = audio_segment.export(file_path, format="mp3", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
                
                return
            
        except sr.WaitTimeoutError:

            logging.warning(f"Listening timed out, retrying... ({attempt + 1}/{retries})")

        except Exception as e:

            logging.error(f"Failed to record audio: {e}")
            
            break
    else:
        logging.error("Recording failed after all retries")
