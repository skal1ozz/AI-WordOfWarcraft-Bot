from __future__ import unicode_literals
from __future__ import absolute_import
import base64
import os
from abc import ABCMeta

import tornado.gen
import tornado.web
from tornadis import ConnectionError

import settings
from utils.log import Log
from utils.pbkdf2_hmac import pbkdf2_hmac
from ...abstract_handler import AbstractHandler
from utils.json import json_loads


TOKEN_TTL = getattr(settings, "TOKEN_TTL", 60)

TAG = __name__


# noinspection PyAbstractClass
class AuthHandler(AbstractHandler):

    PATH = r'/api/v1/auth'

    SUPPORTED_METHODS = ('POST',)

    @tornado.gen.coroutine
    def do_auth(self, body):
        # TODO(s1z): IMPL ME
        # user, token = self.auth.authenticate(login, password)
        # if None not in [user, token]:
        #     return self.finish_json({"token": token})
        self.finish_unauthorized()

    def post(self):
        return self.do_auth(self.request.body)
