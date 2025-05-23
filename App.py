import os
import sys
import time
import datetime
import webbrowser
import threading
import pygame
import requests
import speech_recognition as sr
import wikipedia
import psutil
import tkinter as tk
from tkinter import scrolledtext, Button
from tkinter import filedialog, scrolledtext
import pytesseract
from PIL import Image, ImageTk
import fitz
import customtkinter as ctk
from openai import OpenAI
import pickle
import base64
import time
import google.auth
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytesseract
from tkinter import filedialog, messagebox
import pyautogui
import tkinter as tk
from PIL import Image, ImageTk
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import cv2
from customtkinter import CTkImage
from API_KEY import OPENAI_API_KEY
from API_KEY import client
from API_KEY import Weather_api_key
import random
import io
import screen_brightness_control as sb
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


# Define Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# OpenAI API Key


pygame.mixer.init()
recognizer = sr.Recognizer()
mic_active = True
current_module = "Vox"  # Default module
uploaded_image = None # For Image Recognition Module
image_analysis_output = None # For Image Recognition Module

def get_creator_info():
    creators = [
        {
            "name": "Shantanu Dudhankar",
            "insta_handle": "@shantaannu",
            "email": "Shantanududhankar670@gmail.com"
        },
        {
            "name": "Sneha Patil",
            "insta_handle": "@snehapatil",
            "email": "sneha.patil@example.com"
        },
        {
            "name": "Sanket Deshmukh",
            "insta_handle": "@sanketdeshmukh",
            "email": "sanket.deshmukh@example.com"
        },
        {
            "name": "Harsh Verma",
            "insta_handle": "@harshverma",
            "email": "harsh.verma@example.com"
        },
        {
            "name": "Shiv Kapoor",
            "insta_handle": "@shivkapoor",
            "email": "shiv.kapoor@example.com"
        }
    ]

    response = "I was built by an amazing team:\n"
    for creator in creators:
        response += (
            f"- {creator['name']} (Instagram: {creator['insta_handle']}, Email: {creator['email']})\n"
        )

    return response
def process_vox_query(message):
    ai_response(message)

def process_code_mate_query(message):
    ai_response(f"Write or explain this code: {message}")

def process_image_query(message):
    global uploaded_image
    if uploaded_image:
        prompt = message or "What's in this image?"
        base64_image = encode_image_from_memory(uploaded_image)
        analyze_uploaded_image(base64_image, prompt)
    else:
        speak("Please upload an image first.")
        update_chat("Assistant: Please upload an image first.", "assistant")

def process_health_query(message):
    ai_response(f"Provide health advice based on: {message}")

# Gmail Automation
def authenticate_gmail():
    """Authenticate and return the Gmail service."""
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "C:/Users/shant/Desktop/ChatBot/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)

# Define contacts
contacts = {
    "akash": "akash@example.com",
    "alex": "shantaannu@gmai.com",
    "shantanu": "shantanududhankar670@gmail.com",
    "sanket": "sanketappa57@gmail.com",
    "Sneha": "snehabagde11@gmail.com"
}

def send_email(recipient_name, subject, body):
    """Send an email via Gmail API after resolving recipient's email."""
    try:
        recipient_name = recipient_name.lower()
        recipient_email = contacts.get(recipient_name)

        if not recipient_email:
            speak(f"I couldn't find an email for {recipient_name}. Please provide the email address.")
            recipient_email = take_command()

        if "@" not in recipient_email or "." not in recipient_email:
            speak("That doesn't seem like a valid email address.")
            return

        # Store new email for future use
        contacts[recipient_name] = recipient_email

        service = authenticate_gmail()
        message = EmailMessage()
        message.set_content(body)
        message["To"] = recipient_email
        message["From"] = ""
        message["Subject"] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_request = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": encoded_message})
            .execute()
        )

        print(f"Email sent to {recipient_email} with Message ID: {send_request['id']}")
        speak(f"Email sent to {recipient_name}")

    except Exception as e:
        print(f"Error sending email: {e}")
        speak("I couldn't send the email.")

