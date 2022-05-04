import unittest
from datetime import datetime
from personal_diary.diary import Diary
from personal_diary.app import create_app
from personal_diary.models import Entry, Tag
from personal_diary import db

app = create_app("test_database.db")
app.app_context().push()


class DiaryTestCreateEntry(unittest.TestCase):

    def setUp(self) -> None:
        self.valid_request = {"title": "Title", "body": "Body", "user_id": "1", "tags": ["tag1", "tag2", "tag3"],
                              "mood": "128512"}

    def tearDown(self) -> None:
        db.drop_all()
        db.create_all()
        db.session.commit()

    def test_valid_request_returns_nonzero_entry_id(self):
        self.assertNotEqual(Diary.create_entry(self.valid_request), {"entry_id": "0"})

    def test_response_contains_only_entry_id_key(self):
        create_response = Diary.create_entry(self.valid_request)
        self.assertTrue("entry_id" in create_response)
        self.assertEqual(set(create_response.keys()), {"entry_id"})

    def test_entry_id_is_unique(self):
        ids = []
        for _ in range(10):
            ids.append(Diary.create_entry(self.valid_request)["entry_id"])
        self.assertEqual(len(set(ids)), 10)

    def test_single_create_entry_db_populated_with_correct_values(self):
        entry_id = Diary.create_entry(self.valid_request)["entry_id"]
        db_entry = Entry.query.filter_by(id=entry_id).first()
        self.assertEqual(db_entry.id, entry_id)
        self.assertEqual(db_entry.title, "Title")
        self.assertEqual(db_entry.body, "Body")
        self.assertIsInstance(db_entry.created, datetime)
        self.assertIsInstance(db_entry.created, datetime)

    def test_multiple_create_entry_db_populated_with_correct_values(self):
        for _ in range(10):
            entry_id = Diary.create_entry(self.valid_request)["entry_id"]
            db_entry = Entry.query.filter_by(id=entry_id).first()
            self.assertEqual(db_entry.id, entry_id)
            self.assertEqual(db_entry.title, "Title")
            self.assertEqual(db_entry.body, "Body")
            self.assertIsInstance(db_entry.created, datetime)
            self.assertIsInstance(db_entry.created, datetime)


class DiaryTestAddTagsToEntry(unittest.TestCase):

    def tearDown(self) -> None:
        db.drop_all()
        db.create_all()
        db.session.commit()

    @staticmethod
    def create_fake_entry():
        test_entry = Entry(id="1", title="Title", body="Body", created=datetime.now(), user_id="1", mood="&#128512")
        test_entry.tags.append(Tag(name="test"))
        db.session.add(test_entry)
        db.session.commit()
        return test_entry

    def test_single_tag_doesnt_exist_creates_new_tag_object(self):
        entry = Entry(id="1", title="Title", body="Body", created=datetime.now(), user_id="1", mood="&#128512")
        tags = ["tag1"]
        Diary.add_tags_to_entry(entry, tags)
        db.session.add(entry)
        db.session.commit()
        self.assertEqual(len(Tag.query.all()), 1)

    def test_multiple_tags_doesnt_exist_creates_new_tag_objects(self):
        entry = Entry(id="1", title="Title", body="Body", created=datetime.now(), user_id="1", mood="&#128512")
        tags = ["tag1", "tag2", "tag3"]
        Diary.add_tags_to_entry(entry, tags)
        db.session.add(entry)
        db.session.commit()
        self.assertEqual(len(Tag.query.all()), 3)

    def test_tag_already_exists_doesnt_create_duplicate(self):
        entry = DiaryTestAddTagsToEntry.create_fake_entry()
        tags = ["test"]
        Diary.add_tags_to_entry(entry, tags)
        db.session.add(entry)
        db.session.commit()
        self.assertEqual(len(Tag.query.all()), 1)


class DiaryTestReadSingleEntry(unittest.TestCase):

    def setUp(self) -> None:
        for entry_id in range(5):
            test_entry = Entry(id=str(entry_id), title="Title", body="Body", created=datetime.now(), user_id="1",
                               mood="&#128512")
            db.session.add(test_entry)
        db.session.commit()

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    def test_read_populated_db_one_key_returns_correct_dict(self):
        read_entry = Diary.read_single_entry({"entry_id": "1"}).get("entry")
        self.assertEqual(read_entry.id, "1")
        self.assertEqual(read_entry.title, "Title")
        self.assertEqual(read_entry.body, "Body")

    def test_read_populated_db_multiple_keys_returns_correct_dict(self):
        entry_ids = [str(entry_id) for entry_id in range(5)]
        for entry_id in entry_ids:
            self.assertEqual(Diary.read_single_entry({"entry_id": entry_id}).get("entry").id, entry_id)
            self.assertEqual(Diary.read_single_entry({"entry_id": entry_id}).get("entry").title, "Title")
            self.assertEqual(Diary.read_single_entry({"entry_id": entry_id}).get("entry").body, "Body")


