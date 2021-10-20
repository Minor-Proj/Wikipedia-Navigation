import datetime
from text_to_speech import speak


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 6 and hour <= 12:
        speak("Good morning")
    elif hour > 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    
    speak("i am jarvis sir, please tell me how can i help you")
    
