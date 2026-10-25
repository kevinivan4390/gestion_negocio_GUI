# database/db_caja.py

from database.conexion import obtener_conexion
from models.caja import Caja

def obtener_total_caja():
    caja = Caja.obtener_caja()
    return caja.total

def modificar_total_caja(nuevo_total):
    caja = Caja.obtener_caja()
    caja.modificar_manual(nuevo_total)

def sumar_a_caja(monto):
    caja = Caja.obtener_caja()
    caja.sumar(monto)

def restar_a_caja(monto):
    caja = Caja.obtener_caja()
    caja.restar(monto)
