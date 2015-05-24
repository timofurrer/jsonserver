# -*- coding: utf-8 -*-

from tests.base import *
from unittest import TestCase


class RoutesTestCase(TestCase):

    @with_test_app
    @with_jsonserver({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}], "comments": []})
    def test_get_all(self, server, app):
        """
            Test HTTP: get all data
        """
        response = app.get("/")
        response_data = response.get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}], "comments": []})

    @with_test_app
    @with_jsonserver({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}], "comments": []})
    def test_get_table(self, server, app):
        """
            Test HTTP: get table
        """
        response_data = app.get("/posts").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"author": "tuxtimo", "id": 1, "title": "jsonserver"}]})

        response_data = app.get("/comments").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"comments": []})

    @with_test_app
    @with_jsonserver({"posts": [{"id": 1, "title": "jsonserver"}, {"id": 2, "title": "jsonserver2"}], "comments": [{"id": 1, "title": "jsonserver"}]})
    def test_get_row(self, server, app):
        """
            Test HTTP: get specific row within a table
        """
        response_data = app.get("/posts/1").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"id": 1, "title": "jsonserver"})

        response_data = app.get("/posts/2").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"id": 2, "title": "jsonserver2"})

        response_data = app.get("/comments/1").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"id": 1, "title": "jsonserver"})

    @with_test_app
    @with_jsonserver({"posts": [{"id": 1, "title": "jsonserver"}, {"id": 2, "title": "jsonserver2"}], "comments": [{"id": 1, "title": "jsonserver", "postId": 1}]})
    def test_get_row_sub_table(self, server, app):
        """
            Test HTTP: get specific rows from a connection between tables
        """
        response_data = app.get("/posts/1/comments").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"comments": [{"id": 1, "title": "jsonserver", "postId": 1}]})

        response_data = app.get("/posts/2/comments").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"comments": []})

    @with_test_app
    @with_jsonserver()
    def test_create_table(self, server, app):
        """
            Test HTTP: create new table
        """
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({})

        app.post("/", **get_json({"table": "posts"}))

        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": []})

        app.post("/", **get_json({"table": "comments"}))

        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [], "comments": []})

    @with_test_app
    @with_jsonserver({"posts": [], "comments": []})
    def test_drop_table(self, server, app):
        """
            Test HTTP: drop table
        """
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [], "comments": []})

        app.delete("/comments")

        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": []})

        app.delete("/posts")

        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({})

    @with_test_app
    @with_jsonserver({"posts": [], "comments": []})
    def test_insert_row(self, server, app):
        """
            Test HTTP: insert row into table
        """
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [], "comments": []})

        app.post("/posts", **get_json({"row": {"author": "tuxtimo", "body": "some content"}}))
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "body": "some content"}], "comments": []})

        app.post("/comments", **get_json({"row": {"author": "chuknorris", "body": "some awesome content"}}))
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "body": "some content"}], "comments": [{"id": 1, "author": "chuknorris", "body": "some awesome content"}]})

        app.post("/posts", **get_json({"row": {"author": "luck", "body": "some fancy content"}}))
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "body": "some content"}, {"id": 2, "author": "luck", "body": "some fancy content"}], "comments": [{"id": 1, "author": "chuknorris", "body": "some awesome content"}]})

    @with_test_app
    @with_jsonserver({"posts": [{"id": 1, "author": "tuxtimo", "body": "some content"}, {"id": 2, "author": "luck", "body": "some fancy content"}], "comments": [{"id": 1, "author": "chuknorris", "body": "some awesome content"}]})
    def test_remove_row(self, server, app):
        """
            Test HTTP: insert remove row from table
        """
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "body": "some content"}, {"id": 2, "author": "luck", "body": "some fancy content"}], "comments": [{"id": 1, "author": "chuknorris", "body": "some awesome content"}]})

        app.delete("/comments/1")
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "body": "some content"}, {"id": 2, "author": "luck", "body": "some fancy content"}], "comments": []})

        app.delete("/posts/1")
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"id": 2, "author": "luck", "body": "some fancy content"}], "comments": []})

        app.delete("/posts/2")
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [], "comments": []})

    @with_test_app
    @with_jsonserver({"posts": [{"id": 1, "author": "tuxtimo", "body": "some content"}, {"id": 2, "author": "luck", "body": "some fancy content"}], "comments": [{"id": 1, "author": "chuknorris", "body": "some awesome content"}]})
    def test_update_row(self, server, app):
        """
            Test HTTP: update row from table
        """
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "body": "some content"}, {"id": 2, "author": "luck", "body": "some fancy content"}], "comments": [{"id": 1, "author": "chuknorris", "body": "some awesome content"}]})

        app.put("/comments/1", **get_json({"row": {"author": "tuxtimo", "body": "some awesome edited content"}}))
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "body": "some content"}, {"id": 2, "author": "luck", "body": "some fancy content"}], "comments": [{"id": 1, "author": "tuxtimo", "body": "some awesome edited content"}]})

        app.patch("/posts/2", **get_json({"row": {"author": "obi", "body": "some fancy edited content"}}))
        response_data = app.get("/").get_data(as_text=True)
        json.loads(response_data).should.be.equal({"posts": [{"id": 1, "author": "tuxtimo", "body": "some content"}, {"id": 2, "author": "obi", "body": "some fancy edited content"}], "comments": [{"id": 1, "author": "tuxtimo", "body": "some awesome edited content"}]})
