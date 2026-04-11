import datetime
import time
import platform
import os
import threading
import wikipedia
import pyjokes
import webbrowser
import requests
import json
import subprocess
import re
import random
import sys
import glob
import pyautogui
import win32gui
import operator
import cv2
import urllib.parse
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration ---
LOCAL_MUSIC_DIR = "C:\\Users\\Public\\Music\\Sample Music"
HISTORY_FILE = "assistant_history7.1.json"
ALARM_SOUND_FILE = "alarm.mp3"
WAKEUP_COMMAND = "hello jarvis"

# --- Module Availability Checks ---
try:
    import pygetwindow as gw
    PYGETWINDOW_AVAILABLE = True
except ImportError:
    PYGETWINDOW_AVAILABLE = False
    print("Warning: 'pygetwindow' not found. Window automation limited.")

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("Warning: 'speech_recognition' not found. Voice input disabled.")

try:
    import pyttsx3
    TEXT_TO_SPEECH_AVAILABLE = True
except ImportError:
    TEXT_TO_SPEECH_AVAILABLE = False
    print("Warning: 'pyttsx3' not found. Text-to-speech disabled.")

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: 'pygame' not found. Local music/alarms disabled.")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: 'psutil' not found. Process closing limited.")

try:
    import pywhatkit as kit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False
    print("Warning: 'pywhatkit' not found. YouTube playback limited.")

try:
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_AVAILABLE = True
    else:
        GEMINI_AVAILABLE = False
        print("Warning: GEMINI_API_KEY not set.")
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: 'google-generativeai' not found.")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    print("Warning: OPENWEATHER_API_KEY not set.")

# --- Core Communication Functions ---

def speak(text):
    """Converts text to speech and prints it to the console."""
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        # Voice IDs
        Zira = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
        engine.setProperty('voice', Zira)
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()

        if "Exiting. Have a grate day!" in text:
            write_history("exit", text)
            sys.exit()
        elif "Quitting. See you soon!" in text:
            write_history("quit", text)
            sys.exit()
    except Exception as e:
        print(f"Speech output error: {e}")
    return text

def take_command():
    """Listens for user input via microphone or falls back to text input."""
    if not SPEECH_RECOGNITION_AVAILABLE:
        print("Speech recognition unavailable. Please type.")
        return input("You (type): ").lower()

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=30, phrase_time_limit=45)
        except sr.WaitTimeoutError:
            print("No speech detected. Falling back to typing.")
            return input("You (type): ").lower()

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You (voice): {query}")
        return query.lower()
    except Exception as e:
        print(f"Error recognizing voice: {e}. Falling back to typing.")
        return input("You (type): ").lower()

# --- History Management ---

def write_history(query, response):
    """Writes user query and assistant response to a JSON file."""
    history_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "response": response
    }
    try:
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
        
        history.append(history_entry)
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing history: {e}")

def read_history():
    """Reads and displays recent interaction history."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
                if not history:
                    speak("Your interaction history is empty.")
                    return
                speak("Here's your recent interaction history:")
                for entry in history[-5:]:
                    speak(f"[{entry['timestamp']}] You: {entry['query']} | Assistant: {entry['response']}")
        else:
            speak("No interaction history found yet.")
    except Exception as e:
        speak(f"An error occurred while reading history: {e}")

# --- General Assistant Helpers ---

def wish_user():
    """Greets the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your personal AI assistant. How can I help you today?")

def get_summary_and_speak(text, word_limit=100):
    """Provides a concise summary of text if it's too long."""
    words = text.split()
    if len(words) > word_limit:
        summary = " ".join(words[:word_limit]) + "..."
        return speak(f"I found this, but it's a bit long. Here's a summary: {summary}")
    return speak(f"Here's the summary: {text}")

