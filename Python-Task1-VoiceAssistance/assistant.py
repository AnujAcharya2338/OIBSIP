import speech_recognition as sr
import datetime

att = sr.Recognizer()
date = datetime.date.today()
time = datetime.datetime.now().time()

try:
    with sr.Microphone() as source:
        print("Say something")
        att.adjust_for_ambient_noise(source)
        audio = att.listen(source)
        
    text = att.recognize_google(audio).lower()
    print(text)
    
    if text == "hello":
        print("Hello Matey! How can i help you?")

    elif text == "date":
        print(f"Today date is: {date}")

    elif text == "time":
        print(f"Today time is: {time}")

except sr.UnknownValueError:
    print(f"Couldnt understand init mate")
except sr.RequestError as e:
    print(f"Didn't get your message aye brother ; {e}")
except Exception as e:
    print(f"Someother problem as {e}")








