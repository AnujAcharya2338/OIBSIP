from config import API_KEY
import requests
from tkinter import *
import tkinter as tk
THEME_COLOR = "#375362"
root = tk.Tk()
root.title("Weather App")
root.geometry("1000x700+200+100")
root.config(padx=20 , pady=20, bg=THEME_COLOR)



  
question = tk.Label(text = "Enter the name of the city:", fg="white", bg=THEME_COLOR)
question.grid(row=1, column= 1)
city_entry = tk.Entry(root)
city_entry.grid(row=1, column= 2)


               
def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
         "q":city,
         "appid": API_KEY,
         "units": "metric",
    }  
    try:
        response = requests.get(url , params=params, timeout=10)
        return response
    except requests.exceptions.Timeout:
        print("Request timed out. Check your connection and try again.")
        return None
    except requests.exceptions.ConnectionError:
        print("Could not connect. Check your internet connection.")
        return None

def handle_response(response):
     if response is None:
          return None
     elif response.status_code == 200:
          return response.json()
     elif response.status_code == 404:
          print("city not found!! Please reenter the city's name")
          return None   
     elif response.status_code == 401:
          print("Invalid API key")
          return None
     else:
          print(f"Unexpected error occured. {response.status_code}")
          return None

# def display_weather(checked_city):
#     if checked_city is None:
#          return
#     temp = checked_city["main"]["temp"]
#     faran = round((temp * 9/5)+32, 3)
#     hum = checked_city['main']['humidity']
#     description = (checked_city["weather"][0]["description"])
#     wind_speed = checked_city["wind"]["speed"]
#     print(f"The current temperature is {temp}°C or {faran}F")
#     print(f"The current Humidity is {hum}")
#     print(f"Description:{description}")
#     print(f"Wind Speed:{wind_speed}")


def search():
        try:
            city = city_entry.get().strip()
            if not city:
                tk.Label(text = "Please enter the name of the city:", fg="white", bg=THEME_COLOR)
                return
            response = get_weather(city)   
            checked_city = handle_response(response)  
            print(checked_city)          
        except EOFError:
                tk.Label(text = "Please enter the name of the city:", fg="white", bg=THEME_COLOR)


              
               

# city_weather = get_weather(city)
# display_weather(checked_city)


button = tk.Button(root, text="Search", command=search)
button.grid(row=1,column=3)

# result = tk.Frame(root)
# result.grid(row=2,column=3)

root.mainloop()