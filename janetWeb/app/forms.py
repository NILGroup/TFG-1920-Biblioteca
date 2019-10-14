from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired

class CreateForm(FlaskForm):
    message = TextField('message', validators=[DataRequired()])
