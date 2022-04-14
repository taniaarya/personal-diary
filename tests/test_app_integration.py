import json
import unittest
from unittest import TestCase
from personal_diary import db
from personal_diary.app import create_app
from personal_diary.models import Entry
from personal_diary.diary import Diary


class ApplicationTestCaseEndToEnd(TestCase):
    def setUp(self) -> None:
        flask_app = create_app("test_database.db")
        flask_app.app_context().push()
        self.client = flask_app.test_client()

    def tearDown(self) -> None:
        db.session.query(Entry).delete()
        db.session.commit()

    def test_CRUD_operations_sequentially(self):
        response_list = []
        entry_ids = []
        valid_request_json = {"title": "Title", "body": "Body"}

        # test post endpoint
        for index in range(0, 50):
            response = self.client.post("/diary", json=valid_request_json)

            self.assertEqual(response.status_code, 200)

            entry_ids.append(json.loads(response.get_data())["entry_id"])
            response_list.append(response)

        # test get all endpoint
        response_get_all_start = self.client.get("/diary")
        self.assertEqual(response_get_all_start.status_code, 200)

        response_get_all_start_data = json.loads(response_get_all_start.get_data())
        self.assertEqual(len(response_get_all_start_data.keys()), 50)

        for entry_key, entry_val in response_get_all_start_data.items():
            self.assertEqual(entry_key in entry_ids, True)
            self.assertEqual(set(entry_val.keys()), {"title", "body", "date_created", "time_created"})
            self.assertEqual(response_get_all_start_data[entry_key]["title"], "Title")
            self.assertEqual(response_get_all_start_data[entry_key]["body"], "Body")

        for entry_id in entry_ids:
            # test get single entry endpoint
            response_get = self.client.get(f'/diary/{entry_id}')
            self.assertEqual(response_get.status_code, 200)

            response_get_data = json.loads(response_get.get_data())

            self.assertEqual(len(response_get_data.keys()), 4)

            # test put endpoint
            response_put = self.client.put("/diary", json={"entry_id": entry_id, "title": "NewTitle", "body": "Edited"})
            self.assertEqual(response_put.status_code, 200)

            response_put_data = json.loads(response_put.get_data())

            self.assertEqual(len(response_put_data.keys()), 1)
            self.assertEqual(list(response_put_data.keys())[0], entry_id)

            self.assertEqual(len(list(response_put_data.values())[0]), 4)
            self.assertEqual(response_put_data[entry_id]["title"], "NewTitle")
            self.assertEqual(response_put_data[entry_id]["body"], "Edited")

            # test delete endpoint
            response_delete = self.client.delete("/diary", json={"entry_id": entry_id})
            self.assertEqual(response_delete.status_code, 200)

            response_delete_data = json.loads(response_delete.get_data())
            self.assertEqual(response_delete_data["entry_id"], entry_id)

        response_get_all_end = self.client.get("/diary")
        self.assertEqual(response_get_all_end.status_code, 200)
        self.assertEqual(len(json.loads(response_get_all_end.get_data()).keys()), 0)


if __name__ == '__main__':
    unittest.main()
