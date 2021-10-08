from enum import unique
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class tipoUsuario(db.Model):
    __tablename__ = 'tipoUsuario'
    idTipoUsuario = db.Column(db.Integer, primary_key=True)
    tipoUsuario = db.Column(db.String(11))
    children = db.relationship("usuario")

    def __init__(self, tipoUsuario):
        self.tipoUsuario = tipoUsuario

class usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    idUsuario = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(25), nullable=False, unique=True)
    avatar = db.Column(db.String(200))
    password = db.Column(db.String(32), nullable=False)
    emailUsuario = db.Column(db.String(100), nullable=False, unique=True)
    estadoUsuario = db.Column(db.String(8))
    confirmationHash = db.Column(db.String(50))
    idTipoUsuario = db.Column(db.Integer, db.ForeignKey('tipoUsuario.idTipoUsuario'))
    children = db.relationship("empleado")
    children2 = db.relationship("cliente")

    def get_id(self):
           return (self.idUsuario)

    def __init__(self, usuario, avatar, password, emailUsuario, estadoUsuario, confirmationHash,idTipoUsuario):
        self.usuario = usuario
        self.avatar = avatar
        self.password = password
        self.emailUsuario = emailUsuario
        self.estadoUsuario = estadoUsuario
        self.confirmationHash = confirmationHash
        self.idTipoUsuario = idTipoUsuario

class empleado(db.Model):
    __tablename__ = 'empleado'
    idEmpleado = db.Column(db.Integer, primary_key=True)
    nombreEmpleado = db.Column(db.String(50))
    tipoEmpleado = db.Column(db.String(20))
    celularEmpleado = db.Column(db.BigInteger)
    estadoemplado = db.Column(db.String(8))
    tipoDocEmpleado = db.Column(db.String(4))
    docEmpleado = db.Column(db.String(15))
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    children2 = db.relationship("compra")

    def __init__(self, nombreEmpleado, tipoEmpleado, celularEmpleado, estadoemplado, tipoDocEmpleado, docEmpleado, idUsuario):
        self.nombreEmpleado = nombreEmpleado
        self.tipoEmpleado = tipoEmpleado
        self.celularEmpleado = celularEmpleado
        self.estadoemplado = estadoemplado
        self.tipoDocEmpleado = tipoDocEmpleado
        self.docEmpleado = docEmpleado
        self.idUsuario = idUsuario

class proovedor(db.Model):
    __tablename__ = 'proovedor'
    idProovedor = db.Column(db.Integer, primary_key=True)
    nombreEmpresaProovedor = db.Column(db.String(50))
    nombreProovedor = db.Column(db.String(50))
    docProovedor = db.Column(db.String(15))
    tipoDocProovedor = db.Column(db.String(4))
    correoProovedor = db.Column(db.String(50))
    telefonoProovedor = db.Column(db.BigInteger)
    children = db.relationship("compra")

    def __init__(self, nombreEmpresaProovedor, nombreProovedor, docProovedor, tipoDocProovedor, correoProovedor, telefonoProovedor):
        self.nombreEmpresaProovedor = nombreEmpresaProovedor
        self.nombreProovedor = nombreProovedor        
        self.docProovedor = docProovedor
        self.tipoDocProovedor = tipoDocProovedor
        self.tipoDocProovedor = tipoDocProovedor
        self.correoProovedor = correoProovedor
        self.telefonoProovedor = telefonoProovedor

class compraProducto(db.Model):
    __tablename__ = 'compraProducto'
    idCompra = db.Column(db.ForeignKey('compra.idCompra'), primary_key=True)
    idProducto = db.Column(db.ForeignKey('producto.idProducto'), primary_key=True)
    subtotalCompraProducto = db.Column(db.Integer)
    cantidadCompraProducto = db.Column(db.Integer)
    compra = db.relationship("compra", back_populates="compraMTM")
    producto = db.relationship("producto", back_populates="productoCompraMTM")
    
    def __init__(self, idCompra, idProducto, subtotalCompraProducto, cantidadCompraProducto):
        self.idCompra = idCompra
        self.idProducto = idProducto
        self.subtotalCompraProducto = subtotalCompraProducto
        self.cantidadCompraProducto = cantidadCompraProducto

