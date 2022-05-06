import os
from typing import Union

from flask import Flask, Markup, render_template, url_for, redirect, flash, abort, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug import Response

from personal_diary.diary import Diary
from personal_diary import db
from personal_diary.forms import CreateEntryForm, UpdateEntryForm, SignupForm, SearchEntryForm, LoginForm
from personal_diary.models import User, Entry
from personal_diary.diary_user import DiaryUser
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor


def create_app(db_name) -> Flask:
    """
    Creates the Flask application by setting up the database connection, user management, and page routes.

    Returns:
        app: Flask application to access the diary functions
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
    def load_user(user_id: str) -> str:
        """
        Determines what the currently logged-in user is.

        Returns:
            user_id: the id of the currently logged-in user
        """
        return User.query.get(user_id)

    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()

    @flask_app.route("/", methods=['GET'], defaults={'tag_name': None})
    @flask_app.route("/<tag_name>", methods=['GET', 'POST'])
    @login_required
    def read_entries(tag_name: str) -> str:
        """
        Renders the home page, which shows a list of the current entries or entries matching the user's search query.
        These entries can be sorted based on date.
        If a tag is specified, the entries will be further filtered by the tag name.
        The page also displays a reminder if no entry has been made for the current day.

        Args:
            tag_name: the name of a tag to filter entries by

        Returns:
            response: the HTML to display the home page showing the list of entries
        """
        sort_type = request.args.get('sort_type', default="created_desc")
        search_query = request.args.get('search', default="")

        if not Diary.check_entry_for_today(user_id=current_user.id):
            flash(Markup('You have no entry for today. <a href="/create" class="alert-link"> Create</a>'
                         ' a new entry to reflect on your day!'), 'alert-warning')

        return render_template("index.html",
                               entries=Diary.search_entries(search_query, current_user.id, tag_name, sort_type),
                               form=SearchEntryForm(),
                               search_query=search_query,
                               sort_type=sort_type,
                               tag_name=tag_name)

    @flask_app.route("/entry/<entry_id>", methods=['GET'])
    @login_required
    def read_single_entry(entry_id: str) -> str:
        """
        Renders the page showing the contents for a diary entry. This includes the title, body text, date modified,
        date created, selected mood, and any tags that were added.

        Args:
            entry_id: the id of the entry to display

        Returns:
            response: the HTML to display the page with the entry's contents
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
    @login_required
    def create_entry() -> Union[Response, str]:
        """
        Renders the page with a form for users to create an entry. This form allows users to input the title,
        body text, select a mood rating, and add tags. After creating the entry,
        it redirects back to the page to view that specific entry.

        Returns:
            response: the HTML for the page with the form or the redirect to the read_single_entry page upon
            submission of the form
        """
        create_form = CreateEntryForm()
        if create_form.validate_on_submit():
            input_tags = [create_form.tag1.data, create_form.tag2.data, create_form.tag3.data]
            nonempty_tags = [tag for tag in input_tags if tag]
            create_request = {
                "title": create_form.title.data,
                "body": create_form.body.data,
                "tags": nonempty_tags,
                "user_id": current_user.id,
                "mood": create_form.mood.data
            }

            Diary.create_entry(create_request)
            flash("Entry created!", "alert-success")
            return redirect(url_for("read_entries"))

        return render_template("create_entry.html", form=create_form)

    @flask_app.route("/edit/<entry_id>", methods=["GET", "POST"])
    @login_required
    def update_entry(entry_id: str) -> Union[Response, str]:
        """
        Renders the page with fields for a user to update the contents of an entry. This includes the title, body text,
        mood rating, or tags. After updating the entry, it redirects back to page to view that specific entry.

        Args:
            entry_id: the id of the entry to display and update

        Returns:
            response: the HTML for the page with the fields or the redirect to the read_single_entry page upon
            submission of the form
        """
        entry = Entry.query.get_or_404(entry_id)
        if entry.user_id != current_user.id:
            abort(404)

        update_form = UpdateEntryForm()
        if update_form.validate_on_submit():
            input_tags = [update_form.tag1.data, update_form.tag2.data, update_form.tag3.data]
            nonempty_tags = [tag for tag in input_tags if tag]
            update_request = {
                "entry_id": entry_id,
                "title": update_form.title.data,
                "body": update_form.body.data,
                "tags": nonempty_tags,
                "user_id": current_user.id,
                "mood": update_form.mood.data
            }

            Diary.update_entry(update_request)
            flash("Entry updated!", "alert-success")
            return redirect(url_for("read_single_entry", entry_id=entry.id))

        update_form.title.data = entry.title
        update_form.body.data = entry.body
        update_form.mood.data = entry.mood
        update_form.tag1.data = entry.tags[0].name if len(entry.tags) >= 1 else ""
        update_form.tag2.data = entry.tags[1].name if len(entry.tags) >= 2 else ""
        update_form.tag3.data = entry.tags[2].name if len(entry.tags) >= 3 else ""

        return render_template("update_entry.html", form=update_form, entry=entry)

    @flask_app.route("/delete/<entry_id>", methods=['GET'])
    @login_required
    def delete_entry(entry_id: str) -> Response:
        """
        Deletes the entry with the given entry_id. It redirects back to the
        home screen showing the list of existing entries.

        Args:
            entry_id: the id of the entry to delete

        Returns:
            response: the redirect back to the home page
        """
        entry = Entry.query.get_or_404(entry_id)
        if entry.user_id != current_user.id:
            abort(404)

        Diary.delete_entry({"entry_id": entry_id})
        flash("Entry deleted!", "alert-success")
        return redirect(url_for("read_entries"))

    @flask_app.route("/signup", methods=["GET", "POST"])
    def signup() -> Union[Response, str]:
        """
        Renders signup form allowing user to enter their username, full name, and password.
        If the username already exists, the user will be prompted to sign up again. Otherwise,
        they will be redirected to the login page with the new credentials.

        Returns:
            response: the HTML for the signup page or the redirect to the login page
        """
        signup_form = SignupForm()
        if signup_form.validate_on_submit():
            create_request = {
                "username": signup_form.username.data,
                "full_name": signup_form.full_name.data,
                "password": generate_password_hash(signup_form.password.data),
                "confirm_password": generate_password_hash(signup_form.confirm_password.data)
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
    def login() -> Union[Response, str]:
        """
        Renders login form allowing user to access their account and diary.
        If the username does not exist or the password does not match the record for the username,
        the user will be prompted to try again or create an account. Otherwise, they will be redirected to the home
        page for their account.

        Returns:
            response: the HTML for the page with the login form or the redirect to the home page
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

    @flask_app.route('/logout')
    @login_required
    def logout() -> Response:
        """
        Logs out the currently logged-in user and redirects back to the login page.

        Returns:
            response: the redirect back to the login page
        """
        logout_user()
        return redirect(url_for('login'))

    @flask_app.route("/delete-user", methods=['GET'])
    @login_required
    def delete_user() -> Response:
        """
        Deletes the user with the given user_id. It redirects back to the login screen after completion.

        Returns:
            response: the redirect back to the login page
        """
        DiaryUser.delete_user({"user": current_user})
        flash("User account deleted!", "alert-success")
        return redirect(url_for("login"))

    return flask_app


if __name__ == '__main__':
    app = create_app("database.db")
    app.run(debug=True, host="0.0.0.0", port=5001)
