import os
from flask import render_template, session, redirect, url_for, request, flash, current_app, Response
from sqlalchemy import Integer, func
from flask_login import current_user
from werkzeug.utils import secure_filename
from functools import wraps
from fpdf import FPDF
import datetime
from time import strftime

from . import panel
from ..models import pedido, compra, pedidoProducto, producto, empleado, proovedor, imagenesProducto, compraProducto, cliente, db, tipoProducto, tipoUsuario, usuario 

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.idTipoUsuario == 3:
            return f(*args, **kwargs)
        else:
            flash('Necesitas ser administrador para ver esta pagina', 'info')
            return redirect(url_for('panel.inicioPanel'))

    return wrap

def employ_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.idTipoUsuario == 1 or current_user.idTipoUsuario == 3:
            return f(*args, **kwargs)
        else:
            flash('Necesitas ser empleado para mirar esta pagina', 'info')
            return redirect(url_for('panel.inicioPanel'))

    return wrap

@panel.route('/', methods=['GET', 'POST'])
@panel.route('/inicio', methods=['GET', 'POST'])
def inicioPanel():
    ultimasVentas = db.session.query(pedido).order_by(pedido.idPedido.desc()).limit(5)
    ultimasVentasSuma = pedido.query.with_entities(func.sum(pedido.totalPedido).label("mySum")).first()
    ultimosRegistrosSuma = db.session.query(pedido).count() 

    context = {
        'usuarioLogeadoActualmente' : current_user,
        'ultimasVentas' : ultimasVentas,
        'ultimasGanancias' : int(ultimasVentasSuma.mySum),
        'totalRegistros'  : ultimosRegistrosSuma
    }

    return render_template('panelIndex.html', **context)

# Usuarios ---------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
@panel.route('/usuarios')
def usuariosPanel():
    all_data = usuario.query.filter(usuario.estadoUsuario != 'Inactivo').all()
    context = {
        'usuarioLogeadoActualmente' : current_user,
        'usuarios' : all_data
    }

    return render_template('panelUsuarios.html', **context)

@panel.route('/usuarios/<int:id>')
def usuariosPanelEspecificacion(id):
    all_data = usuario.query.filter(usuario.estadoUsuario != 'Inactivo').all()
    data = usuario.query.filter_by(idUsuario = id).first()
    context = {
        'usuarioLogeadoActualmente' : current_user,
        'usuarios' : all_data
    }
    
    if data.idTipoUsuario == 1 or data.idTipoUsuario == 3:
        userEmp = empleado.query.filter_by(idUsuario = id).first()
        context['especificacionUsuarioEmp'] = userEmp
    if data.idTipoUsuario == 2:
        userCli = cliente.query.filter_by(idCliente = id).first()
        context['especificacionUsuarioCli'] = userCli

   

    return render_template('panelUsuarios.html', **context)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@panel.route('/perfil', methods =['GET', 'POST'])
def perfilPanel():
    if current_user.idTipoUsuario == 2:
        clienteData = cliente.query.filter_by(idUsuario = current_user.idUsuario).first()
        if not clienteData:
            flash('No se encontro el cliente, prueba comprando un articulo primero', 'info')
            return redirect(url_for('panel.inicioPanel'))

        context = {
            'usuarioLogeadoActualmente' : current_user,
            'tipoUsuario': 'cliente',
            'imagen' : current_user.avatar,
            'nombre' : clienteData.nombreCliente,
            'direccion' : clienteData.direccionCliente,
            'correo' : current_user.emailUsuario,
            'telefono' : clienteData.celularCliente,
            'tipoMetodoPago' : clienteData.tipoMetodoPago
        }
        if request.method == 'POST':
            my_dataUser = usuario.query.get(current_user.idUsuario)
            clienteData.nombreCliente = request.form['nombreUsuario']
            clienteData.direccionCliente = request.form['direccionCliente']
            clienteData.celularCliente = request.form['celularCliente']
            db.session.commit()

            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No seleccionaste una imagen y por consiguiente no se actualizo', 'info')
                return redirect(request.referrer)
            if file and allowed_file(file.filename):
                filename = current_user.emailUsuario+secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            my_dataUser.avatar = str(filename)
            session['avatar'] = str(filename)
            db.session.commit()

            flash('Datos modificados correctamente', 'success')
            return redirect(url_for('panel.perfilPanel'))
    else:
        my_dataUser = usuario.query.get(current_user.idUsuario)
        empleadoData = empleado.query.filter_by(idUsuario = current_user.idUsuario).first()
        
        context = {
            'usuarioLogeadoActualmente' : current_user,
            'tipoUsuario': 'empleado',
            'imagen' : current_user.avatar,
            'nombre' : empleadoData.nombreEmpleado,
            'correo' : current_user.emailUsuario,
            'telefono' : empleadoData.celularEmpleado,
            'tipoDoc' : empleadoData.tipoDocEmpleado,
            'documento' : empleadoData.docEmpleado
        }
        if request.method == 'POST':
            empleadoData.nombreEmpleado = request.form['nombreEmpleado']
            empleadoData.celularEmpleado = request.form['telefonoEmpleado']
            empleadoData.tipoDocEmplead = request.form['tipDocumento']
            empleadoData.docEmpleado = request.form['documento']
            db.session.commit()

            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No seleccionaste una imagen y por consiguiente no se actualizo', 'info')
                return redirect(request.referrer)
            if file and allowed_file(file.filename):
                filename = current_user.emailUsuario+secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            my_dataUser.avatar = str(filename)
            session['avatar'] = str(filename)
            db.session.commit()

            flash('Datos modificados correctamente', 'success')
            return redirect(url_for('panel.perfilPanel'))

    return render_template('panelPerfil.html', **context)

