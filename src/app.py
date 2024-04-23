from flask import Flask, redirect, render_template, request, url_for, flash, abort, jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from config import config
from models.ModelUsers import ModelUsers
from models.entities.users import User


app = Flask(__name__)
app.config.from_object(config['development'])
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUsers.get_by_id(db, id)


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.usertype != 1:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view

# rest API webservice

# Ruta para obtener todos los productos


@app.route('/api/productos', methods=['GET'])
def obtener_productosapi():
    try:
        productos = ModelUsers.obtener_todos_los_productos(db)
        productos_serializados = [producto.to_dict() for producto in productos]
        return jsonify(productos_serializados), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

# Ruta para agregar un producto


@app.route('/api/productos', methods=['POST'])
def agregar_productoapi():
    try:
        data = request.json
        nombre = data.get('nombre')
        imagen = data.get('imagen_url')
        precio = data.get('precio')

        if nombre and imagen and precio:
            ModelUsers.agregar_producto(db, nombre, imagen, precio)
            return jsonify({"mensaje": "Producto agregado correctamente"}), 201
        else:
            return jsonify({"error": "Datos incompletos"}), 400
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

# Ruta para eliminar un producto


@app.route('/api/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_productoapi(producto_id):
    try:
        ModelUsers.eliminar_producto(db, producto_id)
        return jsonify({"mensaje": "Producto eliminado correctamente"}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

# Ruta para actualizar un producto


@app.route('/api/productos/<int:producto_id>', methods=['PUT'])
def actualizar_productoapi(producto_id):
    try:
        data = request.json
        nuevo_nombre = data.get('nombre')
        nueva_imagen = data.get('imagen_url')
        nuevo_precio = data.get('precio')

        if nuevo_nombre and nueva_imagen and nuevo_precio:
            # Actualizar el producto en la base de datos
            ModelUsers.actualizar_producto(
                db, producto_id, nuevo_nombre, nueva_imagen, nuevo_precio)
            return jsonify({"mensaje": "Producto actualizado correctamente"}), 200
        else:
            return jsonify({"error": "Datos incompletos"}), 400
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@app.route("/")
def index():
    return redirect("login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        print(
            f"Intento de inicio de sesión: Usuario - {usuario}, Contraseña - {contrasena}")

        user = User(0, usuario, contrasena, 0)
        logged_user = ModelUsers.login(db, user)

        if logged_user is not None:
            print(f"Usuario autenticado: {logged_user}")
            login_user(logged_user)
            return redirect(url_for("principal"))
        else:
            flash("Acceso rechazado. Verifica usuario y contraseña.")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")


@app.route("/principal")
@login_required
def principal():
    return render_template("main.html")


@app.route("/acerca")
@login_required
def acerca():
    return render_template("Acerca_de.html")


@app.route("/catalogo")
@login_required
@admin_required
def catalogo():
    return render_template("catalogo.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/agregar_producto", methods=["POST"])
@login_required
@admin_required
def agregar_producto():
    if request.method == "POST":
        nombre = request.form['nombre']
        imagen = request.form['imagen']
        precio = request.form['precio']
        try:
            ModelUsers.agregar_producto(db, nombre, imagen, precio)
            flash("Producto agregado correctamente")
        except Exception as ex:
            flash(f"Error al agregar el producto: {ex}")
    return redirect(url_for("catalogo"))


@app.route("/editar_producto/<int:id>", methods=["POST"])
@login_required
@admin_required
def editar_producto(id):
    if request.method == "POST":
        nuevo_nombre = request.form.get("nombre")
        nueva_imagen = request.form.get("imagen")
        nuevo_precio = request.form.get("precio")
        ModelUsers.actualizar_producto(
            db, id, nuevo_nombre, nueva_imagen, nuevo_precio)
        return jsonify(success=True)
    return jsonify(success=False)


@app.route("/eliminar_producto/<int:id>", methods=["POST"])
@login_required
@admin_required
def eliminar_producto(id):
    try:
        ModelUsers.eliminar_producto(db, id)
        flash("Producto eliminado correctamente")
    except Exception as ex:
        flash(f"Error al eliminar el producto: {ex}")
    return redirect(url_for("catalogo"))


@app.route('/mostrar_productos')
def mostrar_productos():
    try:
        productos = ModelUsers.obtener_todos_los_productos(db)
        return render_template('catalogo.html', productos=productos)
    except Exception as ex:
        flash(f"Error: {ex}")
        return redirect(url_for("catalogo"))


@app.route('/obtener_productos', methods=['GET'])
def obtener_productos():
    try:
        productos = ModelUsers.obtener_todos_los_productos(db)
        # Estructurar los datos como un diccionario con una clave 'productos'
        return jsonify({"productos": productos})
    except Exception as ex:
        return jsonify(error=str(ex)), 500


@app.route("/mostrar_usuarios")
@login_required
@admin_required
def mostrar_usuarios():
    try:
        usuarios = ModelUsers.obtener_todos_los_usuarios(db)
        # Excluye la contraseña al pasar los datos a la plantilla
        usuarios_data = [
            {
                'id': usuario.id,
                'username': usuario.username,
                'fullname': usuario.fullname,
                'usertype': usuario.password,
                'password': usuario.usertype
            }
            for usuario in usuarios
        ]
        return render_template('usuarios.html',  usuarios=usuarios_data)
    except Exception as ex:
        flash(f"Error: {ex}")
        return redirect(url_for("principal"))


@app.route("/agregar_usuario", methods=["POST"])
@login_required
@admin_required
def agregar_usuario():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        usertype = request.form['usertype']
        try:
            ModelUsers.agregar_usuario(
                db, username, password, fullname, usertype)
            flash("Usuario agregado correctamente")
        except Exception as ex:
            flash(f"Error al agregar el usuario: {ex}")
    return redirect(url_for("mostrar_usuarios"))


@app.route("/editar_usuario/<int:usuario_id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_usuario(usuario_id):
    try:
        if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password')
            fullname = request.form.get('fullname')
            usertype = request.form.get('usertype')

            if username is not None and password is not None and fullname is not None and usertype is not None:
                ModelUsers.actualizar_usuario(
                    db, usuario_id, username, password, fullname, usertype)
                flash("Usuario actualizado correctamente")
            else:
                flash("Datos incompletos")
            return redirect(url_for("mostrar_usuarios"))

        # For GET requests, return the existing user information
        user = ModelUsers.obtener_usuario_por_id(db, usuario_id)
        if user:
            return render_template("edit_user.html", usuario=user)
        else:
            flash("Usuario no encontrado")
            return redirect(url_for("mostrar_usuarios"))
    except Exception as ex:
        flash(f"Error: {ex}")
        return redirect(url_for("mostrar_usuarios"))


@app.route("/eliminar_usuario/<int:id>", methods=["POST"])
@login_required
@admin_required
def eliminar_usuario(id):
    try:
        ModelUsers.eliminar_usuario(db, id)
        flash("Usuario eliminado correctamente")
    except Exception as ex:
        flash(f"Error al eliminar el usuario: {ex}")
    return redirect(url_for("mostrar_usuarios"))


@app.route("/tienda")
@login_required
def tienda():
    try:
        productos = ModelUsers.obtener_todos_los_productos(db)
        return render_template("tienda.html", productos=productos)
    except Exception as ex:
        flash(f"Error: {ex}")
        return redirect(url_for("principal"))


@app.route('/ticket')
@login_required
def ticket():
    # Aquí deberías pasar los datos necesarios para el ticket, por ejemplo, los elementos del carrito.
    return render_template('ticket.html')


@app.route("/realizar_venta", methods=["POST"])
@login_required
def realizar_venta():
    try:
        usuario_id = current_user.id
        datos_venta = request.json['datosCompra']
        print("Inicio de la función realizar_venta")

        # Obtener los IDs de producto, cantidad y subtotal en listas separadas
        productos_ids = [int(venta['id_producto']) for venta in datos_venta]
        cantidades = [int(venta['cantidad']) for venta in datos_venta]
        subtotales = [float(venta['subtotal']) for venta in datos_venta]

        # Empaquetar los datos en un solo objeto
        datos_venta_empaquetados = {
            'productos_ids': productos_ids,
            'cantidades': cantidades,
            'subtotales': subtotales
        }

        # Llamar al procedimiento realizar_venta con los datos de venta empaquetados
        venta_ids = ModelUsers.realizar_venta(
            db, usuario_id, datos_venta_empaquetados)

        print("Venta finalizada:", venta_ids)
        return jsonify({"venta_ids": venta_ids}), 200

    except Exception as e:
        print("Error al realizar la venta:", str(e))
        return jsonify({"error": "Ocurrió un error al procesar la venta"}), 500


@app.route('/ventas')
@login_required
@admin_required
def ventas():
    try:
        ventas = ModelUsers.obtener_ventas_desde_bd(db)
        return render_template('ventas.html', ventas=ventas)
    except Exception as ex:
        flash(f"Error: {ex}")
        return redirect(url_for("principal"))


@app.route("/detalle_venta/<int:venta_id>")
@login_required
def detalle_venta(venta_id):
    try:
        print("Solicitud para obtener detalles de venta para la venta ID:", venta_id)
        detalles_venta = ModelUsers.obtener_detalles_venta(db, venta_id)
        detalles_serializados = [{
            'id': detalle.id,
            'producto_id': detalle.producto_id,
            'nombre_producto': detalle.nombre_producto,
            'precio_unitario': detalle.precio_unitario,
            'cantidad': detalle.cantidad,
            'subtotal': detalle.subtotal
        } for detalle in detalles_venta]
        print("Detalles de venta obtenidos:", detalles_serializados)
        return jsonify({"detalle_venta": detalles_serializados})
    except Exception as ex:
        print("Error al obtener detalles de la venta:", str(ex))
        return jsonify(error=str(ex)), 500


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True, port=5001)
