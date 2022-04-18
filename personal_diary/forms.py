from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SearchField
from wtforms.validators import InputRequired, Length
from flask_ckeditor import CKEditorField


class CreateEntryForm(FlaskForm):
    title = StringField('Title',
                        validators=[InputRequired(), Length(min=1, max=300)],
                        render_kw={'class': 'col-md-10'}
                        )
    body = CKEditorField('Body',
                         validators=[InputRequired(), Length(min=1, max=300)],
                         render_kw={'class': 'col-md-10', 'rows': '10'}
                         )
    submit = SubmitField("Create Entry")


class SearchEntryForm(FlaskForm):
    search = SearchField('')
    submit = SubmitField("Search")


class UpdateEntryForm(FlaskForm):
    title = StringField('Title',
                        validators=[InputRequired(), Length(min=1, max=300)],
                        render_kw={'class': 'col-md-10'}
                        )
    body = CKEditorField('Body',
                         validators=[InputRequired(), Length(min=1, max=300)],
                         render_kw={'class': 'col-md-10', 'rows': '10'}
                         )
    submit = SubmitField("Save Changes")


class SignupForm(FlaskForm):
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
