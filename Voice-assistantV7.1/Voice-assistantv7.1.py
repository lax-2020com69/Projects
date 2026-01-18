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

from dotenv import load_dotenv #load .env file
load_dotenv() # This line loads the variables from .env into the environment

# --- Configuration ---
# IMPORTANT: Replace with your actual local music directory!
LOCAL_MUSIC_DIR = "C:\\Users\\Public\\Music\\Sample Music" # Example for Windows
# LOCAL_MUSIC_DIR = "/Users/YourUser/Music" # Example for macOS/Linux
HISTORY_FILE = "assistant_history7.1.json"
ALARM_SOUND_FILE = "alarm.mp3" # Place this file in the same directory as the script
WAKEUP_COMMAND = "hello jarvis" # Your chosen wakeup word

try:
    import pygetwindow as gw # This is the missing piece!
    PYGETWINDOW_AVAILABLE = True
except ImportError:
    PYGETWINDOW_AVAILABLE = False
    print("Warning: 'pygetwindow' module not found. Window automation features will be limited. Please install it with 'pip install pygetwindow'.")
except Exception as e:
    PYGETWINDOW_AVAILABLE = False
    print(f"Warning: Error importing 'pygetwindow': {e}. Window automation features will be limited.")

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    print("Warning: 'speech_recognition' module not found. Voice input will be disabled. Please install it with 'pip install SpeechRecognition'.")
    SPEECH_RECOGNITION_AVAILABLE = False
except Exception as e:
    print(f"Warning: Error initializing 'speech_recognition': {e}. Voice input will be disabled.")
    SPEECH_RECOGNITION_AVAILABLE = False

# Text-to-Speech
try:
    import pyttsx3
    TEXT_TO_SPEECH_AVAILABLE = True
except ImportError:
    print("Warning: 'pyttsx3' module not found. Text-to-speech will be disabled. Please install it with 'pip install pyttsx3'.")
    TEXT_TO_SPEECH_AVAILABLE = False
except Exception as e:
    print(f"Warning: Error initializing 'pyttsx3': {e}. Text-to-speech will be disabled.")
    TEXT_TO_SPEECH_AVAILABLE = False

# Pygame for Music/Alarm (optional)
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    print("Warning: 'pygame' module not found. Local music playback and custom alarm sounds will be disabled. Please install it with 'pip install pygame'.")
    PYGAME_AVAILABLE = False
except Exception as e:
    print(f"Warning: Error initializing 'pygame': {e}. Local music playback and custom alarm sounds will be disabled.")
    PYGAME_AVAILABLE = False

# For psutil (used in close_application)
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: 'psutil' module not found. Process-based application closing will be limited. Please install it with 'pip install psutil'.")
except Exception as e:
    PSUTIL_AVAILABLE = False
    print(f"Warning: Error importing 'psutil': {e}. Process-based application closing will be limited.")

# For pywhatkit (used in play_youtube_music)
try:
    import pywhatkit as kit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False
    print("Warning: 'pywhatkit' module not found. Direct YouTube playback will be limited. Please install it with 'pip install pywhatkit'.")
except Exception as e:
    print(f"Warning: Error importing 'pywhatkit': {e}. Direct YouTube playback will be limited.")

# Google Gemini API
try:
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_AVAILABLE = True
    else:
        print("Warning: GEMINI_API_KEY environment variable not set. Gemini AI capabilities will be disabled. Get your key from Google AI Studio.")
        GEMINI_AVAILABLE = False
except ImportError:
    print("Warning: 'google-generativeai' module not found. Gemini AI capabilities will be disabled. Please install it with 'pip install google-generativeai'.")
    GEMINI_AVAILABLE = False
except Exception as e:
    print(f"Warning: Error initializing Google Gemini API: {e}. Gemini AI capabilities will be disabled.")
    GEMINI_AVAILABLE = False

# OpenWeatherMap API
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    print("Warning: OPENWEATHER_API_KEY environment variable not set. Weather forecasts will be disabled. Get your key from OpenWeatherMap.")

# --- Core Communication Functions ---

def speak(text):
    """Converts text to speech and prints it to the console."""

    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()

        David="HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
        HAZE="HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-GB_HAZEL_11.0"
        Zira="HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
        
        voice_id=Zira
        # Select voice if voice_id is provided
        if voice_id:
            engine.setProperty('voice', voice_id)
            engine.setProperty('rate', 170)  # Words per minute
            engine.setProperty('volume', 0.9) # Set volume (0.0 to 1.0)

        else:
            # it select default voice_id
            pass 

        engine.say(text)
        engine.runAndWait()
        if "Exiting. Have a grate day!" in text:
            write_history("exit",text)
            sys.exit()
        elif "Quitting. See you soon!" in text:
            write_history("quit",text)
            sys.exit()
    except Exception as e:
        print(f"Speech output error: {e}")
        print("Speech output might not be supported or an issue occurred during initialization/playback.")
    return text #<-- Important: Return the message string for history
    
def take_command():
    """
    Listens for user input via microphone using SpeechRecognition.
    If voice input fails or is unavailable, falls back to text input.
    """
    if not SPEECH_RECOGNITION_AVAILABLE:
        print("Speech recognition is not available. Please type your command.")
        query = input("You (type): ").lower()
        return query # No audio file path for manual input

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command (or type if voice fails)...")
        r.pause_threshold = 0.8 # Seconds of non-speaking before a phrase is considered complete
        r.adjust_for_ambient_noise(source, duration=1) # Adjust for ambient noise for 1 second
        audio = None
        try:
            audio = r.listen(source, timeout=30, phrase_time_limit=45) # Listen for up to 6 seconds, max 8 seconds phrase
        except sr.WaitTimeoutError:
            print("No speech detected within timeout. Falling back to typing.")
            query = input("You (type): ").lower()
            return query # Return typed input

    try:
        print("Recognizing voice...")
        query = r.recognize_google(audio, language='en-in') # Using Google's Web Speech API
        print(f"You (voice): {query}")
        return query.lower() # No audio file path for now
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio. Please type your command.")
        query = input("You (type): ").lower()
        return query
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}. Falling back to typing.")
        query = input("You (type): ").lower()
        return query
    except Exception as e:
        print(f"An unexpected error occurred during speech recognition: {e}. Falling back to typing.")
        query = input("You (type): ").lower()
        return query

