# -*- coding: utf-8 -*-

import sure
import os
import json
from functools import wraps
from tempfile import NamedTemporaryFile

from jsonserver.core import JsonServer


def with_json_db(database=None):
    """
        Create a json database file from a python dict object.
    """
    def _decorator(func):
        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            with NamedTemporaryFile(suffix=".json", mode="w+") as tmpfile:
                if database:
                    json.dump(database, tmpfile)
                    tmpfile.flush()
                ret = func(self, tmpfile.name, *args, **kwargs)
            return ret
        return _wrapper
    return _decorator


def with_jsonserver(database=None):
    """
        Create a json server with the given json database.
    """
    def _decorator(func):
        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            with NamedTemporaryFile(suffix=".json", mode="w+") as tmpfile:
                if database:
                    json.dump(database, tmpfile)
                    tmpfile.flush()

                server = JsonServer()
                server.open(tmpfile.name)
                ret = func(self, server, *args, **kwargs)
            return ret
        return _wrapper
    return _decorator
