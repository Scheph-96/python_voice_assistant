# import all necessary modules
import threading
import time
from pathlib import Path

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import os
import pyautogui

from wikipedia.wikipedia import search
from pygame import mixer, event
from .utilities import screenshots_filename_generator, search_control, search_engine


class Helena:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

    # Initialize the voice
    # If you don't have this one, it will select the default voice on your computer
    @staticmethod
    def change_voice(engine):
        for voice in engine.getProperty('voices'):
            if voice.name == "Microsoft Zira Desktop - English (United States)":
                engine.setProperty('voice', voice.id)
                break

    # Speaking function
    def speak(self, audio):
        self.change_voice(self.engine)
        self.engine.say(audio)
        self.engine.runAndWait()

    # Presentation function
    def who_am_i(self):
        identity = "I am Helena your voice assistant develop by Omar on Thursday September 30, 2021"
        self.speak(identity)

    # Order listening function
    def take_command(self):
        print("speak")
        recognize = sr.Recognizer()
        with sr.Microphone() as source:
            recognize.adjust_for_ambient_noise(source)
            audio = recognize.listen(source)

        try:
            print("Recognizing...")
            query = recognize.recognize_google(audio)
            return query
        except Exception as e:
            print(e)
            self.speak("I do not understand what you are saying")

    def sound_note(self):
        mixer.init()
        mixer.music.load(os.fspath(Path(__file__).resolve().parent / "sound/helena_sound.mp3"))
        mixer.music.play()

    # User data writing function
    def user_data(self):
        self.speak("May i know your name?")
        username = self.take_command().lower()
        data = open("../memoryCenter/userData.txt", "w")
        data.write(username)
        data.close()

    def greet(self):

        hour = datetime.datetime.now().hour

        if 6 <= hour < 12:
            self.speak("Good morning")
        elif 12 <= hour < 18:
            self.speak("Good afternoon")
        elif 18 <= hour < 6:
            self.speak("Good evening")

    # Return current time
    def current_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.speak("It's " + current_time)

    # Return current date
    def current_date(self):
        current_date = datetime.datetime.now().strftime("%A %d %B %Y")
        self.speak("Today's date is " + current_date)

    def wikipedia_search(self):
        self.speak("what should I look for?")
        query = self.take_command().lower()
        self.speak("Searching for " + query)
        wikipedia.set_lang("en")
        time.sleep(0.3)
        result = wikipedia.summary(query, sentences=2)
        self.speak(result)

    def to_remember(self):
        self.speak("What should i remember?")
        memory = self.take_command()
        memoryCenter = open("../memoryCenter/memoryCenter", "a")
        memory += str("\n")
        memoryCenter.write(memory)
        memoryCenter.close()
        self.speak("You told me to remember " + memory)

    def file_launcher(self):
        self.speak("Which file would you like to launch?")
        to_launch = self.take_command().lower()
        resultAvailable = threading.Event()
        thread = threading.Thread(target=search_engine, args=[to_launch, resultAvailable, ])
        thread.start()
        search_control(resultAvailable, self.speak)

    def screenshot(self):
        img = pyautogui.screenshot()
        filename = screenshots_filename_generator()
        folder_path = os.path.normpath(os.path.expanduser("~/Pictures/")) + "\\"
        file_path = folder_path + filename
        img.save(file_path)
        self.speak("screenshot took successfully")

    def shutdown(self):
        self.speak("Do you really want to shutdown?")
        answer = self.take_command().lower()
        if answer == "yes":
            self.speak("Shutting down the computer")
            os.system("shutdown /s /t 1")
        elif answer == "no":
            self.speak("Process abort")
        else:
            self.speak("I do not understand. Process abort")

    def restart(self):
        self.speak("Do you really want to restart?")
        answer = self.take_command().lower()
        if answer == "yes":
            self.speak("Reboot")
            os.system("shutdown /r /t 1")
        elif answer == "no":
            self.speak("Process abort")
        else:
            self.speak("I do not understand. Process abort")

    def logout(self):
        self.speak("Do you really want to logout?")
        answer = self.take_command().lower()
        if answer == "yes":
            self.speak("Logout")
            os.system("shutdown -l")
        elif answer == "no":
            self.speak("Process abort")
        else:
            self.speak("I do not understand. Process abort")


if __name__ == "__module__":
    pass
