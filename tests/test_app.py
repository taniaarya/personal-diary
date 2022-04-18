import unittest
from unittest import TestCase
from personal_diary import db
from personal_diary.app import create_app
from personal_diary.models import Entry, User
from personal_diary.diary import Diary
from werkzeug.security import generate_password_hash


class ApplicationTestGETAll(TestCase):

    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.app_context().push()
        self.client = flask_app.test_client()

    def tearDown(self) -> None:
        self.client = None
        db.session.query(Entry).delete()
        db.session.commit()

    def test_get_can_send_json(self):
        response = self.client.get("/")
        self.assertTrue(response is not None, True)

    def test_get_valid_json_returns_success_response_get(self):
        response = self.client.get("/")
        self.assertTrue(response.status_code, 200)


class ApplicationTestEntryGET(TestCase):

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
        response = self.client.get(f'/entry/{self.entry_id}')
        self.assertTrue(response is not None, True)

    def test_get_valid_json_returns_success_response_get(self):
        response = self.client.get(f'/entry/{self.entry_id}')
        self.assertTrue(response.status_code, 200)


class ApplicationTestCreateEntryGET(TestCase):
    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
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

    def test_get_create_renders_create_page(self):
        response = self.client.get('/create', follow_redirects=True)
        self.assertEqual(response.request.path, "/create")


class ApplicationTestCreateEntryPOST(TestCase):
    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
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

    def test_successful_create_redirects_to_home(self):
        response = self.client.post('/create', data=dict(
            title="Title",
            body="Body",
        ), follow_redirects=True)
        self.assertEqual(response.request.path, "/")

    def test_unsuccessful_create_stays_on_create_page(self):
        response = self.client.post('/create', follow_redirects=True)
        self.assertEqual(response.request.path, "/create")


class ApplicationTestUpdateEntryGET(TestCase):
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
        response = self.client.get("/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response is not None, True)

    def test_put_valid_json_returns_success_response(self):
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.get("/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response.status_code, 200)

    def test_get_create_renders_create_page(self):
        response = self.client.get("/edit/{}".format(self.entry_id), follow_redirects=True)
        self.assertEqual(response.request.path, "/edit/{}".format(self.entry_id))


class ApplicationTestUpdateEntryPOST(TestCase):
    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        flask_app.app_context().push()
        self.client = flask_app.test_client()
        self.entry_id = Diary.create_entry({"title": "Title", "body": "Body"}).get("entry_id")

    def tearDown(self) -> None:
        self.client = None
        db.session.query(Entry).delete()
        db.session.commit()

    def test_update_can_send_json(self):
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.post("/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response is not None, True)

    def test_update_valid_json_returns_success_response(self):
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.post("/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response.status_code, 200)

    def test_successful_edit_redirects_to_home(self):
        response = self.client.post('/edit/{}'.format(self.entry_id), data=dict(
            title="Title",
            body="Body",
        ), follow_redirects=True)
        self.assertEqual(response.request.path, "/")

    def test_unsuccessful_edit_stays_on_create_page(self):
        response = self.client.post('/edit/{}'.format(self.entry_id), follow_redirects=True)
        self.assertEqual(response.request.path, '/edit/{}'.format(self.entry_id))


# class ApplicationTestDELETE(TestCase):
#     def setUp(self) -> None:
#         flask_app = create_app("test_database.db")
#         flask_app.app_context().push()
#         self.client = flask_app.test_client()
#
#     def tearDown(self) -> None:
#         self.client = None
#         db.session.query(Entry).delete()
#         db.session.commit()
#
#     def test_delete_can_send_json(self):
#         response = self.client.delete("/delete")
#         self.assertTrue(response is not None, True)
#
#     def test_delete_valid_json_returns_success_response(self):
#         response = self.client.delete("/delete")
#         self.assertTrue(response.status_code, 200)

class ApplicationTestSignupGET(TestCase):

    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        flask_app.app_context().push()
        self.client = flask_app.test_client()

    def tearDown(self) -> None:
        self.client = None
        db.session.query(User).delete()
        db.session.commit()

    def test_get_can_send_json(self):
        response = self.client.get("/signup")
        self.assertTrue(response is not None, True)

    def test_get_valid_json_returns_success_response_get(self):
        response = self.client.get("/signup")
        self.assertTrue(response.status_code, 200)

    def test_get_renders_signup_page(self):
        response = self.client.get('/signup', follow_redirects=True)
        self.assertEqual(response.request.path, "/signup")


class ApplicationTestSignupPOST(TestCase):

    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        flask_app.app_context().push()
        self.client = flask_app.test_client()

    def tearDown(self) -> None:
        self.client = None
        db.session.query(User).delete()
        db.session.commit()

    def test_post_can_send_json(self):
        response = self.client.post("/signup")
        self.assertTrue(response is not None, True)

    def test_post_valid_json_returns_success_response_get(self):
        response = self.client.post("/signup")
        self.assertTrue(response.status_code, 200)

    def test_successful_signup_redirects_to_login(self):
        response = self.client.post('/signup', data=dict(
            username="username",
            full_name="Test User",
            password="password123"
        ), follow_redirects=True)
        self.assertEqual(response.request.path, "/login")

    def test_unsuccessful_signup_stays_on_signup_page(self):
        response = self.client.post('/signup', follow_redirects=True)
        self.assertEqual(response.request.path, "/signup")

    def test_user_already_exists_redirects_to_signup_page(self):
        user = User(id="1", username="username", name="Test User", password=generate_password_hash("password123"))
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/signup', data=dict(
            username="username",
            full_name="Test User",
            password="password123"
        ), follow_redirects=True)
        self.assertEqual(response.request.path, "/signup")


if __name__ == '__main__':
    unittest.main()
