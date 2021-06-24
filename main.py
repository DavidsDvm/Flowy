from flask import Flask
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def homePage():
    return render_template('index.html')

@app.route('/nosotros', defaults={'_route': 'nosotros'})
@app.route('/tienda', defaults={'_route': 'tienda'})
@app.route('/flores', defaults={'_route': 'flores'})
def navigationPages(_route):
    return render_template(_route+'.html')

@app.route('/login')
def loginCheck():
    return render_template('login.html')