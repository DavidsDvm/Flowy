from flask import render_template, session, redirect, url_for, request
from datetime import date

from . import panel
from ..models import pedido, compra, db

@panel.route('/', methods=['GET', 'POST'])
@panel.route('/inicio', methods=['GET', 'POST'])
def inicioPanel():
    context = {
        'personalName': session['username']
    }

    return render_template('panelIndex.html', **context)

@panel.route('/compras')
def comprasPanel():
    all_data = compra.query.all()

    context = {
        'personalName': session['username'],
        'compras' : all_data
    }

    return render_template('panelCompras.html', **context)

@panel.route('/perfil', defaults={'_route': 'perfil'})
@panel.route('/usuarios', defaults={'_route': 'usuarios'})
def navigationPages(_route):
    return render_template(_route+'.html');



@panel.route('/compras/insert', methods =['POST'])
def addCompras():
    if (request.method == 'POST'):
        fechaCompra = str(date.today())
        totalCompra = request.form['totalPurchase']
        idEmpleado = 1
        idProovedor = request.form['proovedorName']
        especificacionCompra = request.form['buyEspecification']

        my_data = compra(fechaCompra, totalCompra, idEmpleado, idProovedor, especificacionCompra)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('panel.comprasPanel'))

@panel.route('/compras/update/<int:id>', methods =['GET', 'POST'])
def editCompras(id):
    if (request.method == 'POST'):
        my_data = compra.query.get(id)

        my_data.fechaCompra = request.form['fechaCompra']
        my_data.totalCompra = request.form['totalPurchase']
        my_data.idEmpleado = 1
        my_data.idProovedor = request.form['proovedorName']
        my_data.especificacionCompra = request.form['buyEspecification']

        db.session.commit()

        return redirect(url_for('panel.comprasPanel'))

@panel.route('/compras/delete/<int:id>', methods = ['GET', 'POST'])
def deleteCompras(id):
    my_data = compra.query.get(id)

    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('panel.comprasPanel'))

@panel.route('/pedidos')
def pedidosPanel():
    all_data = pedido.query.all()

    context = {
        'personalName': session['username'],
        'pedidos' : all_data
    }

    return render_template('panelPedidos.html', **context)

@panel.route('/pedidos/insert', methods =['POST'])
def addPedidos():
    if (request.method == 'POST'):
        fechaPedido = str(date.today())
        pedidoPrice = request.form['pedidoPrice']
        especificacionPedido = request.form['pedidoEspecification']
        estadoPedido = 'Activo'
        idEmpleado = 1
        idCliente = 1

        my_data = pedido(fechaPedido, pedidoPrice, especificacionPedido, estadoPedido, idEmpleado, idCliente)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('panel.pedidosPanel'))

@panel.route('/pedidos/update/<int:id>', methods =['GET', 'POST'])
def editPedidos(id):
    if (request.method == 'POST'):
        my_data = pedido.query.get(id)

        my_data.fechaPedido = request.form['datePedido']
        my_data.totalPedido = request.form['pedidoPrice']
        my_data.especificacionPedido = request.form['pedidoEspecification']
        my_data.estadoPedido = 'Activo'
        my_data.idEmpleado = 1
        my_data.idCliente = 1

        db.session.commit()

        return redirect(url_for('panel.pedidosPanel'))

@panel.route('/pedidos/delete/<int:id>', methods = ['GET', 'POST'])
def deletePedidos(id):
    my_data = pedido.query.get(id)

    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('panel.pedidosPanel'))