import abc
from random import randint

import tornado.gen


class AbstractBackend(abc.ABC):
    @tornado.gen.coroutine
    def delay(self, duration: float) -> None:
        if duration < 0.15:
            duration = randint(15, 30) * 0.01
        yield tornado.gen.sleep(duration)
