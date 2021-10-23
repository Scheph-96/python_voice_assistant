# Import all dependencies
import os
import random
from datetime import datetime

import psutil
from pconst import const

# Initialize constant variables which represent some specific paths
const.OFFICE = ["Word", "Excel", "PowerPoint", "Project", "OneNote", "Publisher", "Visio", "Outlook"]
const.USEFULLPATH = [os.environ['SYSTEMDRIVE']+"\\Program Files\\", os.environ['SYSTEMDRIVE']+"\\Program Files (x86)\\"]
const.DESKTOPPATH = os.path.normpath(os.path.expanduser("~/Desktop/")) + "\\"
const.PICTURESPATH = os.path.normpath(os.path.expanduser("~/Pictures/")) + "\\"
const.VIDEOSPATH = os.path.normpath(os.path.expanduser("~/Videos/")) + "\\"
const.DOCUMENTSPATH = os.path.normpath(os.path.expanduser("~/Documents/")) + "\\"
const.MUSICPATH = os.path.normpath(os.path.expanduser("~/Music/")) + "\\"
const.STARTMENUPATH = os.environ['SYSTEMDRIVE']+"\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\"
ALLPATH = [const.DESKTOPPATH, const.PICTURESPATH, const.VIDEOSPATH, const.DOCUMENTSPATH, const.MUSICPATH, const.STARTMENUPATH, const.USEFULLPATH]
filesFound = []


def screenshots_filename_generator():
    """
        Return a random filename for helena screenshots feature
        Composed with the current date and time and a random number of four digit
    :return: string
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


def os_mount_points():
    """
        Return the computer drives
    :return: list
    """

    # Get os partitions
    partitions = psutil.disk_partitions()
    mountPoints = []
    for partition in partitions:
        try:
            # Get the os drive
            systemDriveFromOS = os.environ['SYSTEMDRIVE'].split("\\")
            systemDriveFromPython = partition.device.split("\\")
            # Match the os drive with all partition and exclude it
            if systemDriveFromOS[0] != systemDriveFromPython[0]:
                mountPoints.append(partition.mountpoint)
        except PermissionError:
            # this can be caught due to the disk that
            # isn't ready
            continue
    return mountPoints


def search_control(resultAvailable, speak):

    """
        Some kind of controller for the search engine
    :param resultAvailable: event
    :param speak: speaker function
    """

    global filesFound

    while not resultAvailable.wait(timeout=5):
        speak("Searching! Please wait")

    # All files matching the request are put in ine filesFound list.
    # If only one file is find it will be launched else return how many files are found
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
        Search any file in the computer which match the file name gave in parameters
    :param resultAvailable: thread event
    :param filename: string
    :return: string
    """

    global filesFound
    filesFound.clear()

    # If MSOffice is installed and if the request is on an office program
    for file in const.OFFICE:
        if file.lower() == filename:
            path = const.STARTMENUPATH+file
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

    # Loop over all partitions except os's partition to find a file which math the request
    for path in os_mount_points():
        for root, directories, files in os.walk(path):
            for name in files:
                if filename in name.lower():
                    filepath = os.path.join(root, name)
                    filesFound.append(filepath)

    resultAvailable.set()