def wikipedia_search_handler(query_term):
    if not query_term:
        msg = "Please tell me what you want to search on Wikipedia."
        write_history(query_term, msg)
        return speak(msg)
    try:
        result = wikipedia.summary(query_term, sentences=5)
        write_history(query_term, result)
        return get_summary_and_speak(result, word_limit=100)
    except wikipedia.exceptions.PageError:
        msg = "Sorry, I couldn't find anything on Wikipedia for that."
        write_history(query_term, msg)
        return speak(msg)
    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options[:5])
        msg = f"Multiple results found. Options include: {options}..."
        write_history(query_term, msg)
        return speak(msg)
    except Exception as e:
        msg = f"An error occurred while searching Wikipedia: {e}"
        write_history(query_term, msg)
        return speak(msg)

def open_website(site_name):
    """Opens a specified website in the default browser."""
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://x.com",
        "x.com": "https://x.com",
        "linkedin": "https://www.linkedin.com",
        "wikipedia": "https://www.wikipedia.org/"
    }
    for key, url in sites.items():
        if key in site_name:
            webbrowser.open(url)
            return speak(f"Opening {key.capitalize()}.")

    if not (site_name.startswith("http://") or site_name.startswith("https://")):
        site_name = "https://" + site_name.replace(" ", "") + ".com"
    try:
        webbrowser.open(site_name)
        return speak(f"Opening {site_name}.")
    except Exception:
        return speak(f"Sorry, I couldn't open {site_name}.")

def play_youtube_music(song_query):
    """Searches and plays a song on YouTube."""
    if song_query:
        search_url = f"https://www.youtube.com/results?search_query={song_query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return speak(f"Searching for {song_query} on YouTube.")
    return speak("Please tell me what song you want to play on YouTube.")

def play_youtube_music_handler(song_query):
    if not song_query:
        return speak("Please tell me what song you want to play on YouTube.")
    
    speak(f"Playing {song_query} on YouTube.")
    if PYWHATKIT_AVAILABLE:
        try:
            kit.playonyt(song_query)
            write_history(f"youtube play song {song_query}", "Playing on YouTube")
            return
        except Exception as e:
            speak(f"Error: {e}. Opening YouTube search instead.")
    
    play_youtube_music(song_query)

def get_navigation_directions(destination):
    """Opens Google Maps for navigation."""
    if destination:
        map_url = f"https://www.google.com/maps/dir/?api=1&destination={destination.replace(' ', '+')}"
        webbrowser.open(map_url)
        return speak(f"Opening Google Maps with directions to {destination}.")
    return speak("Please tell me your destination.")

def open_application(app_name):
    """Opens a specified application based on the operating system."""
    normalized_app_name = app_name.lower().replace("open ", "").strip()
    app_map = {
        "notepad": "notepad.exe", "calculator": "calc.exe", "paint": "mspaint.exe",
        "cmd": "cmd.exe", "terminal": "cmd.exe", "word": "winword.exe",
        "excel": "excel.exe", "powerpoint": "powerpnt.exe", "chrome": "chrome.exe",
        "firefox": "firefox.exe", "edge": "msedge.exe", "spotify": "spotify.exe",
        "vlc": "vlc.exe", "discord": "discord.exe", "steam": "steam.exe",
        "safari": "Safari", "pages": "Pages", "numbers": "Numbers",
        "keynote": "Keynote", "chrome mac": "Google Chrome",
        "firefox mac": "Firefox", "terminal mac": "Terminal",
        "gedit": "gedit", "gnome terminal": "gnome-terminal", "vlc linux": "vlc"
    }
    executable_name = app_map.get(normalized_app_name)

    try:
        if platform.system() == "Windows":
            if executable_name:
                try:
                    subprocess.Popen(executable_name, shell=True)
                    speak(f"Opening {app_name}.")
                    return
                except FileNotFoundError: pass

            found_app = False
            common_paths = [
                os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), normalized_app_name),
                os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), normalized_app_name),
                os.path.join(os.environ.get("LOCALAPPDATA", ""), normalized_app_name),
                os.path.join(os.environ.get("APPDATA", ""), normalized_app_name),
            ]
            for path_prefix in common_paths:
                full_path = f"{path_prefix}.exe"
                if os.path.exists(full_path):
                    subprocess.Popen(f'"{full_path}"', shell=True)
                    speak(f"Opening {app_name}.")
                    found_app = True; break
                
                matches = glob.glob(f"{path_prefix}/**/*.exe", recursive=True)
                if matches:
                    best_match = next((m for m in matches if os.path.basename(m).lower() == f"{normalized_app_name}.exe"), matches[0])
                    subprocess.Popen(f'"{best_match}"', shell=True)
                    speak(f"Opening {app_name}.")
                    found_app = True; break
            if not found_app:
                speak(f"Sorry, I couldn't find '{app_name}' on Windows.")

        elif platform.system() == "Darwin":
            name = executable_name if executable_name else app_name.title()
            subprocess.Popen(["open", "-a", name])
            speak(f"Opening {app_name}.")
        elif platform.system() == "Linux":
            name = executable_name if executable_name else normalized_app_name
            subprocess.Popen([name])
            speak(f"Opening {app_name}.")
        
        time.sleep(2)
    except Exception as e:
        speak(f"An error occurred while opening {app_name}: {e}")

