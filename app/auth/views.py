from flask import render_template, session, redirect, url_for

from app.forms import LoginForm

from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        session['username'] = username

        return "Lo hiciste felicitaciones"

    return render_template('login.html', **context)
