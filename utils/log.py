import logging
import traceback


class Log(object):

    loggers = {}

    @staticmethod
    def log(level, tag, source, message="", exc_info=None):
        logger = Log.loggers.get(tag, logging.getLogger(tag))
        line = "{source}{message}{ex}"
        ex = ""
        if isinstance(exc_info, (list, tuple)):
            ex_type, ex_value, ex_traceback = exc_info
            ex = ": " + ''.join(
                traceback.format_exception(ex_type, ex_value, ex_traceback)
            )
        message = "::{}".format(message) if message else ""
        logger.log(level, line.format(source=source, message=message, ex=ex))

    @staticmethod
    def w(tag, source, message="", exc_info=None):
        return Log.log(logging.WARN, tag, source, message, exc_info)

    @staticmethod
    def d(tag, source, message="", exc_info=None):
        return Log.log(logging.DEBUG, tag, source, message, exc_info)

    @staticmethod
    def i(tag, source, message="", exc_info=None):
        return Log.log(logging.INFO, tag, source, message, exc_info)

    @staticmethod
    def e(tag, source, message="error", exc_info=None):
        return Log.log(logging.ERROR, tag, source, message, exc_info)
