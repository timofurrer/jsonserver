# -*- coding: utf-8 -*-

"""
    This module is only used as entry point for the json server.
"""

import sys
import os
from flask import Flask

from jsonserver.core import JsonServer
from jsonserver.routes import api


def create_jsonserver(dbfile):
    server = JsonServer()
    server.open(dbfile)

    return server


def create_app():
    # flask app instance
    app = Flask(__name__)
    app.register_blueprint(api)

    return app


def main(args=sys.argv[1:]):
    """
        Main function for the json server.
    """
    if not args:
        sys.stderr.write("Error: no json database file given as first argument\n")
        return 1

    if not os.path.exists(args[0]):
        sys.stderr.write("Error: json database file at '%s' does not exist\n" % args[0])
        return 1

    server = create_jsonserver(args[0])

    # flask app instance
    app = create_app()
    app.run(debug=True)

    server.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
