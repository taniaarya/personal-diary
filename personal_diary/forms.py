from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, SubmitField, PasswordField, SearchField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, Optional
from flask_ckeditor import CKEditorField


class CreateEntryForm(FlaskForm):
    """
    Form used for user to add a new entry to the diary by inputting a title and body.
    The title may only be at most 80 characters long, and the body may only be 300 characters long.
    """
    title = StringField('Title*',
                        validators=[DataRequired(), Length(min=1, max=80)],
                        render_kw={'class': 'col-md-10', 'placeholder': 'Enter title...'}
                        )
    body = CKEditorField('Body*',
                         validators=[DataRequired(), Length(min=1, max=300)],
                         render_kw={'class': 'col-md-10', 'rows': '10'}
                         )
    tag1 = StringField("Tag 1", validators=[Optional(), Length(min=1, max=20)],
                       render_kw={'class': 'col-md-1', 'placeholder': 'Tag 1'})
    tag2 = StringField("Tag 2", validators=[Optional(), Length(min=1, max=20)],
                       render_kw={'class': 'col-md-1', 'placeholder': 'Tag 2'})
    tag3 = StringField("Tag 3", validators=[Optional(), Length(min=1, max=20)],
                       render_kw={'class': 'col-md-1', 'placeholder': 'Tag 3'})
    mood = RadioField('Mood', choices=[('&#128528', Markup('&#128528')),
                                       ('&#128512', Markup('&#128512')),
                                       ('&#128525', Markup('&#128525')),
                                       ('&#128541', Markup('&#128541')),
                                       ('&#128532', Markup('&#128532')),
                                       ('&#129314', Markup('&#129314')),
                                       ('&#128552', Markup('&#128552')),
                                       ('&#128545', Markup('&#128545'))], default="&#128528")
    submit = SubmitField("Create Entry", render_kw={'class': 'rounded-pill btn btn-dark float-end ml-2'})


class SearchEntryForm(FlaskForm):
    """
    Search field to allow user to input keywords used to filter entries.
    """
    search = SearchField('', render_kw={'class': 'w-50 search-btn me-2', 'placeholder': 'Search for an entry...'})
    submit = SubmitField("Search", render_kw={'class': 'btn btn-dark rounded-pill'})


class UpdateEntryForm(FlaskForm):
    """
    Form used for user to update an existing entry in the diary by editing a title and body.
    The title may only be at most 80 characters long, and the body may only be 300 characters long.
    """
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=1, max=80)],
                        render_kw={'class': 'col-md-10'}
                        )
    body = CKEditorField('Body',
                         validators=[DataRequired(), Length(min=1, max=300)],
                         render_kw={'class': 'col-md-10', 'rows': '10'}
                         )

    mood = RadioField('Mood', choices=[('&#128528', Markup('&#128528')),
                                       ('&#128512', Markup('&#128512')),
                                       ('&#128525', Markup('&#128525')),
                                       ('&#128541', Markup('&#128541')),
                                       ('&#128532', Markup('&#128532')),
                                       ('&#129314', Markup('&#129314')),
                                       ('&#128552', Markup('&#128552')),
                                       ('&#128545', Markup('&#128545'))], default="&#128528")

    tag1 = StringField("Tag 1", render_kw={'class': 'col-md-2', 'placeholder': 'Tag 1'})
    tag2 = StringField("Tag 2", render_kw={'class': 'col-md-2', 'placeholder': 'Tag 2'})
    tag3 = StringField("Tag 3", render_kw={'class': 'col-md-2', 'placeholder': 'Tag 3'})

    submit = SubmitField("Save Changes", render_kw={'class': 'rounded-pill btn btn-dark float-end ml-2'})


class SignupForm(FlaskForm):
    """
    Form used for user to register a new User account.
    The user must input a unique username (max 15 characters), full name (max 30 characters),
    and a password (8-15 characters). They must also confirm their password by inputting it again and ensuring the
    input matches.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=15)],
                           render_kw={'class': 'text-start', 'size': "30"}
                           )
    full_name = StringField('Full Name',
                            validators=[DataRequired(), Length(min=1, max=30)],
                            render_kw={'class': 'text-start', 'size': "30"}
                            )
    password = PasswordField('Password (8-15 Characters)',
                             validators=[DataRequired(), Length(min=8, max=15)],
                             render_kw={'class': 'text-start', 'size': "30"}
                             )
    # Verify that passwords match
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                         DataRequired(),
                                         Length(min=8, max=15),
                                         EqualTo("password", message="Passwords must match!")
                                     ],
                                     render_kw={'class': 'text-start', 'size': "30"}
                                     )
    submit = SubmitField("Sign Up", render_kw={'class': 'rounded-pill btn btn-dark mt-3 login-btn mx-auto text-center'})


class LoginForm(FlaskForm):
    """
    Form used for user to log into diary application.
    A user must enter a username and password.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=15)],
                           render_kw={'class': 'text-start', 'size': "30"}
                           )
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw={'class': 'text-start', 'size': "30"}
                             )
    login = SubmitField("Login", render_kw={'class': 'rounded-pill btn btn-dark mt-3 login-btn mx-auto text-center'})