# --- History Management ---

def write_history(query, response):
    """Writes user query and assistant response to a JSON history file."""
    history_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "response": response
    }
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r+', encoding='utf-8') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = [] # Handle empty or malformed JSON
                history.append(history_entry)
                f.seek(0) # Rewind to beginning
                json.dump(history, f, indent=4, ensure_ascii=False)
                f.truncate() # Trim any remaining old content
        else:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump([history_entry], f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error writing to history file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while managing history: {e}")

def read_history():
    """Reads and displays recent interaction history from the JSON file."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
                if not history:
                    speak("Your interaction history is empty.")
                    return
                speak("Here's your recent interaction history:")
                for entry in history[-5:]: # Display last 5 entries
                    speak(f"[{entry['timestamp']}] You: {entry['query']} | Assistant: {entry['response']}")
        else:
            speak("No interaction history found yet.")
    except json.JSONDecodeError:
        speak("Error reading history file. It might be corrupted. Starting fresh history.")
        # Optionally, you could back up the corrupted file here
        if os.path.exists(HISTORY_FILE):
            os.rename(HISTORY_FILE, f"{HISTORY_FILE}.bak_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
    except IOError as e:
        speak(f"Error accessing history file: {e}")
    except Exception as e:
        speak(f"An unexpected error occurred while reading history: {e}")

# --- General Assistant Helper Functions ---

def wish_user():
    """Greets the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return speak("Good Morning!")
    elif 12 <= hour < 18:
        return speak("Good Afternoon!")
    else:
        return speak("Good Evening!")
    return speak("I am your personal AI assistant. How can I help you today?")

def get_summary_and_speak(text, word_limit=100):
    """Provides a concise summary of text if it's too long."""
    words = text.split()
    if len(words) > word_limit:
        summary = " ".join(words[:word_limit]) + "..."
        return speak(f"I found this, but it's a bit long. Here's a summary: {summary}")
    else:
        return speak(f"Here's the summary: {text}")

def wikipedia_search_handler(query_term):
    if not query_term:
        write_history(query_term, "Please tell me what you want to search on Wikipedia.")
        return "Please tell me what you want to search on Wikipedia."
    try:
        result = wikipedia.summary(query_term, sentences=5)
        write_history(query_term, result)
        return get_summary_and_speak(result, word_limit=100)
    except wikipedia.exceptions.PageError:
        write_history(query_term, "Sorry, I couldn't find anything on Wikipedia for that.")
        return "Sorry, I couldn't find anything on Wikipedia for that."
    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options[:5])
        write_history(query_term, f"Multiple results found. Please be more specific. Options include: {options}...")
        return f"Multiple results found. Please be more specific. Options include: {options}..."
    except Exception as e:
        write_history(query_term, f"An error occurred while searching Wikipedia: {e}")
        return f"An error occurred while searching Wikipedia: {e}"

def search_google_knowledge_graph(query_term):
    """Placeholder for Google Knowledge Graph integration (requires API key and setup)."""
    speak(f"I can search the Google Knowledge Graph for '{query_term}', but this feature requires a Google Knowledge Graph API key and further integration setup.")
    speak("For now, I can open Google Search for you.")
    write_history(query_term, f"https://www.google.com/search?q={query_term}")
    return webbrowser.open(f"https://www.google.com/search?q={query_term}")

def play_youtube_music_handler(song_query):
    """Searches and plays a song on YouTube using pywhatkit."""
    if not song_query:
        response_text = speak("Please tell me what song you want to play on YouTube.")
        write_history("youtube play song", response_text)
        return

    response_text = speak(f"Playing {song_query} on YouTube.")
    if PYWHATKIT_AVAILABLE:
        try:
            kit.playonyt(song_query)
            write_history(f"youtube play song {song_query}", response_text)
        except Exception as e:
            response_text = speak(f"An error occurred while trying to play on YouTube: {e}. Opening YouTube search instead.")
            search_youtube(song_query)
            write_history(f"youtube play song {song_query}", response_text)
    else:
        response_text = speak("The 'pywhatkit' module is not installed. I will open a YouTube search instead.")
        search_youtube(song_query)
        write_history(f"play youtube music {song_query}", response_text)

def open_website(site_name):
    """Opens a specified website in the default browser."""
    if "youtube" in site_name:
        webbrowser.open("https://www.youtube.com")
        return speak("Opening YouTube.")
    elif "google" in site_name:
        webbrowser.open("https://www.google.com")
        return speak("Opening Google.")
    elif "facebook" in site_name:
        webbrowser.open("https://www.facebook.com")
        return speak("Opening Facebook.")
    elif "twitter" in site_name or "x.com" in site_name:
        webbrowser.open("https://x.com")
        return speak("Opening X.com (formerly Twitter).")
    elif "linkedin" in site_name:
        webbrowser.open("https://www.linkedin.com")
        return speak("Opening LinkedIn.")
    elif "wikipedia" in site_name:
        webbrowser.open("https://www.wikipedia.org/")
        return speak("Opening Wikipedia")
    else:
        # Attempt to open a generic website
        if not (site_name.startswith("http://") or site_name.startswith("https://")):
            site_name = "https://" + site_name.replace(" ", "") + ".com" # Simple heuristic
        try:
            webbrowser.open(site_name)
            return speak(f"Opening {site_name}.")
        except Exception:
            return speak(f"Sorry, I couldn't open {site_name}. Please make sure it's a valid website name.")

def play_youtube_music(song_query):
    """Searches and plays a song on YouTube."""
    if song_query:
        search_url = f"https://www.youtube.com/results?search_query={song_query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return speak(f"Searching for {song_query} on YouTube and opening the results.")
    else:
        return speak("Please tell me what song you want to play on YouTube.")

