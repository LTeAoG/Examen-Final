# Reino del Comercio - Sistema de Inventario y Ventas

Una aplicación web medieval para gestionar el inventario y ventas de tu reino, desarrollada con Python Flask y diseñada con Tailwind CSS.

![Medieval Theme](https://img.shields.io/badge/Theme-Medieval-goldenrod)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38bdf8)

## Características

- **Gestión de Inventario**: Agregar, editar, eliminar y visualizar productos
- **Registro de Ventas**: Sistema completo para registrar transacciones
- **Historial de Ventas**: Visualiza todas las ventas realizadas
- **Estadísticas en Tiempo Real**: Monitorea el estado de tu inventario
- **Alertas de Stock Bajo**: Notificaciones automáticas de productos con bajo inventario
- **Diseño Medieval**: Interfaz temática con dragones y caballeros
- **Música de Ambiente**: Reproductor de música medieval integrado
- **Base de Datos SQLite**: Almacenamiento persistente y ligero

## Cómo Agregar Música Medieval

Para agregar música de fondo medieval a tu aplicación, sigue estos pasos:

### Opción 1: Usando Archivos Locales (Recomendado)

1. **Descarga música medieval libre de derechos** de sitios como:
   - [FreePD.com](https://freepd.com) - Música de dominio público
   - [Incompetech.com](https://incompetech.com) - Música libre (con atribución)
   - [Pixabay Music](https://pixabay.com/music/) - Música libre
   - [YouTube Audio Library](https://studio.youtube.com/) - Música libre

2. **Busca términos como**:
   - "Medieval Tavern Music"
   - "Celtic Relaxing Music"
   - "Medieval Lute Music"
   - "Fantasy Medieval Ambient"

3. **Guarda el archivo MP3** en la carpeta:
   ```
   static/audio/medieval.mp3
   ```

4. **Verifica que el nombre coincida** con el especificado en el HTML o cambia la ruta en `templates/index.html`:
   ```html
   <source src="/static/audio/medieval.mp3" type="audio/mpeg">
   ```

### Opción 2: Streaming desde URL

Si tienes un enlace directo a un archivo MP3 en línea, modifica `templates/index.html`:

```html
<audio id="bgMusic" loop>
    <source src="URL_DE_TU_MUSICA.mp3" type="audio/mpeg">
</audio>
```

### Opción 3: YouTube Embebido (Más Complejo)

Para música de YouTube, necesitarías usar la API de YouTube o un iframe. Sin embargo, esto es más complejo y puede tener restricciones.

### Recomendaciones de Música

Busca en YouTube o Spotify:
- "Adrian von Ziegler - Medieval Music"
- "BrunuhVille - Celtic/Medieval"
- "Derek & Brandon Fiechter - Medieval Fantasy"
- "Tavern Music - Medieval Relaxing"

**Descarga usando convertidores legales** o servicios que respeten los derechos de autor.

## Requisitos del Sistema

- Python 3.8 o superior
- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- 50 MB de espacio en disco

## Instalación

### 1. Clona o descarga el proyecto

```bash
cd "c:\Epc\2do Semestre\Programación\ExamenFinal"
```

### 2. Crea un entorno virtual (recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. (Opcional) Agrega tu música medieval

Coloca un archivo MP3 de música medieval en:
```
static/audio/medieval.mp3
```

## Uso

### Iniciar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

### Funcionalidades Principales

#### Gestión de Inventario

1. **Ver Productos**: Al iniciar, verás todos los productos en la pestaña "Inventario"
2. **Agregar Producto**:
   - Haz clic en "Agregar Producto"
   - Completa el formulario:
     - Nombre del producto
     - Descripción (opcional)
     - Precio en monedas de oro
     - Cantidad en stock
     - Categoría (Armas, Armaduras, Pociones, etc.)
   - Haz clic en "Guardar"

3. **Editar Producto**:
   - Haz clic en el botón de edición del producto
   - Modifica los campos necesarios
   - Guarda los cambios

4. **Eliminar Producto**:
   - Haz clic en el botón de eliminar
   - Confirma la eliminación

#### Registro de Ventas

1. Ve a la pestaña "Ventas"
2. Selecciona un producto del menú desplegable
3. Ingresa la cantidad a vender
4. Revisa el total calculado automáticamente
5. Haz clic en "Registrar Venta"
6. El stock se actualizará automáticamente

#### Historial de Ventas

1. Ve a la pestaña "Historial"
2. Visualiza todas las ventas realizadas con:
   - Producto vendido
   - Cantidad
   - Precio unitario
   - Total de la venta
   - Fecha y hora

#### Control de Música

- Haz clic en el botón "Música" en la esquina inferior derecha
- La música comenzará a reproducirse en loop
- Haz clic en "Pausar" para detenerla

## Estadísticas

En la parte superior verás 4 tarjetas con información clave:

- **Productos**: Total de productos en inventario
- **Valor Inventario**: Valor total de todos los productos
- **Total Ventas**: Ingresos totales generados
- **Stock Bajo**: Productos con menos de 10 unidades (alerta)

## Estructura del Proyecto

```
ExamenFinal/
│
├── app.py                  # Aplicación Flask principal
├── database.py             # Gestión de base de datos SQLite
├── requirements.txt        # Dependencias de Python
├── README.md              # Este archivo
│
├── templates/
│   └── index.html         # Interfaz HTML con Tailwind CSS
│
├── static/
│   ├── js/
│   │   └── app.js         # Lógica JavaScript del frontend
│   ├── css/
│   │   └── (estilos personalizados si los hay)
│   └── audio/
│       └── medieval.mp3   # Música de fondo (debes agregarla)
│
└── inventario_ventas.db   # Base de datos (se crea automáticamente)
```

## Personalización

### Cambiar el Tema de Colores

Edita los colores en `templates/index.html` en la sección `<style>`:

```css
/* Cambiar el color dorado principal */
.gold-text {
    color: #DAA520; /* Cambia este color */
}
```

### Modificar Categorías de Productos

Edita el select de categorías en `templates/index.html`:

```html
<select id="producto-categoria">
    <option value="Armas">Armas</option>
    <option value="TuCategoria">Tu Nueva Categoría</option>
</select>
```

### Cambiar la Imagen de Fondo

En `templates/index.html`, modifica la URL de la imagen:

```css
body {
    background-image: url('TU_URL_DE_IMAGEN');
}
```

**Sugerencias de búsqueda** para imágenes gratuitas:
- [Unsplash](https://unsplash.com/s/photos/dragon-knight)
- [Pexels](https://www.pexels.com/search/medieval/)
- [Pixabay](https://pixabay.com/images/search/dragon/)

## Solución de Problemas

### La aplicación no inicia

```bash
# Verifica que Flask esté instalado
pip list | grep Flask

# Reinstala las dependencias
pip install -r requirements.txt
```

### No hay música

1. Verifica que el archivo exista en `static/audio/medieval.mp3`
2. Verifica que el formato sea MP3
3. Comprueba que el navegador soporte reproducción de audio
4. Algunos navegadores requieren interacción del usuario antes de reproducir audio

### Errores de base de datos

```bash
# Elimina la base de datos y déjala recrearse
rm inventario_ventas.db
python app.py
```

### Puerto 5000 ocupado

Cambia el puerto en `app.py`:

```python
app.run(debug=True, port=5001)  # Usa otro puerto
```

## Características de Seguridad

- Validación de datos en frontend y backend
- Prevención de SQL injection mediante consultas parametrizadas
- Validación de stock antes de ventas
- Manejo de errores robusto

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Haz un fork del proyecto
2. Crea una rama para tu característica
3. Haz commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

## Autor

Desarrollado para el curso de Programación - 2do Semestre EPC

## Agradecimientos

- Tailwind CSS por el framework de estilos
- Flask por el framework web
- Unsplash por las imágenes de fondo
- La comunidad de música medieval libre

---

**¡Que la fortuna acompañe a tu reino!**
