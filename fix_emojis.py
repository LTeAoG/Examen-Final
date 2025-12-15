"""Script para corregir los emojis corruptos en app_desktop.py"""

# Leer el archivo
with open('app_desktop.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Buscar y reemplazar las líneas problemáticas
# Reemplazar todas las variaciones posibles de emojis corruptos
import re

# Patrón para encontrar las líneas de navegación problemáticas
contenido = re.sub(
    r'self\.create_nav_button\(".*? Compras", "compras"\)',
    'self.create_nav_button("🛒 Compras", "compras")',
    contenido
)

contenido = re.sub(
    r'self\.create_nav_button\(".*?💰 Ventas", "ventas"\)',
    'self.create_nav_button("💰 Ventas", "ventas")',
    contenido
)

# Escribir el archivo corregido
with open('app_desktop.py', 'w', encoding='utf-8') as f:
    f.write(contenido)

print("✅ Emojis corregidos en app_desktop.py")
