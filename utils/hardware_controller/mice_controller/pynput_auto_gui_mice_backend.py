import sys
from concurrent.futures import ThreadPoolExecutor

if sys.platform == 'darwin':
    # without it you're gonna have a NameError exception on BigSur:
    # https://github.com/asweigart/pyautogui/issues/495
    import AppKit

import pyautogui as pyautogui
import tornado.gen
from pynput.mouse import Controller

from .abstract_mice_backend import AbstractMiceBackend


class PynputAutoGUIMiceBackend(AbstractMiceBackend):

    def __init__(self):
        self.controller = Controller()
        self.executor = ThreadPoolExecutor(max_workers=10)

    @tornado.gen.coroutine
    def move_abs(self, x: int, y: int, duration: float):
        yield self.executor.submit(pyautogui.moveTo, x, y, duration,
                                   tween=pyautogui.easeInOutQuad)

    @tornado.gen.coroutine
    def move(self, x: int, y: int, duration: float):
        yield self.executor.submit(pyautogui.moveRel, x, y, duration,
                                   tween=pyautogui.easeInOutQuad)

    @tornado.gen.coroutine
    def press(self, button: int):
        yield self.executor.submit(self.controller.press, button)

    @tornado.gen.coroutine
    def release(self, button: int):
        yield self.executor.submit(self.controller.release, button)

    @tornado.gen.coroutine
    def click(self, button: int, duration: float = 0.0):
        yield self.press(button)
        yield self.delay(duration)
        yield self.release(button)
