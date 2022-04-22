from wsgiref.validate import validator
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from apurva_flask_app.model import User

class RegistrationForm(FlaskForm):
    role=SelectField("Role",choices=["basic","admin"])
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    firstName=StringField("FirstName",validators=[DataRequired(),Length(min =2, max=25)])
    lastName=StringField("LastName",validators=[DataRequired(),Length(min =2, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken.Please choose a different one.')
    
    def validate_email(self, email):

        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken.Please choose a different one.')


class LoginForm(FlaskForm):
    role=SelectField("Role",choices=["basic","admin"])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class addemployeeform(FlaskForm):
    employeeNumber=IntegerField('EmployeeNumber',validators=[DataRequired()])
    lastName=StringField('LastName',validators=[DataRequired(),Length(min =2, max=25)])
    firstName=StringField("FirstName",validators=[DataRequired(),Length(min =2, max=25)])
    extension=StringField('Extension',validators=[DataRequired(),Length(min =2, max=10)])
    email=StringField("Email",validators=[DataRequired(),Length(min =2, max=50),Email()])
    jobTitle=StringField("JobTitle",validators=[DataRequired(),Length(min =2, max=25)])
    submit=SubmitField('Addemployee')
