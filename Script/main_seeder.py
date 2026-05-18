import random
from conexion_base_datos import conectar_bd
from constantes import NUM_TICKETS, LISTA_DE_TICKET, LISTA_DE_MENSAJE
from funciones_base_datos import (cursor,generar_departamentos_y_operadores,generar_clientes,generar_ticket_y_mensaje)

        
if __name__ == "__main__":
    conexion = conectar_bd()
    if conexion is not None:
        lista_operadores=generar_departamentos_y_operadores(conexion)
        lista_id_clientes=generar_clientes(conexion)

        for i in range(NUM_TICKETS):
            id_operador = random.choice(lista_operadores)
            id_cliente = random.choice(lista_id_clientes)
            generar_ticket_y_mensaje(id_cliente,id_operador)

        sql_T = """ INSERT INTO Ticket 
                    (id_ticket, titulo, descripcion, fecha_hora_inicial, categoria, prioridad, estados, fecha_hora_final,id_cliente_fk2, id_empleado_fk2)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor(conexion,LISTA_DE_TICKET, sql_T ,"TICKET")

        sql_M= """ INSERT INTO Mensaje 
                     (id_mensaje, texto, fecha_hora_enviado, id_cliente_fk1, id_empleado_fk1, id_ticket_fk1)
                     VALUES(%s, %s, %s, %s, %s, %s)
        """
        cursor(conexion,LISTA_DE_MENSAJE, sql_M, "MENSAJES")
        conexion.close()
    else:
        print("fallo de conexion")