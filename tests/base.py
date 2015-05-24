# -*- coding: utf-8 -*-

import sure
from nose.tools import nottest
import json
from functools import wraps
from tempfile import NamedTemporaryFile

from jsonserver.main import create_app
from jsonserver.core import JsonServer


def get_json(data):
    """
        Return json for a flask request
    """
    return {"data": json.dumps(data), "content_type": "application/json"}


@nottest
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


@nottest
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


@nottest
def with_test_app(func):
    @wraps(func)
    def _decorator(self, *args, **kwargs):
        app = create_app().test_client()
        return func(self, app, *args, **kwargs)
    return _decorator
