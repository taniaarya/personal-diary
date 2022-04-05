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
