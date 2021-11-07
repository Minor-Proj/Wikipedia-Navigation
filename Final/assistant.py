# import all necessary modules 
import pyttsx3
import datetime
import speech_recognition as sr
from pygame import mixer
import pygame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import re
import json
import requests
import keyboard

pygame.init()





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


def search_page():
    driver.get("https://www.wikipedia.org")
    time.sleep(1)

def search_wikipedia(text):
    search_bar = driver.find_element_by_id("searchInput")
    search_bar.clear()
    time.sleep(1)
    search_bar.send_keys(text)
    search_bar.send_keys(Keys.RETURN)

def move_down():
    driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")


def move_up():
    driver.execute_script("window.scrollTo(0, window.scrollY - 200)")

def getAllContent():
    allHtmlContent = driver.page_source
    htmlContent = BeautifulSoup(allHtmlContent)
    reqHtmlContent = htmlContent.find(class_ = "mw-parser-output")
    all_links = list(reqHtmlContent.find_all('a'))
    all_headings = list(reqHtmlContent.find_all(['h2','h3']))
    all_paras = list(reqHtmlContent.find_all('p'))
    all_images = list(reqHtmlContent.find_all('img',{'src':re.compile('.jpg')}))
    
    return all_links,all_headings,all_paras,all_images


def webPageStats():
    page_title = driver.find_element_by_id("firstHeading").text.replace(' ','_')
    stats_url = f"https://pageviews.toolforge.org/?project=en.wikipedia.org&platform=all-access&agent=user&redirects=0&range=latest-20&pages={page_title}"
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(stats_url)
    time.sleep(2)
    stats_list = driver.find_elements_by_class_name("linear-legend--counts")
    stats_string = ''
    for i in stats_list:
        if i.text != '':
            stats_string += i.text.rstrip() + "\n"
    speak(stats_string)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])



def showImage(img):
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(img)
            time.sleep(2)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])



def dictionary(word):
    url="https://api.dictionaryapi.dev/api/v2/entries/en/"
    link=url+word
    driver.get(link)
    data_json=requests.get(link).text
    
    json.dumps(data_json)
    #data_json=data_json.json()
  
    data_dict=json.loads(data_json)
    print(type(data_dict))
    return data_dict[0]



def news(word):
    count_code="in"
    Base_URL="https://saurav.tech/NewsAPI/top-headlines/category/"
    mid="/"
    address=".json"
    link=Base_URL+word+mid+count_code+address
    driver.get(link)
    data_json1=requests.get(link).text
    data_news=json.loads(data_json1)
    print(type(data_news))
    return data_news