instructions = """Voice Affect: Neutral yet engaging; articulate with consistent pitch and tone, conveying confidence and reliability."""
medical_instructions = """Voice Affect: Neutral yet engaging; articulate with consistent pitch and tone, conveying confidence and reliability"""

# Speak Function
def speak(text):
    """Convert text to speech and play it."""
    try:
        # update_chat(f"Assistant: {text}", "assistant")
        root.update_idletasks()

        # Init pygame mixer early
        pygame.mixer.init()
        print("Pygame mixer initialized.")

        speech_file_path = "speech.mp3"
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="onyx",
            input=text,
            instructions=instructions if current_module != "Health Adviser" else medical_instructions
        )

        with open(speech_file_path, "wb") as f:
            f.write(response.content)

        pygame.mixer.music.load(speech_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.quit()
        os.remove(speech_file_path)

    except pygame.error as pg_err:
        print(f"Pygame error in speak function: {pg_err}")
    except Exception as e:
        print(f"Error in speak function: {e}")

def stop_speaking():
    """Stop the current speech playback."""
    try:
        pygame.mixer.music.stop()
        # pygame.mixer.quit()
    except Exception as e:
        print(f"Error in stop_speaking: {e}")

# take command from users
def take_command():
    """Listen for user input and return recognized text."""
    global mic_active
    if not mic_active:
        return ""

    with sr.Microphone() as source:
        recognizer.pause_threshold = 1.2
        recognizer.adjust_for_ambient_noise(source, duration=0.9)

        try:
            print("Listening...")
            audio = recognizer.listen(source, phrase_time_limit=15)
            print("Audio input received")
            query = recognizer.recognize_google(audio, language="en-in")
            update_chat(f"You: {query}", "user")
            return query.lower()
        except Exception as e:
            return ""

def toggle_mic():
    """Toggle microphone on/off."""
    global mic_active
    mic_active = not mic_active
    mic_button.configure(text="Unmute" if not mic_active else "Mute")

def wish() -> None:
    hour = int(datetime.datetime.now().hour)
    greetings = {
        "morning": [],
        "afternoon": [],
        "evening": []
    }
    city = "Nagpur"
    api_key = Weather_api_key

    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        weather_report = "Weather data not available."
    else:
        weather_data = response.json()
        weather_description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        weather_report = f"today's Temperature: {temperature}°C in {city} city & Humidity: {humidity}%."

    greetings["morning"] = [
    #f"Good morning!",
    f"Good morning! {weather_report}. I hope your day is off to a wonderful start. How can I assist you today?",
    f"Good morning! {weather_report}. A productive day awaits. Let me know how I can support you.",
    f"Good morning! {weather_report}. It's a great time to plan for success. What can I help you with today?"
]

    greetings["afternoon"] = [
    # f"Good afternoon!",
    f"Good afternoon! {weather_report}. I hope your day is going smoothly. Is there anything you'd like assistance with?",
    f"Good afternoon! {weather_report}. Midday is the perfect time to refocus. Let me know if you need any help!",
    f"Good afternoon! {weather_report}. Let’s make the most of the day. How can I assist you?"
]

    greetings["evening"] = [
    f"Good evening! {weather_report}. I hope your day has been productive. Is there anything you need before winding down?",
    f"Good evening! {weather_report}. The evening is a great time to reflect and plan ahead. What can I do for you?",
    f"Good evening! {weather_report}. Let’s wrap up the day on a high note. How may I assist you?"
]
    if hour >= 0 and hour < 12:
        greeting = random.choice(greetings["morning"])
    elif hour >= 12 and hour < 18:
        greeting = random.choice(greetings["afternoon"])
    else:
        greeting = random.choice(greetings["evening"])

    speak(greeting)
    update_chat("Vox is here to assist you!", "assistant") # Initial message

# Ai driven responces
def ai_response(query):
    if not OPENAI_API_KEY:
        speak("API key is missing. Please set your OpenAI API key.")
        return
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": instructions if current_module != "Health Adviser" else medical_instructions},
                      {"role": "user", "content": query}],
            temperature=0.9,
            max_tokens=200,
        )
        response_text = response.choices[0].message.content
        update_chat(f"Assistant: {response_text}", "assistant")
        speak(response_text)
    except Exception as e:
        print(f"Error in AIResponse: {e}")
        speak("Oops! Something went wrong with the AI. Please try again.")

