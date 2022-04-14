import unittest
from datetime import datetime
from personal_diary.diary import Diary
from personal_diary.app import create_app
from personal_diary.models import Entry
from personal_diary import db

app = create_app("test_database.db")
app.app_context().push()


class DiaryTestCreateEntry(unittest.TestCase):

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    def test_valid_request_returns_nonzero_entry_id(self):
        valid_request = {"title": "Title", "body": "Body"}
        self.assertNotEqual(Diary.create_entry(valid_request), {"entry_id": "0"})

    def test_response_contains_only_entry_id_key(self):
        valid_request = {"title": "Title", "body": "Body"}
        create_response = Diary.create_entry(valid_request)
        self.assertTrue("entry_id" in create_response)
        self.assertEqual(set(create_response.keys()), {"entry_id"})

    def test_entry_id_is_unique(self):
        ids = []
        valid_request = {"title": "Title", "body": "Body"}
        for _ in range(10):
            ids.append(Diary.create_entry(valid_request)["entry_id"])
        self.assertEqual(len(set(ids)), 10)

    def test_single_create_entry_db_populated_with_correct_values(self):
        valid_request = {"title": "Title", "body": "Body"}
        entry_id = Diary.create_entry(valid_request)["entry_id"]
        db_entry = Entry.query.filter_by(id=entry_id).first()
        self.assertEqual(db_entry.id, entry_id)
        self.assertEqual(db_entry.title, "Title")
        self.assertEqual(db_entry.body, "Body")
        self.assertIsInstance(db_entry.created, datetime)
        self.assertIsInstance(db_entry.created, datetime)

    def test_multiple_create_entry_db_populated_with_correct_values(self):
        valid_request = {"title": "Title", "body": "Body"}
        for _ in range(10):
            entry_id = Diary.create_entry(valid_request)["entry_id"]
            db_entry = Entry.query.filter_by(id=entry_id).first()
            self.assertEqual(db_entry.id, entry_id)
            self.assertEqual(db_entry.title, "Title")
            self.assertEqual(db_entry.body, "Body")
            self.assertIsInstance(db_entry.created, datetime)
            self.assertIsInstance(db_entry.created, datetime)


class DiaryTestReadSingleEntry(unittest.TestCase):

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    def test_read_populated_db_one_key_returns_correct_dict(self):
        entry_id = Diary.create_entry({"title": "Title", "body": "Body"})
        read_entry = Diary.read_single_entry(entry_id).get("entry")
        self.assertEqual(read_entry.id, entry_id["entry_id"])
        self.assertEqual(read_entry.title, "Title")
        self.assertEqual(read_entry.body, "Body")

    def test_read_populated_db_multiple_keys_returns_correct_dict(self):
        entry_dict = [
            {"title": "Title", "body": "Body", "date_created": "12/22/2021", "time_created": "12:23"},
            {"title": "Title", "body": "Body", "date_created": "12/22/2021", "time_created": "14:23"}
        ]
        entry_ids = []
        for entry in entry_dict:
            entry_ids.append(Diary.create_entry(entry).get("entry_id"))

        for id in entry_ids:
            self.assertEqual(Diary.read_single_entry({"entry_id": id}).get("entry").id, id)
            self.assertEqual(Diary.read_single_entry({"entry_id": id}).get("entry").title, "Title")
            self.assertEqual(Diary.read_single_entry({"entry_id": id}).get("entry").body, "Body")


class DiaryTestReadAllEntries(unittest.TestCase):

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    def test_read_empty_dictionary_returns_empty(self):
        self.assertEqual(Diary.read_all_entries(), {})

    def test_read_populated_db_one_key_returns_correct_dict(self):
        # Create entry and read only (all entry)
        valid_request = {"title": "Title", "body": "Body"}
        entry_id = Diary.create_entry(valid_request).get("entry_id")
        entries = Diary.read_all_entries()

        self.assertEqual(entries[entry_id].title, "Title")
        self.assertEqual(entries[entry_id].body, "Body")
        self.assertEqual(len(entries), 1)

    def test_read_populated_db_multiple_keys_returns_correct_dict(self):
        for i in range(0, 5):
            Diary.create_entry({"title": "Title", "body": "Body"})

        entries = Diary.read_all_entries()
        for entry_id in entries:
            self.assertEqual(entries[entry_id].title, "Title")
            self.assertEqual(entries[entry_id].body, "Body")
        self.assertEqual(len(entries), 5)


