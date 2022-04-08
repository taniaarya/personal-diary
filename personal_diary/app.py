from flask import Flask, request
from personal_diary.diary import Diary


def create_app():
    flask_app = Flask(__name__)

    diary = Diary()

    @flask_app.route("/diary", methods=["GET"])
    def get_all_entries():
        return diary.read_from_db()

    @flask_app.route("/diary/<entry_id>", methods=["GET"])
    def get_entry(entry_id):
        return diary.read_entry({"entry_id": entry_id})

    @flask_app.route("/diary", methods=["POST"])
    def post_entry():
        return diary.create_entry(request.get_json())

    @flask_app.route("/diary", methods=["PUT"])
    def put_entry():
        return diary.update_entry(request.get_json())

    @flask_app.route("/diary", methods=["DELETE"])
    def delete_entry():
        return diary.delete_entry(request.get_json())

    return flask_app
