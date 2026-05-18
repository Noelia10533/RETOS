import random
from datetime import datetime


def generar_id(lista_id):
    """
    Genera un id aleatorio de 6 cifras
    Args:
        lista_id: es la lista de id donde se van añadiendo para comprobar si esta el id
    Returns:
        Un entero  entre 100000 y 999999.
    """
    id=random.randint(100000,999999)
    while id in lista_id:
        id=random.randint(100000,999999)
    return id

def escribir_log(mensaje):
    """
    Registra un mensaje en seed_log.txt
 
    Args:
        mensaje: texto que registro.
    """
    fecha_hora = datetime.now()
    fecha_formateada = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{fecha_formateada}] {mensaje}\n"
    try:
        with open("seed_log.txt", "a") as archivo:
            archivo.write(linea)
    except:
        print("Error no se puedo registrar el fichero")





