from config import API_KEY
import requests
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from io import BytesIO

THEME_COLOR = "#375362"

root = tk.Tk()
root.title("Weather App")
root.geometry("1000x700+200+100")
root.config(padx=20, pady=20, bg=THEME_COLOR)

main_frame = tk.Frame(root, bg=THEME_COLOR)
main_frame.pack(pady=20)

question = tk.Label(main_frame,text="Enter the name of the city:",fg="white",bg=THEME_COLOR)
question.grid(row=0, column=0, padx=5, pady=5)

city_entry = tk.Entry(main_frame)
city_entry.grid(row=0, column=1, padx=5, pady=5)

result_frame = tk.Frame(root, bg=THEME_COLOR)
result_frame.pack(pady=(10,5))

result = tk.Label(result_frame,text="",fg="white",bg=THEME_COLOR)
result.grid(row=0, column=0, padx=10)

result1 = tk.Label(result_frame,text="",fg="white",bg=THEME_COLOR)
result1.grid(row=0, column=1, padx=10)

result2 = tk.Label(result_frame,text="",fg="white",bg=THEME_COLOR)
result2.grid(row=0, column=2, padx=10)

result3 = tk.Label(result_frame,text="",fg="white",bg=THEME_COLOR)
result3.grid(row=0, column=3, padx=10)

icon_label = tk.Label(root, bg=THEME_COLOR)
icon_label.pack(pady=(10,5))

hourly_title = tk.Label(root, text="Next hours", fg="white", bg=THEME_COLOR, font=("Arial", 12, "bold"))
hourly_frame = tk.Frame(root, bg=THEME_COLOR)

daily_title = tk.Label(root, text="Next 5 days", fg="white", bg=THEME_COLOR, font=("Arial", 12, "bold"))
daily_frame = tk.Frame(root, bg=THEME_COLOR)

# hourly_title.place_forget()
# hourly_frame.place_forget()
# daily_title.place_forget()
# daily_frame.place_forget()

hourly_icon_refs = []
daily_icon_refs = []

def clear_weather():
    result.config(text="")
    result1.config(text="")
    result2.config(text="")
    result3.config(text="")
    icon_label.config(image="")
    icon_label.image = None
    for widget in hourly_frame.winfo_children():
        widget.destroy()
    for widget in daily_frame.winfo_children():
        widget.destroy()
    hourly_icon_refs.clear()
    daily_icon_refs.clear()
    hourly_title.place_forget()
    hourly_frame.place_forget()
    daily_title.place_forget()
    daily_frame.place_forget()
     
def get_icon_image(icon_code):
    try:
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        response = requests.get(icon_url, timeout=10)
        image = Image.open(BytesIO(response.content))
        return ImageTk.PhotoImage(image)
    except Exception:
        return None


def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }
    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )
        return response
    except requests.exceptions.Timeout:
        return "timeout"
    except requests.exceptions.ConnectionError:
        return "connection"
    
def get_forecast(city):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        return requests.get(url, params=params, timeout=10)
    except requests.exceptions.Timeout:
        return "timeout"
    except requests.exceptions.ConnectionError:
        return "connection"

def handle_response(response):
    if response == "timeout":
        return None, "Request timed out. Check your connection and try again."
    if response == "connection":
        return None, "Could not connect. Check your internet connection."
    if response is None:
        return None, "Something is wrong."
    if response.status_code == 200:
        return response.json(), None
    if response.status_code == 404:
        return None, "City not found! Please reenter the city's name."
    if response.status_code == 401:
        return None, "Invalid API key."
    return None, f"Unexpected error occurred. {response.status_code}"

def display_weather(checked_city):
    temp = round(checked_city["main"]["temp"])
    faran = round((temp * 9 / 5) + 32, 3)
    hum = checked_city["main"]["humidity"]
    wind_speed = checked_city["wind"]["speed"]
    icon_code = checked_city["weather"][0]["icon"]
    
    icon = get_icon_image(icon_code)
    if icon:
        icon_label.config(image=icon)
        icon_label.image = icon

    result.config(text=f"Temperature: {temp}°C")
    result1.config(text=f"Fahrenheit: {faran}°F")
    result2.config(text=f"Humidity: {hum}%")
    result3.config(text=f"Wind: {wind_speed} m/s")
    
def display_hourly(forecast_data):
    hourly_title.pack(pady=(10, 5))
    hourly_frame.pack(pady=(0, 15))
    
    entries = forecast_data["list"][:6] 
    for i, entry in enumerate(entries):
        time_str = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
        temp = round(entry["main"]["temp"])
        icon_code = entry["weather"][0]["icon"]

        col_frame = tk.Frame(hourly_frame, bg=THEME_COLOR)
        col_frame.grid(row=0, column=i, padx=12)

        tk.Label(col_frame, text=time_str, fg="white", bg=THEME_COLOR).pack()

        icon = get_icon_image(icon_code)
        icon_widget = tk.Label(col_frame, bg=THEME_COLOR)
        if icon:
            icon_widget.config(image=icon)
            icon_widget.image = icon
            hourly_icon_refs.append(icon)
        icon_widget.pack()

        tk.Label(col_frame, text=f"{temp}°C", fg="white", bg=THEME_COLOR).pack()
     
def display_daily(forecast_data):
    daily_title.pack(pady=(10, 5))
    daily_frame.pack(pady=(0, 15))
    entries = forecast_data["list"]
    daily_by_date = {}
    for entry in entries:
        date_str = entry["dt_txt"].split(" ")[0]
        if date_str not in daily_by_date or entry["dt_txt"].endswith("12:00:00"):
            daily_by_date[date_str] = entry

    dates = list(daily_by_date.keys())[:5]

    for i, date_str in enumerate(dates):
        entry = daily_by_date[date_str]
        day_label = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a %d %b")
        temp = round(entry["main"]["temp"])
        icon_code = entry["weather"][0]["icon"]

        col_frame = tk.Frame(daily_frame, bg=THEME_COLOR)
        col_frame.grid(row=0, column=i, padx=12)

        tk.Label(col_frame, text=day_label, fg="white", bg=THEME_COLOR).pack()

        icon = get_icon_image(icon_code)
        icon_widget = tk.Label(col_frame, bg=THEME_COLOR)
        if icon:
            icon_widget.config(image=icon)
            icon_widget.image = icon
            daily_icon_refs.append(icon)
        icon_widget.pack()

        tk.Label(col_frame, text=f"{temp}°C", fg="white", bg=THEME_COLOR).pack()

def search():
    clear_weather()
    city = city_entry.get().strip()
    if not city:
        result.config(text="Please enter the name of the city.")
        return

    weather_data, error = handle_response(get_weather(city))
    if error:
        result.config(text=error)
        return
    display_weather(weather_data)

    forecast_data, forecast_error = handle_response(get_forecast(city))
    if forecast_error:
        return  
    display_hourly(forecast_data)
    display_daily(forecast_data)


button = tk.Button(main_frame,text="Search",command=search)

button.grid(row=0,column=2,padx=5,pady=5)


root.mainloop()