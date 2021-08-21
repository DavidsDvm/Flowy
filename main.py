from flask import render_template, request, session

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
@app.route('/compra', defaults={'_route': 'compra'})
@app.route('/error404', defaults={'_route': '404'})
@app.route('/description', defaults={'_route': 'productDescription'})
def navigationPages(_route):
    return render_template(_route+'.html');

# @app.route('/tienda/<int:id>', methods =['POST'])
# def shopAdd(id):
#     if (request.method == 'POST'):
#         session['shoppingCart'] = []
        
