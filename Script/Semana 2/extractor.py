import mysql.connector
import xml.etree.ElementTree as ET
from datetime import datetime
from funciones_sla_enfado import calcular_alerta_sla, detectar_enfado

log = open("extractor_log.txt", "a", encoding="utf-8")
contador = 0
fallidos  = 0

cursor = None
connection = None
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="hermesadmin",
        password="1234",
        database="Hermes_IT"
    )
  
    cursor = connection.cursor()
  
    cursor.execute("""SELECT T.id_ticket, T.titulo, T.descripcion, T.fecha_hora_inicial, T.categoria, T.fecha_hora_final, T.id_cliente_fk2, T.id_empleado_fk2, C.id_cliente, C.nombre, C.apellido1, C.apellido2, C.correo, C.telefono, O.id_empleado, O.nombre, O.correo, O.id_departamento_fk1
    FROM ticket T JOIN clientes C
    on T.id_cliente_fk2 = C.id_cliente
    JOIN operadores O
    on T.id_empleado_fk2 = O.id_empleado
    WHERE T.estados = 'Archivado'""")
    
    registro = cursor.fetchall()
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
    log.write(f"[{datetime.now()}] ERROR de conexión: {err}\n")
else:
    for ticket in registro:
        T_id_ticket, T_titulo, T_descripcion, T_fecha_hora_inicial, T_categoria, T_fecha_hora_final, T_id_cliente_fk2, T_id_empleado_fk2, C_id_cliente, C_nombre, C_apellido1, C_apellido2, C_correo, C_telefono, O_id_empleado, O_nombre, O_correo, O_id_departamento_fk1 = ticket
        try:
        
        
            cursor.execute(f"""
            SELECT texto, fecha_hora_enviado, id_cliente_fk1, id_empleado_fk1
            FROM Mensaje
            WHERE id_ticket_fk1 = {T_id_ticket} 
            ORDER BY fecha_hora_enviado ASC
            """)
            mensajes = cursor.fetchall()


            raiz = ET.Element("ticket")
            raiz.set("id", str(T_id_ticket))

            textos_cliente = []
            for tupla in mensajes:
                texto_mensaje, fecha_mensaje, id_cli_mensaje, id_emp_mensaje = tupla
                if id_cli_mensaje is not None:
                    textos_cliente.append(texto_mensaje)

            if detectar_enfado(textos_cliente):
                raiz.set("cliente_enfadado", "si")
                

            etiqueta_titulo = ET.Element("titulo")
            etiqueta_titulo.text = T_titulo
            raiz.append(etiqueta_titulo)

            etiqueta_descripcion = ET.Element("descripcion")
            etiqueta_descripcion.text = T_descripcion
            raiz.append(etiqueta_descripcion)

            etiqueta_fecha_hora_inicial = ET.Element("fecha_hora_inicial")
            etiqueta_fecha_hora_inicial.text = str(T_fecha_hora_inicial)
            raiz.append(etiqueta_fecha_hora_inicial)

            etiqueta_categoria = ET.Element("categoria")
            etiqueta_categoria.text = T_categoria
            raiz.append(etiqueta_categoria)

            etiqueta_fecha_hora_final = ET.Element("fecha_hora_final")
            etiqueta_fecha_hora_final.text = str(T_fecha_hora_final)
            raiz.append(etiqueta_fecha_hora_final)
    
            etiqueta_id_cliente_fk2 = ET.Element("id_cliente_fk2")
            etiqueta_id_cliente_fk2.text = str(T_id_cliente_fk2)
            raiz.append(etiqueta_id_cliente_fk2)

            etiqueta_id_empleado_fk2 = ET.Element("id_empleado_fk2")
            etiqueta_id_empleado_fk2.text = str(T_id_empleado_fk2)
            raiz.append(etiqueta_id_empleado_fk2)
        
            dias_retraso = calcular_alerta_sla(T_fecha_hora_inicial, T_fecha_hora_final)
            if dias_retraso is not None:
                etiqueta_sla = ET.Element("alerta_sla")
                etiqueta_sla.set("dias_retraso", str(dias_retraso))
                etiqueta_sla.text = f"Cerrado con {dias_retraso} días de retraso"
                raiz.append(etiqueta_sla)
            
            etiqueta_cliente = ET.Element("cliente")
 
            etiqueta_nombre_cli = ET.Element("nombre")
            etiqueta_nombre_cli.text = C_nombre
            etiqueta_cliente.append(etiqueta_nombre_cli)
 
            etiqueta_apellidos_cli = ET.Element("apellido1")
            etiqueta_apellidos_cli.text = C_apellido1
            etiqueta_cliente.append(etiqueta_apellidos_cli)
            
            etiqueta_apellidos_cli2 = ET.Element("apellido2")
            etiqueta_apellidos_cli2.text = C_apellido2
            etiqueta_cliente.append(etiqueta_apellidos_cli2)
 
            etiqueta_correo_cli = ET.Element("correo")
            etiqueta_correo_cli.text = C_correo
            etiqueta_cliente.append(etiqueta_correo_cli)
 
            etiqueta_telefono_cli = ET.Element("telefono")
            etiqueta_telefono_cli.text = str(C_telefono)
            etiqueta_cliente.append(etiqueta_telefono_cli)
    
            raiz.append(etiqueta_cliente)
    
            etiqueta_operador = ET.Element("operador")
            if O_nombre is not None:  
                etiqueta_nombre_op = ET.Element("nombre")
                etiqueta_nombre_op.text = O_nombre
                etiqueta_operador.append(etiqueta_nombre_op)
                etiqueta_correo_op = ET.Element("correo")
                etiqueta_correo_op.text = O_correo
                etiqueta_operador.append(etiqueta_correo_op)
            raiz.append(etiqueta_operador)

            etiqueta_historial = ET.Element("historial")
            for tupla in mensajes:
                texto_mensaje, fecha_mensaje, id_cli_mensaje, id_emp_mensaje = tupla
                etiqueta_mensaje = ET.Element("mensaje")
                if id_cli_mensaje is not None:
                    autor = "cliente"
                else:
                    autor = "operador"
                etiqueta_mensaje.set("autor", autor)
                etiqueta_mensaje.set("fecha", str(fecha_mensaje)) 
                etiqueta_mensaje.text = texto_mensaje
                etiqueta_historial.append(etiqueta_mensaje)
            raiz.append(etiqueta_historial)


            ET.indent(raiz, space="    ")
            xml_texto = ET.tostring(raiz, encoding="unicode")
            xml_texto = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_texto

            ruta = f"ticket_{T_id_ticket}.xml"
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(xml_texto)

            contador += 1   

        except:
            fallidos += 1
            log.write(f"[{datetime.now()}] ERROR con el ticket {T_id_ticket}\n")
 

if cursor is not None:
    cursor.close()
if connection is not None and connection.is_connected():
    connection.close()
 

log.write(f"[{datetime.now()}] XML generados: {contador} y fallidos: {fallidos}\n")
log.close()
