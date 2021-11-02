from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    chain = SelectField('Chain ID', choices = [('1', 'Ethereum'), ('56', 'Binance Smart Chain'), ('137', 'Polygon'), ('1285', 'Moonriver'), ('42161', 'Arbitrum')], validators=[DataRequired()])
    submit = SubmitField('Submit')