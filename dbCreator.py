from app import create_app
from app.auth import auth
from app.models import tipoUsuario, usuario, empleado, proovedor, compra, cliente, pedido, pedidoProducto, compraProducto, producto, tipoProducto, imagenesProducto, db

app = create_app()

app.app_context().push()

db.create_all()

tipoUsuario1 = tipoUsuario('Empleado')
tipoUsuario2 = tipoUsuario('Cliente')
tipoUsuario3 = tipoUsuario('Admin')

usuario1 = usuario('admin', 'userImage_1.png', 'sadsad', 'davids.dvm@gmail.com', 'activo', None, '3')
usuario2 = usuario('santiago', 'userImage_1.png', 'sadsad', 'santiago@gmail.com', 'activo', None, '2')
usuario3 = usuario('juan', 'userImage_1.png', 'sadsad', 'juan@gmail.com', 'activo', None, '2')

empleado1 = empleado('Pepito Gonzales', 'Administrador', '3105628923', 'Activo', 'CE', '25252525', '3')
empleado2 = empleado('Lucia Cardenas', 'Gerente', '3198524759', 'Inactivo', 'CC', '1052628978', '2')
empleado3 = empleado('Santiago Perez', 'Pepo', '3122055247', 'Activo', 'CC', '1525457845', '1')

proovedor1 = proovedor('Flores C SAS', 'Raul', '1052487895', 'CC', 'flores@flores.com', '3189547569')
proovedor2 = proovedor('LasFloresdePedro', 'Pedro', '1030699585', 'CC', 'Pedro@Flowers.com', '3198274715')
proovedor3 = proovedor('Flowers CORP', 'Will', '1030574151', 'CE', 'FlowerC@gmail.com', '3165024147')

compra1 = compra('2021-06-25', '50000', 'Compra de Tulipanes x100,Rosas x800', 'Activo', 1, 2)
compra2 = compra('2021-05-31', '600000', 'Compra orquideas x30, Compra azucenax 300', 'Activo', 2, 1)
compra3 = compra('2020-06-25', '500000', 'Compra Dalia x50, Compra hortensiax100', 'Activo', 3, 1)

cliente1 = cliente('cll 54 bs24-2', '31030445467', 'Ramiro Gonzalez','CC', '5465765489765432', None, '547', '06', '2023', 'Ramiro Gonzalez', '1')
cliente2 = cliente('Crr 28 v67-21', '3143143142', 'Calceto oliente','Paypal', None, 'calcetoRo@gmail.com', None, None, None, 'Calceto', '2')
cliente3 = cliente('Avenida 30 #24-2', '3213213215', 'Porfilo Rojas','CC', '4705234586872343', None, '665', '02', '2025', 'Carlo magno', '3')

pedido1 = pedido('2020-05-02', '50000', 'Pedido de un Boutique Matrimonial', 'Enviado', 1)
pedido2 = pedido('2021-06-03', '90000', 'Pedido de un Boutique cumpleaños', 'Empaquetando', 2)
pedido3 = pedido('2021-04-02', '60004', 'Pedido 41 Rosas Rojas', 'Entregado', 3)

tipProduct1 = tipoProducto ('Unitario')
tipProduct2 = tipoProducto ('Arreglos')
tipProduct3 = tipoProducto ('Boutique')

imagen1 = imagenesProducto('shop_flower_1.jpg', None, None, None, None)
imagen2 = imagenesProducto('shop_flower_2.jpg', None, None, None, None)
imagen3 = imagenesProducto('shop_flower_3.jpg', None, None, None, None)

producto1 = producto(12000, 'Rosa', 500, 'Flores en un jarron Arreglo Tulipanes Flor tipo tulipán de la familia Liliaceae flor con gran aroma, viene con jarrón Características: Tulipanes: Tulipa gesneriana Colores: A elección del usuario', 1, 1)
producto2 = producto(600000, 'Boutique cumpleaños', 600, 'Arreglo floral de cumpleaños', 2, 2)
producto3 = producto(646545, 'Boutique Matrimonial', 300, 'Arreglo floral Matrimonial', 3, 3)

pedidoP1 = pedidoProducto(1, 1, 500000, 5)
pedidoP2 = pedidoProducto(2, 2, 1500000, 50)
pedidoP3 = pedidoProducto(3, 3, 2600000, 16)

compraP1 = compraProducto(1, 1, 600000, 1)
compraP2 = compraProducto(2, 2, 60000, 6)
compraP3 = compraProducto(3, 3, 400000, 5)

db.session.add(tipoUsuario1)
db.session.add(tipoUsuario2)
db.session.add(tipoUsuario3)
db.session.add(usuario1)
db.session.add(usuario2)
db.session.add(usuario3)
db.session.add(empleado1)
db.session.add(empleado2)
db.session.add(empleado3)
db.session.add(proovedor1)
db.session.add(proovedor2)
db.session.add(proovedor3)
db.session.add(compra1)
db.session.add(compra2)
db.session.add(compra3)
db.session.add(cliente1)
db.session.add(cliente2)
db.session.add(cliente3)
db.session.add(pedido1)
db.session.add(pedido2)
db.session.add(pedido3)
db.session.add(tipProduct1)
db.session.add(tipProduct2)
db.session.add(tipProduct3)
db.session.add(imagen1)
db.session.add(imagen2)
db.session.add(imagen3)
db.session.add(producto1)
db.session.add(producto2)
db.session.add(producto3)
db.session.add(pedidoP1)
db.session.add(pedidoP2)
db.session.add(pedidoP3)
db.session.add(compraP1)
db.session.add(compraP2)
db.session.add(compraP3)

db.session.commit()
