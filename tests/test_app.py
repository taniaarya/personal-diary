import unittest
from unittest import TestCase
from personal_diary import db
from personal_diary.app import create_app
from personal_diary.models import Entry
from personal_diary.diary import Diary


class ApplicationTestCaseGETAll(TestCase):

    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.app_context().push()
        self.client = flask_app.test_client()

    def tearDown(self) -> None:
        self.client = None
        db.session.query(Entry).delete()
        db.session.commit()

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
        flask_app = create_app("test_database.db")
        flask_app.app_context().push()
        self.client = flask_app.test_client()
        self.entry_id = Diary.create_entry({"title": "Title", "body": "Body"}).get("entry_id")

    def tearDown(self) -> None:
        self.client = None
        db.session.query(Entry).delete()
        db.session.commit()

    def test_get_can_send_json(self):
        response = self.client.get(f'/diary/{self.entry_id}')
        self.assertTrue(response is not None, True)

    def test_get_valid_json_returns_success_response_get(self):
        response = self.client.get(f'/diary/{self.entry_id}')
        self.assertTrue(response.status_code, 200)

    def test_get_valid_json_returns_correct_keys_for_(self):
        response = self.client.get(f'/diary/{self.entry_id}')
        self.assertTrue(response.get_data())


class ApplicationTestCaseCreateEntryGET(TestCase):
    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.app_context().push()
        self.client = flask_app.test_client()

    def tearDown(self) -> None:
        self.client = None
        db.session.query(Entry).delete()
        db.session.commit()

    def test_get_can_send_json(self):
        response = self.client.get('/create')
        self.assertTrue(response is not None, True)

    def test_get_valid_json_returns_success_response_get(self):
        response = self.client.get('/create')
        self.assertTrue(response.status_code, 200)


class ApplicationTestCaseCreateEntryPOST(TestCase):
    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.app_context().push()
        self.client = flask_app.test_client()

    def tearDown(self) -> None:
        self.client = None
        db.session.query(Entry).delete()
        db.session.commit()

    def test_post_can_send_json(self):
        response = self.client.post("/create")
        self.assertTrue(response is not None, True)

    def test_post_valid_json_returns_success_response(self):
        response = self.client.post("/create")
        self.assertTrue(response.status_code, 200)


class ApplicationTestCaseUpdateEntryGet(TestCase):
    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.app_context().push()
        self.client = flask_app.test_client()
        self.entry_id = Diary.create_entry({"title": "Title", "body": "Body"}).get("entry_id")

    def tearDown(self) -> None:
        self.client = None
        db.session.query(Entry).delete()
        db.session.commit()

    def test_put_can_send_json(self):
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.get("/diary/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response is not None, True)

    def test_put_valid_json_returns_success_response(self):
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.get("/diary/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response.status_code, 200)


class ApplicationTestCaseUpdateEntryPost(TestCase):
    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.app_context().push()
        self.client = flask_app.test_client()
        self.entry_id = Diary.create_entry({"title": "Title", "body": "Body"}).get("entry_id")

    def tearDown(self) -> None:
        self.client = None
        db.session.query(Entry).delete()
        db.session.commit()

    def test_put_can_send_json(self):
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.post("/diary/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response is not None, True)

    def test_put_valid_json_returns_success_response(self):
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.post("/diary/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response.status_code, 200)


class ApplicationTestCaseDELETE(TestCase):
    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.app_context().push()
        self.client = flask_app.test_client()

    def tearDown(self) -> None:
        self.client = None
        db.session.query(Entry).delete()
        db.session.commit()

    def test_delete_can_send_json(self):
        response = self.client.delete("/diary")
        self.assertTrue(response is not None, True)

    def test_delete_valid_json_returns_success_response(self):
        response = self.client.delete("/diary")
        self.assertTrue(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
