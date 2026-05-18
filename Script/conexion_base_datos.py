import mysql.connector
from funcionalidades_aparte_base_datos import escribir_log

def conectar_bd():
    """
    Establece la conexión con MySQL y la devuelve.
    Returns:
        Objeto conexion y si no None.
    """
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="hermesadmin",
            password="1234",
            database="Hermes_IT"
            )
        return conexion
    except:
        print("Fallo de conexion")
        escribir_log(f"ERROR: Fallo de conexión")
        return None
