from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    address = StringField('Username', validators=[DataRequired()])
    chain = SelectField('Chain ID', choices = [('1', 'Etheremum'), ('56', 'Binance Smart Chain')], validators=[DataRequired()])
    submit = SubmitField('Sign In')