def main_function():
    wish()
    while True:
        query = ''
        try:
            query = takecommand().lower()
        except UnboundLocalError:
            speak("Try again")
        
        if "exit" in query:
            speak("Exitting! Have a nice day")
            return None

        if  "search page" or "main page" in query:
            search_page()
            time.sleep(1)
            
        if "dictionary" in query:
            speak("searching dictionary")
            query=query.replace("dictionary","")
            query=query.replace(" ","")
            x=dictionary(query)
            speak(x["meanings"][0]["definitions"][0]["definition"])
            time.sleep(2)
            
        if "news" in query:
            speak("fetching news")
            query=query.replace("news","")
            query=query.replace(" ","")
            y=news(query)
            speak("first headline")
            speak(y["articles"][0]["content"])
            speak("second headline")
            speak(y["articles"][1]["content"])
            speak("third headline")
            speak(y["articles"][2]["content"])
            time.sleep(3)
            
        if "google" in query:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://www.google.com")
            time.sleep(2)
            search_bar = driver.find_element_by_name("q")
            search_bar.clear()
            search_text = query.replace("google","")
            search_bar.send_keys(search_text)
            search_bar.send_keys(Keys.RETURN)
            time.sleep(4)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
        if "wikipedia" in query:
            speak("searching wikipedia")
            query = query.replace("wikipedia","")
            search_wikipedia(query)
            
            # Scrapping content from wikipedia
            all_links,all_headings,all_paras,all_images = getAllContent()
            
            # initially
            curr_link = all_links[0]
            curr_heading = all_headings[1]
            curr_para = all_paras[0]
            curr_image = all_images[0]
            
            # length of all contents
            all_link_len = len(all_links)
            all_heading_len = len(all_headings)
            all_para_len = len(all_paras)
            all_image_len = len(all_images)
            imgList=[]
            for images in all_images:
                imgList.append(images['src'])
            imgIndex=0
            
            
            # 2 lines , total link,heading,paras,images
            starting = f"This page has {all_link_len} links, {all_heading_len} headings, {all_para_len} paragraphs, {all_image_len} images"
            
            speak(starting)
            time.sleep(2)
            
            while True:

                # take speech input to be done.  ---------------
                speak("Tell me what to do")
                query2 = ''
                try:
                    query2 = takecommand().lower()
                    print("query2: " , query2)
                except UnboundLocalError:
                    speak("Try again")
                    
                if "exit" in query2:
                    speak("Exitting! Have a nice day")
                    return None

                #move up (working)
                if "up" in query2:
                    # if already on the top, then speak feedback ---------------
                    move_up()
                    
                # move down
                elif "down" in query2:
                    # if already on the bottom, then speak feedback ---------------
                    move_down()
                
                # web page statistics  (working)
                elif "stats" in query2 or "statistics" in query2: 
                    webPageStats()
                    time.sleep(2)
                    
                # next link
                elif "next link" in query2:
                    curr_link_index = all_links.index(curr_link)
                    if curr_link_index == all_link_len-1:
                        # do it for all others as well ---------------
                        speak("All links visited")
                    elif curr_link_index < all_link_len:
                        curr_link_index += 1
                        curr_link = all_links[curr_link_index]
                    
                    # locating link in opened tab
                    ActionChains(driver).move_to_element(driver.find_element_by_link_text(curr_link.get_text())).perform()
                    time.sleep(1)
                    speak(curr_link.get_text())

                    
                # prev link
                elif "previous link" in query2:
                    if curr_link_index == 0:
                        # do it for all others as well ---------------
                        speak("Already on first link")
                    curr_link_index = all_links.index(curr_link)
                    if curr_link_index > 0:
                        curr_link_index -= 1
                        curr_link = all_links[curr_link_index]
                        
                    # locating link in opened tab                
                    speak(curr_link.get_text())
                    ActionChains(driver).move_to_element(driver.find_element_by_link_text(curr_link.get_text())).perform()
                    time.sleep(1)
                
                
                #next heading ---------------
                elif "next heading" in query2:
                    curr_heading_index = all_headings.index(curr_heading)
                    if curr_heading_index < all_heading_len:
                        curr_heading_index += 1
                        curr_heading = all_headings[curr_heading_index]

                        
                    #locating heading in tab
                    speak(curr_heading.get_text())
                    curr_heading_id = curr_heading.get_text().replace(" ","_").replace("[edit]",'')
                    ActionChains(driver).move_to_element(driver.find_element_by_id(curr_heading_id)).perform()
                    time.sleep(1)
            
            
            
                # prev heading ---------------
                elif "previous heading" in query2:
                    curr_heading_index = all_headings.index(curr_heading)
                    if curr_heading_index > 1:
                        curr_heading_index -= 1
                        curr_heading = all_headings[curr_heading_index]

                    #locating heading in tab
                    speak(curr_heading.get_text())
                    curr_heading_id = curr_heading.get_text().replace(" ","_").replace("[edit]",'')
                    ActionChains(driver).move_to_element(driver.find_element_by_id(curr_heading_id)).perform()
                    time.sleep(1)
                
                # next para ---------------
                elif "next para" in query2 or "next paragraph" in query2:
                    curr_para_index = all_paras.index(curr_para)
                    if curr_para_index < all_para_len:
                        curr_para_index += 1
                        curr_para = all_paras[curr_para_index]
                    
                    speak(curr_para.get_text())
                
                
                # prev para ---------------
                elif "previous para" in query2 or "previous paragraph" in query2:
                    curr_para_index = all_paras.index(curr_para)
                    if curr_para_index > 0:
                        curr_para_index -= 1
                        curr_para = all_paras[curr_para_index]
                
                    speak(curr_para.get_text())
                
                
    #             next image
                elif "next image" in query2:
                    if imgIndex<len(imgList):
                        imgIndex+=1
                        showImage("https:"+imgList[imgIndex])
    

                # previous image
                elif "previous image" in query2:
                    if imgIndex > 0:
                        imgIndex -= 1
                        showImage("https:"+imgList[imgIndex])
                
                
                # go to main page  ---------------
                # then break this loop
                elif "main page" in query2 or "search page" in query2:
                    speak("Main page loading...")
                    search_page()
                    break
                
                
                # go to google page   ("xyz google")  ---------------
                # first do what he says,then break this loop
                
                    



if __name__ == '__main__':
    
    # create window for navigation
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    # driver.maximize_window()
    time.sleep(2)
    search_page()
    speak("To initiate the wikipedia assistant, press space bar key!")

    while True:
        if keyboard.read_key() == "space":
            print("You pressed space")
            speak("Space Bar key pressed")
            search_page()
            main_function()

    
