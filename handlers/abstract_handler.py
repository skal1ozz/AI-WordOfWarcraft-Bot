import base64
import json
import sys
import traceback

import tornado
from tornado import httputil
from tornado.gen import coroutine
from tornado.gen import Return
from tornado.concurrent import is_future
from tornado.httputil import responses
from tornado.web import Finish
from tornado.web import HTTPError
from tornado.web import RequestHandler

from handlers.status_codes import SuccessCodes, ErrorCodes
from utils.json import json_dumps
from utils.log import Log


TAG = __name__


class NotFoundException(Exception):
    pass


AUTH_TYPE_BEARER = 'bearer'
AUTH_TYPE_BASIC = 'basic'


class Context(object):
    pass


class AbstractHandler(RequestHandler):

    context = None
    PATH = None

    def initialize(self, *args, **kwargs):
        Log.d(TAG, "initialize", "args:{}, kwargs: {}".format(args, kwargs))
        self.context = Context()
        for key, value in kwargs.items():
            setattr(self.context, key, value)

    def set_default_headers(self):
        self.clear_header('Server')
        self.set_header("Content-Type", b"application/json")

    @classmethod
    def register(cls, *args):
        Log.i(TAG, "registering: {}".format(cls.PATH))
        init_list = [cls.PATH, cls]
        for arg in args:
            init_list.append(arg)
        return init_list

    @staticmethod
    def wrapper_auth_required(func):
        @coroutine
        def wr(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            raise Return((yield result if is_future(result) else result))
        return wr

    def response(self, code, message, data=None):
        payload = {"status": {"code": code, "message": message}}
        if data is not None and isinstance(data, (dict, list)):
            payload["data"] = data
        return self.finish(json.dumps(payload))

    def finish(self, *args, **kwargs):
        # We always set 200 to show that's the backend is working.
        # Then we parse body to get status["code"]
        self.set_status(self._status_code or 200)
        return super(AbstractHandler, self).finish(*args, **kwargs)

    def on_finish(self):
        Log.d(TAG, "on_finish")
        super(AbstractHandler, self).on_finish()

    def write_error(self, status_code, **kwargs):
        error_code = status_code
        message = ErrorCodes.ServerError.message
        if "exc_info" in kwargs:
            ex_type, ex_value, ex_traceback = kwargs["exc_info"]
            tb = traceback.format_exception(ex_type, ex_value, ex_traceback)
            Log.e(TAG, "write_error", "Error: {0}".format(tb))
            if isinstance(ex_value, HTTPError):
                message = httputil.responses.get(status_code, "Unknown")
            if self.settings.get("serve_traceback"):
                message = "{0}".format(tb)
        self.finish(json.dumps({"status": {"code": error_code,
                                           "message": message}}))

    def send_error(self, status_code=500, **kwargs):
        if self._headers_written:
            Log.e(TAG, "send_error", "Headers are already written")
            if not self._finished:
                try:
                    self.finish()
                except Exception as e:
                    Log.e(TAG, "send_error",
                          "Failed to flush partial response", e)
            return
        self.clear()

        # We always set 200 to show that's the backend is working.
        # Then we parse body to get status["code"]
        self.set_status(SuccessCodes.WithContent.code,
                        SuccessCodes.WithContent.message)
        try:
            self.write_error(status_code, **kwargs)
        except Exception as e:
            Log.e(TAG, "send_error", "Uncaught exception in write_error", e)
        if not self._finished:
            self.finish()

    def _handle_request_exception(self, e):
        if isinstance(e, NotFoundException) and not self._finished:
            return self.finish(json.dumps(
                {"status": {"code": ErrorCodes.NotFound.code,
                            "message": ErrorCodes.NotFound.message}}
            ))

        if isinstance(e, Finish):
            # Not an error; just finish the request without logging.
            if not self._finished:
                self.finish(*e.args)
            return
        try:
            self.log_exception(*sys.exc_info())
        except Exception as ex:
            # An error here should still get a best-effort send_error()
            # to avoid leaking the connection.
            Log.e(TAG, "_handle_request_exception",
                  "Error in exception logger", ex)
        if self._finished:
            # Extra errors after the request has been finished should
            # be logged, but there is no reason to continue to try and
            # send a response.
            return
        if isinstance(e, HTTPError):
            if e.status_code not in responses and not e.reason:
                Log.e(TAG, "_handle_request_exception",
                      "Bad HTTP status code: %s" % e.status_code, e)
                self.send_error(500, exc_info=sys.exc_info())
            else:
                self.send_error(e.status_code, exc_info=sys.exc_info())
        else:
            self.send_error(500, exc_info=sys.exc_info())

    def finish_json(self, status=None, data=None):
        status = status or (SuccessCodes.WithContent if data else
                            SuccessCodes.NoContent)
        chunk = {"status": {"code": status.code, "message": status.message}}
        if data is not None:
            chunk["data"] = data
        self.finish(json.dumps(chunk))
        raise Return()

    def finish_forbidden(self):
        return self.finish_json(ErrorCodes.Forbidden)

    def finish_unauthorized(self):
        return self.finish_json(ErrorCodes.Unauthorized)

    def __del__(self):
        Log.d(TAG, "%s __deleted__" % self.__class__.__name__)
