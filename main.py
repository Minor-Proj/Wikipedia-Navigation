import speech_recognition as sr
import os
import wikipedia
from text_to_speech import speak
from wishIntro import wish




def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=1,phrase_time_limit=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-in')
        print(f"user said {query}")
    except Exception as e:
        speak("Please speak again")
        return None
    return query



if __name__ == '__main__':
    wish()

    while True:
        query = takecommand().lower()

        if "open notepad" in query:
            npath = "C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(npath)
        
        elif "wikipedia" in query:
            speak("searching wikipedia")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=2)
            speak("According to wikipedia...")
            speak(results)

        speak("Sir do you have any work")
