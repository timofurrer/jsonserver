# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request

from jsonserver.core import JsonServer

api = Blueprint("api", __name__)


@api.route("/", methods=["GET"])
def all():
    data = JsonServer().all()
    return jsonify(data)


@api.route("/<table>", methods=["GET"])
def get_table(table):
    data = JsonServer().get(table=table)
    return jsonify(data)


@api.route("/<table>/<id>", methods=["GET"])
def get_row(table, id):
    data = JsonServer().get(table=table, id=int(id))
    return jsonify(data)


@api.route("/<table1>/<id>/<table2>", methods=["GET"])
def get_row_sub_table(table1, id, table2):
    data = JsonServer().get(table=table1, id=int(id), subtable=table2)
    return jsonify(data)


@api.route("/", methods=["POST"])
def create_table():
    table = request.get_json()["table"]
    JsonServer().create(table)


@api.route("/<table>", methods=["DELETE"])
def drop_table(table):
    JsonServer().drop(table)


@api.route("/<table>", methods=["POST"])
def insert_row(table):
    row = request.get_json()["row"]
    JsonServer().insert(table, row)


@api.route("/<table>/<row>", methods=["DELETE"])
def remove_row(table, row):
    JsonServer().remove(table, int(row))


@api.route("/<table>/<row_id>", methods=["PUT", "PATCH"])
def update_row(table, row_id):
    row = request.get_json()["row"]
    JsonServer().update(table, int(row_id), row)
