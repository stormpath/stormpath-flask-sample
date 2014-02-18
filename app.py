"""
    app.py
    ~~~~~~

    This simple sample application provides a bare-bones website that allows
    you to:

    - Create new user accounts.
    - Log into existing user accounts.
    - View a simple dashboard page that displays user information.
    - Edit your user information on said dashboard page.
    - Log out of the website.

    Please see the README for more information of how to run and use this
    sample application.
"""


from os import environ

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)

from flask.ext.stormpath import (
    StormpathManager,
    User,
    login_required,
    login_user,
    logout_user,
    user,
)

from stormpath.error import Error as StormpathError


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ilovecookies'
app.config['STORMPATH_API_KEY_ID'] = environ.get('STORMPATH_API_KEY_ID')
app.config['STORMPATH_API_KEY_SECRET'] = environ.get('STORMPATH_API_KEY_SECRET')
app.config['STORMPATH_APPLICATION'] = environ.get('STORMPATH_APPLICATION')

stormpath_manager = StormpathManager(app)
stormpath_manager.login_view = '.login'


##### Website
@app.route('/')
def index():
    """Basic home page."""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This view allows a user to register for the site.

    This will create a new User in Stormpath, and then log the user into their
    new account immediately (no email verification required).
    """
    if request.method == 'GET':
        return render_template('register.html')

    try:
        # Create a new Stormpath User.
        _user = stormpath_manager.application.accounts.create({
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'given_name': 'John',
            'surname': 'Doe',
        })
        _user.__class__ = User
    except StormpathError, err:
        # If something fails, we'll display a user-friendly error message.
        return render_template('register.html', error=err.message)

    login_user(_user, remember=True)
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This view logs in a user given an email address and password.

    This works by querying Stormpath with the user's credentials, and either
    getting back the User object itself, or an exception (in which case well
    tell the user their credentials are invalid).

    If the user is valid, we'll log them in, and store their session for later.
    """
    if request.method == 'GET':
        return render_template('login.html')

    try:
        _user = User.from_login(
            request.form.get('email'),
            request.form.get('password'),
        )
    except StormpathError, err:
        return render_template('login.html', error=err.message)

    login_user(_user, remember=True)
    return redirect(request.args.get('next') or url_for('dashboard'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    This view renders a simple dashboard page for logged in users.

    Users can see their personal information on this page, as well as store
    additional data to their account (if they so choose).
    """
    if request.method == 'POST':
        if request.form.get('birthday'):
            user.custom_data['birthday'] = request.form.get('birthday')

        if request.form.get('color'):
            user.custom_data['color'] = request.form.get('color')

        user.save()

    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
    """
    Log out a logged in user.  Then redirect them back to the main page of the
    site.
    """
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
