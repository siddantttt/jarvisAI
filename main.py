import speech_recognition as sr
import os
import webbrowser as web
import openai
import datetime
import wikipedia
import requests
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
'''''
#Defining function to give weather updates
def weather():
    api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
        str(g.latlng[0]) + "&lon=" + str(g.latlng[1])

    data = requests.get(api_url)
    data_json = data.json()
    if data_json['cod'] == 200:
        main = data_json['main']
        wind = data_json['wind']
        weather_desc = data_json['weather'][0]
        say(str(data_json['coord']['lat']) + 'latitude' + str(data_json['coord']['lon']) + 'longitude')
        say('Current location is ' + data_json['name'] + data_json['sys']['country'] + 'dia')
        say('weather type ' + weather_desc['main'])
        say('Wind speed is ' + str(wind['speed']) + ' metre per second')
        say('Temperature: ' + str(main['temp']) + 'degree Celsius')
        say('Humidity is ' + str(main['humidity']))
'''''
#Defining unction to get tell current time
def time():
    time = datetime.datetime.now().strftime("%I:%M%p") #The "%p" is used to include the AM/PM indicator to the time format
    return time
#Function to perform addition, subtraction, multiplication and divison
#Needs improvement, does not work currently
def perform_operation():
    say("What calculation do you want to perform")
    query = takeCommand()
    try:
        # Split the query into words and look for keywords like "add" or "subtract"
        words = query.split()
        if "add" or "plus" in words:
            # Extract the numbers to add
            numbers = [int(word) for word in words if word.isdigit()]
            result = sum(numbers)
            return f"The result of addition is {result}"
        elif "subtract" or "minus" in words:
            # Extract the numbers to subtract
            numbers = [int(word) for word in words if word.isdigit()]
            result = numbers[0] - sum(numbers[1:])
            return f"The result of subtraction is {result}"
        elif "multiply" or "product" or "times" in words:
            # Extract the numbers to multiply
            numbers = [int(word) for word in words if word.isdigit()]
            result = 1
            for num in numbers:
                result *= num
            return f"The result of multiplication is {result}"
        elif "divide" in words:
            # Extract the numbers to divide
            numbers = [int(word) for word in words if word.isdigit()]
            result = numbers[0]
            for num in numbers[1:]:
                if num != 0:
                    result /= num
                else:
                    return "Cannot divide by zero"
            return f"The result of division is {result}" 
        else:
            return "Could not understand the operation"

    except:
        return "Could not perform the operation"

if __name__ == '__main__':
    print("This is T.P")
    say("This is T.P")
    while True:
        query = takeCommand()
        #Creating a list of websites to iterate through it and open websites
        # todo: Add more sites
        sites =[
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["pornhub", "https://www.pornhub.com"]
            ]
        for site in sites:
            if f"Open {site[0]}".lower() in query:
                say(f"Opening {site[0]} Sir!!")
                web.open(site[1])
        #Different greeting scenarios for jarvis to respond to
        greetings = [
            ["good morning", "Goodmorning sir. Did you sleep well last night?"],
            ["good night", "Goodnight sir. Hope you sleep well. Do you want me to remind you anything for tomorrow?"],
            ["how are you", "I am doing good sir. How about you"],
        ]
        for greeting in greetings:
            if f"{greeting[0]}".lower() in query:
                say (f"{greeting[1]}")
        #To exit the program
        if "sleep".lower() in query:
            say("Goodbye Sir!")
            break
        #To say the current time in program
        if ("the time").lower() in query:
            currentTime = time()
            say(f"Sir, the current time is {currentTime}")
        #Checking and fetcihng location
        if 'location' in query:
            say('What is the location?')
            location = takeCommand()
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            web.open(url)
            say('Here is the location ' + location)
        
        if ("calculator") in query:
            say("Opening calculator....")
            result = perform_operation()
            say(result)

        if "who are you" in query:
            say("I'm JARVIS created by Sid and I'm a desktop voice assistant.")
            print("I'm JARVIS created by Sid and I'm a desktop voice assistant.")

        #Getting search results
        if ("what is" or "who is" in query):
            modified_query = query.replace("what is", "").strip()
            modified_query = query.replace("who is", "").strip()
            web.open(f"{modified_query}")
            try:
                results = wikipedia.summary(modified_query, sentences = 1)
                say (results)
                print(results)  
            except wikipedia.exceptions.WikipediaException as e:
                print(f"Error retrieving Wikipedia summary: {e}")
        
        #Getting Jarvis to remember something
        if 'remember that' in query:
            say("what should i remember sir")
            rememberMessage = takeCommand()
            say("you said me to remember"+rememberMessage)
            remember = open('data.txt', 'w')
            remember.write(rememberMessage)
            remember.close()

        if 'do you remember anything' in query:
            remember = open('data.txt', 'r')
            say("you said me to remember that" + remember.read())


        
