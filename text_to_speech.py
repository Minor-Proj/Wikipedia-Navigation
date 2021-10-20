import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

# text to speech
def speak(text):
    engine.say(text)
    print(text)
    engine.runAndWait()

if __name__ == '__main__':
    # speak("hello sir")
    pass