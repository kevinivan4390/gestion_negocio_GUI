# utils/validaciones.py

def validar_producto(nombre, marca, precio_compra, precio_venta, stock):
    if not nombre or not marca:
        return False, "El nombre y la marca son obligatorios."
    if precio_compra <= 0 or precio_venta <= 0:
        return False, "Los precios deben ser mayores a cero."
    if stock < 0:
        return False, "El stock no puede ser negativo."
    return True, ""


def validar_texto(texto):
    """
    Devuelve True si el texto contiene solo letras y espacios.
    """
    return texto.replace(" ", "").isalpha()

def validar_numero(numero):
    """
    Devuelve True si es un número entero positivo.
    """
    return numero.isdigit()

def validar_decimal(valor):
    """
    Devuelve True si es un número decimal positivo.
    """
    try:
        return float(valor) >= 0
    except ValueError:
        return False

def validar_mail(mail):
    """
    Devuelve True si el mail tiene formato válido básico.
    """
    return "@" in mail and "." in mail

def validar_telefono(telefono):
    """
    Devuelve True si el teléfono tiene solo dígitos y puede empezar con "+".
    """
    if telefono.startswith("+"):
        telefono = telefono[1:]
    return telefono.isdigit()

