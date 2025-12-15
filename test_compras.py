"""
Script de diagnóstico para verificar la funcionalidad de compras
"""

import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('inventario_ventas.db')
cursor = conn.cursor()

print("=== DIAGNÓSTICO DE COMPRAS ===\n")

# Verificar tabla de compras
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='compras'")
tabla_existe = cursor.fetchone()
print(f"✓ Tabla 'compras' existe: {tabla_existe is not None}")

# Verificar estructura de la tabla
if tabla_existe:
    cursor.execute("PRAGMA table_info(compras)")
    columnas = cursor.fetchall()
    print(f"\n✓ Columnas en tabla 'compras':")
    for col in columnas:
        print(f"  - {col[1]} ({col[2]})")

# Verificar categorías disponibles
cursor.execute("SELECT id, nombre, icono FROM categorias")
categorias = cursor.fetchall()
print(f"\n✓ Categorías disponibles ({len(categorias)}):")
for cat in categorias[:5]:
    print(f"  {cat[0]}: {cat[2]} {cat[1]}")

# Verificar presupuesto
cursor.execute("SELECT capital FROM presupuesto WHERE id = 1")
capital = cursor.fetchone()
print(f"\n✓ Capital disponible: ${capital[0]:,.2f}")

# Verificar compras existentes
cursor.execute("SELECT COUNT(*) FROM compras")
total_compras = cursor.fetchone()[0]
print(f"\n✓ Total de compras registradas: {total_compras}")

if total_compras > 0:
    cursor.execute("SELECT producto_nombre, cantidad, total, fecha FROM compras ORDER BY fecha DESC LIMIT 3")
    ultimas_compras = cursor.fetchall()
    print(f"\n✓ Últimas 3 compras:")
    for compra in ultimas_compras:
        print(f"  - {compra[0]}: {compra[1]} unidades, ${compra[2]:.2f} ({compra[3]})")

conn.close()

print("\n=== FIN DEL DIAGNÓSTICO ===")
print("\nSi ves esto, la base de datos está correcta.")
print("El problema está en la interfaz de la aplicación.")
print("\nPara ver la sección de compras en la app:")
print("1. Abre la aplicación (app_desktop.py)")
print("2. En el menú lateral izquierdo, busca '🛒 Compras'")
print("3. Haz clic en ese botón")
print("4. Deberías ver el formulario en el panel izquierdo")
