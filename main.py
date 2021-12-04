from flask import render_template, request, session, redirect, url_for, flash
from flask_login import current_user
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import random

from app import create_app
from app.auth import auth
from app.auth.views import load_user
from app.models import producto, imagenesProducto, cliente, pedido, pedidoProducto, db
from app.mailing import s
from flask_login.utils import login_required
from flask_login import current_user
from decouple import config as config_decouple
import os

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
def index():
    return render_template('index.html')

@app.route('/contacto', defaults={'_route': 'contacto'})
@app.route('/tienda', defaults={'_route': 'tienda'})
@app.route('/flores', defaults={'_route': 'flores'})
@app.route('/error404', defaults={'_route': '404'})
def navigationPages(_route):
    if _route == 'tienda':
        context = {
            'productos': producto.query.limit(12).all(),
            'imagenes': imagenesProducto.query.all(),
            'random': random
        }

        return render_template(_route+'.html', **context);

    return render_template(_route+'.html');

@app.route('/tienda/<int:id>', methods =['GET'])
def shopAdd(id):
    data = producto.query.get(id)
    imagenes = imagenesProducto.query.get(data.idImagenes)

    context = {
        'producto' : data,
        'addProducts': producto.query.limit(6).all(),
        'imagenes' : imagenes,
        'allImages': imagenesProducto.query.all(),
        'random': random
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
    if request.method == 'GET' and session.get('Shoppingcart') is None:
        flash('para ver tu carrito tienes que primero agregar algo', 'info')
        if request.referrer == None:
            return redirect(url_for('index'))
        return redirect(request.referrer)
    else:
        total = 0
        for key, product in session['Shoppingcart'].items():
            total += int(product['precio']) * int(product['cantidad'])

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
                if not session['Shoppingcart']:
                    session.pop('Shoppingcart', None)
                    return redirect(url_for('navigationPages', _route = 'tienda'))
                return redirect(request.referrer)
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

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if (request.method == 'GET'):
        total = 0
        for key, product in session['Shoppingcart'].items():
            total += int(product['precio']) * int(product['cantidad'])
    
        return render_template('checkout.html', total = total)

    if (request.method == 'POST'):
        nameClient = request.form['nameClient']
        lastNameClient = request.form['lastNameClient']
        directionClient = request.form['directionClient']
        postalCodeClient = request.form['postalCodeClient']
        mailClient = request.form['mailClient']
        phoneClient = request.form['phoneClient']

        # Bank info
        cardNumber = request.form['cardNumber']
        cardDateMonth = request.form['cardDateMonth']
        cardDateYear = request.form['cardDateYear']
        cardCVV = request.form['cardCVV']
        paypalClient = request.form['paypalClient']

        # Calculations

        total = 0
        for key, product in session['Shoppingcart'].items():
            total += int(product['precio']) * int(product['cantidad'])
        
        # Create client

        if (nameClient == '' or lastNameClient == '' or directionClient == '' or postalCodeClient == '' or mailClient == '' or phoneClient == ''):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('checkout'))
        else:
            if current_user.idTipoUsuario != 2:
                flash('Solo los usuarios que son clientes pueden hacer compras', 'error')
                return redirect(url_for('index'))
            else:
                currentUserIsClient = cliente.query.filter_by(idUsuario = current_user.idUsuario).first()
                if currentUserIsClient:
                    especificacionPedido = "Compra del usuario: " + str(current_user.usuario)
                    newPedido = pedido(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total, especificacionPedido, 'Activo', currentUserIsClient.idCliente)
                    db.session.add(newPedido)
                    db.session.commit()
                                    
                    for key in session['Shoppingcart']:
                        precio = int(session['Shoppingcart'][key]['precio'])
                        inventario = int(session['Shoppingcart'][key]['cantidad'])
                        subtotal = precio * inventario
                        nuevoProducto = pedidoProducto(newPedido.idPedido, key, subtotal , int(session['Shoppingcart'][key]['cantidad']))
                        db.session.add(nuevoProducto)

                    db.session.commit()

                    msg = MIMEMultipart('alternative')

                    contextMail = {
                        'idPedido' : newPedido.idPedido,
                        'fecha' : newPedido.fechaPedido,
                        'total' : newPedido.totalPedido,
                        'estadoPedido': newPedido.estadoPedido,
                        'productos' : session['Shoppingcart'],
                        'cliente' : currentUserIsClient
                    }

                    file = render_template('mail_newFacture.html', **contextMail )

                    text = """\
                    this is your buy invoice
                    here are the products of your buy
                    total: {}
                    """.format(newPedido.totalPedido)

                    msg['From']= 'david@mi.com.co'
                    msg['To']= str(current_user.emailUsuario)
                    msg['Subject']= "#{} Thanks for your purchase on FLOWY".format(newPedido.idPedido)

                    part1 = MIMEText(text, "plain")
                    part2 = MIMEText(file, "html")

                    msg.attach(part1)
                    msg.attach(part2)

                    s.send_message(msg)

                    flash('comprado!', 'success')
                    clearCart()
                    return redirect(url_for('index'))
                else:
                    if (cardNumber != None or cardDateMonth != None or cardDateYear != None or cardCVV != None):
                        newClient = cliente(directionClient, phoneClient, nameClient, 'CC', cardNumber, None, cardCVV, cardDateMonth, cardDateYear, nameClient+lastNameClient, current_user.idUsuario)
                        db.session.add(newClient)
                        db.session.commit()

                        especificacionPedido = "Compra del usuario: " + str(current_user.usuario)
                        newPedido = pedido(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total, especificacionPedido, 'Activo', newClient.idCliente)
                        db.session.add(newPedido)
                        db.session.commit()
                                        
                        for key in session['Shoppingcart']:
                            precio = int(session['Shoppingcart'][key]['precio'])
                            inventario = int(session['Shoppingcart'][key]['cantidad'])
                            subtotal = precio * inventario
                            nuevoProducto = pedidoProducto(newPedido.idPedido, key, subtotal , int(session['Shoppingcart'][key]['cantidad']))
                            db.session.add(nuevoProducto)

                        db.session.commit()

                        msg = MIMEMultipart('alternative')

                        contextMail = {
                            'idPedido' : newPedido.idPedido,
                            'fecha' : newPedido.fechaPedido,
                            'total' : newPedido.totalPedido,
                            'estadoPedido': newPedido.estadoPedido,
                            'productos' : session['Shoppingcart'],
                            'cliente' : currentUserIsClient
                        }

                        file = render_template('mail_newFacture.html', **contextMail )

                        text = """\
                        this is your buy invoice
                        here are the products of your buy
                        total: {}
                        """.format(newPedido.totalPedido)

                        msg['From']= 'david@mi.com.co'
                        msg['To']= str(current_user.emailUsuario)
                        msg['Subject']= "#{} Thanks for your purchase on FLOWY".format(newPedido.idPedido)

                        part1 = MIMEText(text, "plain")
                        part2 = MIMEText(file, "html")

                        msg.attach(part1)
                        msg.attach(part2)

                        s.send_message(msg)

                        flash('comprado!', 'success')
                        clearCart()
                        return redirect(url_for('index'))
                    elif (paypalClient != None):
                        newClient = cliente(directionClient, phoneClient, nameClient, 'CC', None, paypalClient, None, None, None, nameClient+lastNameClient, current_user.idUsuario)
                        db.session.add(newClient)
                        db.session.commit()

                        especificacionPedido = "Compra del usuario: " + str(current_user.usuario)
                        newPedido = pedido(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total, especificacionPedido, 'Activo', newClient.idCliente)
                        db.session.add(newPedido)
                        db.session.commit()
                                        
                        for key in session['Shoppingcart']:
                            precio = int(session['Shoppingcart'][key]['precio'])
                            inventario = int(session['Shoppingcart'][key]['cantidad'])
                            subtotal = precio * inventario
                            nuevoProducto = pedidoProducto(newPedido.idPedido, key, subtotal , int(session['Shoppingcart'][key]['cantidad']))
                            db.session.add(nuevoProducto)

                        db.session.commit()

                        msg = MIMEMultipart('alternative')

                        contextMail = {
                            'idPedido' : newPedido.idPedido,
                            'fecha' : newPedido.fechaPedido,
                            'total' : newPedido.totalPedido,
                            'estadoPedido': newPedido.estadoPedido,
                            'productos' : session['Shoppingcart'],
                            'cliente' : currentUserIsClient
                        }

                        file = render_template('mail_newFacture.html', **contextMail )

                        text = """\
                        this is your buy invoice
                        here are the products of your buy
                        total: {}
                        """.format(newPedido.totalPedido)

                        msg['From']= 'david@mi.com.co'
                        msg['To']= str(current_user.emailUsuario)
                        msg['Subject']= "#{} Thanks for your purchase on FLOWY".format(newPedido.idPedido)

                        part1 = MIMEText(text, "plain")
                        part2 = MIMEText(file, "html")

                        msg.attach(part1)
                        msg.attach(part2)

                        s.send_message(msg)

                        flash('comprado!', 'success')
                        clearCart()
                        return redirect(url_for('index'))
                    else:
                        flash('Todos los campos son obligatorios', 'error')
                        return redirect(url_for('checkout'))

if __name__ == '__main__':
    os.system('python dbCreator.py')

    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port, debug=1)