def get_navigation_directions(destination):
    """Opens Google Maps for navigation."""
    if destination:
        map_url = f"https://www.google.com/maps/dir/?api=1&destination={destination.replace(' ', '+')}"
        webbrowser.open(map_url)
        return speak(f"Opening Google Maps with directions to {destination}.")
    else:
        return speak("Please tell me your destination for navigation.")

def open_application(app_name):
    """
    Opens a specified application based on the operating system,
    with enhanced lookup capabilities and error handling.
    """
    # Normalize the input application name
    normalized_app_name = app_name.lower().replace("open ", "").strip()

    # --- Expanded Application Mapping (More OS-specific and common paths) ---
    app_map = {
        # Windows specific applications and common executable names/paths
        "notepad": "notepad.exe",
        "notepad++": "notepad++.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "terminal": "cmd.exe", # Windows
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "chrome": "chrome.exe", # Often found via shell, or in Program Files
        "firefox": "firefox.exe", # Often found via shell, or in Program Files
        "edge": "msedge.exe",
        "spotify": "spotify.exe", # Often in AppData or Program Files
        "vlc": "vlc.exe",
        "discord": "discord.exe",
        "steam": "steam.exe",

        # macOS specific applications (case-sensitive app bundle names)
        "safari": "Safari",
        "pages": "Pages",
        "numbers": "Numbers",
        "keynote": "Keynote",
        "chrome mac": "Google Chrome", # Explicitly for Chrome on Mac
        "firefox mac": "Firefox",     # Explicitly for Firefox on Mac
        "terminal mac": "Terminal",

        # Linux specific applications (common command names)
        "gedit": "gedit",
        "gnome terminal": "gnome-terminal",
        "kate": "kate",
        "konsole": "konsole",
        "libreoffice writer": "libreoffice --writer",
        "libreoffice calc": "libreoffice --calc",
        "libreoffice impress": "libreoffice --impress",
        "vlc linux": "vlc", # Explicitly for VLC on Linux
    }

    executable_name = app_map.get(normalized_app_name)

    try:
        if platform.system() == "Windows":
            # --- Enhanced Windows Application Launch ---
            if executable_name:
                # Try direct executable name first (works for PATH apps)
                try:
                    subprocess.Popen(executable_name, shell=True)
                    speak(f"Opening {app_name}.")
                    time.sleep(2) # Give some time for the app to open
                    return
                except FileNotFoundError:
                    pass # Continue to more exhaustive search

            # If direct launch failed or no explicit executable_name
            # Try common program file locations for .exe files
            found_app = False
            common_paths = [
                os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), normalized_app_name),
                os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), normalized_app_name),
                os.path.join(os.environ.get("LOCALAPPDATA", ""), normalized_app_name), # For apps like Spotify
                os.path.join(os.environ.get("APPDATA", ""), normalized_app_name),
                os.path.join(os.environ.get("HOMEDRIVE", "C:"), os.environ.get("HOMEPATH", "\\Users\\Default"), "Desktop", normalized_app_name), # Desktop
            ]

            for path_prefix in common_paths:
                # Look for exact .exe match
                full_path = f"{path_prefix}.exe"
                if os.path.exists(full_path):
                    speak(f"Opening {app_name} from {full_path}.")
                    subprocess.Popen(f'"{full_path}"', shell=True) # Quote path for spaces
                    found_app = True
                    break
                
                # Look for a common installation pattern (e.g., in a subfolder)
                # Example: C:\Program Files\Google\Chrome\Application\chrome.exe
                # Or: C:\Users\Username\AppData\Local\Programs\Microsoft VS Code\Code.exe
                # Use glob for more flexible search within common directories
                glob_patterns = [
                    f"{path_prefix}/**/*.exe", # Search deeply for any .exe
                    f"{path_prefix}/*{normalized_app_name}*/*.exe", # Specific subfolder search
                ]
                for pattern in glob_patterns:
                    matches = glob.glob(pattern, recursive=True)
                    if matches:
                        # Prioritize direct matches, then common executable names
                        best_match = None
                        for match in matches:
                            if os.path.basename(match).lower() == f"{normalized_app_name}.exe":
                                best_match = match
                                break
                        if not best_match and matches: # If no exact match, take the first found
                             best_match = matches[0]

                        if best_match:
                            speak(f"Opening {app_name} from {best_match}.")
                            subprocess.Popen(f'"{best_match}"', shell=True) # Quote path for spaces
                            found_app = True
                            break # Break from glob_patterns loop
                if found_app:
                    break # Break from common_paths loop

            if not found_app:
                speak(f"Sorry, I couldn't find '{app_name}' or its executable on Windows. Please ensure it's installed or add its full path to the map.")
                return

        elif platform.system() == "Darwin": # macOS
            if executable_name: # Use mapped name if available
                subprocess.Popen(["open", "-a", executable_name])
                speak(f"Opening {app_name}.")
            else: # Fallback for unmapped apps (assuming app_name is direct app name)
                # Try to open directly as an application
                try:
                    subprocess.Popen(["open", "-a", app_name.title()]) # macOS app names often Title Case
                    speak(f"Opening {app_name}.")
                except Exception:
                    speak(f"Could not find or open '{app_name}' on macOS. Please ensure it's installed.")
                    return

        elif platform.system() == "Linux":
            if executable_name:
                subprocess.Popen([executable_name])
                speak(f"Opening {app_name}.")
            else: # Fallback: try direct app_name
                try:
                    subprocess.Popen([normalized_app_name])
                    speak(f"Opening {app_name}.")
                except FileNotFoundError:
                    speak(f"Could not find or open '{app_name}' on Linux. Please ensure it's installed and in your PATH.")
                    return

        else:
            speak(f"I don't know how to open applications on your operating system ({platform.system()}).")
            return
            
        time.sleep(2) # Give some time for the app to open (universal sleep)

    except FileNotFoundError:
        speak(f"Sorry, I couldn't find '{app_name}'. Please ensure it's installed and in your system's PATH or add its full path to the map.")
    except Exception as e:
        speak(f"An unexpected error occurred while trying to open {app_name}: {e}")

