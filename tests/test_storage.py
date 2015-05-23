# -*- coding: utf-8 -*-

from tests.base import *
from unittest import TestCase

from jsonserver.storage import Storage, JsonStorage


class StorageTest(TestCase):
    """
        Test Storage and JsonStorage objects.
    """

    def test_storage_base_class(self):
        """
            Test the storage base class

            The base class should not be creatable as an object -> pure abstract class.
        """
        Storage.when.called_with().should.throw(TypeError, "Can't instantiate abstract class Storage with abstract methods read, write")

    @with_json_db({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]})
    def test_jsonstorage_read(self, dbfile):
        """
            Test the read functionality of the JsonStorage object
        """
        storage = JsonStorage(dbfile)
        data = storage.read()
        data.should.be.equal({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]})

    @with_json_db()
    def test_jsonstorage_write(self, dbfile):
        """
            Test the write functionality of the JsonStorage object
        """
        storage = JsonStorage(dbfile)
        storage.read().should.be.equal({})

        data = {"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]}
        storage.write(data)
        storage.read().should.be.equal(data)
