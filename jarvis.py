import psutil
import pyttsx3
import speech_recognition as sr
from datetime import datetime, timedelta
import os
import random
import wikipedia
import webbrowser
import sys
import time
import pyautogui
import requests
import instaloader
import geocoder
import google.generativeai as genai
from bs4 import BeautifulSoup
import speedtest
import pywhatkit
import re
from deep_translator import GoogleTranslator
from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer, get_lexer_by_name
from pygments.formatters import TerminalFormatter
from dotenv import load_dotenv

load_dotenv('config.env')

#API KEY Environment
AI_API_KEY = os.getenv("AI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
COUNTRY = os.getenv("COUNTRY")
#Ai API CALLING
genai.configure(api_key = AI_API_KEY)

#Credentials calling
NAME = os.getenv("NAME")
PLACE = os.getenv("PLACE")
PASSWORD = os.getenv("PASSWORD")

# speech function
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
# engine.setProperty('rate', 180)


#REMINDER
def get_greeting():
    current_hour = datetime.now().hour
    if current_hour == 7:
        return "Good Morning sir,"
    elif current_hour == 12:
        return "Good Afternoon sir,"
    elif current_hour == 16:
        return "Good Evening sir,"
    elif current_hour == 21:
        return "Good Night sir,"
    else:
        return None


def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        return battery.percent, battery.power_plugged
    else:
        return None, None

def speak_greeting_and_time():
    greeting = get_greeting()
    if greeting is not None:
        speak(greeting)
    speak_time()


def speak_time():
    now = datetime.now().strftime("%I:%M %p")
    speak(f"Time is {now} sir")


# Speak function
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# weather information
def weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={PLACE}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"].capitalize()

        # Get current day and time
        now = datetime.now()
        day = now.strftime("%A")
        time = now.strftime("%I:%M %p")

        speak(f"Current weather is {day} {time}, {description} sir.")
    else:
        speak("Sorry sir, I couldn't fetch the weather details.")


# Take command function
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=None, phrase_time_limit=None)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said:{query}")
    except Exception as e:
        # speak("Sorry sir, I couldn't understand anything please say again...")
        return "none"
    query = query.lower()
    return query


def wish():
    hour = int(datetime.now().hour)
    # tt = time.strftime("%I:%M %p")
    if hour >= 0 and hour < 12:
        speak(f"Good Morning sir")  # , now {tt}
    elif hour >= 12 and hour < 17:
        speak(f"Good Afternoon sir")
    elif hour >= 17 and hour < 21:
        speak(f"Good Evening sir")
    else:
        speak(f"Good Night sir")
    weather()



# Alarm set
def set_alarm():
    speak("Please say the alarm time sir. For example, 7 45 or 10 45")
    alarm_time = takecommand()
    if ':' in alarm_time:
        # Split the time into hours and minutes
        parts = alarm_time.split(':')
        hours = parts[0]
        minutes = parts[1]
    elif "o'clock" in alarm_time:
        # Extract the hour from the input
        hour_match = re.search(r'(\d+)', alarm_time)
        if hour_match:
            hour = hour_match.group(1)
            if 1 <= int(hour) <= 12:  # Ensure the hour is within range
                hours = hour
                minutes = "00"

        else:
            speak("Sorry sir, I couldn't understand the time. Please try again.")
            set_alarm()
            return
    else:
        # Split the time into hours and minutes
        parts = alarm_time.split()
        if len(parts) == 1:
            # If only one part is provided, assume it's in the format "745"
            time_str = parts[0]
            if len(time_str) == 3:
                hours = time_str[0]
                minutes = time_str[1:]
            elif len(time_str) == 4:
                hours = time_str[:2]
                minutes = time_str[2:]
            else:
                speak("Sorry sir, I couldn't understand the time format. Please try again.")
                set_alarm()
                return
        elif len(parts) == 2:
            # If two parts are provided, assume it's in the format "10 45"
            hours = parts[0]
            minutes = parts[1]
        else:
            speak("Sorry sir, I couldn't understand the time format. Please try again.")
            set_alarm()
            return

    speak("Please say AM or PM for the alarm sir.")
    am_pm = takecommand().lower()

    if hours.isdigit() and minutes.isdigit() and am_pm in ['am', 'pm']:
        # Type the hours
        type_text(hours)
        pyautogui.press('tab')  # Move to the next field

        # Type the minutes
        type_text(minutes)
        pyautogui.press('tab')  # Move to the next field

        # Type the AM/PM
        pyautogui.write(am_pm)  # Type AM or PM
    else:
        speak("Sorry sir, I couldn't understand the time. Please try again.")
        set_alarm()  # Prompt the user to repeat the input


def clock():
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write("clock")
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.press('enter')
    set_alarm()
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press('enter')
    speak("successfully set alarm sir.")
    pyautogui.hotkey('alt', 'f4')


