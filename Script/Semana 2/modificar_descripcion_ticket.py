import mysql.connector
import random
from datetime import timedelta
import faker

palabras = ["incompetentes", "denuncia", "vergüenza", "lento"]
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="hermesadmin",
        password="1234",
        database="Hermes_IT"
    )
    cursor = connection.cursor()

    cursor.execute("SELECT id_mensaje, texto FROM mensaje JOIN ticket on id_ticket_fk1 = id_ticket WHERE estados = 'Archivado' ")
    tickets = cursor.fetchall()

    for id_ticket, descripcion in tickets:
        numero_aleatorio = random.random()
        if numero_aleatorio < 0.10:
            palabra_random=random.choice(palabras)
            if descripcion is None:
                descripcion = ""
            nueva_descripcion = descripcion + " " + palabra_random
            cursor.execute(
                f"UPDATE mensaje SET texto = '{nueva_descripcion}' WHERE id_mensaje = {id_ticket}"
            )
    connection.commit()
    
    fake = faker.Faker() 
    cursor.execute("SELECT id_ticket, fecha_hora_inicial FROM ticket WHERE estados = 'Archivado'")
    tickets = cursor.fetchall()
 
    for id_ticket, fecha_inicial in tickets:
        if fecha_inicial is None:
            continue
 
        inicio = fecha_inicial + timedelta(days=1)
        fin = fecha_inicial + timedelta(days=20)
 
        nueva_fecha_final = fake.date_time_between_dates(
            datetime_start=inicio,
            datetime_end=fin
        )
 
        cursor.execute(
            f"UPDATE ticket SET fecha_hora_final = '{nueva_fecha_final}' WHERE id_ticket = {id_ticket}"
        )
 
    connection.commit()
    cursor.close()
    connection.close()
    
except:
    print("Error con la base de datos")
