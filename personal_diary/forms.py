from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
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
