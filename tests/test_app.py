import json
import os
import unittest
from unittest import TestCase
from personal_diary.app import create_app


class ApplicationTestCaseGETAll(TestCase):

    def setUp(self) -> None:
        flask_app = create_app()
        self.client = flask_app.test_client()
        self.local_db_path = os.path.join(os.path.abspath('..'), "personal_diary/entry_local_storage.json")

    def tearDown(self) -> None:
        self.client = None
        with open(self.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def test_get_can_send_json(self):
        response = self.client.get("/diary")
        self.assertTrue(response is not None, True)

    def test_get_valid_json_returns_success_response_get(self):
        response = self.client.get("/diary")
        self.assertTrue(response.status_code, 200)

    def test_get_valid_json_returns_correct_keys_for_(self):
        response = self.client.get("/diary")
        self.assertTrue(response.get_data())


class ApplicationTestCaseGET(TestCase):

    def setUp(self) -> None:
        flask_app = create_app()
        self.client = flask_app.test_client()
        self.local_db_path = os.path.join(os.path.abspath('..'), "personal_diary/entry_local_storage.json")
        with open(self.local_db_path, 'w') as outfile:
            fake_data = {"1": {"title": "Title", "body": "Body", "date_created": "12/13/2021", "time_created": "12:14"}}
            outfile.write(json.dumps(fake_data))

        self.entry_id = "1"

    def tearDown(self) -> None:
        self.client = None
        with open(self.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def test_get_can_send_json(self):
        response = self.client.get(f'/diary/{self.entry_id}')
        self.assertTrue(response is not None, True)

    def test_get_valid_json_returns_success_response_get(self):
        response = self.client.get(f'/diary/{self.entry_id}')
        self.assertTrue(response.status_code, 200)

    def test_get_valid_json_returns_correct_keys_for_(self):
        response = self.client.get(f'/diary/{self.entry_id}')
        self.assertTrue(response.get_data())


class ApplicationTestCasePOST(TestCase):
    def setUp(self) -> None:
        flask_app = create_app()
        self.client = flask_app.test_client()
        self.local_db_path = os.path.join(os.path.abspath('..'), "personal_diary/entry_local_storage.json")

    def tearDown(self) -> None:
        self.client = None
        with open(self.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def test_post_can_send_json(self):
        valid_request_json = {"title": "Title", "body": "Body"}
        response = self.client.post("/diary", json=valid_request_json)
        self.assertTrue(response is not None, True)

    def test_post_valid_json_returns_success_response(self):
        valid_request_json = {"title": "Title", "body": "Body"}
        response = self.client.post("/diary", json=valid_request_json)
        self.assertTrue(response.status_code, 200)


class ApplicationTestCasePUT(TestCase):
    def setUp(self) -> None:
        flask_app = create_app()
        self.client = flask_app.test_client()
        self.local_db_path = os.path.join(os.path.abspath('..'), "personal_diary/entry_local_storage.json")

    def tearDown(self) -> None:
        self.client = None
        with open(self.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def test_put_can_send_json(self):
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": "1"}
        response = self.client.put("/diary", json=valid_request_json)
        self.assertTrue(response is not None, True)

    def test_put_valid_json_returns_success_response(self):
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": "1"}
        response = self.client.put("/diary", json=valid_request_json)
        self.assertTrue(response.status_code, 200)


class ApplicationTestCaseDELETE(TestCase):
    def setUp(self) -> None:
        flask_app = create_app()
        self.client = flask_app.test_client()
        self.local_db_path = os.path.join(os.path.abspath('..'), "personal_diary/entry_local_storage.json")

    def tearDown(self) -> None:
        self.client = None
        with open(self.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def test_delete_can_send_json(self):
        response = self.client.delete("/diary")
        self.assertTrue(response is not None, True)

    def test_delete_valid_json_returns_success_response(self):
        response = self.client.delete("/diary")
        self.assertTrue(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

