import json
from .entities.users import User
from .entities.productos import Producto
from .entities.Venta import Venta
from .entities.DetalleVenta import DetalleVenta


class ModelUsers:
    @classmethod
    def get_by_id(cls, db, user_id):
        try:
            with db.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, usertype, fullname FROM users WHERE id = %s", (
                        user_id,)
                )
                row = cursor.fetchone()
                if row:
                    return User(row[0], row[1], None, row[2], row[3])
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login(cls, db, user):
        try:
            with db.connection.cursor() as cursor:
                cursor.execute("call sp_verifyIdentity(%s, %s)",
                               (user.username, user.password))
                row = cursor.fetchone()
                if row and row[0] is not None:
                    return User(row[0], row[1], row[2], row[4], row[3])
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    # Métodos relacionados con productos
    @classmethod
    def obtener_todos_los_productos(cls, db):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('obtener_productos')
                rows = cursor.fetchall()
                productos = [Producto(row[0], row[1], row[2], row[3])
                             for row in rows]
                return productos
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_todos_los_productos2(cls, db):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('obtener_productos')
                rows = cursor.fetchall()
                productos = [Producto(row[0], row[1], row[2], row[3])
                             for row in rows]
                productos_serializados = [
                    producto.to_dict() for producto in productos]
                # Retorna un diccionario con una clave "productos"
                return {"productos": productos_serializados}
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def agregar_producto(cls, db, nombre, imagen, precio):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('agregar_producto', (nombre, imagen, precio))
                db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_producto_por_id(cls, db, producto_id):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('obtener_producto_por_id', (producto_id,))
                row = cursor.fetchone()
                if row:
                    return Producto(row[0], row[1], row[2], row[3])
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizar_producto(cls, db, producto_id, nombre, imagen, precio):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('actualizar_producto',
                                (producto_id, nombre, imagen, precio))
                db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def eliminar_producto(cls, db, producto_id):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('eliminar_producto', (producto_id,))
                db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    # Métodos relacionados con usuarios
    @classmethod
    def obtener_todos_los_usuarios(cls, db):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('obtener_usuarios')
                rows = cursor.fetchall()
                usuarios = [User(row[0], row[1], row[4], row[2], row[3])
                            for row in rows]
                return usuarios
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def agregar_usuario(cls, db, username, password, fullname, usertype):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('sp_AddUser', (username,
                                password, fullname, usertype))
                db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_usuario_por_id(cls, db, usuario_id):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('obtener_usuario_por_id', (usuario_id,))
                row = cursor.fetchone()
                if row:
                    return User(row[0], row[1], None, row[2], row[3])
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizar_usuario(cls, db, usuario_id, username, password, fullname, usertype):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('actualizar_usuario', (usuario_id,
                                username, password, fullname, usertype))
                db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def eliminar_usuario(cls, db, usuario_id):
        try:
            with db.connection.cursor() as cursor:
                cursor.callproc('eliminar_usuario', (usuario_id,))
                db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def realizar_venta(cls, db, usuario_id, datos_venta):
        print("Inicio de la función realizar_venta")
        try:
            with db.connection.cursor() as cursor:
                venta_ids = []

                # Desempaquetar los datos de venta
                productos_ids = datos_venta['productos_ids']
                cantidades = datos_venta['cantidades']
                subtotales = datos_venta['subtotales']

                # Convertir listas a JSON
                productos_ids_json = json.dumps(productos_ids)
                cantidades_json = json.dumps(cantidades)
                subtotales_json = json.dumps(subtotales)

                for pProductoId, pCantidad, pSubtotal in zip(productos_ids, cantidades, subtotales):
                    print(
                        f"Producto ID: {pProductoId}, Cantidad: {pCantidad}, Subtotal: {pSubtotal}")

                    cursor.callproc('realizar_venta', [
                                    usuario_id, productos_ids_json, cantidades_json, subtotales_json])

                    result = cursor.fetchone()
                    print(f"Resultado de la venta: {result}")
                    venta_ids.append(result[0] if result else None)

                    cursor.nextset()  # Limpiar resultados pendientes

                db.connection.commit()

                if None in venta_ids:
                    raise ValueError("Error al obtener los IDs de venta")

                return venta_ids

        except Exception as ex:
            print(f"Error en realizar_venta: {ex}")
            raise Exception(ex)

    @classmethod
    def obtener_ventas_desde_bd(cls, db):
        try:
            with db.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM venta")
                rows = cursor.fetchall()
                ventas = [
                    Venta(row[0], row[1], row[2], row[3])
                    for row in rows
                ]
                return ventas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_detalles_venta(cls, db, venta_id):
        try:
            with db.connection.cursor() as cursor:
                query = """
                SELECT dv.id, dv.producto_id, p.nombre, p.precio, dv.cantidad, dv.subtotal
                FROM detalle_venta dv
                JOIN productos p ON dv.producto_id = p.id
                WHERE dv.venta_id = %s
                """
                cursor.execute(query, (venta_id,))
                rows = cursor.fetchall()

                detalles_venta = [
                    DetalleVenta(row[0], row[1], row[2],
                                 row[3], row[4], row[5])
                    for row in rows
                ]
                return detalles_venta
        except Exception as ex:
            raise Exception(
                "Error al obtener detalles de la venta: " + str(ex))
