# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

from jsonserver.core import JsonServer

api = Blueprint("api", __name__)


@api.route("/", methods=["GET"])
def all():
    data = JsonServer().all()
    return jsonify(data)


@api.route("/<table>", methods=["GET"])
def get_table(table):
    data = JsonServer().get(table=table)
    print(data)
    return jsonify(data)


@api.route("/<table>/<id>", methods=["GET"])
def get_row(table, id):
    data = JsonServer().get(table=table, id=int(id))
    print(data)
    return jsonify(data)


@api.route("/<table1>/<id>/<table2>", methods=["GET"])
def get_row_sub_table(table1, id, table2):
    data = JsonServer().get(table=table1, id=int(id), subtable=table2)
    print(data)
    return jsonify(data)
