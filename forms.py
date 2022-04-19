from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class collect(FlaskForm):
    department = StringField('Department:')
    course_number = IntegerField('Course number:')
    submit = SubmitField('Search')
    d_name = StringField('Department:')
    p_name = StringField('Professor:')