# file upload
# Configure Tesseract path (update it according to your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def upload_image():
    global uploaded_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if file_path:
        try:
            uploaded_image = Image.open(file_path).convert("RGB")
            img_thumbnail = uploaded_image.copy()
            img_thumbnail.thumbnail((250, 250))
            img_tk = ImageTk.PhotoImage(img_thumbnail)
            image_label.config(image=img_tk)
            image_label.image = img_tk
            update_chat("Assistant: Image uploaded.", "assistant")
            speak("Image uploaded.")
        except Exception as e:
            print(f"Error loading image: {e}")
            update_chat("Assistant: Error loading image.", "assistant")
            speak("Error loading image.")

def display_image(file_path):
    image = Image.open(file_path)
    image = image.resize((250, 250), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(image)
    image_label.config(image=img_tk)
    image_label.image = img_tk
    extract_text(file_path)

def extract_text(file_path):
    text = pytesseract.image_to_string(Image.open(file_path)).strip()

    if text:
        update_chat(f"Assistant (OCR): {text}", sender="assistant")
        process_command(text)
    else:
        update_chat("Assistant: No readable text found in the image.", sender="assistant")

def close_program(program_name):
    """Find and close a running program by name."""
    for process in psutil.process_iter(['pid', 'name']):
        if program_name.lower() in process.info['name'].lower():
            try:
                psutil.Process(process.info['pid']).terminate()
                update_chat(f"Assistant: Closed {program_name}", "assistant")
                speak(f"Closed {program_name}")
                return
            except Exception as e:
                print(f"Error closing {program_name}: {e}")
                update_chat(f"Assistant: Error closing {program_name}.", "assistant")
                speak(f"Error closing {program_name}.")
    update_chat(f"Assistant: {program_name} is not running.", "assistant")
    speak(f"{program_name} is not running.")

reminders = {}

def set_reminder(name, reminder_time, reminder_message):
    reminders[name] = (reminder_time, reminder_message)
    threading.Thread(target=wait_for_reminder, args=(name,)).start()

def wait_for_reminder(name):
    reminder_time, reminder_message = reminders[name]
    while datetime.datetime.now() < reminder_time:
        time.sleep(60)  # Check every minute
    speak(f"Reminder: {reminder_message}")
    update_chat(f"Reminder: {reminder_message}", "Assistant")
    del reminders[name]

def check_reminders():
    while True:
        for name, (reminder_time, reminder_message) in reminders.items():
            if datetime.datetime.now() >= reminder_time:
                speak(f"Reminder: {reminder_message}")
                update_chat(f"Reminder: {reminder_message}", "Assistant")
                del reminders[name]
        time.sleep(60)  # Check every minute

# Start reminder checker thread
threading.Thread(target=check_reminders, daemon=True).start()

# Medical Symptoms
def analyze_symptoms(symptoms, age, gender, location):
    """Get AI-generated response and speak it."""
    if not OPENAI_API_KEY:
        speak("API key is missing. Please set your OpenAI API key.")
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": medical_instructions},
                {"role": "user", "content": f"I'm experiencing {symptoms}. I'm {age} years old, {gender}, and from {location}. Please advise."}
            ],
            temperature=0.9,
            max_tokens=500,top_p=1,
        )

        response_text = response.choices[0].message.content
        update_chat(f"Assistant: {response_text}", "assistant")
        return response_text  # Return response instead of speaking it inside function

    except Exception as e:
        speak("Oops! Something went wrong with the health analysis. Try again later.")
        print(f"Error in analyze_symptoms: {e}")
        return None

