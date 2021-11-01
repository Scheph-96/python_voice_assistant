from threading import Thread, Event

from .controlCenter import Helena
from .utilities import standby

query = None


def runnable():
    global query

    helena = Helena()
    standbyEvent = Event()

    while True:
        print(standbyEvent.is_set())
        print(query)
        if standbyEvent.is_set():
            query = helena.take_command().lower()
            if query is not None:
                standbyEvent.clear()
        else:
            helena.sound_note()
            query = helena.take_command().lower()

        if "what" and "time" in query:
            helena.current_time()
            standbyEvent.set()
            thread = Thread(target=standby, args=[standbyEvent, ])
            thread.start()
        elif "date" and "what" or "which" and "today" in query:
            helena.current_time()
            standbyEvent.set()
            thread = Thread(target=standby, args=[standbyEvent, ])
            thread.start()
        else:
            helena.speak("I am allowed to perform this task")
            helena.current_time()
            standbyEvent.set()
            thread = Thread(target=standby, args=[standbyEvent, ])
            thread.start()
