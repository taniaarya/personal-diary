import unittest
import json
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


class DiaryTestReadEntry(unittest.TestCase):

    def setUp(self) -> None:
        self.diary = Diary()

    def tearDown(self) -> None:
        with open(self.diary.local_db_path, 'w') as outfile:
            outfile.write("{}")

    def test_read_empty_dictionary_returns_empty(self):
        self.assertEqual(self.diary.read_entry(), {})

    def test_read_populated_db_one_key_returns_correct_dict(self):
        test_dict = {
            "key1": "value1"


class DiaryTestUpdateEntry(unittest.TestCase):

    def setUp(self) -> None:
        self.diary = Diary()
        self.db_path = os.path.join(os.path.abspath('..'), "personal_diary/entry_local_storage.json")

    def tearDown(self) -> None:
        with open(self.db_path, 'w') as outfile:
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
        self.assertEqual(self.diary.read_entry(), test_dict)

    def test_read_populated_db_multiple_keys_returns_correct_dict(self):
        test_dict = {
            "key1": "value1",
            "key2": "value2"
        expected = {
            '20': {
                "title": "value1",
                "body": "Hello Human!"}
        }
        result = self.diary.update_entry({"entry_id": '20', "body": "Hello Human!"})
        self.assertEqual(expected, result)
        pass

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
        pass

    def test_update_with_new_body_valid_entry_id_and_title_returns_updated_entry(self):
        test_dict = {
            20: {
                "title": "value1",
                "body": "Hello World!"}
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.diary.local_db_path, "w") as outfile:
            outfile.write(json_object)
        self.assertEqual(self.diary.read_entry(), test_dict)
        expected = {
            '20': {
                "title": "value2",
                "body": "Hello Human!"}
        }
        result = self.diary.update_entry({"entry_id": '20', "title": "value2", "body": "Hello Human!"})
        self.assertEqual(expected, result)
        pass


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
