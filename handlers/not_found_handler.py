from .abstract_handler import AbstractHandler


class NotFoundHandler(AbstractHandler):

    PATH = r'/.*'
    SUPPORTED_METHODS = ("GET", "POST", "PUT", "DELETE", "OPTIONS",
                         "PATCH", "HEAD")

    def initialize(self, *args, **kwargs):
        pass

    def default(self, *_args, **_kwargs):
        return self.finish({"status": {"code": 404,
                                       "message": "Page Not Found"}})

    def get(self, *args, **kwargs):
        return self.default(*args, **kwargs)

    def head(self, *args, **kwargs):
        return self.default(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.default(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.default(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.default(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.default(*args, **kwargs)

    def options(self, *args, **kwargs):
        return self.default(*args, **kwargs)
