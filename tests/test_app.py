import unittest
from unittest import TestCase, mock
from personal_diary import db
from personal_diary.app import create_app
from personal_diary.models import Entry, User
from personal_diary.diary import Diary
from werkzeug.security import generate_password_hash


def set_up_flask_app_test_client():
    flask_app = create_app("test_database.db")
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config["LOGIN_DISABLED"] = True
    flask_app.app_context().push()
    return flask_app.test_client()


def create_test_user():
    test_user = User(id="1", username="username", name="Test User", password=generate_password_hash("test"))
    db.session.add(test_user)
    db.session.commit()
    return User.query.get("1")


def tear_down_flask_test():
    db.session.query(Entry).delete()
    db.session.query(User).delete()
    db.session.commit()


class ApplicationTestGETAll(TestCase):

    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()
        self.test_user = create_test_user()

    def tearDown(self) -> None:
        tear_down_flask_test()

    @mock.patch('flask_login.utils._get_user')
    def test_get_can_send_json(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.get("/")
        self.assertTrue(response is not None)

    @mock.patch('flask_login.utils._get_user')
    def test_get_valid_json_returns_success_response_get(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class ApplicationTestSearchPOST(TestCase):

    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()
        self.test_user = create_test_user()

    def tearDown(self) -> None:
        tear_down_flask_test()

    @mock.patch('flask_login.utils._get_user')
    def test_post_can_send_json(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.post('/', data=dict(
            search="search term",
        ), follow_redirects=True)
        self.assertTrue(response is not None)

    @mock.patch('flask_login.utils._get_user')
    def test_post_valid_json_returns_success_response(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.post('/', data=dict(
            search="search term",
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('flask_login.utils._get_user')
    def test_successful_create_redirects_to_home(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.post('/', data=dict(
            search="search term",
        ), follow_redirects=True)
        self.assertEqual(response.request.path, "/")


class ApplicationTestReadEntryGET(TestCase):

    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()
        self.test_user = create_test_user()
        self.entry_id = Diary.create_entry({"title": "Title", "body": "Body", "user_id": "1"}).get("entry_id")

    def tearDown(self) -> None:
        tear_down_flask_test()

    @mock.patch('flask_login.utils._get_user')
    def test_get_can_send_json(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.get(f'/entry/{self.entry_id}')
        self.assertTrue(response is not None)

    @mock.patch('flask_login.utils._get_user')
    def test_get_valid_json_returns_success_response_get(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.get(f'/entry/{self.entry_id}')
        self.assertEqual(response.status_code, 200)

    @mock.patch('flask_login.utils._get_user')
    def test_get_nonexistent_entry_returns_404(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.get(f'/entry/100')
        self.assertEqual(response.status_code, 404)

    @mock.patch('flask_login.utils._get_user')
    def test_get_entry_from_different_user_returns_404(self, current_user):
        current_user.return_value = self.test_user
        diff_entry_id = Diary.create_entry({"title": "Title", "body": "Body", "user_id": "2"})["entry_id"]
        response = self.client.get(f'/entry/{diff_entry_id}')
        self.assertEqual(response.status_code, 404)


class ApplicationTestCreateEntryGET(TestCase):

    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()
        self.test_user = create_test_user()

    def tearDown(self) -> None:
        tear_down_flask_test()

    def test_get_can_send_json(self):
        response = self.client.get('/create')
        self.assertTrue(response is not None)

    def test_get_valid_json_returns_success_response_get(self):
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 200)

    def test_get_create_renders_create_page(self):
        response = self.client.get('/create', follow_redirects=True)
        self.assertEqual(response.request.path, "/create")


class ApplicationTestCreateEntryPOST(TestCase):

    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()
        self.test_user = create_test_user()

    def tearDown(self) -> None:
        tear_down_flask_test()

    def test_post_can_send_json(self):
        response = self.client.post("/create")
        self.assertTrue(response is not None)

    def test_post_valid_json_returns_success_response(self):
        response = self.client.post("/create")
        self.assertEqual(response.status_code, 200)

    @mock.patch('flask_login.utils._get_user')
    def test_successful_create_redirects_to_home(self, current_user):
        current_user.return_value = self.test_user
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
        self.client = set_up_flask_app_test_client()
        self.test_user = create_test_user()
        self.entry_id = Diary.create_entry({"title": "Title", "body": "Body", "user_id": "1"}).get("entry_id")

    def tearDown(self) -> None:
        tear_down_flask_test()

    @mock.patch('flask_login.utils._get_user')
    def test_update_can_send_json(self, current_user):
        current_user.return_value = self.test_user
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.get("/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response is not None)

    @mock.patch('flask_login.utils._get_user')
    def test_update_valid_json_returns_success_response(self, current_user):
        current_user.return_value = self.test_user
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.get("/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertEqual(response.status_code, 200)

    @mock.patch('flask_login.utils._get_user')
    def test_get_update_renders_update_page(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.get("/edit/{}".format(self.entry_id), follow_redirects=True)
        self.assertEqual(response.request.path, "/edit/{}".format(self.entry_id))

    @mock.patch('flask_login.utils._get_user')
    def test_get_nonexistent_entry_returns_404(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.get(f'/edit/100')
        self.assertEqual(response.status_code, 404)

    @mock.patch('flask_login.utils._get_user')
    def test_get_entry_from_not_current_user_returns_404(self, current_user):
        current_user.return_value = self.test_user
        diff_entry_id = Diary.create_entry({"title": "Title", "body": "Body", "user_id": "2"})["entry_id"]
        response = self.client.get(f'/edit/{diff_entry_id}')
        self.assertEqual(response.status_code, 404)


class ApplicationTestUpdateEntryPOST(TestCase):
    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()
        self.entry_id = Diary.create_entry({"title": "Title", "body": "Body", "user_id": "1"}).get("entry_id")
        self.test_user = create_test_user()

    def tearDown(self) -> None:
        tear_down_flask_test()

    @mock.patch('flask_login.utils._get_user')
    def test_update_can_send_json(self, current_user):
        current_user.return_value = self.test_user
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.post("/edit/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response is not None)

    @mock.patch('flask_login.utils._get_user')
    def test_update_valid_json_returns_success_response(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.post("/edit/{}".format(self.entry_id))
        self.assertEqual(response.status_code, 200)

    @mock.patch('flask_login.utils._get_user')
    def test_successful_edit_redirects_to_home(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.post('/edit/{}'.format(self.entry_id), data=dict(
            title="Title",
            body="Body",
        ), follow_redirects=True)
        self.assertEqual(response.request.path, "/")

    @mock.patch('flask_login.utils._get_user')
    def test_unsuccessful_edit_stays_on_create_page(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.post('/edit/{}'.format(self.entry_id), follow_redirects=True)
        self.assertEqual(response.request.path, '/edit/{}'.format(self.entry_id))


class ApplicationTestDeleteEntryGET(TestCase):

    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()
        self.test_user = create_test_user()
        self.entry_id = Diary.create_entry({"title": "Title", "body": "Body", "user_id": "1"}).get("entry_id")

    def tearDown(self) -> None:
        tear_down_flask_test()

    @mock.patch('flask_login.utils._get_user')
    def test_delete_can_send_json(self, current_user):
        current_user.return_value = self.test_user
        valid_request_json = {"title": "Title", "body": "Body", "entry_id": self.entry_id}
        response = self.client.get("/delete/{}".format(self.entry_id), json=valid_request_json)
        self.assertTrue(response is not None)

    @mock.patch('flask_login.utils._get_user')
    def test_get_delete_redirects_to_home_page(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.get("/delete/{}".format(self.entry_id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, "/")

    @mock.patch('flask_login.utils._get_user')
    def test_delete_nonexistent_entry_returns_404(self, current_user):
        current_user.return_value = self.test_user
        response = self.client.get(f'/delete/100')
        self.assertEqual(response.status_code, 404)

    @mock.patch('flask_login.utils._get_user')
    def test_delete_entry_from_not_current_user_returns_404(self, current_user):
        current_user.return_value = self.test_user
        diff_entry_id = Diary.create_entry({"title": "Title", "body": "Body", "user_id": "2"})["entry_id"]
        response = self.client.get(f'/delete/{diff_entry_id}')
        self.assertEqual(response.status_code, 404)


class ApplicationTestSignupGET(TestCase):

    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()

    def tearDown(self) -> None:
        tear_down_flask_test()

    def test_get_can_send_json(self):
        response = self.client.get("/signup")
        self.assertTrue(response is not None)

    def test_get_valid_json_returns_success_response_get(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, 200)

    def test_get_renders_signup_page(self):
        response = self.client.get('/signup', follow_redirects=True)
        self.assertEqual(response.request.path, "/signup")


class ApplicationTestSignupPOST(TestCase):

    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()

    def tearDown(self) -> None:
        tear_down_flask_test()

    def test_post_can_send_json(self):
        response = self.client.post("/signup")
        self.assertTrue(response is not None)

    def test_post_valid_json_returns_success_response_get(self):
        response = self.client.post("/signup")
        self.assertEqual(response.status_code, 200)

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


class ApplicationTestLoginGET(TestCase):
    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()

    def tearDown(self) -> None:
        tear_down_flask_test()

    def test_get_can_send_json(self):
        response = self.client.get("/login")
        self.assertTrue(response is not None)

    def test_get_valid_json_returns_success_response_get(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_get_renders_signup_page(self):
        response = self.client.get('/login', follow_redirects=True)
        self.assertEqual(response.request.path, "/login")


class ApplicationTestLoginPOST(TestCase):
    def setUp(self) -> None:
        self.client = set_up_flask_app_test_client()

    def tearDown(self) -> None:
        tear_down_flask_test()

    def test_post_can_send_json(self):
        response = self.client.post("/login")
        self.assertTrue(response is not None)

    def test_post_valid_json_returns_success_response_get(self):
        response = self.client.post("/login")
        self.assertEqual(response.status_code, 200)

    def test_successful_login_redirects_to_home(self):
        user = User(id="1", username="username", name="Test User", password=generate_password_hash("password123"))
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data=dict(
            username="username",
            password="password123"
        ), follow_redirects=True)
        self.assertEqual(response.request.path, "/")

    def test_empty_login_stays_on_login_page(self):
        response = self.client.post('/login', follow_redirects=True)
        self.assertEqual(response.request.path, "/login")

    def test_user_exists_incorrect_password_stays_login_page(self):
        user = User(id="1", username="username", name="Test User", password=generate_password_hash("password123"))
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data=dict(
            username="username",
            password="password1234"
        ), follow_redirects=True)
        self.assertEqual(response.request.path, "/login")

    def test_user_does_not_exist_incorrect_password_stays_login_page(self):
        user = User(id="1", username="username", name="Test User", password=generate_password_hash("password123"))
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data=dict(
            username="username2",
            password="password123"
        ), follow_redirects=True)
        self.assertEqual(response.request.path, "/login")


if __name__ == '__main__':
    unittest.main()
