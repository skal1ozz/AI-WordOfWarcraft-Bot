from concurrent.futures import ThreadPoolExecutor
from random import randint

import tornado.gen
from pynput.keyboard import Controller

from .abstract_keyboard_backend import AbstractKeyboardBackend


class PynputKeyboardBackend(AbstractKeyboardBackend):

    def __init__(self):
        self.controller = Controller()
        self.executor = ThreadPoolExecutor(max_workers=10)

    @tornado.gen.coroutine
    def press(self, key) -> None:
        yield self.executor.submit(self.controller.press, key)

    @tornado.gen.coroutine
    def release(self, key):
        yield self.executor.submit(self.controller.release, key)

    @tornado.gen.coroutine
    def click(self, key, duration: float = 0.0):
        yield self.press(key)
        yield self.delay(duration)
        yield self.release(key)
