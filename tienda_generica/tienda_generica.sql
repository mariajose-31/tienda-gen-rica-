CREATE DATABASE tienda_generica;
USE tienda_generica;

-- Tabla USUARIOS (con cédula como identificador)
CREATE TABLE usuarios (
    cedula VARCHAR(20) PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla CLIENTES
CREATE TABLE clientes (
    cedula VARCHAR(20) PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    direccion VARCHAR(100),
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- Tabla PROVEEDORES
CREATE TABLE proveedores (
    nit BIGINT PRIMARY KEY,
    nombre_proveedor VARCHAR(100) NOT NULL,
    direccion VARCHAR(100),
    telefono VARCHAR(20),
    ciudad VARCHAR(50)
);

-- Tabla PRODUCTOS (según estructura del CSV)
CREATE TABLE productos (
    codigo_producto BIGINT PRIMARY KEY,
    nombre_producto VARCHAR(50) NOT NULL,
    nitproveedor BIGINT NOT NULL,
    precio_compra DOUBLE NOT NULL,
    ivacompra DOUBLE NOT NULL,
    precio_venta DOUBLE NOT NULL,
    FOREIGN KEY (nitproveedor) REFERENCES proveedores(nit)
);

-- Tabla VENTAS (con consecutivo)
CREATE TABLE ventas (
    codigo_venta INT AUTO_INCREMENT PRIMARY KEY,
    cedula_cliente VARCHAR(20) NOT NULL,
    cedula_usuario VARCHAR(20) NOT NULL,
    valor_total DOUBLE NOT NULL,
    valor_iva DOUBLE NOT NULL,
    valor_total_con_iva DOUBLE NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cedula_cliente) REFERENCES clientes(cedula),
    FOREIGN KEY (cedula_usuario) REFERENCES usuarios(cedula)
);

-- Tabla DETALLE VENTAS
CREATE TABLE detalleVentas (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    codigo_venta INT NOT NULL,
    codigo_producto BIGINT NOT NULL,
    cantidad INT NOT NULL,
    valor_unitario DOUBLE NOT NULL,
    valor_total DOUBLE NOT NULL,
    FOREIGN KEY (codigo_venta) REFERENCES ventas(codigo_venta),
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo_producto)
);

-- Usuario inicial por defecto
INSERT INTO usuarios (cedula, nombre_completo, correo, usuario, password)
VALUES ('0000000', 'Administrador Inicial', 'admin@tienda.com', 'admininicial', 'admin123456');

-- Datos de ejemplo para proveedores (necesarios para cargar productos CSV)
INSERT INTO proveedores (nit, nombre_proveedor, direccion, telefono, ciudad) VALUES
(1, 'Distribuidora A', 'Cra 10 #20-30', '3001234567', 'Bogotá'),
(2, 'Distribuidora B', 'Calle 5 #15-20', '3102345678', 'Medellín'),
(3, 'Distribuidora C', 'Av 68 #40-50', '3203456789', 'Cali'),
(4, 'Distribuidora D', 'Cra 15 #100-20', '3154567890', 'Barranquilla'),
(5, 'Distribuidora E', 'Calle 80 #30-40', '3005678901', 'Bucaramanga');

-- Clientes de ejemplo
INSERT INTO clientes (cedula, nombre_completo, direccion, telefono, correo) VALUES
('1001', 'Juan Pérez', 'Cra 10 #20-30', '3001234567', 'juan@email.com'),
('1002', 'Paula Pérez', 'Cra 25 #73-15', '3138874916', 'paula@gmail.com'),
('1003', 'Evelin Sánchez', 'Calle 25 #13-10', '3125719231', 'evelin@gmail.com');