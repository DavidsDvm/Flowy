from flask import render_template, session, redirect, url_for, request
from sqlalchemy import Integer, func
from datetime import date

from . import panel
from ..models import pedido, compra, pedidoProducto, producto, empleado, proovedor, imagenesProducto, db 

@panel.route('/', methods=['GET', 'POST'])
@panel.route('/inicio', methods=['GET', 'POST'])
def inicioPanel():
    ultimasVentas = db.session.query(pedido).order_by(pedido.idPedido.desc()).limit(5)
    ultimasVentasSuma = pedido.query.with_entities(func.sum(pedido.totalPedido).label("mySum")).first()
    ultimosRegistrosSuma = db.session.query(pedido).count() 

    context = {
        'personalName' : session['username'],
        'ultimasVentas' : ultimasVentas,
        'ultimasGanancias' : int(ultimasVentasSuma.mySum),
        'totalRegistros'  : ultimosRegistrosSuma
    }

    return render_template('panelIndex.html', **context)

# @panel.route('/usuarios', defaults={'_route': 'panelUsuarios'})
# def usuariosPanel():
#     context = {
#         'personalName': session['username']
#     }

#     return render_template('panelUser.html', **context)


@panel.route('/perfil')
def perfilPanel():
    context = {
        'personalName': session['username']
    }

    return render_template('panelPerfil.html', **context)

@panel.route('/compras')
def comprasPanel():
    all_data = compra.query.filter(compra.estadoCompra != 'Inactivo').all()
    compras = {}
    for key, data in enumerate(all_data, start=1):
        empleadoNombre = empleado.query.filter_by(idEmpleado = data.idEmpleado).first().nombreEmpleado
        nombreProvedor = proovedor.query.filter_by(idProovedor = data.idProovedor).first().nombreProovedor
        compras[key] = {'especificacionCompra' : data.especificacionCompra, 'totalCompra' : data.totalCompra, 'empleadoNombre' : empleadoNombre, 'fechaCompra' : data.fechaCompra, 'proovedorNombre' : nombreProvedor, 'idCompras' : data.idCompra, 'idProovedor' : data.idProovedor}

    context = {
        'personalName': session['username'],
        'compras' : compras
    }

    return render_template('panelCompras.html', **context)

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
    my_data.estadoCompra = "Inactivo"

    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('panel.comprasPanel'))

@panel.route('/pedidos')
def pedidosPanel():
    all_data = pedido.query.filter(pedido.estadoPedido != 'Inactivo').all()

    context = {
        'personalName': session['username'],
        'pedidos' : all_data
    }

    return render_template('panelPedidos.html', **context)

@panel.route('/pedidos/<int:id>')
def pedidosPanelEspecific(id):
    all_data = pedido.query.all()
    my_data = pedidoProducto.query.filter_by(idPedido = id)
    productos = {}
    for key, data in enumerate(my_data, start=1):
        imagen = imagenesProducto.query.filter_by(idImagenes = data.idProducto).first()
        productoNombre = producto.query.filter_by(idProducto = data.idProducto).first().nombreProducto
        productos[key] = {'nombre' : productoNombre, 'subtotal' : data.subtotalPedidoProducto, 'cantidad' : data.cantidadPedidoProducto, 'imagen' : imagen.imagen1}

    context = {
        'personalName': session['username'],
        'pedidos' : all_data,
        'productos' : productos
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

    my_data.estadoPedido = "Inactivo"
    db.session.commit()

    return redirect(url_for('panel.pedidosPanel'))