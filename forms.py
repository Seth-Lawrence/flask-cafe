"""Forms for Flask Cafe."""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField, URLField, SelectField
from wtforms.validators import InputRequired, Email, Length, URL, Optional
from models import City, connect_db, db


class AddOrEditCafe(FlaskForm):
    """form for adding or editing cafe"""

    name = StringField(
        'name',
        validators=[InputRequired()]
    )

    description = StringField(
        'description',
        validators=[Optional()]
    )

    url = URLField(
        'url',
        validators=[Optional(), URL()]
    )

    address = StringField(
        'adddress',
        validators=[InputRequired()]
    )

    city_code = SelectField(
        'city code',)

    image_url = URLField(
        'image',
        validators=[URL(), Optional()]
    )


class SignupForm(FlaskForm):
    """form to sign up"""

    username = StringField(
        'username',
        validators=[InputRequired()]
    )

    first_name = StringField(
        'first name',
        validators=[InputRequired()]
    )

    last_name = StringField(
        'last name',
        validators=[InputRequired()]
    )

    description = TextAreaField(
        'description',
        validators=[Optional()]
    )

    email = StringField(
        'email',
        validators=[InputRequired(), Email()]
    )

    password = StringField(
        'password',
        validators=[InputRequired(), Length(min=6)]
    )

    image_url = StringField(
        'image',
        validators=[Optional(), URL()]
    )


class LoginForm(FlaskForm):
    """form for handling login"""

    username = StringField(
        'username',
        validators=[InputRequired()]
    )

    password = StringField(
        'password',
        validators=[InputRequired()]
    )

class CSRFProtectionForm(FlaskForm):
    """csrf protection when no form fields"""
    ...
