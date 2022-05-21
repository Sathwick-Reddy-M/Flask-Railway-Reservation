from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, PasswordField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from datetime import date


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Length(min=3)])
    pwd = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Length(min=3)])
    pwd = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('SignUp')


class TrainSearchForm(FlaskForm):
    start = StringField('From', validators=[DataRequired(), Length(min=2)])
    destination = StringField('To', validators=[DataRequired(), Length(min=2)])
    searchdate = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Search')

    def validate_destination(self, destination):
        if (self.start.data == destination.data):
            raise ValidationError('Start and Destination cannot be same')

    def validate_searchdate(self, searchdate):
        if (self.searchdate.data < date.today()):
            raise ValidationError('Choose a valid date')
