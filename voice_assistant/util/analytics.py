from threading import Event

from .helena import Helena
from .utilities import task_controller

query = None


def runnable():
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