def close_application(app_name):
    """Closes a specified application."""
    app_name_lower = app_name.lower().replace("close ", "").strip()
    process_name = f"{app_name_lower}.exe"
    window_title_part = app_name_lower

    if "notepad" in app_name_lower: process_name, window_title_part = "notepad.exe", "notepad"
    elif "chrome" in app_name_lower: process_name, window_title_part = "chrome.exe", "google chrome"
    elif "firefox" in app_name_lower: process_name, window_title_part = "firefox.exe", "mozilla firefox"

    try:
        if platform.system() == "Windows":
            if PYGETWINDOW_AVAILABLE:
                windows = gw.getWindowsWithTitle(window_title_part)
                if windows:
                    target = windows[0]
                    if target.isMinimized: target.restore()
                    target.activate()
                    time.sleep(0.5)
                    pyautogui.hotkey('alt', 'f4')
                    speak(f"Attempted to close {app_name} using Alt+F4.")
                    return

            speak(f"Forcefully closing {app_name}...")
            subprocess.run(f"taskkill /f /im {process_name}", shell=True, check=True, capture_output=True)
            speak(f"Successfully closed {app_name}.")
        elif platform.system() == "Darwin":
            subprocess.run(["osascript", "-e", f'tell application "{app_name_lower.title()}" to quit'], check=True)
            speak(f"Closed {app_name}.")
        elif platform.system() == "Linux":
            subprocess.run(["pkill", "-f", process_name], check=True)
            speak(f"Closed {app_name}.")
    except Exception as e:
        speak(f"Error closing application: {e}")

# --- Alarm and Local Music ---

alarm_thread = None
stop_alarm_event = threading.Event()

def set_alarm(alarm_time_str):
    global alarm_thread, stop_alarm_event
    current_time = datetime.datetime.now()
    try:
        match = re.search(r'(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', alarm_time_str, re.IGNORECASE)
        if not match:
            speak("Please specify time like '7 PM' or '18:30'.")
            return

        time_part = match.group(1).replace(" ", "").upper()
        try:
            if "AM" in time_part or "PM" in time_part:
                alarm_time = datetime.datetime.strptime(time_part, "%I:%M%p").time()
            else:
                alarm_time = datetime.datetime.strptime(time_part, "%H:%M").time()
        except ValueError:
            try:
                if "AM" in time_part or "PM" in time_part:
                    alarm_time = datetime.datetime.strptime(time_part, "%I%p").time()
                else:
                    alarm_time = datetime.datetime.strptime(time_part, "%H").time()
            except ValueError:
                speak("I couldn't parse that time.")
                return

        alarm_datetime = datetime.datetime.combine(current_time.date(), alarm_time)
        if alarm_datetime <= current_time:
            alarm_datetime += datetime.timedelta(days=1)
            speak(f"Setting alarm for tomorrow at {alarm_datetime.strftime('%I:%M %p')}.")
        else:
            speak(f"Setting alarm for today at {alarm_datetime.strftime('%I:%M %p')}.")

        time_diff = (alarm_datetime - current_time).total_seconds()
        if alarm_thread and alarm_thread.is_alive():
            stop_alarm_event.set()
            alarm_thread.join(timeout=2)

        stop_alarm_event.clear()
        alarm_thread = threading.Thread(target=alarm_timer, args=(time_diff, alarm_datetime, stop_alarm_event))
        alarm_thread.daemon = True
        alarm_thread.start()
    except Exception as e:
        speak(f"Error setting alarm: {e}")

