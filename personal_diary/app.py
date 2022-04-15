import os
from flask import Flask, request, render_template
from personal_diary.diary import Diary
from personal_diary import db


def create_app(db_name):
    flask_app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, db_name)
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()

    @flask_app.route("/")
    def home_page():
        return render_template("base.html")

    @flask_app.route("/diary", methods=["GET"])
    def get_all_entries():
        """
        Renders the screen showing a list of the current entries.
        """
        curr_entries = Diary.read_all_entries()
        return render_template("index.html", curr_entries=curr_entries)

    @flask_app.route("/diary/<entry_id>", methods=["GET"])
    def get_entry(entry_id):
        return Diary.read_single_entry({"entry_id": entry_id})

    @flask_app.route("/create")
    def post_entry():
        return Diary.create_entry(request.get_json())

    @flask_app.route("/diary", methods=["PUT"])
    def put_entry():
        return Diary.update_entry(request.get_json())

    @flask_app.route("/diary", methods=["DELETE"])
    def delete_entry():
        return Diary.delete_entry(request.get_json())

    return flask_app


if __name__ == '__main__':
    app = create_app("database.db")
    app.run(debug=True)

