# Weather App

A desktop weather application built with Python and Tkinter. Enter a city name to see current conditions, an hourly forecast for the next ~18 hours, and a 5-day outlook — all pulled from the OpenWeatherMap API.

## Features

- **Current weather** — temperature (°C and °F), humidity, wind speed, and a matching weather icon
- **Hourly forecast** — next six 3-hour forecast slots (OpenWeatherMap's free tier reports in 3-hour steps, not true hourly)
- **5-day forecast** — one representative reading per day (midday where available) for the next 5 days
- Forecast sections stay hidden until a search succeeds, and clear automatically before each new search
- Graceful handling of network timeouts, connection errors, invalid cities, and invalid API keys

## Requirements

- Python 3.8+
- A free [OpenWeatherMap](https://openweathermap.org/api) API key

### Python packages

```bash
pip install requests pillow
```

(`tkinter` ships with most standard Python installs; on some Linux distros you may need `sudo apt install python3-tk`.)

## Setup

1. Clone or download this project.
2. Create a file named `config.py` in the same directory as the main script, containing:

   ```python
   API_KEY = "your_openweathermap_api_key_here"
   ```

3. Make sure `config.py` is excluded from version control (add it to `.gitignore`) so your API key isn't committed.

## Running the app

```bash
python weather_app.py
```

Enter a city name in the input field and click **Search**. Current conditions, the hourly row, and the 5-day row will populate below.

## Project structure

```
.
├── weather_app.py   # Main application
├── config.py        # Your API key (not committed)
└── README.md
```

## Known limitations

- "Hourly" forecast data is limited to 3-hour intervals due to the OpenWeatherMap free tier.
- City name matching depends on OpenWeatherMap's own geocoding — ambiguous city names may return an unexpected location.