SUCCESS_WITH_CONTENT = 200
SUCCESS_NO_CONTENT = 204

ERROR_SERVER_ERROR = 500
ERROR_NOT_IMPLEMENTED = 501
ERROR_BAD_REQUEST = 400
ERROR_UNAUTHORIZED = 401
ERROR_FORBIDDEN = 403
ERROR_NOT_FOUND = 404
ERROR_METHOD = 405


class SuccessCodes(object):

    class WithContent(object):
        code = SUCCESS_WITH_CONTENT
        message = "Ok"

    class NoContent(object):
        code = SUCCESS_NO_CONTENT
        message = "Ok"


class ErrorCodes(object):

    class NotImplemented(object):
        code = ERROR_NOT_IMPLEMENTED
        message = "Not Implemented"

    class ServerError(object):
        code = ERROR_SERVER_ERROR
        message = "Server Error"

    class NotFound(object):
        code = ERROR_NOT_FOUND
        message = "Not Found"

    class Method(object):
        code = ERROR_METHOD
        message = "Method is not supported"

    class BadRequest(object):
        code = ERROR_BAD_REQUEST
        message = "Bad request"

    class Unauthorized(object):
        code = ERROR_UNAUTHORIZED
        message = "Authentication required"

    class Forbidden(object):
        code = ERROR_FORBIDDEN
        message = "Forbidden"
