import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import be.db as bedb

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = bedb.get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.get_user(username) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            print("no errors! Adding a user... Auth succeded.")
            db.add_user(username, generate_password_hash(password))
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = bedb.get_db()
        error = None
        user = db.get_user(username).get('u')
        print("login: user = " + str(user))
        # print("user.keys ==== " + str(user.get('u').id))
        # print("user.keys ==== " + str(user.get('u').labels))
        # print("user.keys ==== " + str(user.get('u')['password']))
        # print("user.keys ==== " + str(user.get('u')['username']))
        
        if user is None:
            error = 'Incorrect username. User does not exist'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            print("session = " + str(session))
            print("user    = " + str(user))
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    print(">session = " + str(session))
    print(">g       = " + str(g))
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = bedb.get_db()
        g.user = db.get_user_by_id(user_id).get('n')
        # print(">type(user) = " + str(type(g.user)))
        # print(">user    = " + str(g.user))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


