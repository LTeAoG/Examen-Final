"""
Gestor de Base de Datos - Sistema de Inventario y Ventas
Incluye gestión de categorías personalizadas y campos adicionales
"""

import sqlite3
import shutil
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_name='inventario_ventas.db'):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        """Inicializa las tablas de la base de datos con campos extendidos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de categorías personalizadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                color TEXT DEFAULT '#3B82F6',
                icono TEXT DEFAULT '📦',
                fecha_creacion TEXT NOT NULL
            )
        ''')
        
        # Tabla de productos con campos extendidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL,
                categoria_id INTEGER,
                instrucciones_manejo TEXT,
                uso_especifico TEXT,
                notas_adicionales TEXT,
                orden_visualizacion INTEGER DEFAULT 0,
                fecha_agregado TEXT NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
        ''')
        
        # Tabla de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                producto_nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                total REAL NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')
        
        # Tabla de compras (registro de adquisiciones)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                producto_nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                costo_unitario REAL NOT NULL,
                total REAL NOT NULL,
                proveedor TEXT,
                fecha TEXT NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')
        
        # Tabla de presupuesto/capital
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presupuesto (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                capital REAL NOT NULL DEFAULT 50000.0,
                ultima_actualizacion TEXT NOT NULL
            )
        ''')
        
        # Inicializar presupuesto si no existe
        cursor.execute('SELECT COUNT(*) FROM presupuesto WHERE id = 1')
        if cursor.fetchone()[0] == 0:
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO presupuesto (id, capital, ultima_actualizacion) VALUES (1, 50000.0, ?)', (fecha,))
        
        # Agregar categorías por defecto si no existen
        categorias_default = [
            ('Electrónica', 'Dispositivos y equipos electrónicos', '#3B82F6', '📱'),
            ('Oficina', 'Suministros y equipos de oficina', '#10B981', '🖊️'),
            ('Hogar', 'Artículos para el hogar', '#F59E0B', '🏠'),
            ('Tecnología', 'Computadoras y accesorios', '#8B5CF6', '💻'),
            ('Deportes', 'Equipamiento deportivo', '#EF4444', '⚽'),
            ('Libros', 'Libros y material educativo', '#06B6D4', '📚'),
            ('Compras', 'Productos adquiridos de proveedores', '#EC4899', '🛒'),
            ('Alimentos', 'Productos alimenticios', '#84CC16', '🍎'),
            ('Ropa', 'Vestimenta y accesorios', '#F97316', '👕'),
            ('Herramientas', 'Herramientas y equipos', '#64748B', '🔧'),
            ('Juguetería', 'Juguetes y entretenimiento', '#A855F7', '🧸'),
            ('Farmacia', 'Productos médicos y farmacéuticos', '#14B8A6', '💊')
        ]
        
        for nombre, desc, color, icono in categorias_default:
            cursor.execute('SELECT COUNT(*) FROM categorias WHERE nombre = ?', (nombre,))
            if cursor.fetchone()[0] == 0:
                fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('''
                    INSERT INTO categorias (nombre, descripcion, color, icono, fecha_creacion)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nombre, desc, color, icono, fecha))
        
        conn.commit()
        conn.close()
    
    # ===== GESTIÓN DE CATEGORÍAS =====
    
    def crear_categoria(self, nombre: str, descripcion: str = '', color: str = '#3B82F6', icono: str = '📦') -> Tuple[Optional[int], str]:
        """Crea una nueva categoría personalizada"""
        conn = self.get_connection()
        cursor = conn.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            cursor.execute('''
                INSERT INTO categorias (nombre, descripcion, color, icono, fecha_creacion)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, descripcion, color, icono, fecha))
            
            categoria_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return categoria_id, "Categoría creada exitosamente"
        except sqlite3.IntegrityError:
            conn.close()
            return None, "Ya existe una categoría con ese nombre"
    
    def obtener_categorias(self) -> List[Tuple]:
        """Obtiene todas las categorías"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categorias ORDER BY nombre')
        categorias = cursor.fetchall()
        conn.close()
        return categorias
    
    def actualizar_categoria(self, categoria_id: int, nombre: str, descripcion: str, color: str, icono: str) -> bool:
        """Actualiza una categoría existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE categorias 
            SET nombre = ?, descripcion = ?, color = ?, icono = ?
            WHERE id = ?
        ''', (nombre, descripcion, color, icono, categoria_id))
        
        conn.commit()
        conn.close()
        return True
    
    def eliminar_categoria(self, categoria_id: int) -> Tuple[bool, str]:
        """Elimina una categoría (solo si no tiene productos)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar si tiene productos
        cursor.execute('SELECT COUNT(*) FROM productos WHERE categoria_id = ?', (categoria_id,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            conn.close()
            return False, f"No se puede eliminar. La categoría tiene {count} producto(s)"
        
        cursor.execute('DELETE FROM categorias WHERE id = ?', (categoria_id,))
        conn.commit()
        conn.close()
        return True, "Categoría eliminada exitosamente"
    
    # ===== GESTIÓN DE PRODUCTOS =====
    
    def agregar_producto(self, nombre: str, descripcion: str, precio: float, cantidad: int, 
                        categoria_id: Optional[int], costo_compra: float,
                        instrucciones_manejo: str = '', uso_especifico: str = '', 
                        notas_adicionales: str = '') -> Tuple[Optional[int], str]:
        """Agrega un nuevo producto con campos extendidos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Calcular costo total de compra
        costo_total = costo_compra * cantidad
        
        # Verificar presupuesto
        cursor.execute('SELECT capital FROM presupuesto WHERE id = 1')
        capital_actual = cursor.fetchone()[0]
        
        if capital_actual < costo_total:
            conn.close()
            return None, f"Presupuesto insuficiente. Disponible: ${capital_actual:.2f}, Necesario: ${costo_total:.2f}"
        
        # Obtener el siguiente orden de visualización
        cursor.execute('SELECT MAX(orden_visualizacion) FROM productos')
        max_orden = cursor.fetchone()[0]
        nuevo_orden = (max_orden or 0) + 1
        
        # Agregar producto
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria_id,
                                 instrucciones_manejo, uso_especifico, notas_adicionales,
                                 orden_visualizacion, fecha_agregado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, precio, cantidad, categoria_id,
              instrucciones_manejo, uso_especifico, notas_adicionales,
              nuevo_orden, fecha))
        
        producto_id = cursor.lastrowid
        
        # Registrar la compra en el historial
        cursor.execute('''
            INSERT INTO compras (producto_id, producto_nombre, cantidad, costo_unitario, total, proveedor, fecha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (producto_id, nombre, cantidad, costo_compra, costo_total, 'Proveedor General', fecha))
        
        # Descontar del presupuesto
        cursor.execute('''
            UPDATE presupuesto 
            SET capital = capital - ?, ultima_actualizacion = ?
            WHERE id = 1
        ''', (costo_total, fecha))
        
        conn.commit()
        conn.close()
        return producto_id, "Producto agregado exitosamente"
    
    def obtener_productos(self, ordenar_por: str = 'orden_visualizacion') -> List[Tuple]:
        """Obtiene todos los productos con información de categoría"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        orden_valido = {
            'orden_visualizacion': 'p.orden_visualizacion ASC',
            'nombre': 'p.nombre ASC',
            'precio': 'p.precio DESC',
            'cantidad': 'p.cantidad ASC',
            'categoria': 'c.nombre ASC'
        }
        
        orden_sql = orden_valido.get(ordenar_por, 'p.orden_visualizacion ASC')
        
        cursor.execute(f'''
            SELECT p.*, c.nombre as categoria_nombre, c.color, c.icono
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            ORDER BY {orden_sql}
        ''')
        productos = cursor.fetchall()
        
        conn.close()
        return productos
    
    def obtener_productos_por_categoria(self, categoria_id: int) -> List[Tuple]:
        """Obtiene productos de una categoría específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre, c.color, c.icono
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.categoria_id = ?
            ORDER BY p.orden_visualizacion ASC
        ''', (categoria_id,))
        productos = cursor.fetchall()
        
        conn.close()
        return productos
    
    def obtener_producto(self, producto_id: int) -> Optional[Tuple]:
        """Obtiene un producto específico con su categoría"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre, c.color, c.icono
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.id = ?
        ''', (producto_id,))
        producto = cursor.fetchone()
        
        conn.close()
        return producto
    
    def actualizar_producto(self, producto_id: int, nombre: str, descripcion: str, 
                           precio: float, cantidad: int, categoria_id: Optional[int],
                           instrucciones_manejo: str = '', uso_especifico: str = '',
                           notas_adicionales: str = '') -> bool:
        """Actualiza un producto existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE productos 
            SET nombre = ?, descripcion = ?, precio = ?, cantidad = ?, categoria_id = ?,
                instrucciones_manejo = ?, uso_especifico = ?, notas_adicionales = ?
            WHERE id = ?
        ''', (nombre, descripcion, precio, cantidad, categoria_id,
              instrucciones_manejo, uso_especifico, notas_adicionales, producto_id))
        
        conn.commit()
        conn.close()
        return True
    
    def reordenar_producto(self, producto_id: int, nuevo_orden: int) -> bool:
        """Cambia el orden de visualización de un producto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE productos 
            SET orden_visualizacion = ?
            WHERE id = ?
        ''', (nuevo_orden, producto_id))
        
        conn.commit()
        conn.close()
        return True
    
    def mover_producto_categoria(self, producto_id: int, nueva_categoria_id: Optional[int]) -> bool:
        """Mueve un producto a otra categoría"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE productos 
            SET categoria_id = ?
            WHERE id = ?
        ''', (nueva_categoria_id, producto_id))
        
        conn.commit()
        conn.close()
        return True
    
    def eliminar_producto(self, producto_id: int) -> bool:
        """Elimina un producto del inventario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
        conn.commit()
        conn.close()
        return True
    
    def buscar_productos(self, termino: str) -> List[Tuple]:
        """Busca productos por nombre, descripción o notas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        termino_busqueda = f'%{termino}%'
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre, c.color, c.icono
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.nombre LIKE ? OR p.descripcion LIKE ? OR p.notas_adicionales LIKE ?
            ORDER BY p.nombre ASC
        ''', (termino_busqueda, termino_busqueda, termino_busqueda))
        productos = cursor.fetchall()
        
        conn.close()
        return productos
    
    # ===== GESTIÓN DE VENTAS =====
    
    def registrar_venta(self, producto_id: int, cantidad: int) -> Tuple[Optional[int], str]:
        """Registra una venta y actualiza el inventario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Obtener información del producto
        cursor.execute('SELECT nombre, precio, cantidad FROM productos WHERE id = ?', (producto_id,))
        producto = cursor.fetchone()
        
        if not producto:
            conn.close()
            return None, "Producto no encontrado"
        
        nombre, precio, stock_actual = producto
        
        if stock_actual < cantidad:
            conn.close()
            return None, f"Stock insuficiente. Disponible: {stock_actual}"
        
        # Registrar venta
        total = precio * cantidad
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO ventas (producto_id, producto_nombre, cantidad, precio_unitario, total, fecha)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (producto_id, nombre, cantidad, precio, total, fecha))
        
        # Actualizar stock
        cursor.execute('UPDATE productos SET cantidad = cantidad - ? WHERE id = ?', (cantidad, producto_id))
        
        # Sumar al presupuesto
        cursor.execute('''
            UPDATE presupuesto 
            SET capital = capital + ?, ultima_actualizacion = ?
            WHERE id = 1
        ''', (total, fecha))
        
        conn.commit()
        venta_id = cursor.lastrowid
        conn.close()
        return venta_id, "Venta registrada exitosamente"
    
    def obtener_ventas(self, limite: Optional[int] = None) -> List[Tuple]:
        """Obtiene el historial de ventas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if limite:
            cursor.execute('SELECT * FROM ventas ORDER BY fecha DESC LIMIT ?', (limite,))
        else:
            cursor.execute('SELECT * FROM ventas ORDER BY fecha DESC')
        
        ventas = cursor.fetchall()
        conn.close()
        return ventas
    
    # ===== PRESUPUESTO Y ESTADÍSTICAS =====
    
    def obtener_presupuesto(self) -> Tuple[float, str]:
        """Obtiene el presupuesto actual"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT capital, ultima_actualizacion FROM presupuesto WHERE id = 1')
        result = cursor.fetchone()
        
        conn.close()
        return result if result else (0, '')
    
    def actualizar_presupuesto(self, nuevo_capital: float) -> bool:
        """Actualiza el presupuesto manualmente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            UPDATE presupuesto 
            SET capital = ?, ultima_actualizacion = ?
            WHERE id = 1
        ''', (nuevo_capital, fecha))
        
        conn.commit()
        conn.close()
        return True
    
    def obtener_productos_bajo_stock(self, limite: int = 10) -> List[Tuple]:
        """Obtiene productos con stock bajo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre, c.color, c.icono
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.cantidad < 10 
            ORDER BY p.cantidad ASC 
            LIMIT ?
        ''', (limite,))
        productos = cursor.fetchall()
        
        conn.close()
        return productos
    
    def obtener_producto_mas_vendido(self) -> Tuple[str, int]:
        """Obtiene el producto más vendido"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT producto_nombre, SUM(cantidad) as total_vendido
            FROM ventas
            GROUP BY producto_nombre
            ORDER BY total_vendido DESC
            LIMIT 1
        ''')
        resultado = cursor.fetchone()
        
        conn.close()
        return resultado if resultado else ("Ninguno", 0)
    
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas generales del sistema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total de productos
        cursor.execute('SELECT COUNT(*) FROM productos')
        total_productos = cursor.fetchone()[0]
        
        # Total de categorías
        cursor.execute('SELECT COUNT(*) FROM categorias')
        total_categorias = cursor.fetchone()[0]
        
        # Total de ventas
        cursor.execute('SELECT COUNT(*) FROM ventas')
        total_ventas = cursor.fetchone()[0]
        
        # Ventas del día
        hoy = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT SUM(total) FROM ventas WHERE DATE(fecha) = ?', (hoy,))
        ventas_dia = cursor.fetchone()[0] or 0
        
        # Ganancia total
        cursor.execute('SELECT SUM(total) FROM ventas')
        ganancia_total = cursor.fetchone()[0] or 0
        
        # Productos con bajo stock
        cursor.execute('SELECT COUNT(*) FROM productos WHERE cantidad < 10')
        productos_bajo_stock = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_productos': total_productos,
            'total_categorias': total_categorias,
            'total_ventas': total_ventas,
            'ventas_dia': ventas_dia,
            'ganancia_total': ganancia_total,
            'productos_bajo_stock': productos_bajo_stock
        }
    
    # ===== GESTIÓN DE ARCHIVOS MENSUALES =====
    
    def guardar_mes_actual(self, nombre_archivo: Optional[str] = None) -> Tuple[bool, str, str]:
        """Guarda una copia de la base de datos actual con la fecha del mes
        
        Args:
            nombre_archivo: Nombre personalizado para el archivo (opcional)
            
        Returns:
            Tupla (éxito, mensaje, ruta_archivo)
        """
        try:
            # Crear carpeta de backups si no existe
            backup_dir = 'backups_mensuales'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Generar nombre del archivo con fecha
            fecha_actual = datetime.now()
            if nombre_archivo:
                archivo_backup = os.path.join(backup_dir, nombre_archivo)
                if not archivo_backup.endswith('.db'):
                    archivo_backup += '.db'
            else:
                mes_anio = fecha_actual.strftime('%Y_%m_%B')
                archivo_backup = os.path.join(backup_dir, f'inventario_{mes_anio}.db')
            
            # Verificar si ya existe
            if os.path.exists(archivo_backup):
                # Agregar timestamp para evitar sobrescribir
                timestamp = fecha_actual.strftime('%Y%m%d_%H%M%S')
                base_name = archivo_backup.replace('.db', '')
                archivo_backup = f'{base_name}_{timestamp}.db'
            
            # Copiar el archivo de base de datos
            shutil.copy2(self.db_name, archivo_backup)
            
            mensaje = f'Base de datos guardada exitosamente en: {archivo_backup}'
            return True, mensaje, archivo_backup
            
        except Exception as e:
            return False, f'Error al guardar la base de datos: {str(e)}', ''
    
    def crear_nuevo_mes(self, mantener_productos: bool = True, mantener_presupuesto: bool = True) -> Tuple[bool, str]:
        """Crea una nueva base de datos para el siguiente mes
        
        Args:
            mantener_productos: Si True, copia los productos actuales (sin ventas/compras)
            mantener_presupuesto: Si True, mantiene el presupuesto actual
            
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            # Primero guardar el mes actual
            exito, mensaje, archivo_backup = self.guardar_mes_actual()
            if not exito:
                return False, mensaje
            
            # Obtener datos a preservar si es necesario
            productos_actuales = []
            categorias_actuales = []
            presupuesto_actual = None
            
            if mantener_productos or mantener_presupuesto:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                if mantener_productos:
                    # Obtener categorías
                    cursor.execute('SELECT * FROM categorias')
                    categorias_actuales = cursor.fetchall()
                    
                    # Obtener productos
                    cursor.execute('SELECT * FROM productos')
                    productos_actuales = cursor.fetchall()
                
                if mantener_presupuesto:
                    # Obtener presupuesto actual
                    cursor.execute('SELECT capital FROM presupuesto WHERE id = 1')
                    resultado = cursor.fetchone()
                    if resultado:
                        presupuesto_actual = resultado[0]
                
                conn.close()
            
            # Eliminar la base de datos actual
            if os.path.exists(self.db_name):
                os.remove(self.db_name)
            
            # Crear nueva base de datos con estructura limpia
            self.init_db()
            
            # Restaurar datos si se solicitó
            if mantener_productos and (categorias_actuales or productos_actuales):
                conn = self.get_connection()
                cursor = conn.cursor()
                
                # Restaurar categorías
                for cat in categorias_actuales:
                    cursor.execute('''
                        INSERT INTO categorias (id, nombre, descripcion, color, icono, fecha_creacion)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', cat)
                
                # Restaurar productos
                for prod in productos_actuales:
                    cursor.execute('''
                        INSERT INTO productos (id, nombre, descripcion, precio, cantidad, categoria_id,
                                              instrucciones_manejo, uso_especifico, notas_adicionales,
                                              orden_visualizacion, fecha_agregado)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', prod)
                
                conn.commit()
                conn.close()
            
            if mantener_presupuesto and presupuesto_actual is not None:
                conn = self.get_connection()
                cursor = conn.cursor()
                fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('''
                    UPDATE presupuesto 
                    SET capital = ?, ultima_actualizacion = ?
                    WHERE id = 1
                ''', (presupuesto_actual, fecha))
                conn.commit()
                conn.close()
            
            mensaje_final = f'Nuevo mes creado exitosamente. Backup guardado en: {archivo_backup}'
            if mantener_productos:
                mensaje_final += f'\nProductos y categorías preservados.'
            if mantener_presupuesto:
                mensaje_final += f'\nPresupuesto preservado: ${presupuesto_actual:.2f}'
            
            return True, mensaje_final
            
        except Exception as e:
            return False, f'Error al crear nuevo mes: {str(e)}'
    
    def listar_backups(self) -> List[Dict[str, any]]:
        """Lista todos los backups mensuales disponibles"""
        backup_dir = 'backups_mensuales'
        backups = []
        
        if not os.path.exists(backup_dir):
            return backups
        
        try:
            archivos = os.listdir(backup_dir)
            for archivo in archivos:
                if archivo.endswith('.db'):
                    ruta_completa = os.path.join(backup_dir, archivo)
                    stat = os.stat(ruta_completa)
                    backups.append({
                        'nombre': archivo,
                        'ruta': ruta_completa,
                        'tamanio': stat.st_size,
                        'fecha_modificacion': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            # Ordenar por fecha de modificación (más reciente primero)
            backups.sort(key=lambda x: x['fecha_modificacion'], reverse=True)
            
        except Exception as e:
            print(f'Error al listar backups: {e}')
        
        return backups
