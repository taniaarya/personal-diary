import uuid
from personal_diary.models import User
from personal_diary import db


class DiaryUser:
    """
    A class containing helper functions related to creating, reading, updating, and deleting a diary user
    """

    @staticmethod
    def create_user(request: dict):
        """
        Adds user specified by request parameter to database.
        Args:
            request: dictionary containing username, full name, and password of new user
        Returns:
            dictionary containing the user id of the new entry
        """
        new_user_id = str(uuid.uuid4())
        new_user = User(id=new_user_id,
                        username=request["username"],
                        name=request["full_name"],
                        password=request["password"]
                        )
        db.session.add(new_user)
        db.session.commit()
        return {"user_id": new_user_id}

    @staticmethod
    def read_user():
        pass

    @staticmethod
    def update_user():
        pass

    @staticmethod
    def delete_user():
        pass