# Compras ---------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
@panel.route('/compras')
@employ_required
def comprasPanel():
    all_data = compra.query.filter(compra.estadoCompra != 'Inactivo').all()
    productoComp = producto.query.filter(producto.estadoProducto != 'Inactivo').all()
    compras = {}
    for key, data in enumerate(all_data, start=1):
        empleadoNombre = empleado.query.filter_by(idEmpleado = data.idEmpleado).first().nombreEmpleado
        nombreProvedor = proovedor.query.filter_by(idProovedor = data.idProovedor).first().nombreProovedor
        compras[key] = {'especificacionCompra' : data.especificacionCompra, 'totalCompra' : data.totalCompra, 'empleadoNombre' : empleadoNombre, 'fechaCompra' : data.fechaCompra, 'proovedorNombre' : nombreProvedor, 'idCompras' : data.idCompra, 'idProovedor' : data.idProovedor}

    context = {
        'usuarioLogeadoActualmente' : current_user,
        'today' : date.today(),
        'compras' : compras,
        'producto' : productoComp
    }

    return render_template('panelCompras.html', **context)

@panel.route('/compras/<int:id>')
@employ_required
def comprasPanelEspecific(id):
    all_data = compra.query.filter(compra.estadoCompra != 'Inactivo').all()
    my_data = compraProducto.query.filter_by(idCompra = id)

    compras = {}
    for key, data in enumerate(all_data, start=1):
        empleadoNombre = empleado.query.filter_by(idEmpleado = data.idEmpleado).first().nombreEmpleado
        nombreProvedor = proovedor.query.filter_by(idProovedor = data.idProovedor).first().nombreProovedor
        compras[key] = {'especificacionCompra' : data.especificacionCompra, 'totalCompra' : data.totalCompra, 'empleadoNombre' : empleadoNombre, 'fechaCompra' : data.fechaCompra, 'proovedorNombre' : nombreProvedor, 'idCompras' : data.idCompra, 'idProovedor' : data.idProovedor}

    productos = {}
    for key, data in enumerate(my_data, start=1):
        imagen = imagenesProducto.query.filter_by(idImagenes = data.idProducto).first()
        productoNombre = producto.query.filter_by(idProducto = data.idProducto).first().nombreProducto
        productos[key] = {'nombre' : productoNombre, 'subtotal' : data.subtotalCompraProducto, 'cantidad' : data.cantidadCompraProducto, 'imagen' : imagen.imagen1}

    context = {
        'usuarioLogeadoActualmente' : current_user,
        'pedidos' : all_data,
        'compras' : compras,
        'productos' : productos
    }

    return render_template('panelCompras.html', **context)

@panel.route('/compras/addnew/<int:id>')
@employ_required
def comprasPanelNewEspecificItem(id):
    all_data = compra.query.filter(compra.estadoCompra != 'Inactivo').all()
    productoComp = producto.query.filter(producto.estadoProducto != 'Inactivo').all()
    exactProduct = producto.query.filter_by(idProducto = id).first()
    compras = {}
    for key, data in enumerate(all_data, start=1):
        empleadoNombre = empleado.query.filter_by(idEmpleado = data.idEmpleado).first().nombreEmpleado
        nombreProvedor = proovedor.query.filter_by(idProovedor = data.idProovedor).first().nombreProovedor
        compras[key] = {'especificacionCompra' : data.especificacionCompra, 'totalCompra' : data.totalCompra, 'empleadoNombre' : empleadoNombre, 'fechaCompra' : data.fechaCompra, 'proovedorNombre' : nombreProvedor, 'idCompras' : data.idCompra, 'idProovedor' : data.idProovedor}

    context = {
        'usuarioLogeadoActualmente' : current_user,
        'today' : date.today(),
        'compras' : compras,
        'exactProducto' : exactProduct,
        'producto' : productoComp
    }

    return render_template('panelCompras.html', **context)

