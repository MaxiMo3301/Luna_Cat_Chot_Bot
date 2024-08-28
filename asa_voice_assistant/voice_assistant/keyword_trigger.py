# voice_assistant/keyword_trigger.py

# Import Module

def keyword_trigger(input):

    command = input

    command = command.lower()

    if 'hey luna' or 'hello luna' or 'hi luna' in command:

        return True
    
    if 'play' in command:

        return "musuic"
    
    else:
        
        return "chatbot"