def close_application(app_name):
    """Closes a specified application, attempting to activate its window and then use Alt+F4,
    with a fallback to system commands."""
    speak(f"Closing applications can be tricky, as it varies by operating system and application. I'll try to close {app_name}.")
    
    # Clean up app_name for process identification and window title matching
    # Common application executable names or window titles.
    # You might need to expand this mapping for more applications.
    app_name_lower = app_name.lower().replace("close ", "").strip()
    
    # Example mapping of common names to potential window titles/process names
    # This is an important part you'll need to expand for your specific use cases
    # A simple approach for now: assume the app_name is close to the window title
    potential_window_titles = [app_name_lower, f"{app_name_lower}.exe"] # Add more variations if needed
    
    # Common applications and their likely process/window names
    if "notepad" in app_name_lower:
        process_name = "notepad.exe"
        window_title_part = "notepad"
    elif "chrome" in app_name_lower:
        process_name = "chrome.exe"
        window_title_part = "google chrome"
    elif "firefox" in app_name_lower:
        process_name = "firefox.exe"
        window_title_part = "mozilla firefox"
    elif "word" in app_name_lower: # Example for MS Word
        process_name = "winword.exe"
        window_title_part = "word"
    # Add more mappings as needed
    else:
        process_name = f"{app_name_lower}.exe" # Default assumption
        window_title_part = app_name_lower


    try:
        if platform.system() == "Windows":
             # Ensure pygetwindow is available before trying to use it
            if PYGETWINDOW_AVAILABLE:
                speak(f"Searching for {app_name} window to activate it and then use Alt+F4.")
            
                target_window = None
                # Try to find the window by title. gw.getWindowsWithTitle() is more robust.
                # It returns a list, we often want the first one if multiple exist.
                
                # Look for windows containing the app_name in their title
                windows = gw.getWindowsWithTitle(window_title_part)
                if windows:
                    target_window = windows[0] # Take the first matching window
                    speak(f"Found window: '{target_window.title}'. Activating it.")
                    try:
                        if target_window.isMinimized:
                            target_window.restore() # Restore if minimized
                        target_window.activate() # Bring to foreground and focus
                        time.sleep(0.5) # Give it a moment to become active
                        
                        speak(f"Sending Alt+F4 to {app_name}.")
                        pyautogui.hotkey('alt', 'f4')
                        time.sleep(1.5) # Give the app time to react to Alt+F4 and close
                        speak(f"Attempted to close {app_name} using Alt+F4.")
                    except Exception as activate_e:
                        speak(f"Could not activate or send hotkey to window. Error: {activate_e}. Falling back to taskkill.")
                        target_window = None # Reset to trigger fallback
            else:
                speak(f"Could not find an active window for {app_name}. Proceeding to forceful termination.")
            
            # Fallback to taskkill if no window was found/activated, or if Alt+F4 failed
            if not target_window: # Or if it failed to close (more complex check required)
                speak(f"Attempting to forcefully close {app_name} with taskkill.")
                try:
                    # Check if process_name has an .exe extension, add if missing for taskkill
                    if not process_name.endswith(".exe"):
                        process_name += ".exe"
                    subprocess.run(f"taskkill /f /im {process_name}", shell=True, check=True, capture_output=True)
                    speak(f"Successfully closed {app_name} using taskkill.")
                except subprocess.CalledProcessError as e:
                    speak(f"Could not forcefully close {app_name} with taskkill. It might not be running or the command failed. Error: {e.stderr.decode().strip()}")
                    
        elif platform.system() == "Darwin": # macOS
            speak(f"Attempting to close {app_name} on macOS.")
            # For macOS, 'process_name' should ideally be the application bundle name, e.g., "Google Chrome"
            # rather than "chrome.exe". You might need a similar mapping.
            subprocess.run(["osascript", "-e", f'tell application "{app_name_lower.title()}" to quit'], check=True, capture_output=True)
            speak(f"Attempted to close {app_name}.")
            
        elif platform.system() == "Linux":
            speak(f"Attempting to close {app_name} on Linux.")
            subprocess.run(["pkill", "-f", process_name], check=True, capture_output=True)
            speak(f"Attempted to close {app_name}.")
            
        else:
            speak(f"I don't know how to close applications on your operating system ({platform.system()}).")
            target_window = None # pygetwindow not available, trigger fallback
            return
            
    except FileNotFoundError:
        speak("Could not find the necessary command or utility to close applications (e.g., pyautogui, pygetwindow, or system commands). Please ensure they are installed and in your PATH.")
    except Exception as e:
        speak(f"An unexpected error occurred while trying to close {app_name}: {e}")

def control_media(action):
    """Placeholder for controlling media (play, pause, next, previous)."""
    speak(f"Media control functionality for '{action}' is under development. I can only control local music for now.")

# --- Alarm and Local Music ---

alarm_thread = None
stop_alarm_event = threading.Event()

