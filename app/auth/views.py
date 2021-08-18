from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template, session, redirect, url_for, flash
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
import uuid

from app.forms import LoginForm, RegisterForm
from ..models import usuario, db
from ..mailing import s

from . import auth

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Tienes que iniciar primero sesion"
login_manager.login_message_category = "error"

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
            if password == user.password:
                if user.estadoUsuario == 'activo':
                    login_user(user)
                    session['username'] = user.usuario
                    
                    flash('Te has logeado correctamente', 'success')

                    return redirect(url_for('panel.inicioPanel'))
                else:
                    flash('Tu usuario no tiene el correo electronico confirmado', 'error')
            else:
                flash('La contrasena es incorrecta', 'error')
        else:
            flash('Hay un problema con tu usuario o contrasena', 'error')

    if register_form.validate_on_submit():
        nombreUsuario = register_form.usernameRegister.data
        correo = register_form.emailRegister.data
        password = register_form.passwordRegister.data
        estadoUsuario = 'inactivo'
        confirmationHash = str(uuid.uuid4().hex)
        idTipoUsuario = '2'
        user = usuario.query.filter_by(usuario = nombreUsuario).first()
        mail = usuario.query.filter_by(emailUsuario = correo).first()

        if user or mail:
            flash('Este usuario o correo ya existen, prueba con otro', 'error')
        else: 
            new_user = usuario(nombreUsuario, password, correo,estadoUsuario, confirmationHash, idTipoUsuario)
            db.session.add(new_user)
            db.session.commit()

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

            flash('Te has registrado correctamente, revisa tu bandeja de entrada', 'success')

            return redirect(url_for('index'))
    
    if current_user.is_authenticated:
        flash('Ya te encuentras logeado, si deseas utilizar otra cuenta cierra sesion primero', 'info')
        return redirect(url_for('panel.inicioPanel'))
    else:
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