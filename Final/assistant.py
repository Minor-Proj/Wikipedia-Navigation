# import all necessary modules 
import pyttsx3
import datetime
import speech_recognition as sr
from pygame import mixer
mixer.init()

# text to speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def speak(text):
    engine.say(text)
    print(text)
    engine.runAndWait()



# introduction 
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 6 and hour <= 12:
        speak("Good morning")
    elif hour > 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    
    speak("I am your wikipedia assistant, what do you want to search")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        
        mixer.init()
        mixer.music.load('Sounds/listen_sound.mp3')  
        mixer.music.play()
        
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        q = r.recognize_google(audio,language='en-in')
        print(f"user said {q}")
        mixer.init()
        mixer.music.load('Sounds/recognise_sound.mp3')  
        mixer.music.play()
        
        print("Recognizing...")
    except UnboundLocalError:
        speak("Sorry could not recognise,try again")
        takecommand()
    except LookupError:                                 # speech is unintelligible
        print("Could not understand audio")
    finally:
        return q


# wish()
takecommand()
# mixer.music.load('Sounds/recognise_sound.mp3')  
# mixer.music.play()


# mixer.music.load('Sounds/listen_sound.mp3')  
# print("Hello")
# mixer.music.play()