def set_alarm(alarm_time_str):
    """Sets an alarm for a specified time."""
    global alarm_thread, stop_alarm_event

    current_time = datetime.datetime.now()
    try:
        # Try different time formats (e.g., 7pm, 7:00 PM, 18:30)
        match = re.search(r'(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', alarm_time_str, re.IGNORECASE)
        if not match:
            speak("Sorry, I couldn't understand the time. Please specify in a clear format like '7 PM' or '18:30'.")
            return

        time_part = match.group(1).replace(" ", "").upper()
        alarm_time = None

        try:
            # Try parsing with AM/PM
            if "AM" in time_part or "PM" in time_part:
                alarm_time = datetime.datetime.strptime(time_part, "%I:%M%p").time()
            else:
                alarm_time = datetime.datetime.strptime(time_part, "%H:%M").time()
        except ValueError:
            # If standard parsing fails, try without minutes or only hour + AM/PM
            try:
                if "AM" in time_part or "PM" in time_part:
                    alarm_time = datetime.datetime.strptime(time_part, "%I%p").time()
                else:
                    alarm_time = datetime.datetime.strptime(time_part, "%H").time()
            except ValueError:
                speak("I couldn't parse that time correctly. Please try a format like '7 AM', '18:30', or '8 o'clock'.")
                return

        alarm_datetime = datetime.datetime.combine(current_time.date(), alarm_time)

        # If the alarm time is in the past, set it for the next day
        if alarm_datetime <= current_time:
            alarm_datetime += datetime.timedelta(days=1)
            speak(f"That time is in the past for today. I'm setting the alarm for tomorrow at {alarm_datetime.strftime('%I:%M %p')}.")
        else:
            speak(f"Setting alarm for today at {alarm_datetime.strftime('%I:%M %p')}.")

        time_difference = (alarm_datetime - current_time).total_seconds()

        if alarm_thread and alarm_thread.is_alive():
            stop_alarm_event.set() # Signal to stop any existing alarm
            alarm_thread.join(timeout=2) # Wait for it to stop gracefully
            if alarm_thread.is_alive():
                speak("Previous alarm could not be stopped gracefully. Starting new one anyway.")

        stop_alarm_event.clear() # Clear the event for the new alarm
        alarm_thread = threading.Thread(target=alarm_timer, args=(time_difference, alarm_datetime, stop_alarm_event))
        alarm_thread.daemon = True # Allow program to exit even if thread is running
        alarm_thread.start()
        speak(f"Alarm set for {alarm_datetime.strftime('%I:%M %p')} on {alarm_datetime.strftime('%A, %B %d, %Y')}.")

    except Exception as e:
        speak(f"I encountered an error while setting the alarm: {e}")
        speak("Please try again with a clear time, for example: 'set an alarm for 7 AM'.")

def alarm_timer(delay_seconds, alarm_datetime, stop_event):
    """Internal function to handle the alarm countdown and trigger."""
    speak(f"Alarm set for {alarm_datetime.strftime('%H:%M:%S')}. Waiting...")
    if stop_event.wait(delay_seconds):
        speak("Alarm cancelled.")
        return

    speak("Time for your alarm!")
    play_alarm_sound()
    speak("Alarm ringing. Say 'stop alarm' to turn it off.")

def play_alarm_sound():
    """Plays the alarm sound."""
    if PYGAME_AVAILABLE and os.path.exists(ALARM_SOUND_FILE):
        try:
            pygame.mixer.music.load(ALARM_SOUND_FILE)
            pygame.mixer.music.play(-1) # Loop indefinitely
        except pygame.error as e:
            speak(f"Error playing alarm sound with Pygame: {e}. Playing system beep instead.")
            # Fallback to system beep if Pygame fails
            if platform.system() == "Windows":
                import winsound
                winsound.Beep(1000, 2000)
            else:
                os.system('play -nq -t alsa synth 2 sine 440' if os.system('which play &> /dev/null') == 0 else 'echo -e "\a"')
    elif PYGAME_AVAILABLE:
        speak(f"Alarm sound file '{ALARM_SOUND_FILE}' not found. Playing system beep.")
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 2000)
        else:
            os.system('play -nq -t alsa synth 2 sine 440' if os.system('which play &> /dev/null') == 0 else 'echo -e "\a"')
    else:
        speak("Pygame not available. Cannot play custom alarm sound. Playing system beep.")
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 2000)
        else:
            os.system('play -nq -t alsa synth 2 sine 440' if os.system('which play &> /dev/null') == 0 else 'echo -e "\a"')

def stop_alarm():
    """Stops the currently ringing alarm."""
    global stop_alarm_event
    if PYGAME_AVAILABLE and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        speak("Alarm stopped.")
    elif alarm_thread and alarm_thread.is_alive():
        stop_alarm_event.set() # Signal the thread to stop
        speak("Alarm stopping.")
    else:
        speak("No alarm is currently active or ringing.")

current_playing_song = None
music_paused = False

def play_local_music(query=""):
    """Plays a random song or a specific song from the local music directory."""
    global current_playing_song, music_paused

    if not PYGAME_AVAILABLE:
        speak("Pygame is not available, so I cannot play local music.")
        return

    if not os.path.isdir(LOCAL_MUSIC_DIR):
        speak(f"The music directory '{LOCAL_MUSIC_DIR}' does not exist or is not configured correctly.")
        return

    music_files = [f for f in os.listdir(LOCAL_MUSIC_DIR) if f.lower().endswith(('.mp3', '.wav', '.ogg'))]

    if not music_files:
        speak(f"No music files found in '{LOCAL_MUSIC_DIR}'.")
        return

    if query and "play" in query:
        song_name_query = query.replace("play", "").replace("music", "").replace("song", "").strip().lower()
        if song_name_query:
            found_songs = [f for f in music_files if song_name_query in f.lower()]
            if found_songs:
                chosen_song = random.choice(found_songs)
                full_path = os.path.join(LOCAL_MUSIC_DIR, chosen_song)
                try:
                    pygame.mixer.music.load(full_path)
                    pygame.mixer.music.play()
                    current_playing_song = chosen_song
                    music_paused = False
                    speak(f"Playing '{chosen_song}'.")
                    return
                except pygame.error as e:
                    return speak(f"Error playing '{chosen_song}': {e}. Trying another song.")
            else:
                return speak(f"Couldn't find any song matching '{song_name_query}'. Playing a random one instead.")

    # Play a random song if specific song not found or no query given
    chosen_song = random.choice(music_files)
    full_path = os.path.join(LOCAL_MUSIC_DIR, chosen_song)
    try:
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play()
        current_playing_song = chosen_song
        music_paused = False
        return speak(f"Playing random song: '{chosen_song}'.")
    except pygame.error as e:
        speak(f"Sorry, I couldn't play any music from your local directory: {e}")
        current_playing_song = None
        return 