def handle_command():
    """Continuously listen and process commands."""
    while True:
        query = take_command()
        if not query:
            continue

        process_command(query)

def process_command(query: str) -> None:
    global current_module

    if current_module == "Vox":
        if "open notepad" in query:
            speak("opening notepad")
            os.startfile("C:\\Windows\\System32\\notepad.exe")
        elif "close notepad" in query:
            speak("closing notepad")
            close_program("notepad.exe")
        elif "introduce us" in query or "introduce" in query:
            speak("Allow me to introduce myself and my creators!")
            update_chat("Allow me to introduce myself and my creators!", "Assistant")

            # Additional introduction response
            response = (
                "Hello, everyone! I am Vox, your friendly and intelligent desktop assistant. "
                "I was built by a talented team: Shantanu, Sneha, Sanket, Harsh, and Shiv. "
                "My name comes from the Latin word for 'voice,' symbolizing my role as your digital vocal companion. "
                "I’m here to help with anything you need—from managing emails, mastering code, setting reminders, and so much more. "
                "Whatever the task, big or small, I'm always up for it. Let me know how I can assist you!")
            speak(response)
            update_chat(response, "Assistant")
        elif "ip address" in query:
            try:
                ip = requests.get('https://api.ipify.org').text
                update_chat(f"Assistant: Your IP address is {ip}", "assistant")
                speak(f"Your IP address is {ip}")
            except:
                speak("I couldn't retrieve your IP address.")
        elif "weather" in query.lower():
            speak("Which city's weather would you like to know?")
            city = take_command()
            if city:
                base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Weather_api_key}&units=metric"
                try:
                    response = requests.get(base_url)
                    weather_data = response.json()
                    if weather_data["cod"] == 200:
                        weather_description = weather_data["weather"][0]["description"]
                        temperature = weather_data["main"]["temp"]
                        humidity = weather_data["main"]["humidity"]
                        wind_speed = weather_data["wind"]["speed"]
                        speak(f"Weather in {city}: {weather_description}. Temperature: {temperature}°C. Humidity: {humidity}%. Wind Speed: {wind_speed} m/s.")
                        update_chat(f"Weather in {city}: {weather_description}. Temperature: {temperature}°C. Humidity: {humidity}%. Wind Speed: {wind_speed} m/s.", "assistant")
                    else:
                        speak("City not found.")
                        update_chat("City not found.", "assistant")
                except Exception as e:
                    speak("Error fetching weather data.")
                    update_chat("Error fetching weather data.", "assistant")
                    print(f"Error: {e}")
        elif "wikipedia" in query:
            speak("opening Wikipedia")
            speak("What would you like to search on Wikipedia?")
            search_query = take_command()
            if search_query:
                try:
                    result = wikipedia.summary(search_query, sentences=2)
                    update_chat(f"Assistant: {result}", "assistant")
                    speak(result)
                except:
                    speak("Error fetching Wikipedia results.")
        elif "open youtube" in query:
            speak("Opening Youtube")
            speak("What should I search on Youtube?")
            search_term = take_command()
            if search_term:
               # webbrowser.open(f"http://google.com/search?q={search_term}&tbm=vid")
               #webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
               webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}")

        elif "close youtube" in query:
            close_program("chrome.exe")  # Adjust based on your browser
            close_program("msedge.exe")
        elif "open google" in query:
            speak("Opening Google")
            speak("What should I search on Google?")
            search_term = take_command()
            if search_term:
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
        elif "close google" in query:
            close_program("chrome.exe")  # Adjust based on your browser
            close_program("msedge.exe")
        elif "close browser" in query:
            for browser in ["chrome.exe", "firefox.exe", "msedge.exe", "opera.exe"]:
                close_program(browser)
        elif "open calculator" in query:
            speak("Opening calculator")
            os.startfile("calc.exe")

        elif "close calculator" in query:
            speak("closing Calculator")
            close_program("CalculatorApp.exe")
        elif "open mail" in query:
            speak("Opening Mail")
            webbrowser.open(f"https://mail.google.com/mail/u/1/#inbox")
        elif "close Gmail" in query:
            for browser in ["chrome.exe", "firefox.exe", "msedge.exe", "opera.exe"]:
                close_program(browser)
        elif "exit" in query or "bye" in query or "quit" in query:
            update_chat("Assistant: Goodbye!", "assistant")
            speak("Goodbye! Have a great day.")
            time.sleep(2)
            root.quit()
                
        elif "take screenshot" in query:
            speak("Taking screenshot")
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            speak("Screenshot saved as screenshot.png")
            update_chat("Assistant: Screenshot taken and saved as screenshot.png", "assistant")

        elif "send email" in query:
            speak("To whom should I send the email?")
            recipient = take_command()

            if recipient:
                speak("What should be the subject?")
                subject = take_command()

                speak("What should I write in the email?")
                body = take_command()
                send_email(recipient, subject, body)

        elif any(keyword in query.lower() for keyword in ["who made you", "who created you","who created"]):
            speak(get_creator_info())
            update_chat(get_creator_info(), "Assistant")
        elif "set reminder" in query:
            speak("What is the reminder time? (e.g., 05 PM)")
            reminder_time_str = take_command()
            if reminder_time_str:  # Check if the input is not empty
                try:
                    reminder_time = datetime.datetime.strptime(reminder_time_str, "%I %p")
                    reminder_time = reminder_time.replace(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
                    if reminder_time < datetime.datetime.now():
                        reminder_time = reminder_time.replace(day=datetime.datetime.now().day + 1) # Set for tomorrow if time has passed
                    speak("What is the reminder message?")
                    reminder_message = take_command()
                    set_reminder("reminder", reminder_time, reminder_message)
                    speak(f"Reminder set for {reminder_time.strftime('%I:%M %p')}: {reminder_message}")
                    update_chat(f"Reminder set for {reminder_time.strftime('%I:%M %p')}: {reminder_message}", "Assistant")
                except ValueError:
                    speak("Invalid time format. Please try again using format like '05 PM'.")
            else:
                speak("No input detected. Please try again.")
        elif "analyze image" in query.lower() and current_module == "Image Recognition":
            speak("Please describe what you want to know about the image.")
            image_prompt = take_command()
            if image_prompt:
                process_image_query(image_prompt)
            else:
                speak("Please provide a description to analyze the image.")
                update_chat("Assistant: Please provide a description to analyze the image.", "assistant")
        else:
            process_vox_query(query)

    elif current_module == "Code Mate":
        if "medical" in query or "symptoms" in query:
            speak("This is not a medical module. Please switch to the Health Adviser module.")
            return

        elif any(kw in query.lower() for kw in ["generate code", "write code", "create a program", "make a script"]):
            try:
                speak("Processing your coding request...")

                coding_instructions = "You are a helpful coding assistant. Provide clean and efficient code based on the user’s request. Code should be working"

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": coding_instructions},
                        {"role": "user", "content": "Write code for the following task: " + query}
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )

                response_text = response.choices[0].message.content
                print("GPT Response:", response_text)
                update_chat(f"Assistant: {response_text}", "assistant")
                return response_text

            except Exception as e:
                import traceback
                print("Error generating code:", e)
                print(traceback.format_exc())
                speak("Sorry, something went wrong while generating the code.")
                return "Error generating code."

    elif current_module == "Image Recognition":
        if "extract text" in query.lower():
            speak("Please upload an image to extract text from.")
        elif "analyze image" in query.lower():
            speak("Please describe what you want to know about the image.")
            image_prompt = take_command()
            if image_prompt:
                process_image_query(image_prompt)
            else:
                speak("Please provide a description to analyze the image.")
                update_chat("Assistant: Please provide a description to analyze the image.", "assistant")
        else:
            process_image_query("") # Send an empty query to trigger image analysis if needed

    elif current_module == "Health Adviser":
        if "medical" in query or "symptoms" in query:
            try:
                speak("What symptoms are you experiencing?")
                update_chat("What symptoms are you experiencing?", "Assistant")
                symptoms = take_command()

                speak("What is your approximate age?")
                update_chat("What is your approximate age?", "Assistant")
                age = take_command()

                speak("What is your gender?")
                update_chat("What is your gender?", "Assistant")
                gender = take_command()

                # You can structure the user's query for clarity
                full_query = f"I am experiencing the following symptoms: {symptoms}. My age is {age} and my gender is {gender}."

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": medical_instructions},
                        {"role": "user", "content": full_query}
                    ],
                    temperature=0.9,
                    max_tokens=500,
                    top_p=1,
                )

                response_text = response.choices[0].message.content
                update_chat(f"Assistant: {response_text}", "assistant")
                speak(response_text)
                return response_text

            except Exception as e:
                print(f"Error generating medical response: {e}")
                speak("Sorry, I couldn't process the medical query.")
                return "Error generating medical response."

    else:
        ai_response(query)

