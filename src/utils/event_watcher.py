from types import FunctionType
from typing import List
from pygame import event, constants
from sys import exit as exit_program


class EventWatcher:
    def __init__(self, callbacks: List) -> None:
        self.stack = callbacks

    def watch_pygame_events(self):
        """Watchs events as provided by pygame"""
        for e in event.get():
            if e.type == constants.QUIT:
                exit_program()
            for fn in self.stack:
                fn(e)
