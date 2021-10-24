import abc

from ..abstract_backend import AbstractBackend


class AbstractKeyboardBackend(AbstractBackend):

    @abc.abstractmethod
    def press(self, key):
        raise NotImplementedError('IMPL ME')

    @abc.abstractmethod
    def release(self, key):
        raise NotImplementedError('IMPL ME')

    @abc.abstractmethod
    def click(self, key, duration: float):
        raise NotImplementedError('IMPL ME')
