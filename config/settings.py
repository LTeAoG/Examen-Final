"""
Configuración global de la aplicación
"""

# Configuración de la aplicación
APP_NAME = "WareInc"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Sistema Profesional de Gestión de Inventario y Ventas"

# Configuración de la base de datos
DATABASE_NAME = "inventario_ventas.db"

# Paleta de colores moderna
COLORS = {
    'primary': '#1E3A8A',      # Azul oscuro profesional
    'secondary': '#3B82F6',    # Azul brillante
    'accent': '#10B981',       # Verde éxito
    'warning': '#F59E0B',      # Amarillo advertencia
    'danger': '#EF4444',       # Rojo error
    'bg_dark': '#0F172A',      # Fondo oscuro
    'bg_card': '#1E293B',      # Fondo tarjetas
    'text_primary': '#F1F5F9',
    'text_secondary': '#94A3B8',
    'border': '#334155'
}

# Iconos disponibles para categorías
ICONOS_DISPONIBLES = [
    '📱', '💻', '🖥️', '⌚', '📷', '🎮', '🎧', '📺',  # Electrónica
    '🖊️', '📎', '📋', '📁', '✂️', '📐', '📌', '📍',  # Oficina
    '🏠', '🛋️', '🛏️', '🍽️', '🔧', '🔨', '💡', '🚪',  # Hogar
    '⚽', '🏀', '🎾', '🏐', '🏓', '🥊', '🏋️', '🚴',  # Deportes
    '📚', '📖', '📝', '✏️', '🎨', '🖼️', '🎭', '🎪',  # Educación/Arte
    '👕', '👔', '👗', '👠', '👟', '🎒', '👜', '🕶️',  # Ropa/Accesorios
    '🍕', '🍔', '🍰', '☕', '🍺', '🥤', '🍎', '🥗',  # Alimentos
    '🚗', '🚙', '🚕', '🛴', '🚲', '🏍️', '✈️', '🚁',  # Vehículos
    '🔐', '🔑', '💊', '💉', '🩹', '🧴', '🧼', '🧻',  # Otros
    '📦', '📮', '🎁', '🏷️', '💰', '💳', '💵', '🪙'   # General
]

# Colores disponibles para categorías
COLORES_DISPONIBLES = [
    ('#3B82F6', 'Azul'),
    ('#10B981', 'Verde'),
    ('#F59E0B', 'Ámbar'),
    ('#EF4444', 'Rojo'),
    ('#8B5CF6', 'Púrpura'),
    ('#EC4899', 'Rosa'),
    ('#06B6D4', 'Cian'),
    ('#F97316', 'Naranja'),
    ('#84CC16', 'Lima'),
    ('#6366F1', 'Índigo')
]

# Opciones de ordenamiento de productos
OPCIONES_ORDENAMIENTO = {
    'orden_visualizacion': 'Orden Personalizado',
    'nombre': 'Nombre (A-Z)',
    'precio': 'Precio (Mayor a Menor)',
    'cantidad': 'Stock (Menor a Mayor)',
    'categoria': 'Categoría'
}

# Configuración de ventanas
WINDOW_CONFIG = {
    'width': 1400,
    'height': 850,
    'min_width': 1200,
    'min_height': 700
}

# Límites y valores por defecto
DEFAULTS = {
    'capital_inicial': 50000.0,
    'stock_minimo_alerta': 10,
    'ventas_recientes_limite': 10,
    'historial_limite': 1000
}
