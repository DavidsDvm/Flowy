from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template, session, redirect, url_for
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
import uuid

from app.forms import LoginForm, RegisterForm
from ..models import usuario, db
from ..mailing import s

from . import auth

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return usuario.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()

    context = {
        'login_form': login_form,
        'register_form' : register_form
    }

    if login_form.validate_on_submit():
        nombreUsuario = login_form.username.data
        password = login_form.password.data

        user = usuario.query.filter_by(usuario = nombreUsuario).first()
        if user:
            if password == user.password and user.estadoUsuario == 'activo':
                login_user(user)
                session['username'] = user.usuario
                return redirect(url_for('panel.inicioPanel'))

    if register_form.validate_on_submit():
        nombreUsuario = register_form.username.data
        correo = register_form.email.data
        password = register_form.password.data
        estadoUsuario = 'inactivo'
        confirmationHash = str(uuid.uuid4().hex)
        idTipoUsuario = '2'

        new_user = usuario(nombreUsuario, password, correo,estadoUsuario, confirmationHash, idTipoUsuario)
        db.session.add(new_user)
        db.session.commit()

        user = usuario.query.filter_by(usuario = nombreUsuario).first()

        msg = MIMEMultipart('alternative')

        contextMail = {
            'nombreUsuario' : nombreUsuario,
            'hash' : confirmationHash
        }

        file = render_template('mail_accountConfirmation.html', **contextMail )

        text = """\
        Confirmation mail
        If you dont see the button below
        Just press on the next link:
        localhost:5000/auth/confirm/{}
        """.format(confirmationHash)

        msg['From']= 'david@mi.com.co'
        msg['To']= str(correo)
        msg['Subject']= "Confirm your email FLOWY"

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(file, "html")

        msg.attach(part1)
        msg.attach(part2)

        s.send_message(msg)

        return redirect(url_for('index'))
        
    return render_template('login.html', **context)


@auth.route('/confirm/<hash>', methods=['GET', 'POST'])
def mailConfirm(hash):
    uniqueHash = hash

    hashExist = usuario.query.filter_by(confirmationHash = hash).first()

    if hashExist:
        hashExist.estadoUsuario = "activo"
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return redirect(url_for('auth.login'))

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))