class DiaryTestUpdateEntry(unittest.TestCase):

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    def test_single_update_with_new_body_valid_entry_id_and_title_returns_updated_entry(self):
        entry_id = Diary.create_entry({"title": "Title", "body": "Body"}).get("entry_id")
        updated_entry = Diary.read_single_entry({"entry_id": entry_id}).get("entry")
        self.assertEqual(updated_entry.title, "Title")
        self.assertEqual(updated_entry.body, "Body")

        Diary.update_entry({"entry_id": entry_id, "title": "value2", "body": "Hello Human!"})
        self.assertEqual(updated_entry.title, "value2")
        self.assertEqual(updated_entry.body, "Hello Human!")

    def test_multiple_update_to_same_entry_returns_updated_entry(self):
        entry_id = Diary.create_entry({"title": "Title", "body": "Body"}).get("entry_id")
        updated_entry = Diary.read_single_entry({"entry_id": entry_id}).get("entry")

        for idx in range(10):
            new_title = "value" + str(idx)
            new_body = "Hello Human!" + str(idx)
            Diary.update_entry({"entry_id": entry_id, "title": new_title, "body": new_body})
            self.assertEqual(updated_entry.title, new_title)
            self.assertEqual(updated_entry.body, new_body)

    def test_update_to_different_entries_returns_updated_entries(self):
        entry_ids = []
        entry_dict = [
            {"title": "Title", "body": "Body", "date_created": "12/22/2021", "time_created": "12:23"},
            {"title": "Title", "body": "Body", "date_created": "12/22/2021", "time_created": "14:23"},
            {"title": "Title", "body": "Body", "date_created": "12/22/2021", "time_created": "16:23"}
        ]

        for entry in entry_dict:
            entry_ids.append(Diary.create_entry(entry).get("entry_id"))

        for entry_id in entry_ids:
            updated_entry = Diary.read_single_entry({"entry_id": entry_id}).get("entry")
            new_title = "value" + str(entry_id)
            new_body = "Hello Human!" + str(entry_id)
            Diary.update_entry({"entry_id": entry_id, "title": new_title, "body": new_body})
            self.assertEqual(updated_entry.title, new_title)
            self.assertEqual(updated_entry.body, new_body)


class DiaryTestDeleteEntry(unittest.TestCase):

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    def test_delete_empties_entries_when_only_one_entry(self):
        request = {"title": "Title", "body": "Body"}
        entry_id = Diary.create_entry(request)
        self.assertDictEqual(Diary.delete_entry(entry_id), entry_id)

        self.assertEqual(Diary.read_all_entries(), {})

    def test_delete_with_two_existing_entries_only_deletes_specified_entry(self):
        entry_dict = [
            {"title": "Title", "body": "Body", "date_created": "12/22/2021", "time_created": "12:23"},
            {"title": "Title", "body": "Body", "date_created": "12/22/2021", "time_created": "14:23"}
        ]
        entry_ids = []
        for entry in entry_dict:
            entry_ids.append(Diary.create_entry(entry).get("entry_id"))

        for id in entry_ids:
            self.assertEqual(Diary.delete_entry({"entry_id": id}), {"entry_id": id})

        self.assertEqual(Diary.read_all_entries(), {})


# class DiaryTestIsIdInvalid(unittest.TestCase):
#     def setUp(self) -> None:
#         Diary = Diary()
#
#     def tearDown(self) -> None:
#         with open(Diary.local_db_path, 'w') as outfile:
#             outfile.write("{}")
#
#     def test_invalid_id_returns_true(self):
#         test_dict = {
#             "1": {"title": "title_value"},
#             "2": {"title": "title_value"}
#         }
#         Diary.write_to_db(test_dict)
#
#         self.assertTrue(Diary.is_id_invalid(-1))
#         self.assertTrue(Diary.is_id_invalid(0))
#         self.assertTrue(Diary.is_id_invalid(50))
#
#     def test_valid_id_returns_false(self):
#         test_dict = {
#             "1": {"title": "title_value"},
#             "2": {"title": "title_value"}
#         }
#         Diary.write_to_db(test_dict)
#
#         self.assertFalse(Diary.is_id_invalid(1))
#         self.assertFalse(Diary.is_id_invalid(2))


if __name__ == '__main__':
    unittest.main()
