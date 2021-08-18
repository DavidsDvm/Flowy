from flask import render_template

from app import create_app
from app.auth import auth

app = create_app()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/nosotros', defaults={'_route': 'nosotros'})
@app.route('/tienda', defaults={'_route': 'tienda'})
@app.route('/flores', defaults={'_route': 'flores'})
@app.route('/error404', defaults={'_route': '404'})
def navigationPages(_route):
    return render_template(_route+'.html');
