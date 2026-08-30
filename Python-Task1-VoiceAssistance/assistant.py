import speech_recognition as sr
import datetime
import pyttsx3 as pt
import webbrowser 
from urllib.parse import quote_plus


att = sr.Recognizer()
tta = pt.init()
date = datetime.date.today()
time = datetime.datetime.now().time()

try:
    with sr.Microphone() as source:
        print("Say something")
        att.adjust_for_ambient_noise(source)
        audio = att.listen(source)
        
    text = att.recognize_google(audio).lower()

    if "hello" in text:
        tta.say("Hello Matey! How can i help you?")
        tta.runAndWait()


    elif  "date" in text:
        tta.say(f"Today's date is: {date}")
        tta.runAndWait()

    elif "time" in text:
        tta.say(f"Today's time is: {time}")
        tta.runAndWait()

    elif "search" in text:
        query = text.split("search", 1)[1].strip()
        quote = quote_plus(query)
        webbrowser.open(f"https://google.com/search?q={quote}")


except sr.UnknownValueError:
    print(f"Couldnt understand init mate")
except sr.RequestError as e:
    print(f"Didn't get your message aye brother : {e}")
except Exception as e:
    print(f"Someother problem as {e}")








