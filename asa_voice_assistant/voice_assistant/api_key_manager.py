# voice_assistant/api_key_manager.py

# Import Module

from voice_assistant.config import Config

# Config Function for getting different API Key
# get Speech To Text API Key

def get_transcription_api_key():

    """
    Select the correct API key for transcription based on the configured model.
    
    Returns:
    str: The API key for the transcription service.
    """

    if Config.TRANSCRIPTION_MODEL == 'groq':

        return Config.GROQ_API_KEY
    
    elif Config.TRANSCRIPTION_MODEL == 'deepgram':

        return Config.DEEPGRAM_API_KEY
    
    return None

# get LLM API Key

def get_response_api_key():

    """
    Select the correct API key for response generation based on the configured model.
    
    Returns:
    str: The API key for the response generation service.
    """

    if Config.RESPONSE_MODEL == 'groq':

        return Config.GROQ_API_KEY
    
    return None

# Get Text To Speech API Key

def get_tts_api_key():

    """
    Select the correct API key for text-to-speech based on the configured model.
    
    Returns:
    str: The API key for the TTS service.
    """

    if Config.TTS_MODEL == 'deepgram':

        return Config.DEEPGRAM_API_KEY

    if Config.TTS_MODEL == 'voicerss':

        return Config.VOICERSS_API_KEY

    return None