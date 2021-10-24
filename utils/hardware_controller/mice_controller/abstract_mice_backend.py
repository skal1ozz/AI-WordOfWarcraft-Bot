import abc

from ..abstract_backend import AbstractBackend


class AbstractMiceBackend(AbstractBackend):

    @abc.abstractmethod
    def move_abs(self, x: int, y: int, duration: float):
        raise NotImplementedError('IMPL ME')

    @abc.abstractmethod
    def move(self, x: int, y: int, duration: float):
        raise NotImplementedError('IMPL ME')

    @abc.abstractmethod
    def click(self, button: int, duration: float):
        raise NotImplementedError('IMPL ME')

    @abc.abstractmethod
    def press(self, button):
        raise NotImplementedError('IMPL ME')

    @abc.abstractmethod
    def release(self, button):
        raise NotImplementedError('IMPL ME')
