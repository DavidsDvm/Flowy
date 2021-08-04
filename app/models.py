from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class tipoUsuario(db.Model):
    __tablename__ = 'tipoUsuario'
    idTipoUsuario = db.Column(db.Integer, primary_key=True)
    tipoUsuario = db.Column(db.String(11))
    children = db.relationship("usuario")

    def __init__(self, tipoUsuario):
        self.tipoUsuario = tipoUsuario

class usuario(db.Model):
    __tablename__ = 'usuario'
    idUsuario = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(25))
    password = db.Column(db.String(32))
    estadoUsuario = db.Column(db.String(8))
    idTipoUsuario = db.Column(db.Integer, db.ForeignKey('tipoUsuario.idTipoUsuario'))
    children = db.relationship("empleado")
    children2 = db.relationship("cliente")

    def __init__(self, usuario, password, estadoUsuario, idTipoUsuario):
        self.usuario = usuario
        self.password = password
        self.estadoUsuario = estadoUsuario
        self.idTipoUsuario = idTipoUsuario

class empleado(db.Model):
    __tablename__ = 'empleado'
    idEmpleado = db.Column(db.Integer, primary_key=True)
    nombreEmpleado = db.Column(db.String(50))
    tipoEmpleado = db.Column(db.String(20))
    celularEmpleado = db.Column(db.Integer)
    estadoemplado = db.Column(db.String(8))
    tipoDocEmpleado = db.Column(db.Integer)
    docEmpleado = db.Column(db.String(15))
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    children = db.relationship("pedido")
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
    docProovedor = db.Column(db.String(15))
    tipoDocProovedor = db.Column(db.String(15))
    correoProovedor = db.Column(db.String(50))
    telefonoProovedor = db.Column(db.Integer)
    children = db.relationship("compra")

    def __init__(self, docProovedor, tipoDocProovedor, correoProovedor, telefonoProovedor):
        self.docProovedor = docProovedor
        self.tipoDocProovedor = tipoDocProovedor
        self.tipoDocProovedor = tipoDocProovedor
        self.correoProovedor = correoProovedor
        self.telefonoProovedor = telefonoProovedor

association_table2 = db.Table('compraprodructo', db.metadata,
    db.Column('cantidadCompraProducto', db.Integer),
    db.Column('idCompra', db.ForeignKey('compra.idCompra')),
    db.Column('idProducto', db.ForeignKey('producto.idProducto'))
)

class compra(db.Model):
    __tablename__ = 'compra'
    idCompra = db.Column(db.Integer, primary_key=True)
    fechaCompra = db.Column(db.DateTime)
    totalCompra = db.Column(db.Integer)
    idEmpleado = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleado'))
    idProovedor = db.Column(db.Integer, db.ForeignKey('proovedor.idProovedor'))
    children = db.relationship("producto", secondary=association_table2)

    def __init__(self, fechaCompra, totalCompra, idEmpleado, idProovedor):
        self.fechaCompra = fechaCompra
        self.totalCompra = totalCompra
        self.idEmpleado = idEmpleado
        self.idProovedor = idProovedor

class cliente(db.Model):
    __tablename__ = 'cliente'
    idCliente = db.Column(db.Integer, primary_key=True)
    direccionCliente = db.Column(db.String(50))
    correoCliente = db.Column(db.String(30))
    celularCliente = db.Column(db.Integer)
    nombreCliente = db.Column(db.String(50))
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    children = db.relationship("pedido")

    def __init__(self, direccionCliente, correoCliente, celularCliente, nombreCliente, idUsuario):
        self.direccionCliente = direccionCliente
        self.correoCliente = correoCliente
        self.celularCliente = celularCliente
        self.nombreCliente = nombreCliente
        self.idUsuario = idUsuario


association_table = db.Table('pedidoProducto', db.metadata,
    db.Column('precioProducto', db.Integer),
    db.Column('cantidadPedidoProducto', db.Integer),
    db.Column('idPedido', db.ForeignKey('pedido.idPedido')),
    db.Column('idProducto', db.ForeignKey('producto.idProducto'))
)

class pedido(db.Model):
    __tablename__ = 'pedido'
    idPedido = db.Column(db.Integer, primary_key=True)
    fechaPedido = db.Column(db.DateTime)
    totalPedido = db.Column(db.Integer)
    especificacionPedido = db.Column(db.String(100))
    estadoPedido = db.Column(db.String(12))
    idEmpleado = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleado'))
    idCliente = db.Column(db.Integer, db.ForeignKey('cliente.idCliente'))
    children = db.relationship("producto", secondary=association_table)

    def __init__(self, fechaPedido, totalPedido, especificacionPedido, estadoPedido, idEmpleado, idCliente):
        self.fechaPedido = fechaPedido
        self.totalPedido = totalPedido
        self.especificacionPedido = especificacionPedido
        self.estadoPedido = estadoPedido
        self.idEmpleado = idEmpleado
        self.idCliente = idCliente

class producto(db.Model):
    __tablename__ = 'producto'
    idProducto = db.Column(db.Integer, primary_key=True)
    precioProducto = db.Column(db.Integer)
    nombreProducto = db.Column(db.String(15))
    cantidadProducto = db.Column(db.Integer)
    especificacionProducto = db.Column(db.String(100))
    idTipProducto = db.Column(db.Integer, db.ForeignKey('tipoProducto.idProducto'))
    child = db.relationship("tipoProducto")

    def __init__(self, precioProducto, nombreProducto, cantidadProducto, especificacionProducto, idTipProducto):
        self.precioProducto = precioProducto
        self.nombreProducto = nombreProducto
        self.cantidadProducto = cantidadProducto
        self.especificacionProducto = especificacionProducto
        self.idTipProducto = idTipProducto

class tipoProducto(db.Model):
    __tablename__ = 'tipoProducto'
    idProducto = db.Column(db.Integer, primary_key=True)
    nombreTipo = db.Column(db.String(20))

    def __init__(self, nombreTipo):
        self.nombreTipo = nombreTipo