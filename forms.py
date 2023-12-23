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
        'city code', coerce=int
    )

    image_url = URLField(
        'image',
        validators=[URL(), Optional()]
    )
