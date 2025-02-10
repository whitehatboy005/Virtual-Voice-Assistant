# 🤖 Virtual Voice Assistant (Jarvis)
[![License](https://img.shields.io/github/license/whitehatboy005/Virtual-Assistant-Jarvis)](LICENSE.md)

It's Python-based virtual voice assistant capable of performing various tasks using voice commands. It utilizes speech recognition, web scraping, automation, and external APIs to provide a wide range of functionalities.

## 🚀 Features

- **Voice Activation**
  - Activates upon recognizing a predefined password.
  - Greets the user and awaits commands.

- **Voice Commands**
  - Interprets voice commands for tasks like opening applications, searching the web, playing music, managing files, and more.

- **Automation**
  - Automates tasks such as sending messages, controlling mouse movements, typing text, and interacting with applications.

- **Information Retrieval**
  - Fetches weather updates, current temperature, latest news, Wikipedia summaries, IP address, and system information.

- **Entertainment**
  - Plays music from a predefined directory and streams songs from YouTube.
  - Offers interactive games like Stone-Paper-Scissors and Number Guessing Game.

- **System Operations**
  - Controls system operations like shutdown, restart, and sleep.
  - Manages volume controls and monitors battery status.

- **Web Interaction**
  - Opens websites based on user commands (e.g., Facebook, Instagram profiles).
  - Searches Google and retrieves results.

- **Utility Functions**
  - Takes screenshots, hides/unhides files, calculates mathematical expressions, translates text into different languages.

- **User Interaction**
  - Responds to user queries, greets, and interacts based on predefined conversation patterns.
  - Provides feedback on executed commands and waits for further instructions.

## Technologies Used

- **Python**: Core programming language for implementing functionalities.
- **SpeechRecognition**: Converts speech to text for interpreting user commands.
- **pyautogui**: Automates mouse and keyboard actions.
- **BeautifulSoup**: Parses HTML for web scraping.
- **Requests**: Makes HTTP requests to fetch data from web services.
- **psutil**: Retrieves system information such as battery status.
- **pywhatkit**: Interacts with YouTube for music playback.

## Usage

To use Jarvis, ensure you have Python installed along with the necessary libraries listed in `requirements.txt`. Run the `jarvis.py` script and follow the voice activation prompt. Speak commands clearly and wait for Jarvis to execute tasks accordingly.


# Model Output
![Screenshot 2024-07-11 210512](https://github.com/whitehatboy005/Jarvis/assets/147156726/8cfd0963-7605-486d-8ce2-4d498f4d279e)
#
## Obtaining API Keys

### GEMINI_API_KEY

To obtain the `GEMINI_API_KEY` required for your project:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Follow the instructions to create a new API key.
3. Copy the API key provided.

### NEWS_API_KEY

To obtain the `NEWS_API_KEY` required for your project:

1. Visit [Media Stack.com](https://mediastack.com/).
2. Sign up or log in to your account.
3. Generate an API key for your project.
4. Copy the API key provided.
#
## ⚙️ Installation
## Clone the Repository
```bash
git clone https://github.com/whitehatboy005/Virtual-Voice-Assistant
cd Virtual-Voice-Assistant
```
## Install Dependencies
```bash
pip install -r requirements.txt
```
## Config Your Details
```bash
notepad config.env
```
## Run the Program
```bash
python jarvis.py
```
#
## 📝 License

This project is licensed under the terms of the [MIT license](LICENSE.md).