def generate_code_snippet(query):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Generate code snippet for: {query}"}],
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating code: {e}")
        speak("Error generating code snippet.")
        return "Error generating code."

def copy_code(text_box):
    code_snippet = text_box.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(code_snippet)
    speak("Code copied to clipboard!")

def update_chat(text: str, sender: str) -> None:
    try:
        chat_area.config(state=tk.NORMAL)
        if sender == "user":
            chat_area.insert(tk.END, f"You: {text}\n", "user")
            chat_area.tag_config("user", foreground="#a8dadc", justify=tk.RIGHT)
        else:
            chat_area.insert(tk.END, f"{text}\n", "assistant")
            chat_area.tag_config("assistant", foreground="#45a247", justify=tk.LEFT)
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)
    except Exception as e:
        print(f"Error updating chat: {e}")

def send_text() -> None:
    query = text_entry.get()
    text_entry.delete(0, tk.END)
    update_chat(f"You: {query}", "user")
    process_command(query)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def switch_module(module_name):
    global current_module, uploaded_image
    current_module = module_name
    update_chat(f"Switched to {module_name} module.", "assistant")
    speak(f"Switched to {module_name} module.")
    chat_area.config(state=tk.NORMAL)
    chat_area.delete("1.0", tk.END)
    chat_area.config(font=("Poppins", 12))
    if module_name == "Image Recognition":
        chat_area.insert("1.0", f"{module_name} is ready. Upload an image and ask questions!\n", "assistant")
        uploaded_image = None # Reset uploaded image when switching
        image_label.config(image='') # Clear previous image
        image_label.image = None
    elif module_name == "Vox":
        chat_area.insert("1.0", f"{module_name} is here to assist you!\n", "assistant")
    elif module_name == "Code Mate":
        chat_area.insert("1.0", f"{module_name} is ready for your code queries!\n", "assistant")
    elif module_name == "Health Adviser":
        chat_area.insert("1.0", f"{module_name} is here to provide health advice.\n", "assistant")
    chat_area.tag_config("assistant", foreground="#45a247", justify=tk.LEFT)
    chat_area.config(state=tk.DISABLED)

