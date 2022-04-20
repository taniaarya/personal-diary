from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SearchField
from wtforms.validators import InputRequired, Length
from flask_ckeditor import CKEditorField


class CreateEntryForm(FlaskForm):
    """
    Form used for user to add a new entry to the diary by inputting a title and body.
    The title may only be at most 80 characters long, and the body may only be 300 characters long.
    """
    title = StringField('Title',
                        validators=[InputRequired(), Length(min=1, max=80)],
                        render_kw={'class': 'col-md-10'}
                        )
    body = CKEditorField('Body',
                         validators=[InputRequired(), Length(min=1, max=300)],
                         render_kw={'class': 'col-md-10', 'rows': '10'}
                         )
    submit = SubmitField("Create Entry")


class SearchEntryForm(FlaskForm):
    """
    Search field to allow user to input keywords used to filter entries.
    """
    search = SearchField('')
    submit = SubmitField("Search")


class UpdateEntryForm(FlaskForm):
    """
    Form used for user to update an existing entry in the diary by editing a title and body.
    The title may only be at most 80 characters long, and the body may only be 300 characters long.
    """
    title = StringField('Title',
                        validators=[InputRequired(), Length(min=1, max=80)],
                        render_kw={'class': 'col-md-10'}
                        )
    body = CKEditorField('Body',
                         validators=[InputRequired(), Length(min=1, max=300)],
                         render_kw={'class': 'col-md-10', 'rows': '10'}
                         )
    submit = SubmitField("Save Changes")


class SignupForm(FlaskForm):
    """
    Form used for user to register a new User account.
    The user must input a unique username (max 15 characters), full name (max 30 characters),
    and a password (8-15 characters).
    """
    username = StringField('Username',
                           validators=[InputRequired(), Length(min=1, max=15)],
                           )
    full_name = StringField('Full Name',
                            validators=[InputRequired(), Length(min=1, max=30)],
                            )
    password = PasswordField('Password (8-15 Characters)',
                             validators=[InputRequired(), Length(min=8, max=15)]
                             )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    """
    Form used for user to log into diary application.
    A user must enter a username and password.
    """
    username = StringField('Username',
                           validators=[InputRequired(), Length(min=1, max=15)],
                           )
    password = PasswordField('Password (8-15 Characters)',
                             validators=[InputRequired()]
                             )
    login = SubmitField("Login")