# calculation
def calculate(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except Exception as e:
        speak("Sorry sir, I couldn't understand the expression. Please try again.")


def calculation():
    while True:
        speak("Would you like to say the question or input the question?")
        choice = takecommand().lower()

        if "say the question" in choice or "say" in choice:
            speak("Please say the question sir")
            query = takecommand()
            calculate(query)
        elif "input the question" in choice or "input" in choice:
            speak("Please input the question sir")
            expression = input("Enter the mathematical expression: ")
            calculate(expression)
        elif "no thanks" in choice or "exit" in choice or "no" in choice:
            speak("ok sir, Exiting Calculation")
            TaskExecution()
        else:
            speak("Sorry, I didn't understand. Please say again.")
            continue

        speak("Do you want to ask another mathematical question sir?")
        response = takecommand().lower()
        if "no thanks" in response or "exit" in response or "no" in response:
            speak("ok sir, Exiting Calculation")
            TaskExecution()


# Backspace function
def parse_erase_command(query):
    num_mapping = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                   'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}

    words = query.split()
    num_to_erase = None
    if ("erase" in words or "backspace" in words) and any(word in words for word in ["letter", "letters"]):
        erase_index = words.index("erase") if "erase" in words else words.index("backspace")

        for i in range(erase_index + 1, len(words)):
            if words[i].isdigit():
                num_to_erase = int(words[i])
                break
            elif words[i].lower() in num_mapping:
                num_to_erase = num_mapping[words[i].lower()]
                break
        else:
            speak("Please specify the number of letters to erase.")
            return None
    else:
        speak("Sorry, I couldn't understand the command. Please try again.")
        return None

    return num_to_erase


def erase_letters(num_letters):
    for _ in range(num_letters):
        pyautogui.press('backspace')


# IP Address
def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Unable to retrieve IP address. Status code: {}".format(response.status_code)
    except Exception as e:
        return "An error occurred: {}".format(str(e))


# type
def type_text(text):
    pyautogui.typewrite(text)


# Geo location
def get_location():
    try:
        # Using geocoder to get the location
        location = geocoder.ip('me')
        if location.ok:
            return location.address
        else:
            return "Unable to retrieve location."
    except Exception as e:
        return "An error occurred: {}".format(str(e))

#Choose game
def game():

    speak("Which game do you want to play sir like Stone, Paper, Scissors or Number Guessing Game?")

    choice = takecommand()

    if "stone" in choice or "paper" in choice or "scissors" in choice:
        SPS()
    elif "number guessing" in choice or "number" in choice:
        NGG()

# Stone, Paper, Scissor Game
def SPS():
    speak("LETS PLAY STONE PAPER SCISSOR !!!")
    print("LETS PLAYYYYYYYYY")
    user_wins = 0
    computer_wins = 0
    tie_games = 0
    for _ in range(5):
        computer_choice = get_computer_choice()
        user_choice = get_user_choice()
        if user_choice == "break":
            speak("Ok sir, Exiting the game.")
            TaskExecution()
        speak("You say " + user_choice)
        speak("I choose " + computer_choice)

        result = determine_winner(user_choice, computer_choice)
        speak(result)
        if "You won" in result:
            user_wins += 1
        elif "I won" in result:
            computer_wins += 1
        elif "It's a tie" in result:
            tie_games += 1


    speak("Game over! You won {} games and I won {} games and {} Tie games.".format(user_wins, computer_wins, tie_games))
    speak("Do you want to play again the game sir? Say yes or No.")
    play_again = takecommand()
    while True:
        if play_again == "yes":
            SPS()
        elif play_again == "no":
            speak("Ok sir, Exiting the game.")
            TaskExecution()
        else:
            speak("Sir, please say Yes or No")
        play_again = takecommand()

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == 'stone' and computer_choice == 'scissors') or \
            (user_choice == 'paper' and computer_choice == 'stone') or \
            (user_choice == 'scissors' and computer_choice == 'paper'):
        return "You won!"
    else:
        return "I won!"


def get_user_choice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your choice...")
        audio = r.listen(source)
    try:
        choice = r.recognize_google(audio).lower()
        if choice in ['stone', 'paper', 'scissors']:
            return choice
        elif choice == 'scissor':
            return 'scissors'
        elif any(keyword in choice for keyword in ['break', 'exit']):
            return "break"
        else:
            speak("I didn't understand. Please repeat.")
            return get_user_choice()
    except sr.UnknownValueError:
        speak("I couldn't understand what you said.")
        return get_user_choice()
    except sr.RequestError:
        speak("There was an issue with the speech recognition service. Please try again later.")
        return get_user_choice()


def get_computer_choice():
    return random.choice(['stone', 'paper', 'scissors'])

#Number Guessing Game
def NGG():
    # Set the range for the random number
    lower_bound = 1
    upper_bound = 100

    # Generate a random number within the specified range
    number_to_guess = random.randint(lower_bound, upper_bound)

    # Initialize the number of attempts
    attempts = 0

    speak("Let's Play Number Guessing Game sir!")
    speak(f"I'm thinking of a number between {lower_bound} and {upper_bound}.")
    speak("Can you guess what it is?")

    while True:
        # Get the user's guess
        guess = input("Enter your guess: ")

        try:
            guess = int(guess)
        except ValueError:
            speak("Please enter a valid number sir.")
            continue

        # Increment the attempt count
        attempts += 1

        # Check if the guess is correct
        if guess < number_to_guess:
            speak("Too low sir! Try again.")
        elif guess > number_to_guess:
            speak("Too high sir! Try again.")
        else:
            speak(f"Congratulations! You've guessed the number {number_to_guess} in {attempts} attempts.")
            break
    speak("Do you want to play again the game sir? Say yes or No.")
    play_again = takecommand()
    while True:
        if play_again == "yes":
            NGG()
        elif play_again == "no":
            speak("Ok sir, Exiting the game.")
            TaskExecution()
        else:
            speak("Sir, please say Yes or No")
            play_again = takecommand()

