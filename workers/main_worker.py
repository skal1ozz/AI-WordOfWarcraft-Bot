import tornado.gen
from tornado.concurrent import is_future


class MainWorker(object):
    def __init__(self, io_loop, screen_controller, keyboard_controller,
                 mice_controller):
        self.io_loop = io_loop
        self.screen_controller = screen_controller
        self.keyboard_controller = keyboard_controller
        self.mice_controller = mice_controller

        self.is_working = False
        self.future_run = None

    def on_start_callback(self):
        pass

    @tornado.gen.coroutine
    def run(self):
        # High level logic is here
        while self.is_working:
            yield tornado.gen.sleep(0.1)

    @tornado.gen.coroutine
    def start(self):
        self.is_working = True
        self.future_run = self.run()
        self.io_loop.add_future(self.future_run, self.on_start_callback)

    @tornado.gen.coroutine
    def stop(self):
        self.is_working = True
        if is_future(self.future_run):
            yield self.future_run
