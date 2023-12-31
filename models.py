"""Data models for Flask Cafe"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_DESCRIPTION="enter description here"
DEFAULT_IMAGE='https://images.unsplash.com/photo-1618794810603-4b384ce62737?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'


class City(db.Model):
    """Cities for cafes."""

    __tablename__ = 'cities'

    code = db.Column(
        db.Text,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    state = db.Column(
        db.String(2),
        nullable=False,
    )

    @classmethod
    def get_cities(self):
        """gets all instances of the class from the db"""
        city_choices = [
            (city.code, city.name) for city in City.query.all()
        ]

        return city_choices


class Cafe(db.Model):
    """Cafe information."""

    __tablename__ = 'cafes'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    url = db.Column(
        db.Text,
        nullable=False,
    )

    address = db.Column(
        db.Text,
        nullable=False,
    )

    city_code = db.Column(
        db.Text,
        db.ForeignKey('cities.code'),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/default-cafe.jpg",
    )

    city = db.relationship("City", backref='cafes')

    def __repr__(self):
        return f'<Cafe id={self.id} name="{self.name}">'

    def get_city_state(self):
        """Return 'city, state' for cafe."""

        city = self.city
        return f'{city.name}, {city.state}'


class User(db.Model):
    """user model"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
        nullable=False
    )

    username = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    email = db.Column(
        db.Text,
        nullable=False
    )

    first_name = db.Column(
        db.Text,
        nullable=False
    )

    last_name = db.Column(
        db.Text,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    image_url = db.Column(
        db.Text,
        default='/static/images/default-pic.png'
    )

    hashed_password = db.Column(
        db.Text,
        nullable=False
    )

    liked_cafes = db.relationship(
        'Cafe',
        secondary='likes',
        backref='liking_users'
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    #TODO: add a default description, image_url / add hashed pw
    @classmethod
    def register(
        cls,
        username,
        email,
        first_name,
        last_name,
        password,
        description=DEFAULT_DESCRIPTION,
        image_url=DEFAULT_IMAGE,
        admin=False
    ):
        """registers a new user and enters it into the db"""

        hashed_password = (
            bcrypt.generate_password_hash(password).decode('utf8')
        )

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            description=description,
            hashed_password = hashed_password,
            image_url=image_url,
            admin=admin
        )

        return user

        # db.session.add(user)
        # db.session.commit()

    @classmethod
    def authenticate(cls, username, password):
        """handles log-on form, authenticates user log-on"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = (
                bcrypt.check_password_hash(user.hashed_password, password)
            )
            if is_auth:
                return user

        return False


class Liked(db.Model):
    '''liked cafes'''

    __tablename__ = 'likes'

    cafe_liked = db.Column(
        db.Integer,
        db.ForeignKey('cafes.id', ondelete='cascade'),
        primary_key=True
    )

    user_liking = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        primary_key=True
    )




def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    app.app_context().push()
    db.app = app
    db.init_app(app)
