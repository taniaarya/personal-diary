import unittest
import json
import re
from datetime import datetime
from personal_diary.diary import Diary


class DiaryTestReadFromDb(unittest.TestCase):

    def setUp(self) -> None:
        self.diary = Diary()

    def tearDown(self) -> None:
        with open(self.diary.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def test_read_empty_dictionary_returns_empty(self):
        self.assertEqual(self.diary.read_from_db(), {})

    def test_read_populated_db_one_key_returns_correct_dict(self):
        test_dict = {
            "key1": "value1"
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.diary.local_db_path, "w") as outfile:
            outfile.write(json_object)

        self.assertEqual(self.diary.read_from_db(), test_dict)

    def test_read_populated_db_multiple_keys_returns_correct_dict(self):
        test_dict = {
            "key1": "value1",
            "key2": "value2"
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.diary.local_db_path, "w") as outfile:
            outfile.write(json_object)

        self.assertEqual(self.diary.read_from_db(), test_dict)


class DiaryTestWriteToDb(unittest.TestCase):

    def setUp(self) -> None:
        self.diary = Diary()

    def tearDown(self) -> None:
        with open(self.diary.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def read(self):
        with open(self.diary.local_db_path, 'r') as openfile:
            return json.load(openfile)

    def test_write_empty_dictionary_populates_empty_db(self):
        self.diary.write_to_db({})
        self.assertEqual(self.read(), {})

    def test_write_dict_one_key_populates_db(self):
        test_dict = {
            "key1": "value1"
        }
        self.diary.write_to_db(test_dict)
        self.assertEqual(self.read(), test_dict)

    def test_write_dict_multiple_keys_populates_db(self):
        test_dict = {
            "key1": "value1",
            "key2": "value2"
        }
        self.diary.write_to_db(test_dict)
        self.assertEqual(self.read(), test_dict)


class DiaryTestCreateEntry(unittest.TestCase):

    def setUp(self) -> None:
        self.diary = Diary()

    def tearDown(self) -> None:
        with open(self.diary.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def read(self):
        with open(self.diary.local_db_path, 'r') as openfile:
            return json.load(openfile)

    def test_request_is_none_returns_invalid_entry_id(self):
        self.assertEqual(self.diary.create_entry(None), {"entry_id": 0})

    def test_request_missing_keys_returns_invalid_entry_id(self):
        missing_title = {"body": "Body"}
        missing_body = {"title": "Title"}
        self.assertEqual(self.diary.create_entry(missing_title), {"entry_id": 0})
        self.assertEqual(self.diary.create_entry(missing_body), {"entry_id": 0})

    def test_valid_request_returns_nonzero_entry_id(self):
        valid_request = {"title": "Title", "body": "Body"}
        self.assertNotEqual(self.diary.create_entry(valid_request), {"entry_id": 0})

    def test_entry_id_is_unique(self):
        ids = []
        valid_request = {"title": "Title", "body": "Body"}
        for _ in range(10):
            ids.append(self.diary.create_entry(valid_request)["entry_id"])
        self.assertEqual(len(set(ids)), 10)

    def test_create_entry_db_populated_with_correct_values(self):
        valid_request = {"title": "Title", "body": "Body"}
        entry_id = self.diary.create_entry(valid_request)["entry_id"]
        db_value = self.read()
        curr_time = datetime.now()
        self.assertEqual(db_value[entry_id]["title"], "Title")
        self.assertEqual(db_value[entry_id]["body"], "Body")
        self.assertTrue(re.match(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$", db_value[entry_id]["date_created"]))
        self.assertTrue(re.match(r"^[0-9]{2}:[0-9]{2}$", db_value[entry_id]["time_created"]))


class DiaryTestReadEntry(unittest.TestCase):

    def setUp(self) -> None:
        self.diary = Diary()

    def tearDown(self) -> None:
        with open(self.diary.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def test_read_populated_db_one_key_returns_correct_dict(self):
        test_dict = {
            "1": {"title": "Title", "body": "Body", "date_created": "12/22/2021", "time_created": "12:23"}
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.diary.local_db_path, "w") as outfile:
            outfile.write(json_object)

        self.assertEqual(self.diary.read_entry({"entry_id": "1"}), test_dict["1"])

    def test_read_populated_db_multiple_keys_returns_correct_dict(self):
        test_dict = {
            "1": {"title": "Title", "body": "Body", "date_created": "12/22/2021", "time_created": "12:23"},
            "2": {"title": "Title", "body": "Body", "date_created": "12/22/2021", "time_created": "14:23"}
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.diary.local_db_path, "w") as outfile:
            outfile.write(json_object)

        self.assertEqual(self.diary.read_entry({"entry_id": "1"}), test_dict["1"])
        self.assertEqual(self.diary.read_entry({"entry_id": "2"}), test_dict["2"])


class DiaryTestUpdateEntry(unittest.TestCase):

    def setUp(self) -> None:
        self.diary = Diary()

    def tearDown(self) -> None:
        with open(self.diary.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def test_update_with_empty_request_invalid(self):
        test_dict = {
            20: {
                "title": "value1",
                "body": "Hello World!"}
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.diary.local_db_path, "w") as outfile:
            outfile.write(json_object)
        self.assertEqual(self.diary.update_entry({}), {"entry_id": 0})

    def test_update_with_no_current_entries_invalid(self):
        self.assertEqual(self.diary.update_entry({"title": "Hello", "body": "The day is nice"}), {"entry_id": 0})

    def test_update_with_multiple_entries_and_invalid_entry_id_returns_error(self):
        test_dict = {
            20: {
                "title": "value1",
                "body": "Hello World!"},
            28: {
                "title": "value2",
                "body": "Hello Human!"}
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.diary.local_db_path, "w") as outfile:
            outfile.write(json_object)
        self.assertEqual(self.diary.update_entry({"entry_id": '2', "title": "Hello"}), {"entry_id": 0})

    def test_update_with_new_body_and_valid_entry_id_returns_updated_entry(self):
        test_dict = {
            20: {
                "title": "value1",
                "body": "Hello World!"}
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.diary.local_db_path, "w") as outfile:
            outfile.write(json_object)
        expected = {
            '20': {
                "title": "value1",
                "body": "Hello Human!"}
        }
        result = self.diary.update_entry({"entry_id": '20', "body": "Hello Human!"})
        self.assertEqual(expected, result)

    def test_update_with_new_title_and_valid_entry_id_returns_updated_entry(self):
        test_dict = {
            20: {
                "title": "value1",
                "body": "Hello World!"}
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.diary.local_db_path, "w") as outfile:
            outfile.write(json_object)
        expected = {
            '20': {
                "title": "value2",
                "body": "Hello World!"}
        }
        result = self.diary.update_entry({"entry_id": '20', "title": "value2"})
        self.assertEqual(expected, result)

    def test_update_with_new_body_valid_entry_id_and_title_returns_updated_entry(self):
        test_dict = {
            20: {
                "title": "value1",
                "body": "Hello World!"}
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.diary.local_db_path, "w") as outfile:
            outfile.write(json_object)
        expected = {
            '20': {
                "title": "value2",
                "body": "Hello Human!"}
        }
        result = self.diary.update_entry({"entry_id": '20', "title": "value2", "body": "Hello Human!"})
        self.assertEqual(expected, result)


class DiaryTestIsIdInvalid(unittest.TestCase):
    def setUp(self) -> None:
        self.diary = Diary()

    def tearDown(self) -> None:
        with open(self.diary.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def test_invalid_id_returns_true(self):
        test_dict = {
            "1": {"title": "title_value"},
            "2": {"title": "title_value"}
        }
        self.diary.write_to_db(test_dict)

        self.assertTrue(self.diary.is_id_invalid(-1))
        self.assertTrue(self.diary.is_id_invalid(0))
        self.assertTrue(self.diary.is_id_invalid(50))

    def test_valid_id_returns_false(self):
        test_dict = {
            "1": {"title": "title_value"},
            "2": {"title": "title_value"}
        }
        self.diary.write_to_db(test_dict)

        self.assertFalse(self.diary.is_id_invalid(1))
        self.assertFalse(self.diary.is_id_invalid(2))


if __name__ == '__main__':
    unittest.main()
