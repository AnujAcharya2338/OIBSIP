import speech_recognition as sr


att = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("Say something")
        att.adjust_for_ambient_noise(source)
        audio = att.listen(source)
        
    text = att.recognize_google(audio)
    print(text)

except sr.UnknownValueError:
    print(f"Couldnt understand init mate")
except sr.RequestError as e:
    print(f"Didn't get your message aye brother ; {e}")
except Exception as e:
    print(f"Someother problem as {e}")




