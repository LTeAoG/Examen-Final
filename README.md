# 💼 InvenBank - Sistema de Inventario y Ventas

Una moderna aplicación de escritorio para gestionar inventario y ventas de forma profesional, diseñada con una interfaz inspirada en aplicaciones bancarias.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57)

## 🎯 Características

- **🖥️ Aplicación de Escritorio Moderna**: Interfaz nativa inspirada en banking apps
- **📦 Gestión de Inventario**: Agregar, editar y visualizar productos
- **💰 Punto de Venta**: Sistema rápido para procesar transacciones
- **📜 Historial Completo**: Registro detallado de todas las ventas
- **📊 Dashboard en Tiempo Real**: Estadísticas y métricas del negocio
- **⚠️ Alertas de Stock**: Notificaciones de productos con bajo inventario
- **🌙 Tema Oscuro**: Diseño profesional con colores modernos
- **💾 Base de Datos SQLite**: Almacenamiento persistente y confiable

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

### Dashboard
- Vista general con métricas clave: capital, productos, ventas del día
- Lista de productos con bajo stock para atención inmediata

### Gestión de Productos
- **Agregar**: Completa el formulario con nombre, descripción, categoría, precio, costo y cantidad
- **Editar**: Doble clic en cualquier producto de la lista
- **Buscar**: Usa la barra de búsqueda para encontrar productos rápidamente
- **Actualizar**: Botón de refrescar para recargar la lista

### Punto de Venta
- Selecciona el producto del menú desplegable
- Ingresa la cantidad deseada
- El sistema muestra automáticamente el total y stock disponible
- Procesa la venta con un clic
- Ver ventas recientes en tiempo real

### Historial de Ventas
- Visualiza todas las transacciones realizadas
- Exporta el historial a CSV para análisis externo
- Actualiza la lista con el botón de refrescar

### Estadísticas
- Ganancias totales y ventas completadas
- Producto más vendido
- Gestión de presupuesto/capital disponible
- Actualizar capital manualmente cuando sea necesario

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

## 📊 Base de Datos

El sistema utiliza SQLite con las siguientes tablas:

- **productos**: ID, nombre, descripción, precio, cantidad, categoría, fecha
- **ventas**: ID, producto_id, producto_nombre, cantidad, precio_unitario, total, fecha
- **presupuesto**: ID, capital, última_actualización

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
