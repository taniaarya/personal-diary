import unittest
import os
from personal_diary.diary_user import DiaryUser
from personal_diary.app import flask_app
from personal_diary.models import User
from personal_diary import db
from werkzeug.security import generate_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "test_database.db")
flask_app.app_context().push()
db.create_all()


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
            
            
class DiaryUserTestDeleteUser(unittest.TestCase):

    def tearDown(self) -> None:
        db.session.query(User).delete()
        db.session.commit()

    @staticmethod
    def populate_multiple_users():
        for user_id in range(5):
            password = generate_password_hash(str(user_id))
            test_user = User(id=str(user_id), username=f"username{user_id}", name="User", password=password)
            db.session.add(test_user)
        db.session.commit()

    @staticmethod
    def populate_single_user():
        test_user = User(id=str(1), username=f"username{1}", name="User", password=generate_password_hash("1"))
        db.session.add(test_user)
        db.session.commit()
        return test_user

    def test_delete_empties_users_when_only_one_user(self):
        test_user = self.populate_single_user()
        self.assertDictEqual(DiaryUser.delete_user({"user": test_user}), {"user_id": "1"})
        self.assertIsNone(User.query.get("1"))

    def test_delete_with_two_existing_users_only_deletes_specified_user(self):
        self.populate_multiple_users()
        for user_id in range(5):
            test_user = User.query.get(str(user_id))
            self.assertDictEqual(DiaryUser.delete_user({"user": test_user}), {"user_id": str(user_id)})
        self.assertEqual(User.query.all(), [])


if __name__ == '__main__':
    unittest.main()
