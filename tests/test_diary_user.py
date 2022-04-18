import unittest
from personal_diary.diary_user import DiaryUser
from personal_diary.app import create_app
from personal_diary.models import User
from personal_diary import db
from werkzeug.security import generate_password_hash

app = create_app("test_database.db")
app.app_context().push()


class DiaryUserTestCreateUser(unittest.TestCase):

    def setUp(self) -> None:
        hashed_password = generate_password_hash("this is a test password")
        self.valid_request = {"username": "username", "full_name": "Test User", "password": hashed_password}
    
    def tearDown(self) -> None:
        db.session.query(User).delete()
        db.session.commit()

    def test_valid_request_returns_nonzero_user_id(self):
        self.assertNotEqual(DiaryUser.create_user(self.valid_request), {"user_id": "0"})

    def test_response_contains_only_user_id_key(self):
        create_response = DiaryUser.create_user(self.valid_request)
        self.assertTrue("user_id" in create_response)
        self.assertEqual(set(create_response.keys()), {"user_id"})

    def test_user_id_is_unique(self):
        ids = []
        for idx in range(10):
            self.valid_request["username"] = "username" + str(idx)
            ids.append(DiaryUser.create_user(self.valid_request)["user_id"])
        self.assertEqual(len(set(ids)), 10)

    def test_single_create_user_db_populated_with_correct_values(self):
        user_id = DiaryUser.create_user(self.valid_request)["user_id"]
        db_entry = User.query.filter_by(id=user_id).first()
        self.assertEqual(db_entry.id, user_id)
        self.assertEqual(db_entry.username, self.valid_request["username"])
        self.assertEqual(db_entry.name, self.valid_request["full_name"])
        self.assertEqual(db_entry.password, self.valid_request["password"])

    def test_multiple_create_user_db_populated_with_correct_values(self):
        for idx in range(10):
            self.valid_request["username"] = "username" + str(idx)
            user_id = DiaryUser.create_user(self.valid_request)["user_id"]
            db_entry = User.query.filter_by(id=user_id).first()
            self.assertEqual(db_entry.id, user_id)
            self.assertEqual(db_entry.username, self.valid_request["username"])
            self.assertEqual(db_entry.name, self.valid_request["full_name"])
            self.assertEqual(db_entry.password, self.valid_request["password"])


if __name__ == '__main__':
    unittest.main()