def encode_image_from_memory(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def analyze_uploaded_image(base64_image, prompt):
    global image_analysis_output
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )
        image_analysis_output = response.choices[0].message.content
        update_chat(f"Assistant (Vision): {image_analysis_output}", "assistant")
        speak(image_analysis_output)

    except Exception as e:
        print(f"Error analyzing image: {e}")
        speak("Error analyzing the image.")
        update_chat("Assistant: Error analyzing the image.", "assistant")

# GUI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("AI Voice Assistant Dashboard")
root.geometry("800x667")

# Sidebar Frame
sidebar_frame = ctk.CTkFrame(root, width=150, corner_radius=10)
sidebar_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
sidebar_frame.grid_rowconfigure(6, weight=1)

vox_button = ctk.CTkButton(sidebar_frame, text="Vox", command=lambda: switch_module("Vox"), font=("Poppins", 14))
vox_button.pack(pady=(20, 10), padx=10, fill="x")

code_mate_button = ctk.CTkButton(sidebar_frame, text="Code Mate", command=lambda: switch_module("Code Mate"), font=("Poppins", 14))
code_mate_button.pack(pady=10, padx=10, fill="x")

image_recognition_button = ctk.CTkButton(sidebar_frame, text="Image Recognition", command=lambda: switch_module("Image Recognition"), font=("Poppins", 14))
image_recognition_button.pack(pady=10, padx=10, fill="x")