class DiaryTestReadAllEntries(unittest.TestCase):

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    @staticmethod
    def populate_multiple_entries():
        for entry_id in range(5):
            test_entry = Entry(id=str(entry_id), title="Title", body="Body", created=datetime.now(), user_id="1",
                               mood="&#128512")
            db.session.add(test_entry)
        db.session.commit()

    @staticmethod
    def populate_single_entry():
        test_entry = Entry(id="1", title="Title", body="Body", created=datetime.now(), user_id="1", mood="&#128512")
        db.session.add(test_entry)
        db.session.commit()

    @staticmethod
    def populate_single_entry_with_tag():
        test_entry = Entry(id="1", title="Title", body="Body", created=datetime.now(), user_id="1", mood="&#128512")
        test_entry.tags.append(Tag(name="test"))
        db.session.add(test_entry)
        db.session.commit()

    def test_read_empty_dictionary_returns_empty(self):
        self.assertEqual(Diary.read_all_entries("1", None), {})

    def test_read_populated_db_one_key_returns_correct_dict(self):
        DiaryTestReadAllEntries.populate_single_entry()
        entries = Diary.read_all_entries("1", None)
        self.assertEqual(entries["1"].title, "Title")
        self.assertEqual(entries["1"].body, "Body")
        self.assertEqual(len(entries), 1)

    def test_read_populated_db_with_tag_returns_correct_dict(self):
        DiaryTestReadAllEntries.populate_single_entry_with_tag()
        entries = Diary.read_all_entries("1", tag_name="test")
        self.assertEqual(entries["1"].title, "Title")
        self.assertEqual(entries["1"].body, "Body")
        self.assertEqual(len(entries), 1)

    def test_read_populated_db_multiple_keys_returns_correct_dict(self):
        DiaryTestReadAllEntries.populate_multiple_entries()
        entries = Diary.read_all_entries("1", None)
        for entry_id in entries:
            self.assertEqual(entries[entry_id].title, "Title")
            self.assertEqual(entries[entry_id].body, "Body")
        self.assertEqual(len(entries), 5)

    def test_read_only_returns_entries_matching_user_id_param(self):
        test_entry = Entry(id="10", title="Title", body="Body", created=datetime.now(), user_id="2", mood="&#128512")
        db.session.add(test_entry)
        db.session.commit()
        DiaryTestReadAllEntries.populate_multiple_entries()
        entries = Diary.read_all_entries("1", None)
        self.assertEqual(len(entries), 5)


class DiaryTestUpdateEntry(unittest.TestCase):

    def setUp(self) -> None:
        for entry_id in range(5):
            test_entry = Entry(id=str(entry_id), title="Title", body="Body", created=datetime.now(), user_id="1",
                               mood="&#128512")
            db.session.add(test_entry)
        db.session.commit()

    def tearDown(self) -> None:
        db.drop_all()
        db.create_all()
        db.session.commit()

    def test_single_update_with_new_body_valid_entry_id_and_title_returns_updated_entry(self):
        Diary.update_entry({"entry_id": "1", "title": "value2", "body": "Hello Human!", "tags": ["tag1"],
                            "mood": "&#128512"})
        updated_entry = Entry.query.get("1")
        self.assertEqual(updated_entry.title, "value2")
        self.assertEqual(updated_entry.body, "Hello Human!")

    def test_multiple_update_to_same_entry_returns_updated_entry(self):
        for idx in range(10):
            new_title = "value" + str(idx)
            new_body = "Hello Human!" + str(idx)
            Diary.update_entry({"entry_id": "1", "title": new_title, "body": new_body, "tags": ["tag1"],
                                "mood": "&#128512"})
            updated_entry = Entry.query.get("1")
            self.assertEqual(updated_entry.title, new_title)
            self.assertEqual(updated_entry.body, new_body)

    def test_update_to_different_entries_returns_updated_entries(self):
        for entry_id in range(5):
            new_title = "value" + str(entry_id)
            new_body = "Hello Human!" + str(entry_id)
            Diary.update_entry({"entry_id": str(entry_id), "title": new_title, "body": new_body, "tags": ["tag1"],
                                "mood": "&#128512"})
            updated_entry = Entry.query.get(str(entry_id))
            self.assertEqual(updated_entry.title, new_title)
            self.assertEqual(updated_entry.body, new_body)


class DiaryTestDeleteEntry(unittest.TestCase):

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    @staticmethod
    def populate_multiple_entries():
        for entry_id in range(5):
            test_entry = Entry(id=str(entry_id), title="Title", body="Body", created=datetime.now(), user_id="1",
                               mood="&#128512")
            db.session.add(test_entry)
        db.session.commit()

    @staticmethod
    def populate_single_entry():
        test_entry = Entry(id="1", title="Title", body="Body", created=datetime.now(), user_id="1", mood="&#128512")
        db.session.add(test_entry)
        db.session.commit()

    def test_delete_empties_entries_when_only_one_entry(self):
        self.populate_single_entry()
        self.assertDictEqual(Diary.delete_entry({"entry_id": "1"}), {"entry_id": "1"})

        self.assertEqual(Diary.read_all_entries("1", None), {})

    def test_delete_with_two_existing_entries_only_deletes_specified_entry(self):
        self.populate_multiple_entries()

        for entry_id in range(5):
            self.assertEqual(Diary.delete_entry({"entry_id": entry_id}), {"entry_id": entry_id})

        self.assertEqual(Diary.read_all_entries("1", None), {})


