import unittest
from unittest import TestCase
from personal_diary.app import Diary
from personal_diary import db
from personal_diary.app import create_app
from personal_diary.models import Entry


class ApplicationTestCaseEndToEnd(TestCase):
    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.app_context().push()
        self.client = flask_app.test_client()
        self.diary = Diary()

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()
        self.client = None
        self.diary = None

    def test_CRUD_operations_sequentially(self):
        response_list = []
        entry_ids = []
        valid_request_json = {"title": "Title", "body": "Body", "user_id": "1", "mood":"&#128512"}

        # test create entry
        for index in range(0, 50):
            create_entry_result = self.diary.create_entry(valid_request_json)
            entry_ids.append(create_entry_result["entry_id"])
            response_list.append(create_entry_result)

        # test read all entries
        read_all_entries_result = self.diary.read_all_entries("1")
        self.assertEqual(len(read_all_entries_result.keys()), 50)

        for entry_key, entry_val in read_all_entries_result.items():
            self.assertEqual(entry_key in entry_ids, True)
            self.assertEqual(read_all_entries_result[entry_key].title, "Title")
            self.assertEqual(read_all_entries_result[entry_key].body, "Body")
            self.assertEqual(read_all_entries_result[entry_key].mood, "&#128512")

        for entry_id in entry_ids:
            # test read single entry
            read_single_entry_result = self.diary.read_single_entry({"entry_id": entry_id}).get("entry")
            self.assertEqual(read_single_entry_result.title, "Title")
            self.assertEqual(read_single_entry_result.body, "Body")
            self.assertEqual(read_single_entry_result.mood, "&#128512")

        # test update entry
            update_entry_result = self.diary.update_entry({"entry_id": entry_id, "title": "NewTitle", "body": "Edited", "mood":"&#128525"})
            self.assertEqual(len(update_entry_result.keys()), 1)
            self.assertEqual(list(update_entry_result.keys())[0], entry_id)
            self.assertEqual(update_entry_result[entry_id].title, "NewTitle")
            self.assertEqual(update_entry_result[entry_id].body, "Edited")
            self.assertEqual(read_single_entry_result.mood, "&#128525")

            # test delete entry
            delete_entry_result = self.diary.delete_entry({"entry_id": entry_id})
            self.assertEqual(delete_entry_result["entry_id"], entry_id)

        response_get_all_end = self.diary.read_all_entries("1")
        self.assertEqual(len(response_get_all_end.keys()), 0)


if __name__ == '__main__':
    unittest.main()
