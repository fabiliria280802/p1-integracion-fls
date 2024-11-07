-- Se crea el schema
CREATE SCHEMA `schemas_sgp_sfp` ;

-- Tabla de Proveedores
CREATE TABLE Proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(50) NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    email VARCHAR(100) UNIQUE
);

-- Tabla de Facturas
CREATE TABLE Facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_proveedor INT,
    monto DECIMAL(10, 2) NOT NULL,
    estado ENUM('pendiente', 'pagada', 'rechazada') DEFAULT 'pendiente',
    fecha_creacion DATE NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor)
);

-- Tabla de Pagos
CREATE TABLE Pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_factura INT,
    fecha_pago DATE,
    estado ENUM('completado', 'pendiente', 'fallido') DEFAULT 'pendiente',
    FOREIGN KEY (id_factura) REFERENCES Facturas(id_factura)
);
