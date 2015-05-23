# -*- coding: utf-8 -*-

from tests.base import *
from unittest import TestCase

from jsonserver.core import JsonServer
from jsonserver.exceptions import TableNotFound, TableAlreadyExists, RowNotFound


class JsonServerTest(TestCase):
    """
        Test Storage and JsonStorage objects.
    """

    @with_json_db({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]})
    def test_init_storage_object(self, dbfile):
        """
            Test initializing of JsonServer and opening json database
        """
        server = JsonServer()
        server.open.when.called_with("somenonexistingfile.json").should.throw(OSError, "Json database file not found at 'somenonexistingfile.json'")

        server.open(dbfile)
        server.all().should.be.equal({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]})

    @with_json_db({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]})
    def test_close_server_storage(self, dbfile):
        """
            Test close the server storage
        """
        server = JsonServer()
        server.open(dbfile)

        server._db._handle.closed.should.be.false
        server.close()
        server._db._handle.closed.should.be.true

    @with_jsonserver({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]})
    def test_read(self, server):
        """
            Test server read functionality
        """
        server.all().should.be.equal({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]})
        server.create("comments")

        with open(server.dbfile, "r") as f:
            json.loads(f.read()).should.be.equal({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]})

        server.read(flush_previous=True)
        server.all().should.be.equal({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}], "comments": []})

    @with_json_db({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}], "comments": [{"id": 1}]})
    def test_get_single_table(self, dbfile):
        """
            Test reading rows of a single table
        """
        server = JsonServer()
        server.open(dbfile)

        server.get_table("posts").should.be.equal({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]})
        server.get_table("comments").should.be.equal({"comments": [{"id": 1}]})

    @with_json_db({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}], "comments": [{"id": 1}]})
    def test_get_single_row(self, dbfile):
        """
            Test reading a single row of a specific table
        """
        server = JsonServer()
        server.open(dbfile)

        server.get_row("posts", 1).should.be.equal({"id": 1, "body": "some text"})
        server.get_row("posts", 2).should.be.equal({"id": 2, "body": "some text"})
        server.get_row("comments", 1).should.be.equal({"id": 1})

    @with_json_db({"comments": [{"body": "some comment", "id": 1, "postId": 1}, {"body": "some comment - foo", "id": 2, "postId": 1}, {"body": "some comment - foo", "id": 3, "postId": 2}], "posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})
    def test_get_subtable(self, dbfile):
        """
            Test reading the rows of a specific subtable of another table
        """
        server = JsonServer()
        server.open(dbfile)

        server.get_row_sub_table("posts", 1, "comments").should.be.equal({"comments": [{"body": "some comment", "id": 1, "postId": 1}, {"body": "some comment - foo", "id": 2, "postId": 1}]})

    @with_json_db()
    def test_table_does_not_exist(self, dbfile):
        """
            Test reading of table if it does not exist
        """
        server = JsonServer()
        server.open(dbfile)
        server.get_table.when.called_with("DoesNotExistTable").should.throw(TableNotFound, "Table 'DoesNotExistTable' not found")

    @with_json_db({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}]})
    def test_row_does_not_exist(self, dbfile):
        """
            Test reading of a specific row of a table if it does not exist
        """
        server = JsonServer()
        server.open(dbfile)

        server.get_row.when.called_with("posts", 3).should.throw(RowNotFound, "Row with id '3' in table 'posts' not found")

    @with_json_db({"posts": [{"id": 1, "body": "some text"}, {"id": 2, "body": "some text"}], "comments": []})
    def test_row_does_not_exist_subtable(self, dbfile):
        """
            Test reading of a specific row of a table when requesting subtable if it does not exist
        """
        server = JsonServer()
        server.open(dbfile)

        server.get_row_sub_table.when.called_with("posts", 3, "comments").should.throw(RowNotFound, "Row with id '3' in table 'posts' not found")

    @with_json_db({"comments": [{"body": "some comment", "id": 1, "postId": 1}, {"body": "some comment - foo", "id": 2, "postId": 1}, {"body": "some comment - foo", "id": 3, "postId": 2}], "posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})
    def test_get_function(self, dbfile):
        """
            Test get function
        """
        server = JsonServer()
        server.open(dbfile)

        # requesting: all
        server.get().should.be.equal({"comments": [{"body": "some comment", "id": 1, "postId": 1}, {"body": "some comment - foo", "id": 2, "postId": 1}, {"body": "some comment - foo", "id": 3, "postId": 2}], "posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})

        # requesting: table
        server.get(**{"table": "posts"}).should.be.equal({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})

        # requesting: table, row
        server.get(**{"table": "posts", "id": 1}).should.be.equal({"author": "tuxtimo", "id": 1, "title": "jsonserver"})

        # requesting: table, row, subtable
        server.get(**{"table": "posts", "id": 1, "subtable": "comments"}).should.be.equal({"comments": [{"body": "some comment", "id": 1, "postId": 1}, {"body": "some comment - foo", "id": 2, "postId": 1}]})

    @with_jsonserver({"posts": []})
    def test_insert_row(self, server):
        """
            Test insert row into table.
        """
        server.insert.when.called_with("DoesNotExistTable", {}).should.throw(TableNotFound, "Table 'DoesNotExistTable' not found")

        server.get_table("posts").should.be.equal({"posts": []})
        server.insert("posts", {"author": "tuxtimo", "title": "foobar"})
        server.get_table("posts").should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "title": "foobar"}]})
        server.insert("posts", {"author": "tuxtimo", "title": "foobar - extension"})
        server.get_table("posts").should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "title": "foobar"}, {"id": 2, "author": "tuxtimo", "title": "foobar - extension"}]})

        with open(server.dbfile, "r") as f:
            json.loads(f.read()).should.be.equal({"posts": []})

        server.insert("posts", {"author": "tuxtimo", "title": "foobar - extension"}, flush=True)

        with open(server.dbfile, "r") as f:
            json.loads(f.read()).should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "title": "foobar"}, {"id": 2, "author": "tuxtimo", "title": "foobar - extension"}, {"id": 3, "author": "tuxtimo", "title": "foobar - extension"}]})

    @with_jsonserver({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})
    def test_remove_row(self, server):
        """
            Test remove specific row from a table
        """
        server.remove.when.called_with("posts", 3).should.throw(RowNotFound, "Row with id '3' in table 'posts' not found")

        server.get_table("posts").should.be.equal({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})

        server.remove("posts", 2)

        server.get_table("posts").should.be.equal({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}]})

        with open(server.dbfile, "r") as f:
            json.loads(f.read()).should.be.equal({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})

        server.remove("posts", 1, flush=True)
        server.get_table("posts").should.be.equal({"posts": []})

        with open(server.dbfile, "r") as f:
            json.loads(f.read()).should.be.equal({"posts": []})

    @with_jsonserver({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})
    def test_update_row(self, server):
        """
            Test update specific row from a table
        """
        server.get_table("posts").should.be.equal({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})

        server.update("posts", 1, {"author": "chucknorris"})

        server.get_table("posts").should.be.equal({"posts": [{"author": "chucknorris", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})

        with open(server.dbfile, "r") as f:
            json.loads(f.read()).should.be.equal({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "jsonserver2"}]})

        server.update("posts", 2, {"title": "more fancy title"}, flush=True)

        server.get_table("posts").should.be.equal({"posts": [{"author": "chucknorris", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "more fancy title"}]})

        with open(server.dbfile, "r") as f:
            json.loads(f.read()).should.be.equal({"posts": [{"author": "chucknorris", "id": 1, "title": "jsonserver"}, {"author": "tuxtimo", "id": 2, "title": "more fancy title"}]})

    @with_jsonserver()
    def test_create_table(self, server):
        """
            Test create a new table
        """
        server.get_table.when.called_with("posts").should.throw(TableNotFound, "Table 'posts' not found")
        server.create("posts")
        server.get_table("posts").should.be.equal({"posts": []})

        with open(server.dbfile, "r") as f:
            data = f.read()
            json.loads(data if data else "{}").should.be.equal({})

        server.create("comments", flush=True)

        with open(server.dbfile, "r") as f:
            json.loads(f.read()).should.be.equal({"posts": [], "comments": []})

        server.create.when.called_with("posts").should.throw(TableAlreadyExists, "Table 'posts' already exists")

    @with_jsonserver({"posts": [], "comments": []})
    def test_drop_table(self, server):
        """
            Test drop a table
        """
        server.all().should.be.equal({"posts": [], "comments": []})
        server.get_table("comments").should.be.equal({"comments": []})
        server.drop("comments")
        server.all().should.be.equal({"posts": []})
        server.get_table.when.called_with("comments").should.thrown(TableNotFound, "Table 'comments' not found")

        with open(server.dbfile, "r") as f:
            json.loads(f.read()).should.be.equal({"posts": [], "comments": []})

        server.drop("posts", flush=True)

        with open(server.dbfile, "r") as f:
            data = f.read()
            json.loads(data if data else "{}").should.be.equal({})

        server.drop.when.called_with("posts").should.throw(TableNotFound, "Table 'posts' not found")
