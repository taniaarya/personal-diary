import os
from flask import Flask, request, render_template, url_for, redirect, flash
from personal_diary.diary import Diary
from personal_diary import db
from personal_diary.forms import CreateEntryForm, SignupForm
from personal_diary.models import User
from personal_diary.diary_user import DiaryUser
from werkzeug.security import generate_password_hash, check_password_hash


def create_app(db_name):
    flask_app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, db_name)
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SECRET_KEY'] = 'super secret key'

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

    @flask_app.route("/create", methods=['GET', 'POST'])
    def create_entry():
        create_form = CreateEntryForm()
        if create_form.validate_on_submit():
            create_request = {
                "title": create_form.title.data,
                "body": create_form.body.data
            }
            Diary.create_entry(create_request)
            return redirect(url_for("get_all_entries"))

        return render_template(
            "create.html",
            form=create_form,
        )

    @flask_app.route("/diary", methods=["PUT"])
    def put_entry():
        return Diary.update_entry(request.get_json())

    @flask_app.route("/diary", methods=["DELETE"])
    def delete_entry():
        return Diary.delete_entry(request.get_json())

    @flask_app.route("/signup", methods=["GET", "POST"])
    def signup():
        """
        Renders signup form allowing user to enter their username, full name, and password.
        If the username already exists, the user will be prompted to sign up again, otherwise
        they will be redirected to the login page with the new credentials.
        """
        signup_form = SignupForm()
        if signup_form.validate_on_submit():
            create_request = {
                "username": signup_form.username.data,
                "full_name": signup_form.full_name.data,
                "password": generate_password_hash(signup_form.username.data)
            }
            # verify username does not already exist
            if User.query.filter_by(username=create_request["username"]).first():
                flash("Username already exists", 'error')
                return redirect(url_for('signup'))

            DiaryUser.create_user(create_request)
            flash("Signup success!", "info")
            return redirect(url_for("login"))

        return render_template("signup.html", form=signup_form)

    @flask_app.route("/login", methods=["GET", "POST"])
    def login():
        return render_template("login.html")

    return flask_app


if __name__ == '__main__':
    app = create_app("database.db")
    app.run(debug=True)

