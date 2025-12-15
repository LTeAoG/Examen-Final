"""
Utilidades y funciones auxiliares
"""

from datetime import datetime
import csv
from typing import List, Tuple
import re


def formatear_moneda(valor: float) -> str:
    """Formatea un valor numérico como moneda"""
    return f"${valor:,.2f}"


def formatear_fecha(fecha_str: str, formato_salida: str = '%d/%m/%Y %H:%M') -> str:
    """Formatea una fecha de string a formato legible"""
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
        return fecha.strftime(formato_salida)
    except:
        return fecha_str


def validar_numero_positivo(valor: str) -> bool:
    """Valida que un string sea un número positivo"""
    try:
        num = float(valor)
        return num > 0
    except:
        return False


def validar_entero_no_negativo(valor: str) -> bool:
    """Valida que un string sea un entero no negativo"""
    try:
        num = int(valor)
        return num >= 0
    except:
        return False


def limpiar_texto(texto: str) -> str:
    """Limpia un texto eliminando espacios extras"""
    return ' '.join(texto.split())


def exportar_a_csv(datos: List[Tuple], columnas: List[str], archivo: str) -> bool:
    """Exporta datos a un archivo CSV"""
    try:
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            writer.writerows(datos)
        return True
    except Exception as e:
        print(f"Error al exportar: {e}")
        return False


def generar_reporte_texto(titulo: str, datos: dict) -> str:
    """Genera un reporte en formato texto"""
    lineas = []
    lineas.append("=" * 50)
    lineas.append(f" {titulo}")
    lineas.append("=" * 50)
    lineas.append(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lineas.append("")
    
    for clave, valor in datos.items():
        lineas.append(f"{clave}: {valor}")
    
    lineas.append("=" * 50)
    return '\n'.join(lineas)


def validar_color_hex(color: str) -> bool:
    """Valida que un string sea un color hexadecimal válido"""
    patron = r'^#[0-9A-Fa-f]{6}$'
    return bool(re.match(patron, color))


def truncar_texto(texto: str, max_length: int = 50) -> str:
    """Trunca un texto si excede la longitud máxima"""
    if len(texto) <= max_length:
        return texto
    return texto[:max_length-3] + '...'


def calcular_porcentaje_cambio(valor_actual: float, valor_anterior: float) -> float:
    """Calcula el porcentaje de cambio entre dos valores"""
    if valor_anterior == 0:
        return 0.0
    return ((valor_actual - valor_anterior) / valor_anterior) * 100


def obtener_fecha_actual() -> str:
    """Obtiene la fecha actual en formato estándar"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def es_fecha_hoy(fecha_str: str) -> bool:
    """Verifica si una fecha corresponde al día de hoy"""
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
        hoy = datetime.now().date()
        return fecha.date() == hoy
    except:
        return False
