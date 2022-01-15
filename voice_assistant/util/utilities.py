# Import all dependencies

import os
import random
import time
import re
from datetime import datetime
from threading import Thread, Event

from voice_assistant.util.tinyDBModal import LocalStorage
from voice_assistant.util.helena import Helena

import psutil
from pconst import const

# Initialize constant variables which represent some specific paths

const.OFFICE = ["Word", "Excel", "PowerPoint", "Project", "OneNote", "Publisher", "Visio", "Outlook"]
const.USEFULLPATH = [os.environ['SYSTEMDRIVE'] + "\\Program Files\\",
                     os.environ['SYSTEMDRIVE'] + "\\Program Files (x86)\\"]
const.DESKTOPPATH = os.path.normpath(os.path.expanduser("~/Desktop/")) + "\\"
const.PICTURESPATH = os.path.normpath(os.path.expanduser("~/Pictures/")) + "\\"
const.VIDEOSPATH = os.path.normpath(os.path.expanduser("~/Videos/")) + "\\"
const.DOCUMENTSPATH = os.path.normpath(os.path.expanduser("~/Documents/")) + "\\"
const.MUSICPATH = os.path.normpath(os.path.expanduser("~/Music/")) + "\\"
const.STARTMENUPATH = os.environ['SYSTEMDRIVE'] + "\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\"
ALLPATH = [const.DESKTOPPATH, const.PICTURESPATH, const.VIDEOSPATH, const.DOCUMENTSPATH, const.MUSICPATH,
           const.STARTMENUPATH, const.USEFULLPATH]
filesFound = []
query = None


def screenshots_filename_generator():
    """
        This function determinate a name for the screenshot
    :return: string: Random filename for helena screenshots feature. Composed with the current date and time and a random number of four digit
    """

    randomize = ""
    # Initialize a random number of four digit
    for number in range(4):
        randomize += str(int(random.uniform(0, 10)))
    # Get date and time
    date = datetime.now().strftime("%Y%m%d-%H%M%S")
    # Concat date and time and the random number
    filename = "screenshot_" + date + "_" + randomize + ".png"
    return filename


def runnable():
    """
        This function deal with users input
    :return:
    """
    global query

    helena = Helena()
    standbyEvent = Event()

    while True:
        query = helena.take_command().lower()
        print("In first")
        if query == "" or query is None:
            print("Reach the continue block")
            continue

        print(standbyEvent.is_set())
        print(query)
        if standbyEvent.is_set():
            print("In standby true")
            # query = helena.take_command().lower()
            print("The query in standby true: ", query)
            print("The type of query in standby true: ", type(query))
            standbyEvent.clear()

            task_controller(helena, query, standbyEvent)

        elif not standbyEvent.is_set() and query == "elena":
            print("In standby false")
            helena.sound_note()
            query = helena.take_command().lower()
            print("The query in standby false: ", query)
            print("The type of query in standby false: ", type(query))

            task_controller(helena, query, standbyEvent)


def standby(standbyEvent):
    """
        This function put the program in standby after a certain amount of time
    :param standbyEvent: Threading event: Event that sets up the stand by process
    """

    counter = 0
    while True:
        if not standbyEvent.is_set():
            break
        time.sleep(1)
        counter += 1
        print("The timeout: ", counter)
        if counter == 45:
            standbyEvent.clear()
            break


def task_controller(helena, userInput, standbyEvent):
    """
        This function analyze user's input and launch the appropriate response
    :param helena: Helena instance: It contains all the potential answers that will be sent to the user.
    :param userInput: string: User's input
    :param standbyEvent: Threading event: Event that sets up the stand by process
    :return:
    """

    print('The query in task controller: ', userInput)
    print('Standby Event in task controller: ', standbyEvent)

    localStorage = LocalStorage()
    patterns = localStorage.getPatterns()
    code = ""

    for pattern in patterns:
        if re.search(pattern['pattern'], userInput):
            code = pattern['code']
            break

    if code == "00h00m":
        helena.current_time()
        print("time gave")
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()
    elif code == "00j00m":
        helena.current_date()
        print("date gave")
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()
    elif code == "00intro00":
        helena.who_am_i()
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()
    elif code == "00shot00":
        helena.screenshot()
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()
    elif code == "00mind00":
        helena.to_remember()
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()
    elif code == "00wikipedia00":
        helena.wikipedia_search()
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()
    elif code == "00shutdown00":
        helena.shutdown()
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()
    elif code == "00reboot00":
        helena.restart()
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()
    elif code == "00logout00":
        helena.logout()
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()
    elif code == "00file00launcher00":
        helena.file_launcher()
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()
    else:
        helena.speak("I do not understand "+userInput)
        standbyEvent.set()
        thread = Thread(target=standby, args=[standbyEvent, ])
        thread.start()


def os_mount_points():
    """
        This function allows to recover the computer partitions except the operating system partition
    :return: list: List of computer's drives
    """

    # Get os partitions
    partitions = psutil.disk_partitions()
    mountPoints = []
    for partition in partitions:
        try:
            # Get the os drive
            OSDrive = os.environ['SYSTEMDRIVE'].split("\\")
            systemDrives = partition.device.split("\\")
            # Match the os drive with all partition and exclude it
            if OSDrive[0] != systemDrives[0]:
                mountPoints.append(partition.mountpoint)
        except PermissionError:
            # this can be caught due to the disk that
            # isn't ready
            continue
    return mountPoints


def search_control(resultAvailable, speak):
    """
        This function is some kind of controller for the search engine
    :param resultAvailable: Threading event: Event that tracks search time
    :param speak: Helena's speak function: Return a voice note of the text gave as parameter
    :return:
    """

    global filesFound

    while not resultAvailable.wait(timeout=5):
        speak("Searching! Please wait")

    # All files matching the request are put in ine filesFound list.
    # If only one file is find it will be launched and if it doesn't it will return how many files are found
    # And if there is no file matching the request a message will be returned
    if len(filesFound) != 0:
        if len(filesFound) == 1:
            speak("File found")
            os.startfile(filesFound[0])
        else:
            speak("I found " + str(len(filesFound)) + " files corresponding to your request")
    elif len(filesFound) == 0:
        speak("There is no file matching your request")


def search_engine(filename, resultAvailable):
    """
        Search any file in the computer that match the file name gave in parameters
    :param resultAvailable: Threading event: Event that tracks search time
    :param filename: string: The name of the file to search
    :return:
    """

    global filesFound
    filesFound.clear()

    # If MSOffice is installed and if the request is on an office program
    for file in const.OFFICE:
        if file.lower() == filename:
            path = const.STARTMENUPATH + file
            filesFound.append(path)

    # Loop over the specific paths declare early to find a file which the request
    for path in ALLPATH:
        if type(path) is str:
            for root, directories, files in os.walk(path):
                for name in files:
                    if filename in name.lower():
                        filepath = os.path.join(root, name)
                        filesFound.append(filepath)

        else:
            for systemDrivePath in path:
                for root, directories, files in os.walk(systemDrivePath):
                    for name in files:
                        if filename in name.lower():
                            filepath = os.path.join(root, name)
                            filesFound.append(filepath)

    # Loop over all partitions except os's partition to find a file which match the request
    for path in os_mount_points():
        for root, directories, files in os.walk(path):
            for name in files:
                if filename in name.lower():
                    filepath = os.path.join(root, name)
                    filesFound.append(filepath)

    resultAvailable.set()
