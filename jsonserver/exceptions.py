# -*- coding: utf-8 -*-


class JsonServerError(Exception):
    """
        Exception which is raised when an error occures in the json server.
    """
    pass


class TableNotFound(JsonServerError):
    """
        Exception which is raised when a requested table could not be found.
    """
    def __init__(self, table):
        super(TableNotFound, self).__init__("Table '{}' not found".format(table))


class TableAlreadyExists(JsonServerError):
    """
        Exception which is raised when the table to create already exists.
    """
    def __init__(self, table):
        super(TableAlreadyExists, self).__init__("Table '{}' already exists".format(table))


class RowNotFound(JsonServerError):
    """
        Exception which is raised when a requested row from a table could not be found.
    """
    def __init__(self, table, id):
        super(RowNotFound, self).__init__("Row with id '{}' in table '{}' not found".format(id, table))
