# -*- coding: utf-8 -*-

"""
    Core module for the python json server.
"""

import os
from singleton import singleton
from threading import Lock

from jsonserver.storage import JsonStorage
from jsonserver.exceptions import TableNotFound, TableAlreadyExists, RowNotFound


@singleton()
class JsonServer(object):
    """
        Instance of the json server.
    """
    def __init__(self):
        self._dbfile = None
        self._db = None
        self._autoincrement_id_lock = Lock()

    @property
    def dbfile(self):
        return self._dbfile

    def open(self, dbfile):
        if not os.path.exists(dbfile):
            raise OSError("Json database file not found at '%s'" % dbfile)

        self._dbfile = dbfile
        self._db = JsonStorage(dbfile)
        self._data = {}
        self.read(flush_previous=False)

    def close(self):
        if self._db:
            self._db.close()

    def read(self, flush_previous=True):
        if flush_previous:
            self.flush()
        self._data = self._db.read()

    def flush(self):
        """
            Flush all data to storage
        """
        self._db.write(self._data)

    def table_exists(self, table):
        """
            Checks if a table exists

            :params string table: the table to check

            :returns: if the table exists or not
            :rtype: bool
        """
        try:
            self._data[table]
        except KeyError:
            return False
        else:
            return True

    def row_exists(self, table, row_id):
        """
            Checks if a row exists within a table

            :params string table: the table of the row
            :params string row_id: the row to find

            :returns: if the row exists or not
            :rtype: bool
        """
        table_data = self.get_table(table)[table]
        for row in table_data:
            if row["id"] == row_id:
                return True
        return False

    def all(self):
        return self._data

    def get(self, **kwargs):
        if not kwargs:
            return self.all()

        if "table" in kwargs:
            if "id" in kwargs:
                if "subtable" in kwargs:
                    return self.get_row_sub_table(kwargs["table"], kwargs["id"], kwargs["subtable"])

                return self.get_row(kwargs["table"], kwargs["id"])

            return self.get_table(kwargs["table"])

    def get_table(self, table):
        try:
            return {table: self._data[table]}
        except KeyError:
            raise TableNotFound(table)

    def get_row(self, table, id):
        rows = self.where(table, id=id)
        if not rows:
            raise RowNotFound(table, id)

        return rows[0]

    def get_row_sub_table(self, table, id, subtable):
        if table.endswith("s"):
            foreign_id = "{}Id".format(table[:-1])
        else:
            foreign_id = "{}Id".format(table)

        rows = self.where(subtable, **{foreign_id: id})
        if not rows:
            raise RowNotFound(table, id)

        return {subtable: rows}

    def where(self, table, **kwargs):
        table_data = self.get_table(table)[table]
        matches = []
        for row in table_data:
            does_match = True
            for key, value in kwargs.items():
                if row[key] != value:
                    does_match = False

            if does_match:
                matches.append(row)
        return matches

    def create(self, name, flush=False):
        """
            Create a new table

            :param string name: the name of the table to create
        """
        if self.table_exists(name):
            raise TableAlreadyExists(name)

        self._data[name] = []

        if flush:
            self.flush()

        return True

    def drop(self, table, flush=False):
        """
            Drop a table

            :param string table: the name of the table to drop
        """
        # FIXME: implement cascade
        if not self.table_exists(table):
            raise TableNotFound(table)

        del self._data[table]

        if flush:
            self.flush()

        return True

    def insert(self, table, row, flush=False):
        """
            Insert row into a given table

            :params string table: the table name
            :params dict row: the row to insert
        """
        if not self.table_exists(table):
            raise TableNotFound(table)

        with self._autoincrement_id_lock:
            if not self._data[table]:
                highest_id = 0
            else:
                highest_id = max(row["id"] for row in self._data[table])
            row["id"] = highest_id + 1
            self._data[table].append(row)

            if flush:
                self.flush()

        return True

    def remove(self, table, row_id, flush=False):
        """
            Remove a row from a table

            :params string table: the table name
            :params dict row_id: the id of the row to remove
        """
        if not self.row_exists(table, row_id):
            raise RowNotFound(table, row_id)

        self._data[table][:] = [r for r in self._data[table] if r["id"] != row_id]

        if flush:
            self.flush()

        return True

    def update(self, table, row_id, data, flush=False):
        """
            Update a row in a table

            :params string table: the table name
            :params int row_id: the id of the row to remove
            :params dict data: the row data
        """
        row = self.get_row(table, row_id)
        for key, value in data.items():
            row[key] = value

        if flush:
            self.flush()

        return True
