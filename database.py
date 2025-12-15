import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='inventario_ventas.db'):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        """Inicializa las tablas de la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL,
                categoria TEXT,
                fecha_agregado TEXT NOT NULL
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
        
        # Tabla de presupuesto/capital
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presupuesto (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                capital REAL NOT NULL DEFAULT 10000.0,
                ultima_actualizacion TEXT NOT NULL
            )
        ''')
        
        # Inicializar presupuesto si no existe
        cursor.execute('SELECT COUNT(*) FROM presupuesto WHERE id = 1')
        if cursor.fetchone()[0] == 0:
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO presupuesto (id, capital, ultima_actualizacion) VALUES (1, 10000.0, ?)', (fecha,))
        
        conn.commit()
        conn.close()
    
    # ===== PRODUCTOS =====
    def agregar_producto(self, nombre, descripcion, precio, cantidad, categoria, costo_compra=None):
        """Agrega un nuevo producto al inventario y descuenta del presupuesto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Si no se proporciona costo de compra, usar el precio como costo
        if costo_compra is None:
            costo_compra = precio
        
        # Calcular costo total de compra
        costo_total = costo_compra * cantidad
        
        # Verificar si hay suficiente presupuesto
        cursor.execute('SELECT capital FROM presupuesto WHERE id = 1')
        capital_actual = cursor.fetchone()[0]
        
        if capital_actual < costo_total:
            conn.close()
            return None, f"Presupuesto insuficiente. Disponible: {capital_actual:.2f}, Necesario: {costo_total:.2f}"
        
        # Agregar producto
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria, fecha_agregado)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, precio, cantidad, categoria, fecha))
        
        producto_id = cursor.lastrowid
        
        # Descontar del presupuesto
        cursor.execute('''
            UPDATE presupuesto 
            SET capital = capital - ?, ultima_actualizacion = ?
            WHERE id = 1
        ''', (costo_total, fecha))
        
        conn.commit()
        conn.close()
        return producto_id, "Producto agregado exitosamente"
    
    def obtener_productos(self):
        """Obtiene todos los productos del inventario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM productos ORDER BY nombre')
        productos = cursor.execute('SELECT * FROM productos ORDER BY nombre').fetchall()
        
        conn.close()
        return productos
    
    def obtener_producto(self, producto_id):
        """Obtiene un producto específico por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        producto = cursor.fetchone()
        
        conn.close()
        return producto
    
    def actualizar_producto(self, producto_id, nombre, descripcion, precio, cantidad, categoria):
        """Actualiza un producto existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE productos 
            SET nombre = ?, descripcion = ?, precio = ?, cantidad = ?, categoria = ?
            WHERE id = ?
        ''', (nombre, descripcion, precio, cantidad, categoria, producto_id))
        
        conn.commit()
        conn.close()
    
    def eliminar_producto(self, producto_id):
        """Elimina un producto del inventario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
        
        conn.commit()
        conn.close()
    
    def actualizar_stock(self, producto_id, cantidad):
        """Actualiza el stock de un producto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE productos SET cantidad = cantidad + ? WHERE id = ?', (cantidad, producto_id))
        
        conn.commit()
        conn.close()
    
    # ===== VENTAS =====
    def registrar_venta(self, producto_id, cantidad):
        """Registra una venta y actualiza el inventario y presupuesto"""
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
    
    def obtener_ventas(self, limite=None):
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
    
    # ===== PRESUPUESTO =====
    def obtener_presupuesto(self):
        """Obtiene el presupuesto actual"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT capital, ultima_actualizacion FROM presupuesto WHERE id = 1')
        result = cursor.fetchone()
        
        conn.close()
        return {'capital': result[0], 'ultima_actualizacion': result[1]} if result else None
    
    def actualizar_presupuesto(self, nuevo_capital):
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
    
    def obtener_productos_bajo_stock(self, limite=10):
        """Obtiene productos con stock bajo (menos de 10 unidades)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM productos WHERE cantidad < 10 ORDER BY cantidad ASC LIMIT ?', (limite,))
        productos = cursor.fetchall()
        
        conn.close()
        return productos
    
    def obtener_producto_mas_vendido(self):
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
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas generales actualizadas para la app"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total de productos
        cursor.execute('SELECT COUNT(*) FROM productos')
        total_productos = cursor.fetchone()[0]
        
        # Total de ventas
        cursor.execute('SELECT COUNT(*) FROM ventas')
        total_ventas = cursor.fetchone()[0]
        
        # Ventas del día
        hoy = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT SUM(total) FROM ventas WHERE DATE(fecha) = ?', (hoy,))
        ventas_dia = cursor.fetchone()[0] or 0
        
        # Ganancia total (suma de todas las ventas)
        cursor.execute('SELECT SUM(total) FROM ventas')
        ganancia_total = cursor.fetchone()[0] or 0
        
        # Productos con bajo stock
        cursor.execute('SELECT COUNT(*) FROM productos WHERE cantidad < 10')
        productos_bajo_stock = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_productos': total_productos,
            'total_ventas': total_ventas,
            'ventas_dia': ventas_dia,
            'ganancia_total': ganancia_total,
            'productos_bajo_stock': productos_bajo_stock
        }
