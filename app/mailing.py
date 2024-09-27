import smtplib
import os

# Variables con los datos del correo
username = 'flowydomain@gmail.com'
password = os.getenv('MAIL_PASS', 'flowysi1')

# Conexion con servidor SMTP
s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
s.ehlo()

s.login(username, password)