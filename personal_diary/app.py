from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from personal_diary.diary import Diary
import os


db = SQLAlchemy()


def create_app():
    flask_app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()

    diary = Diary()

    @flask_app.route("/")
    def home_page():
        return render_template("base.html")

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
