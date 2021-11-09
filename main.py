#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tornadis
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web
import settings as settings
from handlers.api.v1.auth_handler import AuthHandler
from handlers.not_found_handler import NotFoundHandler
from utils.abstract_worker import AbstractWorker
from utils.hardware_controller import MiceController, \
    PynputAutoGUIMiceBackend, PynputKeyboardBackend, KeyboardController


TAG = __name__


class Main(AbstractWorker):

    @tornado.gen.coroutine
    def run(self):
        # io_loop = tornado.ioloop.IOLoop.current()

        # init mice
        mice_backend = PynputAutoGUIMiceBackend()
        mice = MiceController(mice_backend)

        # init keyboard
        keyboard_backend = PynputKeyboardBackend()
        keyboard = KeyboardController(keyboard_backend)

        # init redis client
        redis = tornadis.Client(host=settings.Redis.host,
                                port=settings.Redis.port)

        # init context
        context = dict(mice=mice, keyboard=keyboard, redis=redis)

        # init bober module
        # bober = Bober()

        # init server app
        app = tornado.web.Application([AuthHandler.register(context),
                                       NotFoundHandler.register(context)])

        # init server
        server = tornado.httpserver.HTTPServer(app)
        server.listen(settings.Server.port,
                      settings.Server.host)
        server.start()
        raise tornado.gen.Return([])


if __name__ == "__main__":
    Main().start()