@panel.route('/compras/insert', methods =['POST'])
@employ_required
def addCompras():
    if (request.method == 'POST'):
        fechaCompra = str(date.today())
        totalCompra = request.form['totalPurchase']
        idEmpleado = current_user.idUsuario
        idProovedor = request.form['proovedorName']
        especificacionCompra = request.form['buyEspecification']
        Producto = request.form.get('idProductoa', False)
        estadoCompra = "Completo"

        my_data = compra(fechaCompra, totalCompra, Producto, especificacionCompra, estadoCompra, idEmpleado, idProovedor)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('panel.comprasPanel'))

@panel.route('/compras/update/<int:id>', methods =['GET', 'POST'])
@employ_required
def editCompras(id):
    if (request.method == 'POST'):
        my_data = compra.query.get(id)

        if request.form['fechaCompra'] > str(date.today()):
            flash('No puedes poner fechas superiores a la actual', 'error')
            return redirect(url_for('panel.comprasPanel'))

        my_data.fechaCompra = request.form['fechaCompra']
        my_data.totalCompra = request.form['totalPurchase']
        my_data.idEmpleado = 1
        my_data.idProovedor = request.form['proovedorName']
        my_data.especificacionCompra = request.form['buyEspecification']

        db.session.commit()

        return redirect(url_for('panel.comprasPanel'))

@panel.route('/compras/delete/<int:id>', methods = ['GET', 'POST'])
@employ_required
def deleteCompras(id):
    my_data = compra.query.get(id)
    my_data.estadoCompra = "Inactivo"

    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('panel.comprasPanel'))

# Pedidos ---------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
@panel.route('/pedidos')
@employ_required
def pedidosPanel():
    all_data = pedido.query.filter(pedido.estadoPedido != 'Inactivo').all()

    context = {
        'usuarioLogeadoActualmente' : current_user,
        'pedidos' : all_data
    }

    return render_template('panelPedidos.html', **context)

@panel.route('/pedidos/<int:id>')
@employ_required
def pedidosPanelEspecific(id):
    all_data = pedido.query.filter(pedido.estadoPedido != 'Inactivo').all()
    my_data = pedidoProducto.query.filter_by(idPedido = id)
    productos = {}
    for key, data in enumerate(my_data, start=1):
        imagen = imagenesProducto.query.filter_by(idImagenes = data.idProducto).first()
        productoNombre = producto.query.filter_by(idProducto = data.idProducto).first().nombreProducto
        productos[key] = {'nombre' : productoNombre, 'subtotal' : data.subtotalPedidoProducto, 'cantidad' : data.cantidadPedidoProducto, 'imagen' : imagen.imagen1}

    context = {
        'usuarioLogeadoActualmente' : current_user,
        'pedidos' : all_data,
        'productos' : productos
    }

    return render_template('panelPedidos.html', **context)

@panel.route('/pedidos/insert', methods =['POST'])
@employ_required
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
@employ_required
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
@employ_required
def deletePedidos(id):
    my_data = pedido.query.get(id)

    my_data.estadoPedido = "Inactivo"
    db.session.commit()

    return redirect(url_for('panel.pedidosPanel'))



# Productos ---------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
@panel.route('/productos')
def productosPanel():
    all_data = producto.query.filter(producto.estadoProducto != 'Inactivo').all()

    context = {
        'usuarioLogeadoActualmente' : current_user,
        'productos' : all_data
    }
    return render_template('panelProductos.html', **context)

@panel.route('/productos/insert', methods =['POST'])
@employ_required
def addProductos():
    if (request.method == 'POST'):
        nombreProducto = request.form['NombreProducto']
        precioProducto = request.form['PrecioProducto']
        cantidadProducto = request.form['CantidadProducto']
        especificacionProducto = request.form['EspecificacionProducto']
        estadoProducto = 'Activo'
        tipoProducto = request.form['TipoProducto']
        idImagenes = 1

        my_data = producto(precioProducto, nombreProducto, cantidadProducto, especificacionProducto, estadoProducto, idImagenes, tipoProducto)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('panel.productosPanel'))