# NEWS function
def fetch_news_from_mediastack(country=COUNTRY):
    # Force category to "general"
    category = "general"
    main_url = f"http://api.mediastack.com/v1/news?access_key={NEWS_API_KEY}&categories={category}&countries={country}&limit=10"


    response = requests.get(main_url)

    if response.status_code != 200:
        speak("There was an issue fetching news.")
        print(f"Error: {response.status_code}")
        print(response.json())  # Debugging: Print error details
        return []

    main_page = response.json()
    if not main_page.get("data"):
        speak("No news articles were found for the general category.")
        return []

    return main_page["data"]

def get_ordinal_word(num):
    """Convert a number to its word form (e.g., 1 -> first, 2 -> second, ...)."""
    ordinals = {
        1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth",
        6: "Sixth", 7: "Seventh", 8: "Eighth", 9: "Ninth", 10: "Tenth"
    }
    return ordinals.get(num, f"{num}th")  # Default to 'nth' for values over 10, but we won't need it here.

def news():
    articles = fetch_news_from_mediastack(country=COUNTRY)

    if not articles:
        speak("Sorry sir, I couldn't fetch any news at the moment.")
        return

    # Speak the top news with word ordinals
    for i, article in enumerate(articles[:10], start=1):  # Limiting to top 10 news
        headline = article.get("title", "No headline available")
        ordinal_word = get_ordinal_word(i)  # Get the ordinal word representation (first, second, etc.)
        speak(f"Today's {ordinal_word} news is: {headline}")

#Translator function
def translate_text(query):
    # Languages supported by Google Translator (subset for example purposes)
    supported_languages = {
        'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian',
        'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian',
        'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)',
        'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish',
        'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino',
        'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian',
        'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa',
        'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong',
        'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish',
        'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh',
        'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao',
        'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian',
        'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori',
        'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian',
        'or': 'odia', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese',
        'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic',
        'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala',
        'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese',
        'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu',
        'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur',
        'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish',
        'yo': 'yoruba', 'zu': 'zulu'
    }

    # Display supported languages
    print("Supported languages:")
    for code, language in supported_languages.items():
        print(f"{code}: {language}")

    speak("Please enter which language you want to translate sir?")

    # Capture user input for the target language
    destination_language = input("Enter language code: ").lower()

    # Check if the entered language is valid
    if destination_language not in supported_languages:
        speak("Invalid language code entered. Please try again.")
        return translate_text(query)  # Retry if invalid language code

    # Ask the user to speak the sentence to translate
    speak("Please say the sentence you want to translate.")
    sentence_to_translate = takecommand()

    if sentence_to_translate:
        # Translate the sentence
        translated_text = GoogleTranslator(source='auto', target=destination_language).translate(sentence_to_translate)

        # Display the translated text
        speak("Your Translated text displayed sir")
        print(f"Translated text: {translated_text}")
    else:
        speak("No sentence was recognized. Please try again.")

def translate():
    query = "Translate sentence"
    translate_text(query)

#Usage file calling colorful
def print_colorful_usage(content):
    # ANSI escape codes for colors
    BLUE = '\033[94m'  # Color for text before the hyphen
    GREEN = '\033[92m'  # Color for text after the hyphen
    RESET = '\033[0m'  # Reset color to default

    # Split the content into lines
    lines = content.splitlines()

    for line in lines:
        # Check if there's a hyphen in the line
        if '-' in line:
            # Split the line at the hyphen
            before_hyphen, after_hyphen = line.split('-', 1)  # Only split at the first hyphen
            # Print in specified colors
            print(f"{BLUE}{before_hyphen.strip()}{RESET} - {GREEN}{after_hyphen.strip()}{RESET}")
        else:
            # Print lines without hyphen in default color (optional)
            print(line)


# AI response
class SessionManager:
    def __init__(self):
        self.sessions = []

    def save_session(self, user_input, ai_response):
        self.sessions.append({"user_input": user_input, "ai_response": ai_response})

    def get_session(self):
        return self.sessions
def ai_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

def is_code(text):
    """Check if the response contains code-like content."""
    # Code detection patterns
    code_indicators = ['<html>', 'def ', 'class ', 'import ', '</', 'function', 'let ', 'const ', 'public ', 'private ',
                       '```', '{', '}']
    return any(indicator in text for indicator in code_indicators)

def split_response(response):
    """Split AI response into explanation and code parts."""
    lines = response.splitlines()
    explanation = []
    code = []
    in_code_block = False

    for line in lines:
        # Detect code block markers or code-like content
        if '```' in line or is_code(line):
            in_code_block = not in_code_block  # Toggle code block
        if in_code_block or is_code(line):
            code.append(line)
        else:
            explanation.append(line)

    return "\n".join(explanation), "\n".join(code)

