"""Contains tests for networking.py and app.py"""

import os
import unittest
import unittest.mock as mock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from gradio import Interface, close_all, routes

os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"


class TestRoutes(unittest.TestCase):
    def setUp(self) -> None:
        self.io = Interface(lambda x: x + x, "text", "text")
        self.app, _, _ = self.io.launch(prevent_thread_lock=True)
        self.client = TestClient(self.app)

    def test_get_main_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # def test_get_api_route(self):
    #     response = self.client.get("/api/")
    #     self.assertEqual(response.status_code, 200)

    def test_static_files_served_safely(self):
        # Make sure things outside the static folder are not accessible
        response = self.client.get(r"/static/..%2findex.html")
        self.assertEqual(response.status_code, 404)
        response = self.client.get(r"/static/..%2f..%2fapi_docs.html")
        self.assertEqual(response.status_code, 404)

    def test_get_config_route(self):
        response = self.client.get("/config/")
        self.assertEqual(response.status_code, 200)

    def test_predict_route(self):
        response = self.client.post(
            "/api/predict/", json={"data": ["test"], "fn_index": 0}
        )
        self.assertEqual(response.status_code, 200)
        output = dict(response.json())
        self.assertEqual(output["data"], ["testtest"])

    def test_predict_route_without_fn_index(self):
        response = self.client.post("/api/predict/", json={"data": ["test"]})
        self.assertEqual(response.status_code, 200)
        output = dict(response.json())
        self.assertEqual(output["data"], ["testtest"])

    def test_state(self):
        def predict(input, history):
            if history is None:
                history = ""
            history += input
            return history, history

        io = Interface(predict, ["textbox", "state"], ["textbox", "state"])
        app, _, _ = io.launch(prevent_thread_lock=True)
        client = TestClient(app)
        response = client.post(
            "/api/predict/",
            json={"data": ["test", None], "fn_index": 0, "session_hash": "_"},
        )
        output = dict(response.json())
        self.assertEqual(output["data"], ["test", None])
        response = client.post(
            "/api/predict/",
            json={"data": ["test", None], "fn_index": 0, "session_hash": "_"},
        )
        output = dict(response.json())
        self.assertEqual(output["data"], ["testtest", None])

    def tearDown(self) -> None:
        self.io.close()
        close_all()


class TestApp:
    def test_create_app(self):
        app = routes.App.create_app(Interface(lambda x: x, "text", "text"))
        assert isinstance(app, FastAPI)


class TestAuthenticatedRoutes(unittest.TestCase):
    def setUp(self) -> None:
        self.io = Interface(lambda x: x, "text", "text")
        self.app, _, _ = self.io.launch(
            auth=("test", "correct_password"),
            prevent_thread_lock=True,
            enable_queue=False,
        )
        self.client = TestClient(self.app)

    def test_post_login(self):
        response = self.client.post(
            "/login", data=dict(username="test", password="correct_password")
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            "/login", data=dict(username="test", password="incorrect_password")
        )
        self.assertEqual(response.status_code, 400)

    def tearDown(self) -> None:
        self.io.close()
        close_all()


if __name__ == "__main__":
    unittest.main()
