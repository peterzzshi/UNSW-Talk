from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, DateField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from app.models import Student


class LoginForm(FlaskForm):
    email = EmailField('Email address', [DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    zid = StringField('Zid', validators=[DataRequired()])
    email = EmailField('Email address', validators=[DataRequired(), Email()])

    full_name = StringField('Full Name', validators=[DataRequired()])
    birthday = DateField("birthday", validators=[DataRequired()])
    # image = StringField('image', validators=[])

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    def validate_zid(self, zid):
        student = Student.get_by_id(zid)
        if student is not None:
            raise ValidationError('Please use a different Zid.')


    def validate_email(self, email):
        student = Student.get_by_email(email)
        if student is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    full_name = StringField('Full name', validators=[DataRequired()])
    # program = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')