from .abstract_mice_backend import AbstractMiceBackend


class MiceController(object):

    backend = None

    def __init__(self, backend: AbstractMiceBackend):
        self.backend = backend

    def move_abs(self, x: int, y: int, duration: float):
        return self.backend.move_abs(x, y, duration)

    def move(self, x: int, y: int, duration: float):
        return self.backend.move(x, y, duration)

    def click(self, button: int, duration: float):
        return self.backend.click(button, duration)

    def press(self, button):
        return self.backend.press(button)

    def release(self, button):
        return self.backend.release(button)
