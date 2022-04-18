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

    @staticmethod
    def search_entries(search_query: str) -> dict:
        """
        Returns entries that contain the keywords in the search query. The search is not case-sensitive.
        An entry matches the search query if it contains all keywords in its title or body text.

        Args:
            search_query: a string containing keywords to search for in the query. For example, a string of
            "apple pear" has two keywords of "apple" and "pear".

        Returns:
            dictionary containing the entries that match the search query
        """
        matching_entries = Entry.query.filter()
        for keyword in search_query.split(' '):
            matching_entries = matching_entries.filter(Entry.title.ilike("%" + keyword + "%") |
                                                       Entry.body.ilike("%" + keyword + "%"))

        entry_dict = {}
        for entry in matching_entries:
            entry_dict[entry.id] = entry

        return entry_dict
