import pyttsx3
from urllib.request import urlopen
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

# text to speech
def speak(text):
    engine.say(text)
    print(text)
    engine.runAndWait()

if __name__ == '__main__':
    # speak("hello")
    # pass
    d="Gravity"
    url = f"https://en.wikipedia.org/wiki/{d}"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    
    speak(text)