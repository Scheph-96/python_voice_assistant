# import all necessary modules
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil

from wikipedia.wikipedia import search
from pygame import mixer


class Helena:
    def __init__(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)

    # Initialize the voice
    # If you don't have this one, it will select the default voice on your computer
    def change_voice(self, engine, language, gender='VoiceGenderFemale'):
        for voice in engine.getProperty('voices'):
            if voice.name == "Microsoft Zira Desktop - English (United States)":
                engine.setProperty('voice', voice.id)
                break

    # Speaking funtion
    def speak(self, audio):
        change_voice(engine, language=None, gender=None)
        engine.say(audio)
        engine.runAndWait()

    # Presentation function
    def who_am_i(self):
        identity = "I am Héléna your voice assistant develop by Omar on Thursday September 30, 2021"
        speak(identity)

    # Order listening function
    def takeCommand(self):
        recognize = sr.Recognizer()
        with sr.Microphone() as source:
            mixer.init()
            mixer.music.load('helena_sound.mp3')
            mixer.music.play()
            recognize.adjust_for_ambient_noise(source)
            audio = recognize.listen(source)

    # User data writting function
    def user_data(self):
        speak("Can i know your name ?")
        data = open("data.txt", "w")
        data.write(data)
        data.close()

    # Return current time
    def time(self):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak("It's "+time)

    # Return current date
    def date(self):
        date = datetime.datetime.now().strftime("%A %d %B %Y")
        speak("Today we are "+date)


    def wishme(self):

        hour = datetime.datetime.now()

        if hour >= 6 and hour < 12:
            speak("Good morning")
        elif hour >= 12 and hour <18:
            speak("Good afternoon")
        elif hour >= 18 and hour < 24:
            speak("Good evening")


     def toRemember(self):
         speak("What shoud i remember ?")
         memory = self.takeCommand()
         memoryCenter = open("memory_center", "a")
         memoryCenter.write(memory)
         memoryCenter.close()
         speak("You told me to remember "+memory)


     def shutdown(self):
         speak(Sutting down the computer)
         os.system("shutdown")


if __name__ == "__module__":
    pass
