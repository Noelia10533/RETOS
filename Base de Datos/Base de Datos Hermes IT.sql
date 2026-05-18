CREATE DATABASE IF NOT EXISTS Hermes_IT;
USE Hermes_IT;


CREATE TABLE Clientes (
    id_cliente INT,
    nombre VARCHAR(50) NOT NULL,
    apellido1 VARCHAR(50) NOT NULL,
    apellido2 VARCHAR(50) NOT NULL,
    correo VARCHAR(50) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,/*PONEMOS 20 PORQUE FAKE.number() nos puede dar como máximo  20 caracteres*/
    PRIMARY KEY(id_cliente)
)
ENGINE = InnoDB;


CREATE TABLE Departamento (
    id_departamento INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(50) NOT NULL,
    PRIMARY KEY(id_departamento)
)
ENGINE = InnoDB;


CREATE TABLE Operadores (
    id_empleado INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    correo VARCHAR(50) NOT NULL UNIQUE,
    id_departamento_fk1 INT NOT NULL,
    PRIMARY KEY(id_empleado),
    CONSTRAINT FK_departamento_operador
        FOREIGN KEY(id_departamento_fk1)
        REFERENCES Departamento(id_departamento)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
)
ENGINE = InnoDB;


CREATE TABLE Ticket(
    id_ticket INT NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    fecha_hora_inicial DATETIME NOT NULL,
    categoria ENUM('Hardware','Software','Redes','Seguridad') NOT NULL,
    prioridad ENUM('Baja','Media','Alta','Critica') NOT NULL,
    estados ENUM('Abierto','En proceso','Cerrado','Archivado') NOT NULL,
    fecha_hora_final DATETIME,
    id_cliente_fk2 INT NOT NULL,
    id_empleado_fk2 INT,
    PRIMARY KEY(id_ticket),
    CONSTRAINT FK_empleado_ticket
        FOREIGN KEY(id_empleado_fk2)
        REFERENCES Operadores(id_empleado)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT FK_cliente_ticket
        FOREIGN KEY(id_cliente_fk2)
        REFERENCES Clientes(id_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)
ENGINE = InnoDB;


CREATE TABLE Mensaje(
    id_mensaje INT NOT NULL,
    texto VARCHAR(200) NOT NULL,
    fecha_hora_enviado DATETIME NOT NULL,
    id_cliente_fk1 INT,
    id_empleado_fk1 INT,
    id_ticket_fk1 INT NOT NULL,
    PRIMARY KEY(id_mensaje),
    CONSTRAINT CHK_autoria_mensaje CHECK (
        (id_cliente_fk1 IS NOT NULL AND id_empleado_fk1 IS NULL)
        OR
        (id_cliente_fk1 IS NULL AND id_empleado_fk1 IS NOT NULL)
    ),
    CONSTRAINT FK_ticket_mensaje
        FOREIGN KEY(id_ticket_fk1)
        REFERENCES Ticket(id_ticket)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT FK_empleado_mensaje
        FOREIGN KEY(id_empleado_fk1)
        REFERENCES Operadores(id_empleado),
    CONSTRAINT FK_mensaje_cliente
        FOREIGN KEY(id_cliente_fk1)
        REFERENCES Clientes(id_cliente)
)
ENGINE = InnoDB;

