import sys

import simplejson as json
import simplejson.scanner as json_scanner

from utils.log import Log


TAG = __name__


def json_loads(data, default=None):
    try:
        j_data = json.loads(data, strict=False)
        if isinstance(j_data, dict) or isinstance(j_data, list):
            return j_data
    except TypeError:
        Log.e(TAG, "json_loads", "TypeError", sys.exc_info())
    except json_scanner.JSONDecodeError:
        Log.e(TAG, "json_loads", "JSONDecodeError", sys.exc_info())
    return default


def json_dumps(*args, **kwargs):
    try:
        return json.dumps(*args, **kwargs)
    except Exception:
        Log.e(TAG, "json_loads", exc_info=sys.exc_info())
        raise
