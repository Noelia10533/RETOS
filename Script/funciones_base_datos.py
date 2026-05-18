import random
from constantes import (FAKE,DEPARTAMENTOS,NUM_OPERADORES,NUM_CLIENTES,PRIORIDAD_LISTA,CATEGORIA_LISTA,LISTA_DE_ESTADOS,LISTA_ID_TICKET,LISTA_ID_MENSAJE,LISTA_DE_TICKET,LISTA_DE_MENSAJE,)
from funcionalidades_aparte_base_datos import escribir_log, generar_id

def cursor(conexion,lista, sql,nombre_tabla):
    """
    Hace una insercion grande con executemany ya que le pasamos una lista de tuplas con los datos 
    Args:
        conexion: conexion SQL
        lista: lista de tuplas con los datos
        sql: sentencia SQL 
        nombre_tabla: nombre de la tabla destino para apuntarla en el log.
    """
    try:
        cursor = conexion.cursor()
        cursor.executemany(sql,lista)
        conexion.commit()
        escribir_log(f"INFO: {len(lista)} registros insertados en {nombre_tabla}")
    except:
        print("Error al insertar en la base de datos ")

def generar_departamentos_y_operadores(conexion):
    """
    Crea los departamentos que estan en la constante departamentos y genera los operadores
    Args:
        conexion

    Returns:
        Lista con los IDs de los operadores para despues poderlos asignar a un ticket
    """
    lista_de_departamentos_a_insertar = []
    lista_id = []    
    for departamento in DEPARTAMENTOS:
        id_departamento = generar_id(lista_id)
        lista_id.append(id_departamento)
        numero = random.randint(1,5)
        ubicacion = f"Planta {numero}"
        lista_de_departamentos_a_insertar.append((id_departamento,departamento,ubicacion))
    sql = """ INSERT INTO Departamento
            VALUES (%s,%s,%s)
    """
    cursor(conexion,lista_de_departamentos_a_insertar, sql,"DEPARTAMENTO")

    lista_id_operadores = []
    lista_de_operadores = []
    for veces in range(NUM_OPERADORES):
        id_empleado = generar_id(lista_id_operadores)
        lista_id_operadores.append(id_empleado)
        departamento=random.choice(lista_de_departamentos_a_insertar)
        nombre = FAKE.first_name()
        correo = FAKE.unique.email()
        id_departamento_fk1 = departamento[0]
        lista_de_operadores.append((id_empleado,nombre,correo,id_departamento_fk1)) 
        
    sql = """ INSERT INTO Operadores
            VALUES(%s,%s,%s,%s)
    """
    cursor(conexion,lista_de_operadores, sql,"OPERADORES")
    
    return lista_id_operadores


def generar_clientes(conexion):
    """
    Genera los clientes 
    Args:
        conexion SQL

    Returns:
        Lista con los Id de los clientes
    """
    lista_de_clientes = []
    lista_id_clientes = []
    for i in range(NUM_CLIENTES):
        nombre = FAKE.first_name()
        apellido1 = FAKE.last_name()
        apellido2 = FAKE.last_name()
        correo = FAKE.email()
        telefono = FAKE.phone_number()
        id_cliente = generar_id(lista_id_clientes)
        lista_id_clientes.append(id_cliente)
        lista_de_clientes.append((id_cliente,nombre,apellido1,apellido2,correo,telefono))
    
    sql = """ INSERT INTO Clientes
            VALUES(%s,%s,%s,%s,%s,%s)
    """

    cursor(conexion,lista_de_clientes, sql,"CLIENTES")
    
    return lista_id_clientes


def generar_ticket_y_mensaje(id_cliente,id_operador):
    """
    generamos un ticket que puede ser de un cliente o un operador y que tenga entre 1 o 3 mensajes
    Args:
        id_cliente
        id_operador
    """
    id_ticket = generar_id(LISTA_ID_TICKET)
    LISTA_ID_TICKET.append(id_ticket)
    titulo = FAKE.sentence(nb_words=4)
    descripcion = FAKE.text(max_nb_chars=100)
    estado = random.choice(LISTA_DE_ESTADOS)
    if estado == "Abierto" or estado == "En proceso" or estado == "Archivado":
        fecha_hora_inicial = FAKE.date_time_between(start_date="-2y" , end_date="now")
        fecha_hora_final = None
    else:
        fecha_hora_inicial = FAKE.date_time_between(start_date="-2y" , end_date="now")
        fecha_hora_final = FAKE.date_time_between(start_date=fecha_hora_inicial, end_date="now")
    prioridad = random.choice(PRIORIDAD_LISTA)
    categoria = random.choice(CATEGORIA_LISTA)
    
    LISTA_DE_TICKET.append((id_ticket,titulo,descripcion,fecha_hora_inicial,categoria,prioridad,estado,fecha_hora_final,id_cliente,id_operador))
    
    
    numero_de_mensajes = random.randint(1,3)
    for veces in range(numero_de_mensajes):
        id_mensaje = generar_id(LISTA_ID_MENSAJE)
        LISTA_ID_MENSAJE.append(id_mensaje)
        texto = FAKE.text(max_nb_chars=100)
        fecha_hora_enviado = FAKE.date_time_between(start_date=fecha_hora_inicial, end_date="now")
        quien_habla = random.choice(["cliente","operador"])
        if quien_habla == "cliente" :
            id_cliente_fk1 = id_cliente
            id_empleado_fk1 = None
        else:
            id_cliente_fk1 = None
            id_empleado_fk1 = id_operador

        LISTA_DE_MENSAJE.append((id_mensaje, texto, fecha_hora_enviado, id_cliente_fk1, id_empleado_fk1, id_ticket))
        
        
