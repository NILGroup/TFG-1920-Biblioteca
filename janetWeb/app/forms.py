from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired
#Temporal para comprobar conectividad
class CreateForm(FlaskForm):
    message = TextField('message', validators=[DataRequired()])
