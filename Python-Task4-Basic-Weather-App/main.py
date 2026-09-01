from config import API_KEY
import requests


def get_city():
    while True:
            try:
                city_name = input("Enter the city's name:")
                city = city_name.strip()

                if not city:
                     print("Please enter the city's name:")
                     continue
                return city
                
            except EOFError:
                print("Please enter the name of a city.")

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

def display_weather(checked_city):
    if checked_city is None:
         return
    temp = checked_city["main"]["temp"]
    faran = round((temp * 9/5)+32, 3)
    hum = checked_city['main']['humidity']
    description = (checked_city["weather"][0]["description"])
    wind_speed = checked_city["wind"]["speed"]
    print(f"The current temperature is {temp}°C or {faran}F")
    print(f"The current Humidity is {hum}")
    print(f"Description:{description}")
    print(f"Wind Speed:{wind_speed}")
          
city = get_city()
city_weather = get_weather(city)
checked_city = handle_response(city_weather)
display_weather(checked_city)