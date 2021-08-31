from flask import render_template, request, session, redirect, url_for, flash
from flask_login import current_user

from app import create_app
from app.auth import auth
from app.models import producto, imagenesProducto, db

app = create_app()

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def not_found(error):
    return render_template('500.html', error=error)

@app.errorhandler(505)
def not_found(error):
    return render_template('505.html', error=error)

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

@app.route('/tienda/<int:id>', methods =['GET'])
def shopAdd(id):
    data = producto.query.get(id)
    imagenes = imagenesProducto.query.get(data.idImagenes)

    context = {
        'data' : data,
        'imagenes' : imagenes
    }

    return render_template('productDescription.html', **context)


def magerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance (dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/tienda/add', methods = ['GET', 'POST'])
def addCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')

        product = producto.query.get(product_id)
        imagenes = imagenesProducto.query.get(product.idImagenes)

        if int(quantity) > int(product.cantidadProducto):
            flash(f'Solo puedes agregar maximo: {int(product.cantidadProducto)} productos de este tipo', 'error')
        else:
            if product_id and quantity and request.method == 'POST':
                dictItems = {product_id:{'precio': product.precioProducto,'nombre': product.nombreProducto, 'cantidad': quantity, 'imagen': imagenes.imagen1}}
                if 'Shoppingcart' in session:
                    print(session['Shoppingcart'])
                    if product_id in session['Shoppingcart']:
                        for key, item in session['Shoppingcart'].items():
                            if int(key) == int(product_id):
                                session.modified = True
                                item['cantidad'] = int(item['cantidad']) + int(quantity)
                                if item['cantidad'] > int(product.cantidadProducto):
                                    flash(f'Solo puedes agregar maximo: {int(product.cantidadProducto)} productos de este tipo', 'error')
                                    session.modified = True
                                    item['cantidad'] = int(product.cantidadProducto)
                    else:
                        session['Shoppingcart'] = magerDicts(session['Shoppingcart'], dictItems)
                        return redirect(request.referrer)
                else:
                    session['Shoppingcart'] = dictItems
                    return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/compra', methods=['GET', 'POST'])
def buyShopping():
    total = 0
    for key, product in session['Shoppingcart'].items():
        total += int(product['precio']) * int(product['cantidad'])

    if request.method == 'POST':
        if current_user.is_authenticated:
            flash('comprado!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Ya casi tienes tu producto, primero registrate', 'info')
            return redirect(url_for('auth.login'))

    return render_template('compra.html', total = total)

@app.route('/compra/delete/<int:id>', methods=['GET', 'POST'])
def deleteItem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('navigationPages', _route = 'tienda'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('buyShopping'))
    except Exception as e:
        print(e)
        return redirect(url_for('buyShopping'))

@app.route('/compra/clear')
def clearCart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('navigationPages', _route = 'tienda'))
    except Exception as e:
        print(e)