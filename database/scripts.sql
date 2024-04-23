-- Crear la base de datos "store"
CREATE SCHEMA store;

-- Conectar a la base de datos "store"
USE store;



-- Tablas --------------------------------------------------------------------------------------------------------------------------------------

-- Crear la tabla "users"
CREATE TABLE users (
    id smallint unsigned NOT NULL AUTO_INCREMENT,
    username varchar(20) NOT NULL,
    password char(102) NOT NULL,
    fullname varchar(50),
    usertype tinyint NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Tabla de productos
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    imagen VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);

CREATE TABLE venta (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_id SMALLINT UNSIGNED NOT NULL,  
    total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES users(id)
);

CREATE TABLE detalle_venta (
    id SERIAL PRIMARY KEY,
    venta_id INT UNSIGNED NOT NULL,
    producto_id INT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES venta(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);




-- Procedimientos -----------------------------------------------------------------------------------------

-- Obtener usuarios
DELIMITER //

CREATE PROCEDURE obtener_usuarios()
BEGIN
    SELECT id, username, password, fullname, usertype FROM users;
END //
DELIMITER ;

-- Obtener usuarios por id
DELIMITER //
CREATE PROCEDURE obtener_usuario_por_id(in usuario_id INT)
BEGIN
    SELECT * FROM users WHERE id = usuario_id;
END //
DELIMITER ;

-- Agregar usuario
DELIMITER //
CREATE PROCEDURE sp_AddUser(IN pUserName VARCHAR(20), IN pPassword VARCHAR(102), IN pFullName VARCHAR(50), IN pUserType tinyint)
BEGIN
    DECLARE hashedPassword VARCHAR(255);
    SET hashedPassword = SHA2(pPassword, 256);
    
    INSERT INTO users (username, password, fullname, usertype)
    VALUES (pUserName, hashedPassword, pFullName, pUserType);
END //
DELIMITER ;


-- Actualizar usuario 
DELIMITER //
CREATE PROCEDURE actualizar_usuario(
    IN usuario_id INT,
    IN username VARCHAR(20),
    IN password VARCHAR(50),
    IN fullname VARCHAR(50),
    IN usertype TINYINT
)
BEGIN
    DECLARE new_hashed_password CHAR(102);

    -- Verifica si se proporciona una nueva contraseña
    IF password IS NOT NULL THEN
        -- Hash de la nueva contraseña
        SET new_hashed_password = SHA2(password, 256);
    ELSE
        -- Mantén la contraseña existente
        SET new_hashed_password = (SELECT password FROM users WHERE id = usuario_id);
    END IF;

    -- Actualiza la información del usuario
    UPDATE users
    SET username = username,
        password = new_hashed_password,
        fullname = fullname,
        usertype = usertype
    WHERE id = usuario_id;
END //
DELIMITER;


-- Eliminar usuarios

DELIMITER //

CREATE PROCEDURE eliminar_usuario(in usuario_id INT)
BEGIN
    DELETE FROM users WHERE id = usuario_id;
END //
DELIMITER ;

-- Obtener productos
DELIMITER //
CREATE PROCEDURE obtener_productos()
BEGIN
    SELECT * FROM productos;
END //
DELIMITER ;

-- Obtener un producto especifico por id
DELIMITER //

CREATE PROCEDURE obtener_producto_por_id(in producto_id INT)
BEGIN
    SELECT * FROM productos WHERE id = producto_id;
END //
DELIMITER ;

-- Agregar producto

DELIMITER //

CREATE PROCEDURE agregar_producto(in nombre VARCHAR(255), in imagen VARCHAR(255), in precio DECIMAL(10, 2))
BEGIN
    INSERT INTO productos (nombre, imagen, precio) VALUES (nombre, imagen, precio);
END //
DELIMITER ;

-- actualizar un producto
DELIMITER //

CREATE PROCEDURE actualizar_producto(in producto_id INT, in nombre VARCHAR(255), in imagen VARCHAR(255), in precio DECIMAL(10, 2))
BEGIN
    UPDATE productos SET nombre = nombre, imagen = imagen, precio = precio WHERE id = producto_id;
END //
DELIMITER ;

-- Eliminar un producto
DELIMITER //

CREATE PROCEDURE eliminar_producto(in producto_id INT)
BEGIN
    DELETE FROM productos WHERE id = producto_id;
END //

DELIMITER ;

-- Procedimiento para veridicar contraseña 
DELIMITER $$

CREATE PROCEDURE `sp_verifyIdentity`(IN pUsername VARCHAR(20), IN pPlainTextPassword VARCHAR(20))
BEGIN
    DECLARE storedPassword VARCHAR(255);

    SELECT password INTO storedPassword FROM users
    WHERE username = pUsername COLLATE utf8mb4_unicode_ci;

    IF storedPassword IS NOT NULL AND storedPassword = SHA2(pPlainTextPassword, 256) THEN
        SELECT id, username, storedPassword, fullname, usertype FROM users
        WHERE username = pUsername COLLATE utf8mb4_unicode_ci;
    ELSE
        SELECT NULL;
    END IF;
END$$

DELIMITER ;


DELIMITER //
CREATE PROCEDURE realizar_venta(
    IN pUsuarioId INT,
    IN pDatosVenta JSON
)
BEGIN
    DECLARE ventaId INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE producto_id INT; -- Declarar la variable producto_id
    DECLARE cantidad INT;
    DECLARE precio_unitario DECIMAL(10, 2);

    DECLARE cur CURSOR FOR 
        SELECT producto_id, cantidad, precio_unitario 
        FROM JSON_TABLE(pDatosVenta, '$[*]' 
            COLUMNS (
                producto_id INT PATH '$.producto_id', 
                cantidad INT PATH '$.cantidad', 
                precio_unitario DECIMAL(10, 2) PATH '$.precio_unitario')
        ) AS detalles_venta;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Iniciar transacción
    START TRANSACTION;

    -- Insertar la venta en la tabla 'venta'
    INSERT INTO venta (usuario_id, total) VALUES (pUsuarioId, 0);
    SET ventaId = LAST_INSERT_ID();

    -- Iterar sobre los detalles de la venta
    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO producto_id, cantidad, precio_unitario;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Insertar el detalle de la venta en la tabla 'detalle_venta'
        INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal) 
        VALUES (ventaId, producto_id, cantidad, precio_unitario, cantidad * precio_unitario);
    END LOOP;
    CLOSE cur;

    -- Calcular el total de la venta
    UPDATE venta SET total = (SELECT SUM(subtotal) FROM detalle_venta WHERE venta_id = ventaId) WHERE id = ventaId;

    -- Confirmar transacción
    COMMIT;
END;
//

DELIMITER ;




call sp_AddUser("admin","123","juan perez",1);
call sp_AddUser("user","123","Usuario",2);
call sp_verifyIdentity("admin","123");