def pause_local_music():
    """Pauses currently playing local music."""
    global music_paused
    if PYGAME_AVAILABLE and pygame.mixer.music.get_busy() and not music_paused:
        pygame.mixer.music.pause()
        music_paused = True
        return speak("Music paused.")
    elif music_paused:
        return speak("Music is already paused.")
    else:
        return speak("No music is currently playing.")

def unpause_local_music():
    """Unpauses currently paused local music."""
    global music_paused
    if PYGAME_AVAILABLE and music_paused:
        pygame.mixer.music.unpause()
        music_paused = False
        return speak("Music unpaused.")
    elif not pygame.mixer.music.get_busy():
        return speak("No music is playing to unpause.")
    else:
        return speak("Music is not paused.")

def stop_local_music():
    """Stops currently playing local music."""
    global current_playing_song, music_paused
    if PYGAME_AVAILABLE and (pygame.mixer.music.get_busy() or music_paused):
        pygame.mixer.music.stop()
        current_playing_song = None
        music_paused = False
        return speak("Music stopped.")
    else:
        return speak("No music is currently playing or paused.")

def next_local_music():
    """Plays the next random song."""
    speak("Playing next song.")
    play_local_music()
    return 

def what_is_playing():
    """Tells the user what song is currently playing."""
    if current_playing_song:
        return speak(f"Currently playing: {current_playing_song}.")
    else:
        return speak("No music is currently playing.")

# --- External Service Integrations ---

