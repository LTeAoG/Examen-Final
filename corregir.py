# coding: utf-8
"""Script simple para reemplazar las líneas problemáticas"""

# Leer archivo
with open('app_desktop.py', 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Reemplazar líneas específicas (índices 89 y 90, que son líneas 90 y 91)
lineas[89] = '        self.create_nav_button("🛒 Compras", "compras")\n'
lineas[90] = '        self.create_nav_button("💰 Ventas", "ventas")\n'

# Escribir archivo
with open('app_desktop.py', 'w', encoding='utf-8') as f:
    f.writelines(lineas)

print("✅ Archivo corregido exitosamente")