def alarm_timer(delay, alarm_dt, stop_event):
    speak(f"Alarm set for {alarm_dt.strftime('%H:%M:%S')}. Waiting...")
    if stop_event.wait(delay):
        speak("Alarm cancelled.")
        return
    speak("Time for your alarm!")
    play_alarm_sound()
    speak("Alarm ringing. Say 'stop alarm' to turn it off.")

def play_alarm_sound():
    if PYGAME_AVAILABLE and os.path.exists(ALARM_SOUND_FILE):
        try:
            pygame.mixer.music.load(ALARM_SOUND_FILE)
            pygame.mixer.music.play(-1)
            return
        except Exception: pass
    
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 2000)
    else:
        os.system('echo -e "\a"')

def stop_alarm():
    global stop_alarm_event
    if PYGAME_AVAILABLE and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        speak("Alarm stopped.")
    elif alarm_thread and alarm_thread.is_alive():
        stop_alarm_event.set()
        speak("Alarm stopping.")
    else:
        speak("No active alarm.")

current_playing_song = None
music_paused = False

def play_local_music(query=""):
    global current_playing_song, music_paused
    if not PYGAME_AVAILABLE:
        return speak("Pygame not available.")
    if not os.path.isdir(LOCAL_MUSIC_DIR):
        return speak("Music directory not found.")

    music_files = [f for f in os.listdir(LOCAL_MUSIC_DIR) if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
    if not music_files:
        return speak("No music files found.")

    if query and "play" in query:
        song_q = query.replace("play", "").replace("music", "").replace("song", "").strip().lower()
        found = [f for f in music_files if song_q in f.lower()]
        if found:
            chosen = random.choice(found)
            try:
                pygame.mixer.music.load(os.path.join(LOCAL_MUSIC_DIR, chosen))
                pygame.mixer.music.play()
                current_playing_song, music_paused = chosen, False
                return speak(f"Playing '{chosen}'.")
            except Exception as e:
                return speak(f"Error: {e}")
        else:
            speak(f"Couldn't find '{song_q}'. Playing random song.")

    chosen = random.choice(music_files)
    try:
        pygame.mixer.music.load(os.path.join(LOCAL_MUSIC_DIR, chosen))
        pygame.mixer.music.play()
        current_playing_song, music_paused = chosen, False
        return speak(f"Playing random song: '{chosen}'.")
    except Exception as e:
        speak(f"Error playing music: {e}")

def pause_local_music():
    global music_paused
    if PYGAME_AVAILABLE and pygame.mixer.music.get_busy() and not music_paused:
        pygame.mixer.music.pause()
        music_paused = True
        return speak("Music paused.")
    return speak("No music playing or already paused.")

def unpause_local_music():
    global music_paused
    if PYGAME_AVAILABLE and music_paused:
        pygame.mixer.music.unpause()
        music_paused = False
        return speak("Music unpaused.")
    return speak("No music to unpause.")

def stop_local_music():
    global current_playing_song, music_paused
    if PYGAME_AVAILABLE and (pygame.mixer.music.get_busy() or music_paused):
        pygame.mixer.music.stop()
        current_playing_song, music_paused = None, False
        return speak("Music stopped.")
    return speak("No music playing.")

def next_local_music():
    speak("Playing next song.")
    play_local_music()

def what_is_playing():
    if current_playing_song:
        return speak(f"Currently playing: {current_playing_song}.")
    return speak("No music is playing.")

# --- External Service Integrations ---

def search_on_website(query, website_url):
    search_query = query.replace("search", "").replace("for", "").replace("on", "").strip()
    if "google.com" in website_url:
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching Google for {search_query}.")
    elif "wikipedia.org" in website_url:
        webbrowser.open(f"https://en.wikipedia.org/wiki/{search_query}")
        speak(f"Searching Wikipedia for {search_query}.")
    elif "youtube.com" in website_url:
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        speak(f"Searching YouTube for {search_query}.")
    else:
        webbrowser.open(f"{website_url}/search?q={search_query}")
        speak(f"Searching {website_url} for {search_query}.")
    write_history(query, f"Searched {website_url} for {search_query}")

def search_on_gemini(query):
    if not GEMINI_AVAILABLE:
        speak("Gemini AI unavailable.")
        return None
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"As a helpful AI assistant, answer the following question concisely: {query}"
        response = model.generate_content(prompt, request_options={'timeout': 60})
        text = response.text.strip()
        speak(text)
        write_history(query, text)
        return text
    except Exception as e:
        msg = f"Gemini AI error: {e}"
        speak(msg)
        write_history(query, msg)
        return None

def get_weather_forecast(city="Colombo"):
    if not OPENWEATHER_API_KEY:
        speak("Weather API key not configured.")
        return
    try:
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
        geo_data = requests.get(geo_url).json()
        if not geo_data:
            speak(f"Location '{city}' not found.")
            return
        
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
        city_name = geo_data[0]['name']
        full_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={OPENWEATHER_API_KEY}"
        weather_data = requests.get(full_url).json()

        curr = weather_data['list'][0]
        speak(f"Current weather in {city_name}: {curr['weather'][0]['description']}, {curr['main']['temp']:.1f}°C.")

        speak("5-day forecast:")
        daily = {}
        for entry in weather_data['list']:
            date = datetime.datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')
            day = datetime.datetime.fromtimestamp(entry['dt']).strftime('%A')
            if date not in daily:
                daily[date] = {'day': day, 'min': entry['main']['temp_min'], 'max': entry['main']['temp_max'], 'desc': entry['weather'][0]['description']}
        
        for _, data in list(daily.items())[1:6]:
            res = f"{data['day']}: Low {data['min']:.1f}°C, High {data['max']:.1f}°C. {data['desc']}."
            speak(res)
            write_history(f"weather {city}", res)
    except Exception as e:
        speak(f"Weather error: {e}")

def joke_handler(query):
    joke = pyjokes.get_joke()
    speak(joke)
    write_history(query, joke)

# --- General AI Chat Handler ---

def handle_ai_chat(query):
    if any(x in query for x in ["hi", "hello", "hey"]):
        return speak("Hello there! How can I help you today?")
    elif "wakeup" in query or "wake" in query:
        return speak("I'm ready! How can I help you sir?")
    elif any(x in query for x in ["goodbye", "bye"]):
        speak("Goodbye! Have a great day!")
        sys.exit()
    elif "how are you" in query:
        speak("I am doing great, thank you for asking!")
        speak("I am just a program, but I'm functioning well!")
        return "I am doing great!"
    elif any(x in query for x in ["jarvis", "voice assistant", "name"]):
        speak("Yes sir, I am your voice assistant, designed to help you.")
        return "I am your voice assistant."
    elif "who are you" in query:
        speak("I am your personal AI assistant v7.1, also known as JARVIS.")
        return "I am JARVIS."
    elif "who made you" in query or "creator" in query:
        return speak("I was created by a human developer. My core intelligence comes from Google Gemini.")
    elif "what can you do" in query:
        return speak("I can tell time, open apps, search the web, set alarms, play music, and more. Just ask for 'help'.")
    elif "interesting fact" in query:
        return speak("Did you know honey never spoils? Archaeologists found edible honey in 3,000-year-old Egyptian tombs!")
    elif "list voice" in query:
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            speak("Available Voices:")
            for i, v in enumerate(voices):
                speak(f"Voice {i}: {v.name}")
            return "Voices listed."
        except Exception as e:
            return speak(f"Error listing voices: {e}")
    else:
        if GEMINI_AVAILABLE:
            speak("Let me think...")
            return search_on_gemini(query)
        else:
            speak("AI capabilities limited. Would you like me to search the web?")
            return "AI disabled."

# --- Main Assistant Logic ---

def run_assistant():
    wish_user()

    command_processor = {
        "what time is it": lambda q: speak(datetime.datetime.now().strftime("%I:%M %p")),
        "time": lambda q: speak(datetime.datetime.now().strftime("%I:%M %p")),
        "what is the date": lambda q: speak(datetime.datetime.now().strftime("%A, %B %d, %Y")),
        "date": lambda q: speak(datetime.datetime.now().strftime("%A, %B %d, %Y")),
        "tell me a joke": lambda q: speak(pyjokes.get_joke()),
        "joke": lambda q: joke_handler("joke"),
        "open google": lambda q: open_website("google"),
        "open youtube": lambda q: open_website("youtube"),
        "open facebook": lambda q: open_website("facebook"),
        "open twitter": lambda q: open_website("twitter"),
        "open x.com": lambda q: open_website("x.com"),
        "open linkedin": lambda q: open_website("linkedin"),
        "open wikipedia": lambda q: open_website("wikipedia"),
        "open": lambda q: open_application(q.replace("open", "").strip()),
        "close": lambda q: close_application(q.replace("close", "").strip()),
        "play music": lambda q: play_local_music(q),
        "pause music": lambda q: pause_local_music(),
        "unpause music": lambda q: unpause_local_music(),
        "resume music": lambda q: unpause_local_music(),
        "stop music": lambda q: stop_local_music(),
        "next song": lambda q: next_local_music(),
        "what is playing": lambda q: what_is_playing(),
        "set an alarm for": lambda q: set_alarm(q.replace("set an alarm for", "").strip()),
        "set alarm": lambda q: set_alarm(q.replace("set alarm", "").strip()),
        "stop alarm": lambda q: stop_alarm(),
        "show history": lambda q: read_history(),
        "show my history": lambda q: read_history(),
        "read history": lambda q: read_history(),
        'search wikipedia for': wikipedia_search_handler,
        "search wikipedia": lambda q: search_on_website(q.replace("search wikipedia", "").strip(), "https://www.wikipedia.org"),
        "wikipedia": lambda q: search_on_website(q.replace("wikipedia", "").strip(), "https://www.wikipedia.org"),
        "search for": lambda q: search_on_website(q.replace("search for", "").strip(), "https://www.google.com"),
        "search on": lambda q: search_on_website(q.replace("search on", "").strip(), "https://www.google.com"),
        "search": lambda q: search_on_website(q.replace("search", "").strip(), "https://www.google.com"),
        "google search for": lambda q: search_on_website(q.replace("google search for", "").strip(), "https://www.google.com"),
        "search google for": lambda q: search_on_website(q.replace("search google for", "").strip(), "https://www.google.com"),
        "search google": lambda q: search_on_website(q.replace("search google", "").strip(), "https://www.google.com"),
        "google": lambda q: search_on_website(q.replace("google", "").strip(), "https://www.google.com"),
        "navigate to": lambda q: get_navigation_directions(q.replace("navigate to", "").strip()),
        "directions to": lambda q: get_navigation_directions(q.replace("directions to", "").strip()),
        "direction": lambda q: get_navigation_directions(q.replace("direction", "").strip()),
        "map": lambda q: get_navigation_directions(q.replace("map", "").strip()),
        "open map": lambda q: get_navigation_directions(q.replace("open map", "").strip()),
        "play on youtube": lambda q: play_youtube_music(q.replace("play on youtube", "").strip()),
        "play song on youtube": lambda q: play_youtube_music(q.replace("play song on youtube", "").strip()),
        "play music on youtube": lambda q: play_youtube_music(q.replace("play music on youtube", "").strip()),
        "youtube play song": lambda q: play_youtube_music_handler(q.replace("youtube play song", "").strip()),
        "search youtube": lambda q: search_on_website(q.replace("search youtube", "").strip(), "https://www.youtube.com"),
        "youtube": lambda q: search_on_website(q.replace("youtube", "").strip(), "https://www.youtube.com"),
        "current weather in": lambda q: get_weather_forecast(q.replace("current weather in", "").strip()),
        "weather in": lambda q: get_weather_forecast(q.replace("weather in", "").strip()),
        "weather": lambda q: get_weather_forecast("Colombo"),
        "what is the weather in": lambda q: get_weather_forecast(q.replace("what is the weather in", "").strip()),
        "how's the weather in": lambda q: get_weather_forecast(q.replace("how's the weather in", "").strip()),
        "help": lambda q: speak("I can tell time, date, jokes, open websites/apps, set alarms, play music, and search the web."),
        "command": lambda q: speak("I can help with time, date, jokes, websites, apps, alarms, and music."),
        "commands": lambda q: speak("I can help with time, date, jokes, websites, apps, alarms, and music."),
        "thank you": lambda q: speak("You're welcome!"),
        "thanks": lambda q: speak("My pleasure!"),
        "exit": lambda q: speak("Exiting. Have a grate day!"),
        "quit": lambda q: speak("Quitting. See you soon!"),
    }
    sorted_commands = sorted(command_processor.keys(), key=len, reverse=True)

    while True:
        query = take_command()
        response_text = ""
        handled = False

        if "stop alarm" in query and alarm_thread and alarm_thread.is_alive():
            stop_alarm()
            response_text, handled = "Alarm stopped.", True
        elif "stop music" in query or "turn off music" in query:
            stop_local_music()
            response_text, handled = "Music stopped.", True
        elif "pause music" in query:
            pause_local_music()
            response_text, handled = "Music paused.", True
        elif "unpause music" in query or "resume music" in query:
            unpause_local_music()
            response_text, handled = "Music unpaused.", True
        elif "next song" in query:
            next_local_music()
            response_text, handled = "Playing next song.", True
        elif "what is playing" in query or "what song is this" in query:
            what_is_playing()
            response_text, handled = (current_playing_song if current_playing_song else "No music playing."), True
        elif "shutdown" in query:
            response_text = "Jarvis shutting down. Goodbye!"
            speak(response_text)
            write_history(query, response_text)
            break
        elif "hello jarvis" in query:
            response_text = "Hello! How can I help you today?"
            speak(response_text)
            handled = True

        if not handled:
            for prefix in sorted_commands:
                if query.startswith(prefix):
                    command_processor[prefix](query)
                    response_text, handled = f"Executed: {prefix}", True
                    break

        if not handled:
            response_text = handle_ai_chat(query)
            if not response_text:
                response_text = "I'm sorry, I didn't understand that."

        write_history(query, response_text)

if __name__ == "__main__":
    speak(f"Waiting for wakeup command: {WAKEUP_COMMAND}")
    while True:
        command = input(f"Say '{WAKEUP_COMMAND}' or type 'exit' to quit: ").lower()
        if WAKEUP_COMMAND in command:
            speak("Wakeup command received! Starting assistant...")
            run_assistant()
            speak(f"Assistant session ended. Waiting for '{WAKEUP_COMMAND}'...")
        elif "exit" in command or "quit" in command:
            speak("Exiting program.")
            break
        else:
            speak(f"Still waiting for '{WAKEUP_COMMAND}'. You said: '{command}'")