def search_on_website(query, website_url):
    """Searches a specific website (e.g., Google, Wikipedia) or performs a generic web search."""
    if "google.com" in website_url:
        search_query = query.replace("search google for", "").replace("on google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching Google for {search_query}.")
        write_history(query, f"Searching Google for {search_query}.")
    elif "wikipedia.org" in website_url:
        search_query = query.replace("search wikipedia for", "").replace("on wikipedia", "").strip()
        webbrowser.open(f"https://en.wikipedia.org/wiki/{search_query}")
        speak(f"Searching wikipedia for {search_query}.")
        write_history(query, f"Searching wikipedia for {search_query}.")
    elif "youtube.com" in website_url:
        search_query = query.replace("search Youtube for", "").replace("on youtube", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        speak(f"Searching Youtube for {search_query}.")
        write_history(query, f"Searching Youtube for {search_query}.")
    else:
        # Fallback for generic web search
        webbrowser.open(f"{website_url}/search?q={query.replace(' ', '+')}")
        speak(f"Searching {website_url} for {query}.")
        write_history(query, f"Searching {website_url} for {query}.")

def search_on_gemini(query):
    """Uses Google Gemini to answer general questions or provide information."""
    if not GEMINI_AVAILABLE:
        speak("Gemini AI is not available. Please ensure your GEMINI_API_KEY is set and the module is installed.")
        return None # Explicitly return None

    try:
        model = genai.GenerativeModel('gemini-pro')
        # Use a more conversational prompt for general questions
        prompt = f"As a helpful AI assistant, answer the following question concisely and informatively: {query}"
        #response = model.generate_content(prompt)
        # Add a timeout for robustness
        response = model.generate_content(prompt, request_options={'timeout': 60}) # 60 seconds
        response_text = response.text.strip()
        speak(response_text)
        write_history(query, response_text)
        return response_text
    except Exception as e:
        error_message = f"Sorry, I couldn't get a response from Gemini AI. There might be an issue with the API or your query. Error: {e}"
        speak(error_message)
        write_history(query, error_message) # Corrected from query_term to query
        return None

def open_gemini_website_for_query(query_term):
    """Opens Google Search with a query to simulate Gemini web search."""
    if query_term:
        webbrowser.open(f"https://www.google.com/search?q={query_term}")
        write_history(query_term, f"Opening Google Search for '{query_term}'.")
        return speak(f"Opening Google Search for '{query_term}'.")
    else:
        write_history(query_term, "Please tell me what you want to search on Gemini (Google).")
        return speak("Please tell me what you want to search on Gemini (Google).")

def get_weather_forecast(city="Colombo"):
    """Gets current weather and a 5-day forecast using OpenWeatherMap."""
    if not OPENWEATHER_API_KEY:
        speak("OpenWeatherMap API key is not configured. I cannot fetch weather information.")
        return

    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    try:
        # First, get city coordinates (Geocoding API)
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data:
            speak(f"Sorry, I couldn't find the location for '{city}'. Please try a different city name.")
            return

        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        city_name_from_api = geo_data[0]['name'] # Use the official name

        # Then, get forecast using coordinates
        full_url = f"{base_url}lat={lat}&lon={lon}&units=metric&appid={OPENWEATHER_API_KEY}"
        response = requests.get(full_url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        weather_data = response.json()

        current_list = weather_data['list'][0]
        current_temp = current_list['main']['temp']
        feels_like = current_list['main']['feels_like']
        humidity = current_list['main']['humidity']
        description = current_list['weather'][0]['description']
        wind_speed = current_list['wind']['speed']

        speak(f"Current weather in {city_name_from_api}: {description}, with a temperature of {current_temp:.1f} degrees Celsius, feels like {feels_like:.1f} degrees. Humidity is {humidity} percent, and wind speed is {wind_speed} meters per second.")

        speak("Here's a 5-day forecast:")
        # Group forecast data by day
        daily_forecast = {}
        for entry in weather_data['list']:
            date = datetime.datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')
            day_name = datetime.datetime.fromtimestamp(entry['dt']).strftime('%A')
            temp_min = entry['main']['temp_min']
            temp_max = entry['main']['temp_max']
            weather_desc = entry['weather'][0]['description']

            if date not in daily_forecast:
                daily_forecast[date] = {
                    'day': day_name,
                    'min_temp': temp_min,
                    'max_temp': temp_max,
                    'descriptions': [weather_desc]
                }
            else:
                daily_forecast[date]['min_temp'] = min(daily_forecast[date]['min_temp'], temp_min)
                daily_forecast[date]['max_temp'] = max(daily_forecast[date]['max_temp'], temp_max)
                if weather_desc not in daily_forecast[date]['descriptions']:
                    daily_forecast[date]['descriptions'].append(weather_desc)

        for date, data in list(daily_forecast.items())[1:6]: # Get next 5 days, skipping today
            desc_summary = ", ".join(set(data['descriptions'])) # Use set to remove duplicates
            speak(f"{data['day']}: Low of {data['min_temp']:.1f}°C, High of {data['max_temp']:.1f}°C. Generally {desc_summary}.")
            response_text=f"{data['day']}: Low of {data['min_temp']:.1f}°C, High of {data['max_temp']:.1f}°C. Generally {desc_summary}."
            speak(response_text)
            write_history(query, response_text)
            
            

    except requests.exceptions.ConnectionError:
        speak("I couldn't connect to the weather service. Please check your internet connection.")
    except requests.exceptions.Timeout:
        speak("The weather service took too long to respond. Please try again.")
    except requests.exceptions.HTTPError as e:
        speak(f"Error fetching weather data: {e}. The city name might be incorrect or API limits reached.")
    except json.JSONDecodeError:
        speak("Could not parse weather data. The response from the service was invalid.")
    except Exception as e:
        response_text="Hello there! How can i help you today?"
        speak(response_text)
        write_history(query, response_text)
        speak(f"An unexpected error occurred while fetching weather: {e}")

def joke_handler(query):
    joke= pyjokes.get_joke()
    speak(joke)
    write_history(query, joke)

# --- General AI Chat Handler ---

def handle_ai_chat(query):
    """Handles general conversational queries, prioritizing Gemini if available."""
    # Fallback to simple rules or just acknowledge limitation
    if "hi" in query or "hello" in query or "hey" in query or "welcome" in query:
        response_text = "Hello there! How can I help you today?"
        speak(response_text) # Speak it
        # write_history(query, response_text) # Uncomment if desired for these cases
        return response_text # Return the string
    elif "wakeup" in query or "wake" in query:
        response_text="I'm ready! How can i help you sir?"
        return speak(response_text)
        #write_history(query, response_text)
    elif "goodbye" in query or "bye" in query:
        #write_history(query, "Goodbye! Have a great day!")
        return sys.exit(speak("Goodbye! Have a great day!"))
    elif "how are you" in query or "how do you doing" in query:
        response_text="I am doing great, thank you for asking!"+", "+"I am just a program, but I'm functioning well! How can I assist you?"
        speak("I am doing great, thank you for asking!")
        speak("I am just a program, but I'm functioning well! How can I assist you?")
        return response_text
        #write_history(query, response_text)
    elif "jarvis" in query or "voice assistant" in query or "name" in query:
        response_text="Yes sir, I am your voice assistant, designed to help you with various tasks."+", "+"I am your personal AI assistant, created to help you."
        speak("Yes sir, I am your voice assistant, designed to help you with various tasks.")
        speak("I am your personal AI assistant, created to help you.")
        return response_text
        #write_history(query, response_text)
    elif "who are you" in query or "your name" in query:
        speak("I am your personal AI assistant")
        speak("Hi! I am your voice assistantv7.1.")
        speak("Or you can call me JARVIS.")
        speak("designed to help you with various tasks.")
        response_text="I am your personal AI assistant"+", "+"Hi! I am your voice assistantv7.1."+", "+"Or you can call me JARVIS."+", "+"designed to help you with various tasks."
        return response_text
        #write_history(query, response_text)
    elif "who made you" in query or "who created you" in query or "creater" in query:
        response_text="I was created by a human developer. My core intelligence comes from Google Gemini."
        return speak(response_text)
        #write_history(query, response_text)
    elif "what can you do" in query:
        response_text="I can tell you the time and date, open applications, search the web, set alarms, play local music, and more. Just ask me for 'help'."
        return speak(response_text)
        #write_history(query, response_text)
    elif "tell me something interesting" in query or "interesting fact" in query:
        response_text="Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!"
        return speak(response_text)
        #write_history(query, response_text)
    elif "list voice" in query:
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            speak("Available Voices:")
            response_text="Available Voices:"
            write_history(query, response_text)
            for i, voice in enumerate(voices):
                speak(f"  Voice {i}:")
                speak(f"    ID: {voice.id}")
                speak(f"    Name: {voice.name}")
                speak(f"    Languages: {voice.languages}")
                speak(f"    Gender: {voice.gender}")
                speak(f"    Age: {voice.age}")
                speak("-" * 20)
                response_text=f"  Voice {i}:"+", "+f"    ID: {voice.id}"+", "+f"    Name: {voice.name}"+", "+f"    Languages: {voice.languages}"+", "+f"    Gender: {voice.gender}"+", "+f"    Age: {voice.age}"+", "+("-" * 20)
                write_history(query, response_text)
            engine.stop() # It's good practice to stop the engine when done
            response_text="list voice printed."
            return response_text
        except Exception as e:
            speak(f"Error listing voices: {e}")
            speak("Please ensure pyttsx3 is installed (`pip install pyttsx3`) and your system has a text-to-speech engine configured.")
            return
    else:
        if GEMINI_AVAILABLE:
            speak("Let me think...")
            response = search_on_gemini(query)
            if response:
                response_text=response
                #write_history(query, response_text)
                return response
            else:
                response_text="I had trouble with Gemini, but I can still try to answer simpler questions or search the web."
                speak(response_text)
                #write_history(query, response_text)
                return "I had trouble with Gemini, but I can still try to answer simpler questions or search the web."
        else:
            response_text="I'm sorry, I don't have a direct answer for that right now, as my advanced AI capabilities are currently limited without Gemini. Would you like me to search the web for it?"
            speak(response_text)
            #write_history(query, response_text)
            return "Sorry, I cannot process this without AI. Would you like me to search the web?"

def run_assistant():
    """Main function to run the voice assistant."""
    wish_user()

    # Dictionary to map command prefixes to functions
    # Sort keys by length in descending order to prioritize more specific commands
    # e.g., "search wikipedia for" should match before "search for"
    command_processor = {
        "what time is it": lambda q: speak(datetime.datetime.now().strftime("%I:%M %p")),
        "time": lambda q: speak(datetime.datetime.now().strftime("%I:%M %p")),
        "what is the date": lambda q: speak(datetime.datetime.now().strftime("%A, %B %d, %Y")),
        "date": lambda q: speak(datetime.datetime.now().strftime("%A, %B %d, %Y")),
        "tell me a joke": lambda q: speak(pyjokes.get_joke()),
        #"joke": lambda q: speak(pyjokes.get_joke()),
        #"joke": lambda q: joke_handler(q.replace("joke","").strip()),
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
        "weather": lambda q: get_weather_forecast(q.replace("weather in", "").strip()),
        "what is the weather in": lambda q: get_weather_forecast(q.replace("what is the weather in", "").strip()),
        "how's the weather in": lambda q: get_weather_forecast(q.replace("how's the weather in", "").strip()),
        "help": lambda q: speak("I can tell you the time and date, tell jokes, open websites like Google or YouTube, open applications like Notepad or Calculator. I can set alarms, play local music, and search Wikipedia or the web. I can also answer general questions using AI if configured. Just ask! For example: 'What time is it?', 'Open YouTube', 'Set an alarm for 7 AM', 'Search Wikipedia for World War 2', 'What is the weather in London?'"),
        "command": lambda q: speak("I can tell you the time and date, tell jokes, open websites like Google or YouTube, open applications like Notepad or Calculator. I can set alarms, play local music, and search Wikipedia or the web. I can also answer general questions using AI if configured. Just ask! For example: 'What time is it?', 'Open YouTube', 'Set an alarm for 7 AM', 'Search Wikipedia for World War 2', 'What is the weather in London?'"),
        "commands": lambda q: speak("I can tell you the time and date, tell jokes, open websites like Google or YouTube, open applications like Notepad or Calculator. I can set alarms, play local music, and search Wikipedia or the web. I can also answer general questions using AI if configured. Just ask! For example: 'What time is it?', 'Open YouTube', 'Set an alarm for 7 AM', 'Search Wikipedia for World War 2', 'What is the weather in London?'"),
        "thank you": lambda q: speak("You're welcome!"),
        "thanks": lambda q: speak("My pleasure!"),
        #"goodbye": lambda q: sys.exit(speak("Goodbye! Have a grate day!")),
        #"bye": lambda q: sys.exit(speak("Goodbye. Have a grate day!")),
        #"exit": lambda q: sys.exit(speak("Exiting. Have a grate day!")),
        #"quit": lambda q: sys.exit(speak("Quitting. See you soon!")),
        #"shutdown": lambda q: sys.exit(speak("Shutdown. Have a grate day!")),
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
            response_text = "Alarm stopped."
            handled = True
        elif "stop music" in query or "turn off music" in query:
            stop_local_music()
            response_text = "Music stopped."
            handled = True
        elif "pause music" in query:
            pause_local_music()
            response_text = "Music paused."
            handled = True
        elif "unpause music" in query or "resume music" in query:
            unpause_local_music()
            response_text = "Music unpaused."
            handled = True
        elif "next song" in query:
            next_local_music()
            response_text = "Playing next song."
            handled = True
        elif "what is playing" in query or "what song is this" in query:
            what_is_playing()
            response_text = current_playing_song if current_playing_song else "No music is currently playing."
            handled = True
        elif "shutdown" in query:
            response_text = "Jarvis shutting down. Goodbye!"
            speak(response_text)
            write_history(query, response_text)
            handled = True
            break
        elif "hello jarvis" in query:
            response_text = "Hello! How can I help you today?"
            speak(response_text)
            handled = True

        if not handled: # Process other commands only if not already handled by specific media/alarm logic
            for command_prefix in sorted_commands:
                if query.startswith(command_prefix):
                    func = command_processor[command_prefix]
                    func(query) # Pass the full query to the function
                    response_text = f"Executed: {command_prefix}" # Generic placeholder for history
                    handled = True
                    break

        if not handled:
            # If no specific command matched, try to handle it with AI or a generic response
            response_text = handle_ai_chat(query)
            if not response_text:
                response_text = "I'm sorry, I didn't understand that. Can you please rephrase?"

        write_history(query, response_text)

if __name__ == "__main__":
    #WAKEUP_COMMAND = "jarvis"
    #speak(f"Waiting for wakeup command: '{WAKEUP_COMMAND}'...")
    speak(f"Waiting for wakeup command: WAKEUP_COMMAND")
    while True:
        # We'll use input() here so the program doesn't constantly try to listen
        # with SpeechRecognition if SPEECH_RECOGNITION_AVAILABLE is True,
        # until the wakeup command is given.
        # Once run_assistant is called, take_command will handle speech input.
        #typed_command = input(f"Say '{WAKEUP_COMMAND}' or type 'exit' to quit: ").lower()
        #typed_command = input(f"Say 'WAKEUP_COMMAND' or type 'exit' to quit: ").lower()
        #command = take_command()

        # if SPEECH_RECOGNITION_AVAILABLE:
        #     command = take_command()
        # else:
        # command = input(f"Say '{WAKEUP_COMMAND}' or type 'exit' to quit: ").lower()
        command = input(f"Say 'WAKEUP_COMMAND' or type 'exit' to quit: ").lower()
        #write_history(f"Waiting for wakeup command: WAKEUP_COMMAND"+"\n"+f"Say 'WAKEUP_COMMAND' or type 'exit' to quit: ", command)
        
        if WAKEUP_COMMAND in command:
            speak("Wakeup command received! Starting assistant...")
            run_assistant()
            # After run_assistant exits, we return here and wait for the wakeup command again.
            speak(f"\nAssistant session ended. Waiting for wakeup command: 'WAKEUP_COMMAND'...")
        elif "exit" in command or "quit" in command:
            speak("Exiting program.")
            break
        else:
            speak(f"Still waiting for 'WAKEUP_COMMAND'. You said: '{command}'")
