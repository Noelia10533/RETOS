SET GLOBAL event_scheduler = ON;

CREATE TABLE IF NOT EXISTS Auditoria_Tickets (
    id_auditoria  INT NOT NULL AUTO_INCREMENT,
    id_ticket  INT NOT NULL,
    estado_antiguo ENUM('Abierto','En proceso','Cerrado','Archivado') NOT NULL,
    estado_nuevo ENUM('Abierto','En proceso','Cerrado','Archivado') NOT NULL,
    fecha_cambio  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_auditoria),
    CONSTRAINT FK_ticket_auditoria
        FOREIGN KEY (id_ticket)
        REFERENCES Ticket(id_ticket)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)
ENGINE = InnoDB;

DELIMITER $$
CREATE PROCEDURE InsertarTicketManual (
    IN  p_correo  VARCHAR(50),
    IN  p_nombre  VARCHAR(50),
    IN  p_apellido1 VARCHAR(50),
    IN  p_apellido2 VARCHAR(50),
    IN  p_telefono VARCHAR(20),
    IN  p_titulo  VARCHAR(200),
    IN  p_descripcion VARCHAR(200),
    IN  p_id_empleado INT
)
MODIFIES SQL DATA
BEGIN
    DECLARE v_id_cliente INT DEFAULT NULL;
    DECLARE v_contador INT  DEFAULT 0;
    
    SELECT COUNT(*) INTO v_contador
    FROM clientes
    WHERE correo = p_correo;

    IF v_contador = 0 THEN
        INSERT INTO clientes (nombre, apellido1, apellido2, correo, telefono)
        VALUES (p_nombre, p_apellido1, p_apellido2, p_correo, p_telefono);
        SET v_id_cliente = LAST_INSERT_ID();
    ELSE
        SELECT id_cliente INTO v_id_cliente
        FROM clientes
        WHERE correo = p_correo;
    END IF;

    INSERT INTO ticket (id_cliente_fk2, id_empleado_fk2, titulo, descripcion, prioridad,  categoria,  estados,    fecha_hora_inicial)
    VALUES (v_id_cliente, p_id_empleado, p_titulo, p_descripcion, 'Media', 'Hardware', 'Abierto',  NOW());
    SET @ultimo_ticket = LAST_INSERT_ID();

END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER estado_ticket
    BEFORE UPDATE ON Ticket
    FOR EACH ROW
BEGIN
    IF NEW.estados = 'Cerrado' THEN
        IF NOT EXISTS (
            SELECT 1
            FROM mensaje
            WHERE id_ticket_fk1 = NEW.id_ticket 
        ) THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'No se puede cerrar un ticket sin historial de mensajes';
        END IF;
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER auditoria_cambio_estado
    AFTER UPDATE ON Ticket
    FOR EACH ROW
BEGIN
    IF OLD.estados <> NEW.estados THEN
        INSERT INTO Auditoria_Tickets (id_ticket, estado_antiguo, estado_nuevo, fecha_cambio)
        VALUES (OLD.id_ticket, OLD.estados, NEW.estados, NOW());
    END IF;
END $$

DELIMITER ;
DELIMITER $$
CREATE EVENT archivar_ticket
    ON SCHEDULE EVERY 1 DAY
    STARTS TIMESTAMP(CURRENT_DATE + INTERVAL 1 DAY, '03:00:00')
    DO
BEGIN
    UPDATE Ticket
    SET estados = 'Archivado'
    WHERE  estados = 'Cerrado'
      AND  fecha_hora_final <= NOW() - INTERVAL 1095 DAY;
END $$
DELIMITER ;
