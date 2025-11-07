-- Tabla para el enum EstadoPedido
CREATE TABLE EstadoPedido (
    id SERIAL PRIMARY KEY,
    estado VARCHAR(20) NOT NULL UNIQUE
);

-- Insertar valores del enum
INSERT INTO EstadoPedido (estado) VALUES 
('PENDIENTE'),
('CONFIRMADO'),
('EN_PROCESO'),
('ENVIADO'),
('ENTREGADO'),
('CANCELADO');

-- Tabla para el enum MetodoPago
CREATE TABLE MetodoPago (
    id SERIAL PRIMARY KEY,
    metodo VARCHAR(30) NOT NULL UNIQUE
);

-- Insertar valores del enum
INSERT INTO MetodoPago (metodo) VALUES 
('TARJETA_CREDITO'),
('TARJETA_DEBITO'),
('TRANSFERENCIA_BANCARIA');

-- Tabla para el enum EstadoPago
CREATE TABLE EstadoPago (
    id SERIAL PRIMARY KEY,
    estado VARCHAR(20) NOT NULL UNIQUE
);

-- Insertar valores del enum
INSERT INTO EstadoPago (estado) VALUES 
('PENDIENTE'),
('PROCESANDO'),
('COMPLETADO'),
('RECHAZADO'),
('REEMBOLSADO');

-- Tabla para el enum EstadoProducto
CREATE TABLE EstadoProducto (
    id SERIAL PRIMARY KEY,
    estado VARCHAR(20) NOT NULL UNIQUE
);

-- Insertar valores del enum
INSERT INTO EstadoProducto (estado) VALUES 
('DISPONIBLE'),
('AGOTADO'),
('DESCONTINUADO'),
('PROMOCION');

-- Tabla Cliente
CREATE TABLE Cliente (
    id VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT
);

-- Tabla Producto
CREATE TABLE Producto (
    id VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    estado_id INT NOT NULL,
    CONSTRAINT fk_estado FOREIGN KEY (estado_id) REFERENCES EstadoProducto(id)
);


-- Tabla Pedido
CREATE TABLE Pedido (
    id VARCHAR(50) PRIMARY KEY,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    cliente_id VARCHAR(50) NOT NULL,
    CONSTRAINT fk_estado_pedido FOREIGN KEY (estado_id) REFERENCES EstadoPedido(id),
    CONSTRAINT fk_cliente_pedido FOREIGN KEY (cliente_id) REFERENCES Cliente(id)
);


-- Tabla ItemPedido
CREATE TABLE ItemPedido (
    id VARCHAR(50) PRIMARY KEY,
    pedido_id VARCHAR(50) NOT NULL,
    producto_id VARCHAR(50) NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_pedido_item FOREIGN KEY (pedido_id) REFERENCES Pedido(id),
    CONSTRAINT fk_producto_item FOREIGN KEY (producto_id) REFERENCES Producto(id)
);


-- Tabla Pago
CREATE TABLE Pago (
    id VARCHAR(50) PRIMARY KEY,
    monto DECIMAL(10,2) NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metodo_id INT NOT NULL,
    estado_id INT NOT NULL,
    pedido_id VARCHAR(50) NOT NULL,
    CONSTRAINT fk_metodo_pago FOREIGN KEY (metodo_id) REFERENCES MetodoPago(id),
    CONSTRAINT fk_estado_pago FOREIGN KEY (estado_id) REFERENCES EstadoPago(id),
    CONSTRAINT fk_pedido_pago FOREIGN KEY (pedido_id) REFERENCES Pedido(id)
);
