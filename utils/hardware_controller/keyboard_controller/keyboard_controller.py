from .abstract_keyboard_backend import AbstractKeyboardBackend
from ..wrappers import wrapper_backend_required


class KeyboardController(object):

    # TODO(s1z): Add press/release click with modifiers (ctr/shift/alt/win/cmd)

    backend = None

    def __init__(self, backend: AbstractKeyboardBackend):
        self.backend = backend

    @wrapper_backend_required
    def press(self, key):
        return self.backend.press(key)

    @wrapper_backend_required
    def release(self, key):
        return self.backend.release(key)

    @wrapper_backend_required
    def click(self, key, duration: float = 0.0):
        return self.backend.click(key, duration)
