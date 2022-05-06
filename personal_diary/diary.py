from datetime import datetime
import uuid
from personal_diary.models import Entry, Tag
from sqlalchemy import desc, asc
from personal_diary import db
from typing import Iterable


class Diary:
    """
    A class representing a personal diary. The diary contains Entry objects which are defined in models.py.
    """

    @staticmethod
    def create_entry(request: dict) -> dict:
        """
        Adds entry specified by request parameter to database.

        Args:
            request: dictionary containing title, and body text
                  representing the entry to be added, as well as the user id of
                  the user the entry is for

        Returns:
             dictionary containing the entry_id of the new entry
        """
        new_entry_id = str(uuid.uuid4())
        curr_datetime = datetime.now()
        entry = Entry(id=new_entry_id,
                      title=request["title"],
                      body=request["body"],
                      created=curr_datetime,
                      modified=curr_datetime,
                      user_id=request["user_id"],
                      mood=request["mood"])
        Diary.add_tags_to_entry(entry, request["tags"])
        db.session.add(entry)
        db.session.commit()
        return {"entry_id": new_entry_id}

    @staticmethod
    def add_tags_to_entry(entry: Entry, tags: list) -> None:
        """
        Attaches tags to the given entry.

        Args:
            entry: an Entry object which the tags will be attached to
            tags: a list of tags to attach to the entry parameter in the form ["tag1", "tag2", "tag3"]
        """
        entry.tags = []
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            entry.tags.append(tag)

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
    def read_all_entries(user_id: str, tag_name: str, sort_by: str = "created_desc") -> dict:
        """
        Reads all entries currently stored in local database.

        Args:
            user_id: string representing the id of the user the entry belongs to
            tag_name: name of entry tag to filter by
            sort_by: string indicating how entries should be sorted by

        Returns:
             dictionary containing all the stored entries, where each entry has an id, title, body, date, and time
        """
        all_entries = Entry.query.filter_by(user_id=user_id)
        if tag_name:
            all_entries = all_entries.join(Entry.tags).filter(Tag.name == tag_name).all()

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
        entry.mood = request["mood"]
        entry.modified = datetime.now()
        Diary.add_tags_to_entry(entry, request["tags"])
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
    def search_entries(search_query: str, user_id: str, tag_name: str, sort_by: str = "created_desc") -> dict:
        """
        Returns entries that contain the keywords in the search query. The search is not case-sensitive.
        An entry matches the search query if it contains all keywords in its title or body text.

        Args:
            search_query: a string containing keywords to search for in the query. For example, a string of
            "apple pear" has two keywords of "apple" and "pear".
            user_id: string representing the id of the user the entry belongs to
            tag_name: name of entry tag to filter by
            sort_by: string representing how entries should be sorted by

        Returns:
            dictionary containing the entries that match the search query
        """
        if search_query is None:
            return Diary.read_all_entries(user_id, tag_name)

        matching_entries = Entry.query.filter_by(user_id=user_id)
        matching_entries = Diary.sort_entries(matching_entries, sort_by)

        for keyword in search_query.split(' '):
            matching_entries = matching_entries.filter(Entry.title.ilike("%" + keyword + "%") |
                                                       Entry.body.ilike("%" + keyword + "%"))

        if tag_name:
            matching_entries = matching_entries.join(Entry.tags).filter(Tag.name == tag_name).all()

        entry_dict = {}
        for entry in matching_entries:
            entry_dict[entry.id] = entry

        return entry_dict

    @staticmethod
    def sort_entries(entries: Entry, sort_type: str) -> Iterable:
        """
        Sorts a collection of entries based on either date created or date modified.

        Args:
            entries: an Entry object that is used to do the sorting on
            sort_type: a string indicating the type of sort to do. The sorting can be based on the date modified
            or date created time, ascending or descending.

        Returns:
            an iterable collection of sorted entries
        """
        if sort_type == "created_asc":
            return entries.order_by(asc(Entry.created))
        elif sort_type == "modified_asc":
            return entries.order_by(asc(Entry.modified))
        elif sort_type == "modified_desc":
            return entries.order_by(desc(Entry.modified))
        else:
            return entries.order_by(desc(Entry.created))
