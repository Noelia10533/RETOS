def calcular_alerta_sla(fecha_inicial, fecha_final):
    """Devuelve los días de retaso si el ticket se cerró después de 7 días, o None """
    if fecha_inicial is None or fecha_final is None:
        return None
    dias = (fecha_final - fecha_inicial).days
    if dias > 7:
        return dias -7
    return None
 
 
def detectar_enfado(mensajes_cliente):
    """Devuelve True si algún mensaje del cliente contiene palabras de enfado."""
    palabras = ["incompetentes", "denuncia", "vergüenza", "lento"]
    texto_junto = " ".join(mensajes_cliente).lower()
    for palabra in palabras:
        if palabra in texto_junto:
            return True
    return False