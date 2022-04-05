import unittest
import os
import json
from personal_diary.diary import Diary


class DiaryTestReadFromDb(unittest.TestCase):

    def setUp(self) -> None:
        self.diary = Diary()
        self.db_path = os.path.join(os.path.abspath('..'), "personal_diary/entry_local_storage.json")

    def tearDown(self) -> None:
        with open(self.db_path, 'w') as outfile:
            outfile.write("{}")

    def testReadEmptyDictionaryReturnsEmpty(self):
        self.assertEqual(self.diary.read_from_db(), {})

    def testReadPopulatedDbOneKeyReturnsCorrectDict(self):
        test_dict = {
            "key1": "value1"
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.db_path, "w") as outfile:
            outfile.write(json_object)

        self.assertEqual(self.diary.read_from_db(), test_dict)

    def testReadPopulatedDbMultipleKeysReturnsCorrectDict(self):
        test_dict = {
            "key1": "value1",
            "key2": "value2"
        }
        json_object = json.dumps(test_dict, indent=4)
        with open(self.db_path, "w") as outfile:
            outfile.write(json_object)

        self.assertEqual(self.diary.read_from_db(), test_dict)


class DiaryTestWriteToDb(unittest.TestCase):

    def setUp(self) -> None:
        self.diary = Diary()
        self.db_path = os.path.join(os.path.abspath('..'), "personal_diary/entry_local_storage.json")

    def tearDown(self) -> None:
        with open(self.db_path, 'w') as outfile:
            outfile.write("{}")

    def read(self):
        with open(self.db_path, 'r') as openfile:
            return json.load(openfile)

    def testWriteEmptyDictionaryPopulatesEmptyDb(self):
        self.diary.write_to_db({})
        self.assertEqual(self.read(), {})

    def testWriteDictOneKeyPopulatesDb(self):
        test_dict = {
            "key1": "value1"
        }
        self.diary.write_to_db(test_dict)
        self.assertEqual(self.read(), test_dict)

    def testWriteDictMultipleKeysPopulatesDb(self):
        test_dict = {
            "key1": "value1",
            "key2": "value2"
        }
        self.diary.write_to_db(test_dict)
        self.assertEqual(self.read(), test_dict)


if __name__ == '__main__':
    unittest.main()
