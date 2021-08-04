from flask import render_template, session, redirect, url_for

from . import panel
from ..models import pedido

@panel.route('/inicio')
def inicioPanel():
    return render_template('panelIndex.html')

@panel.route('/compras')
def comprasPanel():
    return render_template('panelCompras.html')

@panel.route('/pedidos')
def pedidosPanel():
    all_data = pedido.query.all()

    return render_template('panelPedidos.html', pedidos = all_data)