@panel.route('/producto/update/<int:id>', methods =['GET', 'POST'])
@employ_required
def editProductos(id):
    if (request.method == 'POST'):
        my_data = producto.query.get(id)

        my_data.precioProducto = request.form['PrecioProducto']
        my_data.nombreProducto = request.form['NombreProducto']
        my_data.cantidadProducto = request.form['CantidadProducto']
        my_data.especificacionProducto = request.form['EspecificacionProducto']
        my_data.idImagenes = 1
        my_data.idTipProducto = request.form['TipoProducto']

        db.session.commit()

        return redirect(url_for('panel.productosPanel'))

@panel.route('/producto/delete/<int:id>', methods = ['GET', 'POST'])
@employ_required
def deleteProductos(id):
    my_data = producto.query.get(id)

    my_data.estadoProducto = "Inactivo"
    db.session.commit()

    return redirect(url_for('panel.productosPanel'))


# Reportes-----------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------

@panel.route('/reportes')
def download_report():
        datosPedido = db.session.query(pedido, cliente).join(cliente).limit(10)

        pdf = FPDF()
        pdf.add_page()

        page_with = pdf.w - 2 * pdf.l_margin
        col_width = page_with/5

        pdf.set_font('Helvetica', 'B', 14.0)
        pdf.cell(page_with, 0.0, 'Reporte Ventas', align='C')
        pdf.ln(10)

        pdf.set_font('Helvetica', '', 12)
        pdf.cell(col_width, pdf.font_size, 'id', border=1, ln=0, align='C', fill=0)
        pdf.cell(col_width, pdf.font_size, 'Fecha', border=1, ln=0, align='C', fill=0)
        pdf.cell(col_width, pdf.font_size, 'Total', border=1, ln=0, align='C', fill=0)
        pdf.cell(col_width, pdf.font_size, 'Estado', border=1, ln=0, align='C', fill=0)
        pdf.cell(col_width + 5, pdf.font_size, 'Cliente', border=1, ln=0, align='C', fill=0)

        pdf.ln(4)

        th = pdf.font_size
        pdf.set_font('Helvetica', '', 12)

        for row, row2 in datosPedido:
            fecha = (row.fechaPedido).strftime("%Y-%m-%d")
            pdf.cell(col_width, th, str(row.idPedido) , border=1, ln=0, align='C')
            pdf.cell(col_width, th, fecha, border=1, ln=0, align='C')
            pdf.cell(col_width, th, str(row.totalPedido), border=1, ln=0, align='C')
            pdf.cell(col_width, th, str(row.estadoPedido), border=1, ln=0, align='C')
            pdf.cell(col_width + 5, th, str(row2.nombreCliente), border=1, ln=0, align='C')
            pdf.ln(th)

        pdf.ln(10)

        # --------------------------------------------------------------------------------------------

        pdf.add_page()

        page_with = pdf.w - 2 * pdf.l_margin
        col_width = page_with/6

        registros = db.session.query(usuario, tipoUsuario).join(tipoUsuario).limit(10)

        pdf.set_font('Helvetica', 'B', 14.0)
        pdf.cell(page_with, 0.0, 'Reporte Ultimos registros', align='C')
        pdf.ln(9)

        pdf.set_font('Helvetica', '', 12)
        pdf.cell(col_width, pdf.font_size, 'id', border=1, ln=0, align='C', fill=0)
        pdf.cell(col_width, pdf.font_size, 'Usuario', border=1, ln=0, align='C', fill=0)
        pdf.cell(col_width + col_width, pdf.font_size, 'Email', border=1, ln=0, align='C', fill=0)
        pdf.cell(col_width, pdf.font_size, 'Estado', border=1, ln=0, align='C', fill=0)
        pdf.cell(col_width, pdf.font_size, 'Tipo Usuario', border=1, ln=0, align='C', fill=0)

        pdf.ln(4)

        th = pdf.font_size
        pdf.set_font('Helvetica', '', 12)

        for row, row2 in registros:
            pdf.cell(col_width, th, str(row.idUsuario) , border=1, ln=0, align='C')
            pdf.cell(col_width, th, str(row.usuario), border=1, ln=0, align='C')
            pdf.cell(col_width + col_width, th, str(row.emailUsuario), border=1, ln=0, align='C')
            pdf.cell(col_width, th, str(row.estadoUsuario), border=1, ln=0, align='C')
            pdf.cell(col_width, th, str(row2.tipoUsuario), border=1, ln=0, align='C')
            pdf.ln(th)

        pdf.ln(10)


        pdf.set_font('Helvetica',  '', 10.0)
        pdf.cell(page_with, 0.0, '- Fin del reporte -', align='C')



        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=ReporteGeneral.pdf'})


