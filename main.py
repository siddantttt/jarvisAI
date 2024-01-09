import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import wikipedia

#Defining a function to say out loud
def say(text):
    os.system(f"say {text}")

#Defining a function to take command
def takeCommand():
    # Create a recognizer (r) object from the SpeechRecognition library
    r = sr.Recognizer()
    
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        # Print a message to indicate that the system is listening
        print("Listening....")
        # Set an initial energy threshold (you may need to experiment with this value)
        r.energy_threshold = 3000 
        # Capture audio input from the microphone
        audio = r.listen(source)
        try:
            # Use Google Speech Recognition to convert the audio to text
            query = r.recognize_google(audio, language = "en-us") #Language is US English
            print(f"User said: {query}") # Print the recognized text
            return query.lower() # Return the recognized text in lowercase for easier processing
        
        # If the audio cannot be understood, return an appropriate message
        except sr.UnknownValueError:
            return "Could not understand the audio"
        
        # If there is an error with the Google Speech Recognition service, return an error message
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

def time():
    time = datetime.datetime.now().strftime("%I:%M:%S")
    say(f"Sir, the current time is {time}")
    print(f"Sir, the current time is {time}")

if __name__ == '__main__':
    print("This is Jarvis")
    say("Hello I am Jarvis A.I")
    while True:
        query = takeCommand()
        #Creating a list of websites to iterate through it and open websites
        # todo: Add more sites
        sites =[
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"]
            ]
        for site in sites:
            if f"Open {site[0]}".lower() in query:
                say(f"Opening {site[0]} Sir!!")
                webbrowser.open(site[1])
        #To exit the program
        if "sleep".lower() in query:
            say("Goodbye Sir!")
            break
        #To say the current time in program
        if ("the time").lower() in query:
            time()

        #To search something in wikipedia
        if "wikipedia" in query:
            try:
                say("Wikipedia is open sir. What do you want me to search?")
                query = query.replace("wikipedia","")
                result = wikipedia.summary(query, sentences=2)
                print(result)
                say(result)
            except:
                say("Can't find this page sir, please ask something else")
        #Getting Jarvis to remember something
        if "remember that" in query:
            say("What should I remember")
            data = takeCommand()
            say("You said me to remember that" + data)
            print("You said me to remember that " + str(data))
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        #Asking if Jarvis Remembers anything
        elif "do you remember anything" in query:
            remember = open("data.txt", "r")
            say("You told me to remember that" + remember.read())
            print("You told me to remember that " + str(remember))
        