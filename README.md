# 💼 InvenBank Pro - Sistema de Inventario y Ventas v2.0

Una moderna aplicación de escritorio profesional para gestionar inventario y ventas, diseñada con una interfaz inspirada en aplicaciones bancarias. Ahora con arquitectura modular y funcionalidades extendidas.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57)
![Version](https://img.shields.io/badge/version-2.0-brightgreen)

## 🎯 Características Principales

### ✨ Nuevas Funcionalidades v2.0
- **📁 Gestión de Categorías**: Crea carpetas personalizadas con colores e iconos
- **📝 Campos Personalizados**: Instrucciones de manejo, uso específico y notas para cada producto
- **🔄 Ordenamiento Flexible**: Ordena productos por nombre, precio, stock o categoría
- **🏷️ Organización Avanzada**: Agrupa productos en categorías con colores distintivos
- **🎨 Personalización Total**: Elige iconos y colores para tus categorías
- **📊 Arquitectura Modular**: Código organizado en módulos profesionales

### 🚀 Características Principales
- **🖥️ Aplicación de Escritorio Moderna**: Interfaz nativa inspirada en banking apps
- **📦 Gestión Completa de Inventario**: Agregar, editar, organizar y visualizar productos
- **💰 Punto de Venta Rápido**: Sistema ágil para procesar transacciones
- **📜 Historial Detallado**: Registro completo de todas las ventas con exportación a CSV
- **📊 Dashboard en Tiempo Real**: Estadísticas y métricas actualizadas del negocio
- **⚠️ Alertas Inteligentes**: Notificaciones de productos con bajo inventario
- **🌙 Tema Oscuro Profesional**: Diseño moderno con paleta de colores bancarios
- **💾 Base de Datos Robusta**: SQLite con relaciones y campos extendidos

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior instalado
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 📱 Ejecutar la Aplicación de Escritorio

Para iniciar la aplicación de escritorio moderna:

```bash
python app_desktop.py
```

La aplicación se abrirá en una ventana nativa de tu sistema operativo.

## 🌐 Ejecutar la Aplicación Web (Versión Antigua)

Si prefieres usar la versión web con tema medieval:

```bash
python app.py
```

Luego abre tu navegador en `http://localhost:5000`

## 📚 Uso de la Aplicación

### 📊 Dashboard
- Vista general con 4 métricas clave: Capital actual, Total de productos, Ventas del día, Ganancias totales
- Tabla de productos con stock bajo (menos de 10 unidades) para atención inmediata
- Actualización automática al cambiar entre secciones

### 📦 Gestión de Productos
- **Agregar Producto**: 
  - Nombre, descripción, categoría, precio de venta, costo de compra
  - **NUEVO**: Instrucciones de manejo (ej: "Refrigerar a 4°C")
  - **NUEVO**: Uso específico (ej: "Para uso en exteriores")
  - **NUEVO**: Notas adicionales personalizadas
- **Editar**: Doble clic en cualquier producto de la lista
- **Ordenar**: Selecciona criterio de ordenamiento (personalizado, nombre, precio, stock, categoría)
- **Filtrar**: Próximamente - filtrar por categoría
- El sistema descuenta automáticamente del presupuesto al agregar productos

### 📁 Gestión de Categorías
- **Crear Carpetas**: Organiza tus productos en categorías personalizadas
- **Personalizar**: Elige un nombre, descripción, color e icono para cada categoría
- **Iconos Disponibles**: Más de 80 emojis para representar tus categorías
- **Colores**: 10 colores profesionales predefinidos
- **Ver Productos**: Cantidad de productos en cada categoría
- Las categorías no se pueden eliminar si contienen productos

### 💰 Punto de Venta
- Selecciona producto del menú desplegable (muestra stock disponible)
- Ingresa cantidad deseada
- Visualización en tiempo real de: producto, precio unitario, stock, total
- Procesa la venta con un clic
- Panel de ventas recientes con las últimas 10 transacciones
- Actualización automática de inventario y capital

### 📜 Historial de Ventas
- Tabla completa de todas las transacciones
- Información: ID, Producto, Cantidad, Precio unitario, Total, Fecha/hora
- **Exportar a CSV**: Descarga el historial para análisis en Excel
- Límite de 1000 ventas más recientes
- Botón de actualización manual

### 📈 Estadísticas
- **Ganancias Totales**: Suma de todas las ventas realizadas
- **Total de Ventas**: Número de transacciones completadas
- **Producto Más Vendido**: Producto con mayor cantidad de unidades vendidas
- **Capital Disponible**: Presupuesto actual del negocio
- **Gestionar Presupuesto**: Modal para ajustar el capital manualmente

## 🎨 Diseño de la Interfaz

La aplicación de escritorio está diseñada con una interfaz moderna inspirada en aplicaciones bancarias:

- **Paleta de Colores Profesional**: Azules oscuros, verdes de éxito, tonos premium
- **Sidebar de Navegación**: Acceso rápido a todas las secciones
- **Tarjetas de Estadísticas**: Información importante al instante
- **Tablas Modernas**: Visualización limpia de datos con scrolling
- **Formularios Intuitivos**: Campos de entrada claros y bien organizados
- **Botones de Acción**: Diseño distintivo para acciones importantes
- **Tema Oscuro**: Reduce fatiga visual en sesiones largas

### Paleta de Colores

```
Primary: #1E3A8A (Azul profesional)
Secondary: #3B82F6 (Azul brillante)
Accent: #10B981 (Verde éxito)
Warning: #F59E0B (Amarillo advertencia)
Danger: #EF4444 (Rojo error)
Background: #0F172A (Fondo oscuro)
```

## 📊 Estructura del Proyecto

```
ExamenFinal/
│
├── app_desktop.py              # Aplicación principal de escritorio
├── app.py                      # Versión web (Flask) - legacy
├── database.py                 # Base de datos legacy
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
├── .gitignore                  # Archivos ignorados por git
│
├── config/                     # Configuración
│   └── settings.py             # Configuración global (colores, opciones)
│
├── src/                        # Código fuente modular
│   ├── __init__.py
│   ├── models/                 # Modelos de datos
│   │   ├── __init__.py
│   │   └── database_manager.py  # Gestor de base de datos mejorado
│   ├── views/                  # Interfaces (futuro)
│   ├── controllers/            # Controladores (futuro)
│   └── utils/                  # Utilidades
│       ├── __init__.py
│       └── helpers.py          # Funciones auxiliares
│
├── assets/                     # Recursos multimedia
│   └── images/                 # Imágenes (futuro)
│
├── static/                     # Archivos estáticos (web)
│   ├── js/
│   ├── css/
│   └── audio/
│
└── templates/                  # Plantillas HTML (web)
    └── index.html
```

## 🗄️ Base de Datos

El sistema utiliza SQLite con las siguientes tablas mejoradas:

### **categorias**
- `id`: INTEGER PRIMARY KEY
- `nombre`: TEXT NOT NULL UNIQUE
- `descripcion`: TEXT
- `color`: TEXT (código hexadecimal)
- `icono`: TEXT (emoji)
- `fecha_creacion`: TEXT

### **productos** (extendida)
- `id`: INTEGER PRIMARY KEY
- `nombre`: TEXT NOT NULL
- `descripcion`: TEXT
- `precio`: REAL NOT NULL
- `cantidad`: INTEGER NOT NULL
- `categoria_id`: INTEGER (FK a categorias)
- `instrucciones_manejo`: TEXT ⭐ NUEVO
- `uso_especifico`: TEXT ⭐ NUEVO
- `notas_adicionales`: TEXT ⭐ NUEVO
- `orden_visualizacion`: INTEGER (para ordenamiento personalizado) ⭐ NUEVO
- `fecha_agregado`: TEXT

### **ventas**
- `id`: INTEGER PRIMARY KEY
- `producto_id`: INTEGER (FK a productos)
- `producto_nombre`: TEXT
- `cantidad`: INTEGER
- `precio_unitario`: REAL
- `total`: REAL
- `fecha`: TEXT

### **presupuesto**
- `id`: INTEGER (siempre 1)
- `capital`: REAL
- `ultima_actualizacion`: TEXT

## 🔧 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación
- **CustomTkinter**: Framework moderno para interfaces gráficas
- **SQLite3**: Base de datos embebida
- **Pillow (PIL)**: Procesamiento de imágenes
- **Flask**: Servidor web (versión web opcional)

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verifica que Python 3.8+ esté instalado: `python --version`
- Asegúrate de haber instalado las dependencias: `pip install -r requirements.txt`

### Error de módulos no encontrados
```bash
pip install customtkinter pillow
```

### La base de datos no guarda cambios
- Verifica permisos de escritura en la carpeta del proyecto
- Elimina `inventario_ventas.db` para crear una nueva base de datos limpia

### Problemas de visualización
- Asegúrate de tener los drivers gráficos actualizados
- La aplicación requiere resolución mínima de 1280x720

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:
1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso educativo.

## 👨‍💻 Autor

Desarrollado como proyecto final para el curso de Programación.

---

## 📝 Notas Adicionales

### Diferencias entre Versión Web y Escritorio

**Aplicación de Escritorio (app_desktop.py)**:
- ✅ Interfaz nativa y moderna
- ✅ Mejor rendimiento
- ✅ No requiere navegador
- ✅ Diseño inspirado en banking apps
- ✅ Más rápida y fluida

**Aplicación Web (app.py)**:
- ✅ Tema medieval divertido
- ✅ Accesible desde cualquier dispositivo
- ✅ Requiere navegador
- ✅ Música de ambiente
- ⚠️ Requiere servidor corriendo

### Próximas Características Planeadas

- 📈 Gráficos y reportes avanzados
- 🔐 Sistema de usuarios y permisos
- 📧 Notificaciones por email
- 🖨️ Impresión de tickets de venta
- 📱 Versión móvil responsive
- 🌍 Soporte multi-idioma
- ☁️ Respaldos automáticos en la nube

### FAQ

**¿Puedo usar ambas versiones simultáneamente?**
Sí, ambas usan la misma base de datos SQLite, pero no las ejecutes al mismo tiempo para evitar conflictos.

**¿Cómo respaldo mis datos?**
Simplemente copia el archivo `inventario_ventas.db` a un lugar seguro.

**¿Puedo personalizar los colores?**
Sí, edita el diccionario `COLORS` en [app_desktop.py](app_desktop.py#L18) para cambiar la paleta.

**¿Funciona en Mac/Linux?**
Sí, CustomTkinter es multiplataforma y funciona en Windows, macOS y Linux.

---

**¡Gracias por usar InvenBank!** 💼✨
