"""Flask App for Flask Cafe."""

import os

from flask import Flask, render_template, redirect, url_for, flash, session, g

from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, Cafe, db, City, User
from forms import AddOrEditCafe, SignupForm, LoginForm, CSRFProtectionForm


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_cafe')
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "shhhh")
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


#######################################
# homepage

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# cafes


@app.get('/cafes')
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )


@app.get('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )


@app.route('/cafes/add', methods=["GET", "POST"])
def show_or_add_cafe():
    """shows form for cafe or handles submit"""

    form = AddOrEditCafe()
    form.city_code.choices = City.get_cities()
    # breakpoint()

    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            description=form.description.data,
            url=form.url.data,
            address=form.address.data,
            city_code=form.city_code.data,
            image_url=form.image_url.data
        )

        db.session.add(new_cafe)
        db.session.commit()

        redirect_url = url_for('cafe_list')
        flash(f"{new_cafe.name} added", 'success')

        return redirect(redirect_url)

    else:

        return render_template(
            'cafe/add-form.html',
            form=form
        )


@app.route('/cafes/<int:cafe_id>/edit', methods=['GET', 'POST'])
def edit_cafe(cafe_id):
    """handles form for editing a specific cafe"""

    cafe = Cafe.query.get_or_404(cafe_id)
    city_selections = City.get_cities()

    form = AddOrEditCafe(obj=cafe)
    form.city_code.choices = city_selections

    if form.validate_on_submit():
        form.populate_obj(cafe)

        db.session.add(cafe)
        db.session.commit()

        flash(f"{cafe.name} edited", 'success')

        return redirect(url_for('cafe_list'))

    else:
        return render_template(
            'cafe/edit-form.html',
            cafe_id=cafe_id,
            form=form,
            cafe=cafe
        )


######     USER ROUTES      #######################################################
################################################################################


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """handles signing up a new user or shows user form"""

    form = SignupForm()

    if form.validate_on_submit():

        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        description = form.description.data
        email = form.email.data
        password = form.password.data
        image_url = form.image_url.data

        User.register(
            username,
            first_name,
            last_name,
            description,
            email,
            password,
            image_url
        )

        flash("You are signed up and logged in")
        return redirect(url_for('cafe_list'))

    else:

        return render_template('auth/signup-form.html',form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """handles login form"""

    form = LoginForm()

    if form.validate_on_submit():
        if User.authenticate(form.username.data, form.password.data):
            do_login(form.username.data)
            flash(f"Hello {form.username.data}")
            return redirect(url_for('cafe_list'))
        else:
            flash('invalid login')

    return render_template('auth/login-form.html',form=form)


app.post('/logout')
def logout():
    """handles logout"""

    form = CSRFProtectionForm()

    if form.validate_on_submit():
        do_logout()
        flash('You should have successfully logged out')
        return redirect(url_for('homepage'))









