import json
from datetime import datetime
import uuid

from flask import jsonify

from personal_diary.models import Entry
from personal_diary import db


class Diary:
    """
    A class representing a personal diary, with entry information stored in "personal_diary/entry_local_storage.json"
    """

    @staticmethod
    def create_entry(request: dict) -> dict:
        """
        Adds entry specified by request parameter to database.

        Args:
         request: dictionary containing title, and body text
                  representing the entry to be added
        Returns:
             dictionary containing the entry_id of the new entry
        """
        new_entry_id = str(uuid.uuid4())
        curr_datetime = datetime.now()
        entry = Entry(id=new_entry_id,
                      title=request["title"],
                      body=request["body"],
                      created=curr_datetime,
                      modified=None,
                      folder=None)
        db.session.add(entry)
        db.session.commit()
        return {"entry_id": new_entry_id}

    @staticmethod
    def read_single_entry(request: dict) -> dict:
        """
        Reads single diary entry from the database.

        Args:
            request: a dictionary a single key, "entry_id" whose value is the id of the entry to be read
        Returns:
            a dictionary containing a key "entry" with of a value of type Entry. The Entry has information about the
            title, body, date_created, and time_created of the requested entry_id
        """
        entry = Entry.query.get_or_404(request["entry_id"])
        return {"entry": entry}

    @staticmethod
    def read_all_entries() -> dict:
        """
        Reads all entries currently stored in local database.

        Returns:
             dictionary containing all the stored entries, where each entry has an id, title, body, date, and time
        """
        all_entries = Entry.query.all()
        entry_dict = {}

        for entry in all_entries:
            entry_dict[entry.id] = entry

        return entry_dict

    @staticmethod
    def update_entry(request: dict) -> dict:
        """
        Updates the entry specified by request parameter. The user may update the body text or title
        of a given entry.

        Args:
            request: a dictionary containing title, body and id of the specific entry.

        Returns:
            a dictionary containing the updated entry
        """
        entry = Entry.query.get(request["entry_id"])
        entry_id = request["entry_id"]
        entry.body = request["body"]
        entry.title = request["title"]
        db.session.commit()
        return {entry_id: entry}

    @staticmethod
    def delete_entry(request: dict) -> dict:
        """
        Deletes the entry with the id specified by the request parameter.

        Args:
            request: a dictionary containing a key-value pair where the value is the id of the entry to delete

        Returns:
            dictionary containing the id of the entry that was deleted
        """
        entry_id = request.get("entry_id")
        deleted_entry = Entry.query.get(entry_id)
        db.session.delete(deleted_entry)
        db.session.commit()

        return {"entry_id": entry_id}

    # @staticmethod
    # def is_id_invalid(entry_id: int):
    #     """
    #     Checks whether an id matches an existing diary entry or not.
    #
    #     Args:
    #         entry_id: an int which represents the id of a diary entry
    #
    #     Returns:
    #          is_invalid: boolean representing if the id is invalid or not. The value is true if the id is invalid,
    #          meaning that it does not match an existing diary entry. The value is false if the id is valid, meaning that
    #          it does match an existing entry.
    #     """
    #     saved_entries = self.read_from_db()
    #     return str(entry_id) not in saved_entries.keys()
