# Voice Assistant

A Python-based voice assistant built for the Oasis Infobyte Python Programming internship (Task 1). It listens for spoken commands via microphone and responds with synthesized speech.

## Features (Beginner Tier — Complete)

- Captures voice input via microphone (`speech_recognition`)
- Responds to greetings ("hello")
- Tells the current date and time
- Performs a web search on a spoken topic ("search for ...") by opening the default browser
- Graceful error handling — asks the user to try again if speech isn't understood, and keeps listening in a loop until an "exit" command is given
- Text-to-speech feedback (`pyttsx3`) for every response, including errors


## Setup

1. Install dependencies:

   pip install speech_recognition pyttsx3 pyaudio

   Note: `pyaudio` can require extra system-level setup depending on your OS — see the `speech_recognition` PyPI page for platform-specific install notes.

2. Run the assistant:

   python assistant.py
   

3. Speak a command when prompted ("Say something"). Say "exit" to quit.

## Data & Privacy

- **Microphone audio** is captured locally and sent to Google's speech recognition service (via the `speech_recognition` library) to be converted into text. Audio is not saved to disk or stored anywhere by this application.

- **No conversation history or personal data is retained** between sessions — each run starts fresh, and nothing is logged beyond console output for debugging.

- **Web searches**: when a "search" command is used, the resulting query is sent to Google via a standard browser search URL — the same as typing it into a browser directly.

- As Advanced-tier features (email, weather, reminders) are added, this section will be updated to reflect any additional external services or credentials involved.

## Tech Stack

Python, `speech_recognition`, `pyttsx3`, `webbrowser`, `urllib.parse`