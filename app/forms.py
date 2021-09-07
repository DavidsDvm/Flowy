from flask import flash, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError

from .models import usuario

csrf = CSRFProtect()

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=4, max=25)], render_kw={"placeholder": "Ingresa tu usario"})
    password = PasswordField(validators=[DataRequired(), Length(min=4, max=32)], render_kw={"placeholder": "Ingresa tu contrasena"})
    submit = SubmitField('Logeate')

class RegisterForm(FlaskForm):
    usernameRegister = StringField(validators=[DataRequired(), Length(min=4, max=25)], render_kw={"placeholder": "Ingresa tu usario"})
    emailRegister = StringField(validators=[DataRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Ingresa tu Correo"})
    passwordRegister = PasswordField(validators=[DataRequired(), Length(min=4, max=32)], render_kw={"placeholder": "Ingresa tu contrasena"})
    termsAndConditions = BooleanField(validators=[DataRequired()])
    submitRegister = SubmitField('Registrate')

    def validate_username(self, usernameRegister):
        existing_user_username = usuario.query.filter_by(usuario = usernameRegister.data).first()
        if existing_user_username:
            flash('Este usuario o correo ya existen, prueba con otro', 'error')
            return redirect(url_for('login'))

    def validate_mail(self, correo):
        existing_user_mail = usuario.query.filter_by(emailUsuario = correo.data).first()
        if existing_user_mail:
            flash('Este usuario o correo ya existen, prueba con otro', 'error')
            return redirect(url_for('login'))