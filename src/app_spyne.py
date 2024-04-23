import logging
from flask import Flask, redirect, render_template, request, url_for, flash, abort, jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from config import config
from models.ModelUsers import ModelUsers
from models.entities.users import User
from models.ModelUsers import ModelUsers
from models.entities.users import User
from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


logging.basicConfig(level=logging.DEBUG)
logging.getLogger("spyne.protocol.xml").setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object(config['development'])
db = MySQL(app)


class ProductosService(ServiceBase):
    @rpc(_returns=Iterable(Unicode))
    def obtener_productos(self):
        try:
            productos = ModelUsers.obtener_todos_los_productos(db)
            for producto in productos:
                yield producto.to_dict()
        except Exception as ex:
            yield {"error": str(ex)}

    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def agregar_producto(self, nombre, imagen, precio):
        try:
            ModelUsers.agregar_producto(db, nombre, imagen, precio)
            return "Producto agregado correctamente"
        except Exception as ex:
            return str(ex)

    @rpc(Integer, _returns=Unicode)
    def eliminar_producto(self, producto_id):
        try:
            ModelUsers.eliminar_producto(db, producto_id)
            return "Producto eliminado correctamente"
        except Exception as ex:
            return str(ex)

    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def editar_producto(self, producto_id, nombre, imagen, precio):
        try:
            ModelUsers.actualizar_producto(
                db, producto_id, nombre, imagen, precio)
            return "Producto editado correctamente"
        except Exception as ex:
            return str(ex)


application = Application([ProductosService],
                          tns='productos.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11(validator='lxml'))


wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    print("Iniciando el servidor...")
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, wsgi_application)
    logging.info("listening on 127.0.0.1:8000")
    server.serve_forever()
