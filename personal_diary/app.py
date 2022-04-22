import os
from flask import Flask, Markup, render_template, url_for, redirect, flash, abort
from flask_login import LoginManager, login_user, current_user
from personal_diary.diary import Diary
from personal_diary import db
from personal_diary.forms import CreateEntryForm, UpdateEntryForm, SignupForm, SearchEntryForm, LoginForm
from personal_diary.models import User, Entry
from personal_diary.diary_user import DiaryUser
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor


def create_app(db_name):
    """
    Creates the Flask application by setting up the database connection, user management, and page routes.
    """

    flask_app = Flask(__name__)
    CKEditor(flask_app)

    basedir = os.path.abspath(os.path.dirname(__file__))

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, db_name)
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SECRET_KEY'] = 'super secret key'

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(flask_app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(user_id)

    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()

    @flask_app.route("/", methods=['GET', 'POST'])
    def read_entries():
        """
        Renders the page showing a list of the current entries or entries matching the user's search query.
        """
        search_form = SearchEntryForm()
        if search_form.validate_on_submit():
            search_query = search_form.data["search"]
            return render_template("index.html",
                                   entries=Diary.search_entries(search_query, current_user.id),
                                   form=search_form)

        all_entries = Diary.read_all_entries(current_user.id)
        return render_template("index.html", entries=all_entries, form=search_form)

    @flask_app.route("/entry/<entry_id>", methods=['GET'])
    def read_single_entry(entry_id: str):
        """
        Renders the page showing the title and body for a diary entry.

        Args:
            entry_id: the id of the entry to display
        """
        read_request = {
            "entry_id": entry_id,
            "user_id": current_user.id
        }
        entry = Diary.read_single_entry(read_request)["entry"]
        if entry.user_id != current_user.id:
            abort(404)

        return render_template("read_single_entry.html", entry=entry)

    @flask_app.route("/create", methods=['GET', 'POST'])
    def create_entry():
        """
        Renders the page with a form for users to input the title and body for an entry.
        """
        create_form = CreateEntryForm()
        if create_form.validate_on_submit():
            create_request = {
                "title": create_form.title.data,
                "body": create_form.body.data,
                "user_id": current_user.id
            }
            Diary.create_entry(create_request)
            return redirect(url_for("read_entries"))

        return render_template("create_entry.html", form=create_form)

    @flask_app.route("/edit/<entry_id>", methods=["GET", "POST"])
    def update_entry(entry_id: str):
        """
        Renders the page with fields for a user to update the title and body text of an entry. After updating
        the entry, it redirects back to the home page showing the list of existing entries.

        Args:
            entry_id: the id of the entry to display and update
        """
        entry = Entry.query.get_or_404(entry_id)
        if entry.user_id != current_user.id:
            abort(404)

        update_form = UpdateEntryForm()
        if update_form.validate_on_submit():
            update_request = {
                "entry_id": entry_id,
                "title": update_form.title.data,
                "body": update_form.body.data,
                "user_id": current_user.id
            }
            Diary.update_entry(update_request)
            return redirect(url_for("read_entries"))

        update_form.title.data = entry.title
        update_form.body.data = entry.body

        return render_template("update_entry.html", form=update_form, entry=entry)

    @flask_app.route("/delete/<entry_id>", methods=['GET'])
    def delete_entry(entry_id: str):
        """
        Deletes the entry with the given entry_id. It redirects back to the
        home screen showing the list of existing entries.

        Args:
            entry_id: the id of the entry to delete
        """
        entry = Entry.query.get_or_404(entry_id)
        if entry.user_id != current_user.id:
            abort(404)

        Diary.delete_entry({"entry_id": entry_id})
        flash("Entry deleted!", "alert-success")
        return redirect(url_for("read_entries"))

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
                "password": generate_password_hash(signup_form.password.data)
            }
            # verify username does not already exist
            if User.query.filter_by(username=create_request["username"]).first():
                flash("Username already exists", 'alert-danger')
                return redirect(url_for('signup'))

            DiaryUser.create_user(create_request)
            flash("Signup success!", "alert-success")
            return redirect(url_for("login"))

        return render_template("signup.html", form=signup_form)

    @flask_app.route("/login", methods=["GET", "POST"])
    def login():
        """
        Renders login form allowing user to access their account and diary.
        If the username does not exist or the password does not match the record for the username,
        the user will be prompted to try again or create an account, otherwise
        they will be redirected to the home page for their account.
        """
        login_form = LoginForm()
        if login_form.validate_on_submit():
            get_request = {
                "username": login_form.username.data,
                "password": login_form.password.data
            }

            user = User.query.filter_by(username=get_request["username"]).first()

            # verify username exists and password is correct
            if not user or not check_password_hash(user.password, get_request["password"]):
                flash(Markup('Your credentials could not be verified, please try again. Or, if you do not currently '
                             'have an account, please <a href="/signup" class="alert-link">sign up for an '
                             'account.</a>'), "alert-danger")
                return redirect(url_for('login'))

            # if success display success message and redirect to home page
            flash("Login success!", "alert-success")
            login_user(user)
            return redirect(url_for("read_entries"))

        return render_template("login.html", form=login_form)

    return flask_app


if __name__ == '__main__':
    app = create_app("database.db")
    app.run(debug=True, host="0.0.0.0", port=5001)
