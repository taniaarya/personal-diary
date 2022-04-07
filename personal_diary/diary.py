import json
import os


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

        :return: dictionary containing all the stored entries, where each entry has an
        id, title, body, date, and time
        """
        with open(self.local_db_path, "r") as stored_entries:
            return json.load(stored_entries)

    def write_to_db(self, entry_dict: dict) -> None:
        """
        Writes updated entry storage to local database.

        :param: entry_dict: dictionary containing all new entries where the key is the entry_id and the value is
                           a dictionary containing that entry's title, body, date, and time
        """
        with open(self.local_db_path, "w") as stored_entries:
            json.dump(entry_dict, stored_entries, indent=4)

    def create_entry(self, request: dict) -> dict:
        pass

    def remove_entry(self, request: dict) -> dict:
        pass

    def update_entry(self, request: dict) -> dict:
        pass

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
