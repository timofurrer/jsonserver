# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import os
import json


class Storage(metaclass=ABCMeta):
    """
        Base class for storage classes.
        A storage class provides the functionality to serialize/deserialize written data.
    """
    @abstractmethod
    def read(self):
        """
            Read latest state from the stored data.

            :returns: deserialized data
            :rtype: dict

            :raises NotImplementedError: if this method is not overwritten by the subclass.
        """
        raise NotImplementedError("this method has to be overwritten")

    @abstractmethod
    def write(self, data):
        """
            Write the current data to the storage.

            :params dict data: the data to serialize

            :returns: if serialization was successful
            :rtype: bool

            :raises NotImplementedError: if this method is not overwritten by the subclass.
        """
        raise NotImplementedError("this method has to be overwritten")


class JsonStorage(Storage):
    """
        Class to store data as json file.
    """
    def __init__(self, jsonfile):
        """
            Create new json storage object.

            :params string jsonfile: the file to load from
        """
        super(JsonStorage, self).__init__()
        self._jsonfile = jsonfile

        self._handle = open(jsonfile, "r+")

    def __del__(self):
        self.close()

    def close(self):
        """
            Close storage handle
        """
        self._handle.close()

    def read(self):
        if os.path.getsize(self._jsonfile) == 0:  # return empty object if database has no entries
            return {}

        self._handle.seek(0)
        return json.load(self._handle)

    def write(self, data):
        self._handle.seek(0)
        json.dump(data, self._handle)
        self._handle.flush()
        self._handle.truncate()