class compra(db.Model):
    __tablename__ = 'compra'
    idCompra = db.Column(db.Integer, primary_key=True)
    fechaCompra = db.Column(db.DateTime)
    totalCompra = db.Column(db.Integer)
    especificacionCompra = db.Column(db.String(100))
    estadoCompra = db.Column(db.String(12))
    idEmpleado = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleado'))
    idProovedor = db.Column(db.Integer, db.ForeignKey('proovedor.idProovedor'))
    compraMTM = db.relationship("compraProducto", back_populates="compra")

    def __init__(self, fechaCompra, totalCompra, especificacionCompra, estadoCompra, idEmpleado, idProovedor):
        self.fechaCompra = fechaCompra
        self.totalCompra = totalCompra
        self.especificacionCompra = especificacionCompra
        self.estadoCompra = estadoCompra
        self.idEmpleado = idEmpleado
        self.idProovedor = idProovedor

class cliente(db.Model):
    __tablename__ = 'cliente'
    idCliente = db.Column(db.Integer, primary_key=True)
    direccionCliente = db.Column(db.String(150))
    celularCliente = db.Column(db.BigInteger)
    nombreCliente = db.Column(db.String(50))
    tipoMetodoPago = db.Column(db.String(30))
    numeroTarjeta = db.Column(db.String(60), unique=True)
    correoDetalleCliente = db.Column(db.String(50))
    codigoSeguridad = db.Column(db.String(60))
    mesVencimiento = db.Column(db.String(60))
    añoVencimiento = db.Column(db.String(60))
    titularTargeta = db.Column(db.String(60), unique=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    children = db.relationship("pedido")

    def __init__(self, direccionCliente, celularCliente, nombreCliente,tipoMetodoPago, numeroTarjeta, correoDetalleCliente, codigoSeguridad, mesVencimiento, añoVencimiento, titularTargeta, idUsuario):
        self.direccionCliente = direccionCliente
        self.celularCliente = celularCliente
        self.nombreCliente = nombreCliente
        self.tipoMetodoPago = tipoMetodoPago
        self.numeroTarjeta = numeroTarjeta
        self.correoDetalleCliente = correoDetalleCliente
        self.codigoSeguridad = codigoSeguridad
        self.mesVencimiento = mesVencimiento
        self.añoVencimiento = añoVencimiento
        self.titularTargeta = titularTargeta
        self.idUsuario = idUsuario

class pedidoProducto(db.Model):
    __tablename__ = 'pedidoProducto'
    idPedido = db.Column(db.ForeignKey('pedido.idPedido'), primary_key=True)
    idProducto = db.Column(db.ForeignKey('producto.idProducto'), primary_key=True)
    subtotalPedidoProducto = db.Column(db.Integer)
    cantidadPedidoProducto = db.Column(db.Integer)
    pedido = db.relationship("pedido", back_populates="pedidoMTM")
    producto = db.relationship("producto", back_populates="productoMTM")

    def __init__(self, idPedido, idProducto, subtotalPedidoProducto ,cantidadPedidoProducto):
        self.idPedido = idPedido
        self.idProducto = idProducto
        self.subtotalPedidoProducto = subtotalPedidoProducto
        self.cantidadPedidoProducto = cantidadPedidoProducto


# class detalleCliente(db.Model):
#     __tablename__ = 'detalleCliente'
#     idDetalleCliente = db.Column(db.Integer, primary_key=True, )
#     tipoMetodoPago = db.Column(db.String(30))
#     numeroTarjeta = db.Column(db.String(60), unique=True)
#     correoDetalleCliente = db.Column(db.String(50), unique=True)
#     codigoSeguridad = db.Column(db.String(60))
#     mesVencimiento = db.Column(db.String(60))
#     añoVencimiento = db.Column(db.String(60))
#     titularTargeta = db.Column(db.String(60), unique=True)
#     idCliente = db.Column(db.Integer, db.ForeignKey('cliente.idCliente'))

#     def __init__(self, tipoMetodoPago, numeroTarjeta, correoDetalleCliente, codigoSeguridad, mesVencimiento, añoVencimiento, titularTargeta, idCliente):
#         self.tipoMetodoPago = tipoMetodoPago
#         self.numeroTarjeta = numeroTarjeta
#         self.correoDetalleCliente = correoDetalleCliente
#         self.codigoSeguridad = codigoSeguridad
#         self.mesVencimiento = mesVencimiento
#         self.añoVencimiento = añoVencimiento
#         self.titularTargeta = titularTargeta
#         self.idCliente = idCliente

class pedido(db.Model):
    __tablename__ = 'pedido'
    idPedido = db.Column(db.Integer, primary_key=True)
    fechaPedido = db.Column(db.DateTime)
    totalPedido = db.Column(db.Integer)
    especificacionPedido = db.Column(db.String(100))
    estadoPedido = db.Column(db.String(12))
    idCliente = db.Column(db.Integer, db.ForeignKey('cliente.idCliente'))
    pedidoMTM = db.relationship("pedidoProducto", back_populates="pedido")

    def __init__(self, fechaPedido, totalPedido, especificacionPedido, estadoPedido, idCliente):
        self.fechaPedido = fechaPedido
        self.totalPedido = totalPedido
        self.especificacionPedido = especificacionPedido
        self.estadoPedido = estadoPedido
        self.idCliente = idCliente

class producto(db.Model):
    __tablename__ = 'producto'
    idProducto = db.Column(db.Integer, primary_key=True)
    precioProducto = db.Column(db.Integer)
    nombreProducto = db.Column(db.String(50))
    cantidadProducto = db.Column(db.Integer)
    especificacionProducto = db.Column(db.String(255))
    estadoProducto = db.Column(db.String(12))
    idImagenes = db.Column(db.Integer, db.ForeignKey('imagenesProducto.idImagenes'))
    idTipProducto = db.Column(db.Integer, db.ForeignKey('tipoProducto.idProducto'))
    child = db.relationship("tipoProducto")
    productoMTM = db.relationship("pedidoProducto", back_populates="producto")
    productoCompraMTM = db.relationship("compraProducto", back_populates="producto")

    def __init__(self, precioProducto, nombreProducto, cantidadProducto, especificacionProducto, estadoProducto, idImagenes ,idTipProducto):
        self.precioProducto = precioProducto
        self.nombreProducto = nombreProducto
        self.cantidadProducto = cantidadProducto
        self.especificacionProducto = especificacionProducto
        self.estadoProducto = estadoProducto
        self.idImagenes = idImagenes
        self.idTipProducto = idTipProducto

class tipoProducto(db.Model):
    __tablename__ = 'tipoProducto'
    idProducto = db.Column(db.Integer, primary_key=True)
    nombreTipo = db.Column(db.String(20))

    def __init__(self, nombreTipo):
        self.nombreTipo = nombreTipo

class imagenesProducto(db.Model):
    __tablename__ = 'imagenesProducto'
    idImagenes = db.Column(db.Integer, primary_key=True)
    imagen1 = db.Column(db.String(255), nullable=False)
    imagen2 = db.Column(db.String(255))
    imagen3 = db.Column(db.String(255))
    imagen4 = db.Column(db.String(255))
    imagen5 = db.Column(db.String(255))
    children = db.relationship("producto")

    def __init__(self, imagen1, imagen2, imagen3, imagen4, imagen5):
        self.imagen1 = imagen1
        self.imagen2 = imagen2
        self.imagen3 = imagen3
        self.imagen4 = imagen4
        self.imagen5 = imagen5