import speech_recognition as sr
import datetime
import pyttsx3 as pt
import webbrowser 
from urllib.parse import quote_plus


att = sr.Recognizer()
date = datetime.date.today()
time = datetime.datetime.now().time()

def say(text):
    tta = pt.init()
    tta.say(text)
    tta.runAndWait()


while True:
    try:
        with sr.Microphone() as source:
            print("Say something")
            att.adjust_for_ambient_noise(source)
            audio = att.listen(source)
            
        text = att.recognize_google(audio).lower()
        print(text)

        if "hello" in text:
           say("Hello mate! What can i do for you?")

        elif  "date" in text:
            say(f"Today's date is: {date}")

        elif "time" in text:
            say(f"Today's time is: {time}")


        elif "search" in text:
            query = text.split("search", 1)[1].strip()
            quote = quote_plus(query)
            say(f"Searching for {query}")
            webbrowser.open(f"https://google.com/search?q={quote}")

        elif "exit" in text:
            say("Goodbye")
            break



    except sr.UnknownValueError:
        say(f"Couldn't understand your message! Please Speak again!!")


    except sr.RequestError as e:
        say("Check your internet connection pleasee")
        print(e)

    except Exception as e:
        say(f"Didn't get your message ! Please refresh the page!")
        print(e)








