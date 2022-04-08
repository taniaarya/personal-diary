import json
import os
from datetime import datetime


class Diary:
    """
    A class representing a personal diary, with entry information stored in "personal_diary/entry_local_storage.json"
    """

    def __init__(self):
        self.last_id = 0
        self.local_db_path = os.path.join(os.path.abspath('..'), "personal_diary/entry_local_storage.json")

    def read_from_db(self):
        """
        Reads all entries currently stored in local database.

        Returns:
             dictionary containing all the stored entries, where each entry has an id, title, body, date, and time
        """
        with open(self.local_db_path, "r") as stored_entries:
            return json.load(stored_entries)

    def write_to_db(self, entry_dict: dict) -> None:
        """
        Writes updated entry storage to local database.

        Args:
             entry_dict: dictionary containing all new entries where the key is the entry_id and the value is
                           a dictionary containing that entry's title, body, date, and time
        """
        with open(self.local_db_path, "w") as stored_entries:
            json.dump(entry_dict, stored_entries, indent=4)

    def create_entry(self, request: dict) -> dict:
        """
        Adds entry specified by request parameter to local database.

        Args:
         request: dictionary containing title, and body text
                  representing the entry to be added
        Returns:
             dictionary containing the entry_id of the new entry
        """
        if not request or "title" not in request or "body" not in request:
            return {"entry_id": 0}

        entry_id = self.last_id + 1
        self.last_id = entry_id
        curr_entries = self.read_from_db()
        curr_datetime = datetime.now()
        curr_entries[entry_id] = {
            "title": request["title"],
            "body": request["body"],
            "date_created": curr_datetime.strftime("%m/%d/%Y"),
            "time_created": curr_datetime.strftime("%H:%M"),
        }
        self.write_to_db(curr_entries)
        return {"entry_id": str(entry_id)}

    def read_entry(self) -> dict:
        """
        Reads all current diary entries from the database and pretty prints them.

        Returns:
             dictionary containing all diary entries, where each entry has an id, title, body, date, and time
        """
        return self.read_from_db()

    def update_entry(self, request: dict) -> dict:
        """
        Updates the entry specified by request parameter. The user may update the body text or title
        of a given entry.

        Args:
            request: a dictionary containing the information to update and the specific entry.
        Returns:
            a dictionary containing the updated entry
        """
        curr_entries = self.read_from_db()
        if len(request) == 0 or len(curr_entries) == 0 or request["entry_id"] not in curr_entries.keys():
            return {"entry_id": 0}

        entry_id = request["entry_id"]
        will_update_body = "body" in request
        will_update_text = "title" in request
        if will_update_text or will_update_body:
            # if the updated body or title of the entry is specified in the request, then
            # update the entry, otherwise leave value unchanged
            curr_entries[entry_id]["body"] = request["body"] if will_update_body \
                else curr_entries[entry_id]["body"]
            curr_entries[entry_id]["title"] = request["title"] if will_update_text \
                else curr_entries[entry_id]["title"]
            self.write_to_db(curr_entries)
        return {request["entry_id"]: curr_entries[entry_id]}

    def delete_entry(self, request: dict) -> dict:
        pass

    def is_id_invalid(self, entry_id: int):
        """
        Checks whether an id matches an existing diary entry or not.

        Args:
            entry_id: an int which represents the id of a diary entry

        Returns:
             is_invalid: boolean representing if the id is invalid or not. The value is true if the id is invalid,
             meaning that it does not match an existing diary entry. The value is false if the id is valid, meaning that
             it does match an existing entry.
        """
        saved_entries = self.read_from_db()
        return str(entry_id) not in saved_entries.keys()