health_adviser_button = ctk.CTkButton(sidebar_frame, text="Health Adviser", command=lambda: switch_module("Health Adviser"), font=("Poppins", 14))
health_adviser_button.pack(pady=10, padx=10, fill="x")

creator_info_button_sidebar = ctk.CTkButton(sidebar_frame, text="Creator Info", command=lambda: [get_creator_info()], fg_color="gray", font=("Poppins", 12))
creator_info_button_sidebar.pack(pady=(20, 10), padx=10, fill="x", side="bottom")

upload_button_sidebar = ctk.CTkButton(sidebar_frame, text="Upload Image", command=upload_image, fg_color="gray", font=("Poppins", 12))
upload_button_sidebar.pack(pady=10, padx=10, fill="x", side="bottom")

# Main Chat Area Frame
main_chat_frame = ctk.CTkFrame(root, corner_radius=10)
main_chat_frame.grid(row=0, column=1, padx=(0, 20), pady=(20, 0), sticky="nsew")
main_chat_frame.grid_rowconfigure(0, weight=1)
main_chat_frame.grid_columnconfigure(0, weight=1)

chat_area = tk.Text(main_chat_frame, wrap=tk.WORD, bg="#2f2f2f", fg="#ffffff", state=tk.DISABLED)
chat_area.pack(padx=20, pady=15, fill="both", expand=True)
chat_area.config(font=("Poppins", 12))

# Image Label (initially empty)
image_label = tk.Label(main_chat_frame, bg="#2f2f2f")
image_label.pack(pady=10)

# Input Frame
input_frame = ctk.CTkFrame(root, corner_radius=10)
input_frame.grid(row=1, column=1, padx=(0, 20), pady=(0, 20), sticky="ew")
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=0)
input_frame.grid_columnconfigure(2, weight=0)

# Text Entry
text_entry = ctk.CTkEntry(input_frame, placeholder_text="Type a command...", font=("Poppins", 13))
text_entry.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="ew")
text_entry.bind("<Return>", lambda event: send_text())

# Send Button
send_button = ctk.CTkButton(input_frame, text="Send", command=send_text, font=("Poppins", 13))
send_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

# Mic Button
mic_button = ctk.CTkButton(input_frame, text="Mute", command=toggle_mic, fg_color="red", font=("Poppins", 13))
mic_button.grid(row=0, column=2, padx=(10, 20), pady=10, sticky="e")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Stop Button Below
input_frame.grid_columnconfigure(0, weight=1)
stop_button = ctk.CTkButton(input_frame, text="Stop", command=stop_speaking, fg_color="cyan", text_color="black", font=("Poppins", 13))
stop_button.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="nsew")

wish()
# Start continuous voice listening in a separate thread
threading.Thread(target=handle_command, daemon=True).start()

root.mainloop()