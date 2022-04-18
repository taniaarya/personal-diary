from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length


class CreateEntryForm(FlaskForm):
    title = StringField('Title',
                        validators=[InputRequired(), Length(min=1, max=80)],
                        render_kw={'class': 'col-md-10'}
                        )
    body = TextAreaField('Body',
                         validators=[InputRequired(), Length(min=1, max=300)],
                         render_kw={'class': 'col-md-10', 'rows': '10'}
                         )
    submit = SubmitField("Create Entry")


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