class DiaryTestSearchEntries(unittest.TestCase):

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    @staticmethod
    def populate_multiple_entries():
        entry_list = [
            Entry(id="1", title="New Title", body="Hello World", created=datetime.now(), user_id="1", mood="&#128512"),
            Entry(id="2", title="A new day", body="class was so good", created=datetime.now(), user_id="1",
                  mood="&#128512"),
            Entry(id="3", title="A long Day", body="Today was monday", created=datetime.now(), user_id="1",
                  mood="&#128512")
        ]
        for test_entry in entry_list:
            db.session.add(test_entry)
        db.session.commit()

    def test_search_empty_dictionary_returns_empty(self):
        self.assertEqual(Diary.search_entries("hello", "1", None), {})

    def test_search_empty_query_returns_empty(self):
        self.assertEqual(Diary.search_entries(None, "1", None), {})

    def test_search_multiple_keyword_query_returns_correct_entries(self):
        DiaryTestSearchEntries.populate_multiple_entries()

        self.assertEqual(list(Diary.search_entries("new class", "1", None).keys()), ["2"])

        self.assertEqual(list(Diary.search_entries("long monday was", "1", None).keys()), ["3"])

    def test_search_multiple_entries_no_match_returns_empty(self):
        DiaryTestSearchEntries.populate_multiple_entries()

        self.assertEqual(Diary.search_entries("happy", "1", None), {})
        self.assertEqual(Diary.search_entries("dance", "1", None), {})
        self.assertEqual(Diary.search_entries("food", "1", None), {})

    def test_search_multiple_entries_match_returns_correct_entries(self):
        DiaryTestSearchEntries.populate_multiple_entries()

        self.assertEqual(set(Diary.search_entries("day", "1", None).keys()), {"2", "3"})

        self.assertEqual(set(Diary.search_entries("good", "1", None).keys()), {"2"})


class DiaryTestSortEntries(unittest.TestCase):

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    @staticmethod
    def populate_multiple_entries():
        entry_list = [
            Entry(id="1", title="New Title", body=" ", created=datetime(1, 1, 1), modified=datetime(1, 1, 1),
                  user_id="1", mood="&#128512"),
            Entry(id="2", title="A new day", body=" ", created=datetime(2, 2, 2), modified=datetime(3, 3, 3),
                  user_id="1", mood="&#128512"),
            Entry(id="3", title="A long Day", body=" ", created=datetime(3, 3, 3), modified=datetime(4, 4, 4),
                  user_id="1", mood="&#128512")
        ]
        for test_entry in entry_list:
            db.session.add(test_entry)
        db.session.commit()

    def test_sort_no_entries_returns_empty(self):
        test_entries = Entry.query.filter_by(user_id="1")

        sorted_entries = Diary.sort_entries(test_entries, "created_desc")
        self.assertEqual(sum(1 for _ in sorted_entries), 0)

    def test_sort_created_desc_returns_correct(self):
        DiaryTestSortEntries.populate_multiple_entries()
        test_entries = Entry.query.filter_by(user_id="1")

        sorted_entries = Diary.sort_entries(test_entries, "created_desc")

        entry_id = 3
        for entry in sorted_entries:
            self.assertEqual(int(entry.id), entry_id)
            entry_id = entry_id - 1

    def test_sort_created_asc_returns_correct(self):
        DiaryTestSortEntries.populate_multiple_entries()
        test_entries = Entry.query.filter_by(user_id="1")

        sorted_entries = Diary.sort_entries(test_entries, "created_asc")

        entry_id = 1
        for entry in sorted_entries:
            self.assertEqual(int(entry.id), entry_id)
            entry_id = entry_id + 1

    def test_sort_modified_desc_returns_correct(self):
        DiaryTestSortEntries.populate_multiple_entries()
        test_entries = Entry.query.filter_by(user_id="1")

        sorted_entries = Diary.sort_entries(test_entries, "modified_desc")

        entry_id = 3
        for entry in sorted_entries:
            self.assertEqual(int(entry.id), entry_id)
            entry_id = entry_id - 1

    def test_sort_modified_asc_returns_correct(self):
        DiaryTestSortEntries.populate_multiple_entries()
        test_entries = Entry.query.filter_by(user_id="1")

        sorted_entries = Diary.sort_entries(test_entries, "modified_asc")

        entry_id = 1
        for entry in sorted_entries:
            self.assertEqual(int(entry.id), entry_id)
            entry_id = entry_id + 1


if __name__ == '__main__':
    unittest.main()
