# Nombre del Proyecto

La tienda de cafetería es un proyecto web diseñado para ofrecer a los usuarios una experiencia completa al explorar y comprar productos en línea desde la comodidad de sus dispositivos. Desarrollado con tecnologías como Flask, HTML, CSS y JavaScript, esta aplicación combina funcionalidad y estética para crear un entorno atractivo y fácil de usar.

La interfaz de usuario, construida con HTML y CSS, presenta un diseño limpio y moderno que refleja la esencia acogedora y reconfortante de una cafetería. El enfoque en la responsividad garantiza una experiencia uniforme en una variedad de dispositivos, desde computadoras de escritorio hasta tablets y teléfonos móviles, permitiendo a los usuarios explorar el catálogo de productos de manera fluida y eficiente.

La funcionalidad principal del sitio web se implementa mediante Flask, un marco web de Python que facilita el desarrollo rápido y eficiente de aplicaciones web. Flask gestiona las operaciones del lado del servidor, asegurando una comunicación eficiente entre el cliente y la base de datos. La arquitectura modular de Flask permite una fácil expansión de características, proporcionando una base sólida para futuras mejoras y actualizaciones.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:

- Python 
- MySQL
- Flask

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/HumbertoSuk/Flaskpy.git
    ```

2. Ve al directorio del proyecto:

    ```bash
    cd /Directorio de instalacion
    ```

3. Crea y activa un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate      # Para sistemas basados en Unix
    # o
    .\venv\Scripts\activate       # Para sistemas basados en Windows
    ```

4. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

5. Configura la base de datos:

    - Crea una base de datos MySQL.
    - Actualiza la configuración de la base de datos en el archivo `config.py`.
    - ejecutar los scripts en la BD o importa la BD  en la carpeta de BD
  

   ``` Bash
   
    pip install -r requirements.txt


   ```

6. Ejecuta la aplicación:

``` bash
class DevelopmentConfig():
    DEBUG = True
    SECRET_KEY = "qhrf$edjYTJ)*21nsThdK"
    MYSQL_HOST = "localhost" //Cambiar el host
    MYSQL_USER = "root" //Cambiuar el usuario
    MYSQL_PASSWORD = "Fidelio1524" //Contraseña
    MYSQL_DB = "store" 


config = {"development": DevelopmentConfig}

```

7. Accede a la aplicación desde tu navegador:

   Ejecutar el app.py

   ```bash
   python ./src/app.py

   ```

Accede a la aplicacion

   `http://127.0.0.1:5000/`

## Uso

Explora el Catálogo:

-  `Iniciar sesion:`  en el campo Usuario y Contraseña poner los correspondientes del usuario, si no se tiene por default es el usuario Admin y contra 123.
     - Si no coinciden te mandara un error.

  Si se hace correctamente se puede visualizar la pantalla principal, las opciones desplegadas dependeran del tipo de usuario, si eres administrador tienes acceso total y puedes editar, de lo contrario si eres solo usuario solo puedes visualizar la tienda, acerca de y la calculadora.
  
- `Calculadora:` La calculadora es visible en todos los lugares del sitio, al darle clic se despliega la calculadora, dar de nuevo clic se oculta, como se muestre dependera del tamaño de tu resolucion.

-  `catalogo:` en el apartado de catalogo tenemos el CRUD, es decir agregar, eliminar, mostrar y actualizar productos de nuestra tienda, se despliega en una lista todos los productos, en la parte superior tenemos el formulario para agregar uno, tenemos el nombre, la URL de la imagen y el precio; el ID se hace automaticamente ya que es un autoincrementable. Al darle a agregar se actualiza la tabla automaticamente. si no seleccionamos un campo marca un error y no deja agregar.
    - Tenemos en catalogo la columna de acciones, donde se puede eliminar y editar un producto ya hecho, si damos a eliminar se muestra 
      un mensaje para confirmar su eliminacion, si se da a cancelar se anula la accion, pero si se acepta se elimina permanentemente.
    - Para editar es un poco diferente asl dar editar se despliega un formulario donde se autocompleta con los datos del producto, si se       quiere editar se puede cambiar a un campo y darle a guardar cambios, donde se actualizara la pagina mostrando los nuevos datos 
      cargados 
- `usuarios:` Para el apartado de usuarios se usa el mismo funcionamiento, solo que este no muestra la contaseña por seguridad, puede 
   cambiar los datos en editar y en eliminar solo si se confirma el aceptar. 
- `tienda:` el apartado de tienda tiene los productos desplegados en tarjetas donde se pueden añadir en el carrito, cuando se agrega al carrito el resumen de la compra se actualiza, mostrando el producto y totall dependiendo de lo que se haya ingresado, finalizando la comprar se crea el ticket con el resumen de compra, tenemos que se limpia todo lo del resumen.
- La tienda no afecta a la base de datos ya que solo usa el almacenamiento local.
  
- `acerca de:` es un apartado que muestra el texto acerca de la tienda.

-`logout:` Para desloguearte solo se preciona desde cualquier seccion el boton de logout y se redirege a login.

## Contribuciones

Este proyecto se hizo bajo la colaboracion de Kevin Fausto estudiante de Ing. en sistemas computacionales.


