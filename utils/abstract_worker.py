import sys

import tornado
import tornado.ioloop
import tornado.gen
import signal
import logging

from tornado.concurrent import is_future

from utils.log import Log


TAG = __name__


class AbstractWorker(object):

    def __init__(self, io_loop=None):
        self.io_loop = io_loop or tornado.ioloop.IOLoop.current()
        self.workers = list()
        self.stop_future = None

    @staticmethod
    def init_logging(level=logging.INFO, logfile=None):
        try:
            import settings
        except ImportError:
            settings = {}
        logging_config = {
            "format": "%(asctime)-23s %(levelname)8s: %(message)s",
            "level": getattr(settings, "LOG_LEVEL", level),
        }
        logfile = logfile or getattr(settings, "LOG_FILE", None)
        if logfile is not None:
            logging_config["filename"] = logfile
        logging.basicConfig(**logging_config)

    def init_signal_handler(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        Log.d(TAG, "signal_handler", "signum:'{}', frame:'{}'".format(signum,
                                                                      frame))
        self.io_loop.add_callback_from_signal(self.stop)

    @tornado.gen.coroutine
    def run(self, *args, **kwargs):
        raise NotImplementedError("IMPL ME")

    @tornado.gen.coroutine
    def stop_routine(self):
        for worker in self.workers:
            if worker and getattr(worker, "stop", None):
                stop_method = worker.stop()
                if is_future(stop_method):
                    yield stop_method

    def on_start_callback(self, _future):
        Log.i(TAG, "on_start_callback", "Server is started: {}".format(self))

    def on_stop_callback(self, _future):
        Log.i(TAG, "on_stop_callback", "Server is stopped: {}".format(self))
        self.stop_future = None
        self.io_loop.stop()

    @tornado.gen.coroutine
    def start_routine(self, *args, **wrags):
        try:
            method = getattr(self, "run", None)
            if method is None:
                raise NotImplementedError("run method is not implemented!")
            result = yield method(*args, **wrags)
            if result:
                if isinstance(result, list):
                    self.workers.extend(result)
                else:
                    self.workers.append(result)
                raise tornado.gen.Return()
            Log.w(TAG, "start_routine", "run method returned nothing!")
        except tornado.gen.Return:
            raise
        except Exception:
            Log.e(TAG, "start_routine", "error", sys.exc_info())
            Log.e(TAG, "start_routine", "shutting down the server")
            self.stop()

    def start(self, *args, **kwargs):
        self.init_logging()
        self.init_signal_handler()
        self.io_loop.add_future(self.start_routine(*args, **kwargs),
                                self.on_start_callback)
        self.io_loop.start()

    def stop(self):
        if self.stop_future is None:
            Log.i(TAG, "stop", "Server is stopping")
            self.stop_future = self.stop_routine()
            self.io_loop.add_future(self.stop_routine(), self.on_stop_callback)
