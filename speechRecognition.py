import speech_recognition as sr
import os
import webbrowser
import openai
import datetime

#Defining a function to say out loud
def say(text):
    os.system(f"say {text}")
#Defining a function to take command
def takeCommand():
    r = sr.Recognizer()
    print("Listening....")
    with sr.Microphone() as source:
        # Set an initial energy threshold (you may need to experiment with this value)
        r.energy_threshold = 3000  # Adjust this value based on your environment
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language = "en-us") #Language is US English
            print(f"User said: {query}")
            return query 
        except Exception as e:
            return "Some error occoured. Sorry from Jarvis"

if __name__ == '__main__':
    print("This is Jarvis")
    say("Hello I am Jarvis A.I")
    while True:
        query = takeCommand()
        sites =[
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"]
            
            ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Sir!!")
                webbrowser.open(site[1])
        if "Sleep".lower() in query.lower():
            say("Goodbye Sir!")
            break
        if ("the time").lower() in query.lower():
            hours = datetime.datetime.now().strftime("%H")
            mins = datetime.datetime.now().strftime("%M")
            say(f"Sir, it's {hours},{mins}")
