
import smtplib
import os

username = 'david@mi.com.co'
password = os.environ.get('mailDavidPass')
# file = codecs.open("index.html", "r", "utf-8")

s = smtplib.SMTP('smtp.mi.com.co')
s.connect(host='smtp.mi.com.co', port='587')
s.starttls()
s.login(username, password)