def highlight_code(code, language="python"):
    """Highlight the code using Pygments for colorful display in the terminal."""
    try:
        lexer = get_lexer_by_name(language)  # Get lexer by name like 'python', 'html', etc.
    except:
        lexer = PythonLexer()  # Default to Python syntax highlighting if no lexer is found
    formatter = TerminalFormatter()
    return highlight(code, lexer, formatter)

def ai():
    speak("Ok sir, Activated AI mode")
    speak(f"Welcome to {NAME} AI. How can I help you?")
    session_manager = SessionManager()
    while True:
        user_input = takecommand()
        if user_input == "none":
            continue  # If no valid input, continue listening

        if "deactivate" in user_input or "exit" in user_input:
            speak("Deactivating AI mode.")
            break

        # Generate AI response
        ai_reply = ai_response(user_input)
        session_manager.save_session(user_input, ai_response)
        # Split the response into explanation and code parts
        explanation, code = split_response(ai_reply)

        # Speak the explanation
        if explanation:
            speak(explanation)

        # Print the code examples with colorful highlighting
        if code:
            print("Code/Examples")
            print("-------------")
            print(highlight_code(code, language="python"))  # You can change language based on user input


# MAIN PROGRAM
def TaskExecution():
    previous_plugged = None
    previous_battery_percent = None
    last_announcement_time = None
    last_full_charge_announcement = None
    last_15_percent_announcement = None
    last_10_percent_announcement = None
    last_5_percent_announcement = None
    last_2_percent_announcement = None

    while True:
        current_minute = datetime.now().minute
        current_hour = datetime.now().hour

        # Check if it's a new minute
        current_time = datetime.now().replace(second=0, microsecond=0)
        if last_announcement_time is None or current_time != last_announcement_time:
            last_announcement_time = current_time

            if current_hour in [7, 12, 16, 21] and current_minute == 0:
                speak_greeting_and_time()
            elif current_minute == 0:
                speak_time()

        battery_percent, plugged = get_battery_status()

        if battery_percent is not None and plugged is not None:
            now = datetime.now()

            if previous_plugged is not None and plugged != previous_plugged:
                if plugged:
                    speak("Charger plugged in sir.")
                else:
                    speak(f"Charger is removed, and you have {battery_percent} percent backup left.")

            if battery_percent == 100 and plugged:
                if last_full_charge_announcement is None or (now - last_full_charge_announcement) > timedelta(
                        minutes=1):
                    speak("Battery is full. Please remove the plug sir.")
                    last_full_charge_announcement = now

            if battery_percent == 15 and not plugged:
                if last_15_percent_announcement is None or (now - last_15_percent_announcement) > timedelta(minutes=1):
                    speak("Charge is 15, please charge the system sir.")
                    last_15_percent_announcement = now

            if battery_percent == 10 and not plugged:
                if last_10_percent_announcement is None or (now - last_10_percent_announcement) > timedelta(minutes=1):
                    speak("Charge is 10, please charge the system sir.")
                    last_10_percent_announcement = now

            if battery_percent == 5 and not plugged:
                if last_5_percent_announcement is None or (now - last_5_percent_announcement) > timedelta(minutes=1):
                    speak("Charge is 5, please charge the system sir.")
                    last_5_percent_announcement = now

            if battery_percent <= 2 and not plugged:
                if last_2_percent_announcement is None or (now - last_2_percent_announcement) > timedelta(seconds=30):
                    speak("Charge is very low sir, Quickly charge the system .")
                    last_2_percent_announcement = now
            previous_plugged = plugged
            previous_battery_percent = battery_percent
        query = takecommand().lower()

        # introduce ourself
        if "tell me about yourself" in query or "introduce yourself" in query or "who are you" in query:
            speak("Sure sir, I am Jarvis, an Advanced Voice Assistant. I am equipped with a variety of features to enhance your productivity and convenience. I can open and close any apps, search anything on Google and Wikipedia, check the temperature, facilitate message passing, transcribe spoken words into text, play games, utilize AI features for various tasks, perform keyboard shortcuts, control volume, provide the latest news updates, print documents, manage system functions such as shutdown, restart, and sleep, check internet speed, and much more. I can also translate languages to help you communicate effectively. Simply tell me what you need, and I'll do my best to assist you efficiently.")

        # open any apps
        elif ("open" in query) and ("settings" not in query and "task" not in query and "accessibility" not in query and "it" not in query and "run" not in query and "emoji" not in query and "clipboard" not in query and "mail" not in query and "notification" not in query and "tab" not in query and "facebook" not in query and "youtube" not in query and "window" not in query and "downloads" not in query):
            pyautogui.press('win')
            time.sleep(0.5)
            text_to_type = query.split("open", 1)[-1].strip()
            speak(f"ok sir, opening {text_to_type}")
            type_text(text_to_type)
            pyautogui.press('enter')

        # closing any apps
        elif ("close" in query) and ("settings" not in query and "task" not in query and "program" not in query and "it" not in query and "accessibility" not in query and "run" not in query and "emoji" not in query and "clipboard" not in query and "mail" not in query and "page" not in query and "notification" not in query and "tab" not in query and "facebook" not in query and "youtube" not in query and "window" not in query and "downloads" not in query):
            text_to_type = query.split("close", 1)[-1].strip()
            speak(f"ok sir, closing {text_to_type}")
            pyautogui.hotkey('alt', 'f4')
            speak("Do you have any other work sir....")

        #show functions text file
        elif "show usage file" in query or "how to use" in query or "show your functionalities" in query:
            speak("Sure sir, showing my functionalities. Please read this...")
            with open('Usage.txt', 'r') as file:
                content = file.read()
                print_colorful_usage(content)
            speak("Do you have any other work sir....")

        #time
        elif "time" in query:
            tt = time.strftime("%I:%M %p")
            speak(f"now {tt} sir")

        # camera functions
        elif "take photo" in query or "take video" in query:
            pyautogui.press('enter')
        elif "change photo" in query or "switch to photo" in query:
            pyautogui.press('down')
        elif "change video" in query or "switch to video" in query:
            pyautogui.press('up')

        # Alarm set
        elif "set alarm" in query:
            clock()
            speak("Do you have any other work sir....")

        # settings open
        elif "open settings" in query:
            speak("Ok sir, Opening Settings")
            pyautogui.hotkey('win', 'i')

        # Task manager open
        elif "open task manager" in query:
            speak("ok sir, Opening task manager")
            pyautogui.hotkey('ctrl', 'shift', 'esc')

        # open run prompt
        elif "open run prompt" in query or "open run bar" in query or "open run dialog box" in query:
            pyautogui.hotkey('win', 'r')

        # open accessibility
        elif "open accessibility" in query:
            speak("Ok sir, Opening Accessibility")
            pyautogui.hotkey('win', 'u')

        # lock the system
        elif "lock the system" in query:
            speak("Ok sir, Lock your system")
            pyautogui.hotkey('win', 'l')

        # open clipboard bar
        elif "open clipboard" in query:
            speak("Ok sir, Opening Clipboard")
            pyautogui.hotkey('win', 'v')

        # open emoji panel
        elif "open emoji panel" in query:
            speak("Ok sir, Opening emoji panel")
            pyautogui.hotkey('win', '.')

        # open mail
        elif "open mail" in query or "check mail" in query or "open email" in query or "check email" in query:
            speak("Please wait sir. I will display your inbox")
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")

        # Minimize and maximize control
        elif "minimise all windows" in query or "minimise all window" in query:
            speak("Ok sir, Minimizing all windows")
            pyautogui.hotkey('win', 'm')
        elif "maximize all windows" in query or "maximise all window" in query:
            speak("Ok sir, Maximizing all windows")
            pyautogui.hotkey('win', 'shift', 'm')
        elif "minimise the window" in query or "minimise the page" in query:
            speak("Ok sir, Minimizing the window")
            pyautogui.hotkey('win', 'down')
        elif "maximize the window" in query or "maximise the page" in query:
            speak("Ok sir, Maximizing the window")
            pyautogui.hotkey('win', 'up')

        # Taskbar open and close function
        elif "open first task" in query or "open 1st task" in query:
            pyautogui.hotkey('win', '1')
        elif "close first task" in query or "close 1st task" in query:
            pyautogui.hotkey('win', '1')
            pyautogui.hotkey('alt', 'f4')
        elif "open second task" in query or "open 2nd task" in query:
            pyautogui.hotkey('win', '2')
        elif "close second task" in query or "close 2nd task" in query:
            pyautogui.hotkey('win', '2')
            pyautogui.hotkey('alt', 'f4')
        elif "open third task" in query or "open 3rd task" in query:
            pyautogui.hotkey('win', '3')
        elif "close third task" in query or "close 3rd task" in query:
            pyautogui.hotkey('win', '3')
            pyautogui.hotkey('alt', 'f4')
        elif "open fourth task" in query or "open 4th task" in query:
            pyautogui.hotkey('win', '4')
        elif "close fourth task" in query or "close 4th task" in query:
            pyautogui.hotkey('win', '4')
            pyautogui.hotkey('alt', 'f4')
        elif "open fifth task" in query or "open 5th task" in query:
            pyautogui.hotkey('win', '5')
        elif "close fifth task" in query or "close 5th task" in query:
            pyautogui.hotkey('win', '5')
            pyautogui.hotkey('alt', 'f4')
        elif "open sixth task" in query or "open 6th task" in query:
            pyautogui.hotkey('win', '6')
        elif "close sixth task" in query or "close 6th task" in query:
            pyautogui.hotkey('win', '6')
            pyautogui.hotkey('alt', 'f4')
        elif "open seventh task" in query or "open 7th task" in query:
            pyautogui.hotkey('win', '7')
        elif "close seventh task" in query or "close 7th task" in query:
            pyautogui.hotkey('win', '7')
            pyautogui.hotkey('alt', 'f4')
        elif "open eighth task" in query or "open 8th task" in query:
            pyautogui.hotkey('win', '8')
        elif "close eighth task" in query or "close 8th task" in query:
            pyautogui.hotkey('win', '8')
            pyautogui.hotkey('alt', 'f4')
        elif "open ninth task" in query or "open 9th task" in query:
            pyautogui.hotkey('win', '9')
        elif "close ninth task" in query or "close 9th task" in query:
            pyautogui.hotkey('win', '9')
            pyautogui.hotkey('alt', 'f4')
        elif "open tenth task" in query or "open 10th task" in query:
            pyautogui.hotkey('win', '0')
        elif "close tenth task" in query or "close 10th task" in query:
            pyautogui.hotkey('win', '0')
            pyautogui.hotkey('alt', 'f4')

        # print screen
        elif "print the page" in query or "print" in query:
            speak("ok sir, printed the screen")
            pyautogui.hotkey('ctrl', 'p')
            pyautogui.press('enter')
            speak("Do you have any other work sir....")

        # notification open
        elif "open notification bar" in query or "display notification" in query or "notification" in query or "show notification" in query:
            speak("Ok sir, showing notifications")
            pyautogui.hotkey('win', 'n')
            speak("Do you have any other work sir....")

        # Don't disturb mode
        elif "don't disturb" in query:
            pyautogui.hotkey('win', 'n')
            time.sleep(0.5)
            pyautogui.press('enter')
            pyautogui.press('esc')
            speak("Do you have any other work sir....")

        # open new tab and close
        elif "open new tab" in query or "create new tab" in query:
            speak("Ok sir, Opening New Tab")
            pyautogui.hotkey('ctrl', 't')

        elif "no no close them" in query or "no no close it" in query or "close it" in query:
            speak("ok sir, closing it")
            pyautogui.hotkey('alt', 'f4')
            speak("Do you have any other work sir....")

        elif "close this tab" in query or "delete this tab" in query:
            speak("Ok sir, closing this tab")
            pyautogui.hotkey("ctrl", "w")

        # Closing the page
        elif "close the page" in query or "closing the page" in query or "close this page" in query or "closing this page" in query:
            speak("Okay sir, Closing this page")
            pyautogui.hotkey("ctrl", "w")
            speak("Do you have any other work sir....")

        #Delete
        elif "delete it" in query:
            speak("ok sir, Deleting it")
            pyautogui.press('del')

        #show downloads
        elif "downloads" in query:
            speak("ok sir, showing downloads page")
            pyautogui.hotkey('ctrl', 'j')

        #find something
        elif "find" in query:
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            text_to_type = query.split("find", 1)[-1].strip()
            speak("showing our result sir")
            type_text(text_to_type)



        # open new window
        elif "open new window" in query or "create new window" in query:
            speak("Ok sir, Opening New window")
            pyautogui.hotkey('ctrl', 'n')

        # Move tab next and previous
        elif "move next tab" in query or "move the next tab" in query or "move to next tab" in query:
            speak("Ok sir, Moving Next Tab")
            pyautogui.hotkey('ctrl', 'tab')
        elif "move previous tab" in query or "move the previous tab" in query or "move to previous tab" in query:
            speak("Ok sir, Moving Previous Tab")
            pyautogui.hotkey('ctrl', 'shift', 'tab')

        # Select all,cut,copy,paste,save as
        elif "select all text" in query or "select all" in query:
            speak("Ok sir, selecting all text")
            pyautogui.hotkey('ctrl', 'a')
        elif "cut the text" in query or "cut" in query or "cut their" in query or "cut them" in query or "cut it" in query:
            speak("Ok sir, cut the text")
            pyautogui.hotkey('ctrl', 'x')
        elif "copy the text" in query or "copy" in query or "copy their" in query or "copy them" in query or "copy it" in query:
            speak("Ok sir, copied the text")
            pyautogui.hotkey('ctrl', 'c')
        elif "paste the text" in query or "paste" in query or "paste their" in query or "paste them" in query or "paste it" in query:
            speak("Ok sir, pasting the text")
            pyautogui.hotkey('ctrl', 'v')
        elif "save as the file" in query or "save as" in query or "save as their" in query or "save as them" in query or "save as it" in query:
            speak("Ok sir, saving the file")
            pyautogui.hotkey('ctrl', 's')
            speak("Do you have any other work sir....")


        # youtube opening and closing
        elif "open youtube" in query:
            speak("Ok sir, Opening YouTube")
            webbrowser.open("www.youtube.com")
            speak("Do you have any other work sir....")
        elif "close youtube" in query:
            speak("Ok sir, Closing You Tube")
            pyautogui.hotkey('alt', 'f4')
            speak("Do you have any other work sir....")
        elif "minimise the video" in query:
            pyautogui.press('i')
        elif "maximize the video" in query:
            pyautogui.press('i')
        elif "full screen" in query:
            pyautogui.press('f')
        elif "exit full screen" in query:
            pyautogui.press('esc')
        elif "caption" in query or "subtitle" in query:
            pyautogui.press('c')

        # facebook open and closing
        elif "open facebook" in query:
            speak("Okay sir, Opening Facebook")
            webbrowser.open("www.facebook.com")

        elif "close facebook" in query:
            speak("Okay sir, Closing Facebook")
            pyautogui.hotkey('alt', 'f4')
            speak("Do you have any other work sir....")

        # song on youtube
        elif "song on youtube" in query:
            speak("Please say the song name you want to play sir!")
            song_name = takecommand()
            # song_name = input("Please enter the name of the song you want to play: ")
            pywhatkit.playonyt(song_name)
            speak(f"Searching for {song_name} song on YouTube...")
            speak("wait a second sir your song play quickly")
            time.sleep(8)
            pyautogui.press('k')

        # find ip address
        elif "ip address" in query:
            ip_address = get_ip_address()
            speak("Your IP address is " + ip_address)
            speak("Do you have any other work sir....")

        # find my location
        elif "where i am" in query or "where we are" in query:
            speak("wait a second sir, let me check")
            location = get_location()
            speak("sir i am not sure, but i think we are in " + location)
            speak("Do you have any other work sir....")

        # search wikipedia
        elif "search on wikipedia" in query:
            speak("searching on wikipedia...")
            text_to_type = query.split("search on wikipedia")[0].strip()
            if text_to_type:
                try:
                    # Fetching summary from Wikipedia
                    results = wikipedia.summary(text_to_type, sentences=2)
                    speak(f"According to Wikipedia: {results}")
                except wikipedia.exceptions.DisambiguationError as e:
                    speak("There are multiple results. Could you be more specific?")
                except wikipedia.exceptions.HTTPTimeoutError:
                    speak("Sorry, there was a problem with the connection. Please try again later.")
                except Exception as e:
                    speak("Sorry sir, I couldn't find any information on that.")
            else:
                speak("Please specify what you want to search on Wikipedia, for example, 'what is python search on wikipedia'.")
            speak("Do you have any other work sir...")

        # search on google
        elif "search on google" in query:
            speak("Searching Google...")

            # Extract the text before "search on google"
            text_to_type = query.split("search on google")[0].strip()

            if text_to_type:
                try:
                    # Construct the Google search URL
                    search_url = f"https://www.google.com/search?q={text_to_type}"
                    webbrowser.open(search_url)  # Open the browser with the Google search URL
                    speak(f"Here are the results for {text_to_type} on Google.")
                except Exception as e:
                    speak("Sorry sir, I couldn't perform the Google search.")
            else:
                speak("Please specify what you want to search on Google, for example, 'what is python search on Google'.")

            speak("Do you have any other work sir...")

        #Mouse controls
        elif "right click" in query:
            pyautogui.rightClick()
        elif "left click" in query:
            pyautogui.leftClick()
        elif "click" in query:
            pyautogui.click()
        elif "double click" in query or "open it" in query:
            pyautogui.doubleClick()

        # keyboard contols
        elif "zoom in" in query:
            pyautogui.hotkey('ctrl', '+')
        elif "zoom out" in query:
            pyautogui.hotkey('ctrl', '-')
        elif "pause" in query or "stop" in query:
            pyautogui.press('playpause')
        elif ("play" in query or "start" in query) and ("game" not in query and "song" not in query):
            pyautogui.press('playpause')
        elif "increase speed" in query or "increase play speed" in query:
            pyautogui.hotkey('shift', '.')
        elif "decrease speed" in query or "decrease play speed" in query:
            pyautogui.hotkey('shift', ',')
        elif "next video" in query:
            pyautogui.hotkey('alt', 'right')
            speak("ok sir, move to next video")
        elif "previous video" in query:
            pyautogui.hotkey('alt', 'left')
            speak("ok sir, move to previous video")
        elif "scroll up" in query:
            pyautogui.press("pageup")
        elif "scroll down" in query:
            pyautogui.press("pagedown")
        elif "type" in query:
            text_to_type = query.split("type", 1)[-1].strip()
            type_text(text_to_type)
        elif "enter" in query or "send it" in query:
            pyautogui.press('enter')
        elif "tab" in query or "go to next field" in query or "go to next box" in query:
            pyautogui.press('tab')

        # erase and backspace function
        elif ("erase" in query or "backspace" in query) and ("letter" in query or "letters" in query):

            num_letters = parse_erase_command(query)

            # If a valid number of letters to erase is found, proceed with erasing
            if num_letters is not None:
                erase_letters(num_letters)
            else:
                speak("Sorry, I couldn't understand the number of letters to erase.")

        # search anything type model
        elif "search" in query:
            text_to_type = query.split("search", 1)[-1].strip()
            type_text(text_to_type)
            pyautogui.press('enter')
            speak("ok sir, Searching your result")

        # send message
        elif "message" in query:
            text_to_type = query.split("message", 1)[-1].strip()
            type_text(text_to_type)
            pyautogui.press('enter')
        elif "send" in query:
            text_to_type = query.split("send", 1)[-1].strip()
            type_text(text_to_type)
            pyautogui.press('enter')

        # Volume controls
        elif "mute" in query and "system" not in query and "all" not in query:
            pyautogui.press("m")
        elif "unmute" in query and "system" not in query and "all" not in query:
            pyautogui.press("m")
        elif "mute the system" in query or "mute the hole system" in query or "mute all" in query:
            pyautogui.press("volumemute")
        elif "unmute the system" in query or "mute the hole system" in query or "mute all" in query:
            pyautogui.press("volumemute")
        elif "volume up" in query:
            pyautogui.press("volumeup")
        elif "volume down" in query:
            pyautogui.press("volumedown")

        # GAME
        elif "let's play a game" in query or "let's play game" in query or "let's play game" in query or "let's play a game" in query:
            game()

        # check battery percent
        elif "how much power left" in query or "battery" in query or "how much power we have" in query:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f"Our system have {percentage}% battery sir")
            speak("Do you have any other work sir....")

        # check internet speed
        elif "internet speed" in query:
            speak("please wait a minute sir, checking internet speed...")
            st = speedtest.Speedtest()
            dp = st.download() / 1_000_000
            up = st.upload() / 1_000_000
            # ping = st.results.ping
            speak(f"sir your internet speed is {dp:.2f} Mbps downloading speed and {up:.2f} Mbps uploading speed")
            speak("Do you have any other work sir....")

        # shutdown system
        elif "shutdown the system" in query or "shutdown our system" in query or "shutdown my system" in query:
            os.system("shutdown /s /t 5")
            speak("Ok sir, Shutdown our system")

        # restart system
        elif "restart the system" in query or "restart our system" in query or "restart my system" in query:
            os.system("shutdown /r /t 5")
            speak("Ok sir, Restart our system")

        # sleep system
        elif "sleep the system" in query or "sleep our system" in query or "sleep my system" in query:
            os.system("sudo pmset sleepnow")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            speak("ok sir, sleep our system")

        # switch window
        elif "switch the window" in query or "switch" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(0.5)
            pyautogui.keyUp("alt")
            speak("ok sir, switching the window")

        # latest news
        elif "tell me a latest news" in query or "today latest news" in query or "today top 10 news" in query or "today news" in query:
            speak("please wait sir, Fetching the top 10 general news.")
            news()
            speak("Do you have any other work sir....")

        # closing Jarvis
        elif "goodbye Jarvis" in query or "goodbye" in query or "close the program" in query or "exit the program" in query:
            speak("Goodbye sir, have a good day.")
            speak("Jarvis Deactivated")
            sys.exit()

        # Normal commands
        elif "no thanks" in query:
            speak("okay sir, if you have any work call me anytime sir")
            while True:
                permission = takecommand()
                if "jarvis" in permission or "wake up" in permission:
                    speak("Welcome back sir, please tell me how may i help you sir?")
                    TaskExecution()
        elif "ready" in query:
            speak("Yes sir, I'm ready")
        elif "thankyou" in query:
            speak("your welcome sir.")
        elif "hello" in query or "hey" in query:
            speak("Hello sir, may i help you with something.")
        elif "how are you" in query:
            speak("I am fine sir,what about you.")
        elif "also good" in query or "fine" in query:
            speak("That's great to hear from you.")
        elif "thank you" in query or "thanks" in query:
            speak("It's my pleasure sir.")
        elif "you can sleep" in query or "sleep now" in query or "go to sleep mode" in query or "go to sleep" in query:
            speak("okay sir, i am going to sleep you call me anytime sir.")
            while True:
                permission = takecommand()
                if "jarvis" in permission or "wake up" in permission:
                    speak("Welcome back sir, please tell me how may i help you sir?")
                    TaskExecution()

        # check instagram profile
        elif "instagram profile" in query or "profile on instagram" in query or "check instagram profile" in query or "let me check instagram profile" in query:
            speak("sir please enter the username correctly.")
            name = input("Enter username here:")
            webbrowser.open(f"www.instagram.com/{name}")
            speak(f"Sir here is the profile of the user {name}")
            time.sleep(5)
            speak("sir would you like to download a profile of this account.")
            condition = takecommand().lower()
            if "okay" in condition:
                mod = instaloader.Instaloader()
                mod.download_profile(name, profile_pic_only=True)
                speak("i am done sir, profile picture is saved in our main folder. Now i am ready for next command")
            elif "don't want" in condition or "no" in condition:
                speak("Ok sir")
                pass
            speak("Do you have any other work sir....")

        # take screenshot
        elif "take screenshot" in query or "take a screenshot" in query:
            speak("sir, please tell me the name for this screenshot file")
            name = takecommand().lower()
            speak("please sir hold the screen for few seconds, i am taking screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("i am done sir, the screen shot is saved in our main folder.")
            speak("Do you have any other work sir....")

        # Hide file
        elif "hide all files" in query or "hide this folder" in query or "visible for everyone" in query:
            speak("Sir please tell me you want to hide this folder or make it visible for everyone")
            condition = takecommand().lower()
            if "hide" in condition:
                os.system("attrib +h /s /d")
                speak("sir, all the files in this folder are now hidden.")
            elif "visible" in condition:
                os.system("attrib -h /s /d")
                speak("sir, all the files in this folder are now visible to everyone. I wish you are taking the folder")
            elif "leave it" in condition or "leave for now" in condition:
                speak("ok sir")
            speak("Do you have any other work sir....")

        # Calculation
        elif "calculate" in query or "calculation" in query:
            calculation()
            speak("Do you have any other work sir....")

        #Translator
        elif "translate" in query or "activate translate mode" in query:
            translate()


        # check temperature
        elif "temperature" in query:
            search = f"temperature in {PLACE}"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            speak(f"current temperature is {temp} sir")
            speak("Do you have any other work sir....")

        # check weather
        elif "weather" in query or "whether" in query:
            weather()
            speak("Do you have any other work sir....")

        # AI response
        elif "activate ai" in query or "ai mode" in query:
            ai()
            speak("Do you have any other work sir....")


if __name__ == "__main__":
    speak("Voice Activation Required")
    while True:
        permission = takecommand()
        if PASSWORD in permission:
            speak("Access Granted")
            speak("Jarvis Activated")
            wish()
            speak("I am Jarvis, please tell me how may i help you sir?")
            TaskExecution()

        else:
            speak("Access Denied")


