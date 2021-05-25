# Creacion de la base de datos y dando uso a la base de datos
CREATE DATABASE Gimnasio; # Codigo para crear una base de datos
USE Gimnasio; # Usar la base de datos

#Eliminar Base de Datos
DROP DATABASE Gimnasio;

# Creacion de todas las tablas de la base de datos
# Tabla MEMBRESIA
CREATE TABLE MEMBRESIA (
	idMem INT AUTO_INCREMENT PRIMARY KEY,
	nombreMem VARCHAR(50) not null,
	duracion VARCHAR (15) not null, # De INT a VARCHAR
	precioMem FLOAT not null
);

# Tabla CLIENTES
CREATE TABLE CLIENTES (
	idClien INT AUTO_INCREMENT PRIMARY KEY,
    idMem INT not null,
	nombre VARCHAR(20) not null,
	apellidoPat VARCHAR(20) not null,
	apellidoMat VARCHAR(20) not null,
	apodo VARCHAR(20) not null,
    duracion INT not null,
    FOREIGN KEY (idMem) REFERENCES MEMBRESIA (idMem)
);

# Tabla PERMANENCIA
CREATE TABLE PERMANENCIA (
	idPerm INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE not null
);

# Tabla PERMANENCIA_DETALLADA
CREATE TABLE PERMANENCIA_DETALLADA (
	idPerm INT not null,
	idClien INT not null,
	fecha DATE not null,
	horaEntrada TIME not null,
	horaSalida TIME not null,
    FOREIGN KEY (idPerm) REFERENCES PERMANENCIA (idPerm),
	FOREIGN KEY (idClien) REFERENCES CLIENTES (idClien)
);

# Tabla PRODUCTOS
CREATE TABLE PRODUCTOS (
	idProd INT AUTO_INCREMENT PRIMARY KEY,
	nombreProd VARCHAR(50) not null,
	stock INT not null,
	precioProd FLOAT not null,
    estado_venta INT CHECK(estado_venta = 0 or estado_venta = 1)
);

# Tabla BEBIDAS
CREATE TABLE BEBIDAS (
	idProd INT not null,
	cantidadMililitros INT not null,
	FOREIGN KEY (idProd) REFERENCES PRODUCTOS (idProd)
);

# Tabla SUPLEMENTOS
CREATE TABLE SUPLEMENTOS (
	idProd INT not null,
	cantidadGramos INT not null,
	FOREIGN KEY (idProd) REFERENCES PRODUCTOS (idProd)
);

# Tabla ROPA
CREATE TABLE ROPA (
	idProd INT not null,
	tipo VARCHAR(20) not null,
	talla VARCHAR(20) not null,
	FOREIGN KEY (idProd) REFERENCES PRODUCTOS (idProd)
);

# Tabla COMPRA
CREATE TABLE COMPRA (
	idCom INT AUTO_INCREMENT PRIMARY KEY,
    idClien INT not null,
    fechaCom DATE not null,
    horaCom TIME not null,
	totalCom FLOAT not null,
    FOREIGN KEY (idClien) REFERENCES CLIENTES (idClien)
);

# Tabla DETALLES_COMPRAS
CREATE TABLE DETALLES_COMPRAS (
	idCom INT not null,
	idProd INT not null,
	nombreProd VARCHAR(50) not null,
    precioProd FLOAT not null,
	cantidadCom INT not null,
	subTotalCom FLOAT not null,
	FOREIGN KEY (idCom) REFERENCES COMPRA (idCom),
	FOREIGN KEY (idProd) REFERENCES PRODUCTOS (idProd)
);

# Tabla PROVEEDOR
CREATE TABLE PROVEEDOR (
	idProv INT AUTO_INCREMENT PRIMARY KEY,
	nombreProv VARCHAR(50) not null,
	telefono VARCHAR(10) not null
);

# Tabla SUMINISTRA
CREATE TABLE SUMINISTRA (
	idSum INT AUTO_INCREMENT PRIMARY KEY,
	idProv INT not null,
    fechaSum DATE not null,
    horaSum TIME not null,
    totalSum FLOAT not null,
	FOREIGN KEY (idProv) REFERENCES PROVEEDOR (idProv)
);

# Tabla SUMINISTRA
CREATE TABLE DETALLES_SUMINISTRA (
	idSum INT not null,
	idProd INT not null,
	nombreProd VARCHAR(20) not null,
    precioSum FLOAT not null,
	cantidadSum INT not null,
	subTotalSum FLOAT not null,
	FOREIGN KEY (idSum) REFERENCES SUMINISTRA (idSum),
	FOREIGN KEY (idProd) REFERENCES PRODUCTOS (idProd)
);