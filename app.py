from flask import Flask, render_template, request, jsonify, redirect, url_for
from src.models.database_manager import DatabaseManager
from datetime import datetime
import os

app = Flask(__name__)
db = DatabaseManager()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

# ===== RUTAS DE PRODUCTOS =====
@app.route('/api/productos', methods=['GET'])
def get_productos():
    """Obtiene todos los productos"""
    productos = db.obtener_productos()
    productos_list = []
    for p in productos:
        productos_list.append({
            'id': p[0],
            'nombre': p[1],
            'descripcion': p[2],
            'precio': p[3],
            'cantidad': p[4],
            'categoria': p[5],
            'fecha_agregado': p[6]
        })
    return jsonify(productos_list)

@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    """Agrega un nuevo producto"""
    data = request.json
    
    try:
        resultado = db.agregar_producto(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=float(data['precio']),
            cantidad=int(data['cantidad']),
            categoria=data.get('categoria', 'General'),
            costo_compra=float(data.get('costo_compra', data['precio']))
        )
        
        if resultado[0]:
            return jsonify({'success': True, 'message': resultado[1], 'id': resultado[0]})
        else:
            return jsonify({'success': False, 'message': resultado[1]}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    """Actualiza un producto existente"""
    data = request.json
    
    try:
        db.actualizar_producto(
            producto_id=producto_id,
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=float(data['precio']),
            cantidad=int(data['cantidad']),
            categoria=data.get('categoria', 'General')
        )
        return jsonify({'success': True, 'message': 'Producto actualizado exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    """Elimina un producto"""
    try:
        db.eliminar_producto(producto_id)
        return jsonify({'success': True, 'message': 'Producto eliminado exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# ===== RUTAS DE COMPRAS =====
@app.route('/api/compras', methods=['GET'])
def get_compras():
    """Obtiene el historial de compras"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, producto_nombre, cantidad, costo_unitario, total, proveedor, fecha
            FROM compras
            ORDER BY fecha DESC
            LIMIT 100
        ''')
        
        compras = cursor.fetchall()
        conn.close()
        
        compras_list = []
        for c in compras:
            compras_list.append({
                'id': c[0],
                'producto_nombre': c[1],
                'cantidad': c[2],
                'costo_unitario': c[3],
                'total': c[4],
                'proveedor': c[5],
                'fecha': c[6]
            })
        return jsonify(compras_list)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/compras', methods=['POST'])
def registrar_compra():
    """Registra una nueva compra de productos"""
    data = request.json
    
    try:
        nombre_producto = data.get('nombre_producto', '').strip()
        categoria_id = data.get('categoria_id')
        precio_venta = float(data.get('precio_venta', 0))
        cantidad = int(data.get('cantidad', 0))
        costo_unitario = float(data.get('costo_unitario', 0))
        proveedor = data.get('proveedor', 'Proveedor General').strip()
        
        # Validaciones
        if not nombre_producto:
            return jsonify({'success': False, 'message': 'El nombre del producto es obligatorio'}), 400
        
        if cantidad <= 0:
            return jsonify({'success': False, 'message': 'La cantidad debe ser mayor a 0'}), 400
        
        if costo_unitario <= 0:
            return jsonify({'success': False, 'message': 'El costo unitario debe ser mayor a 0'}), 400
        
        if precio_venta <= 0:
            return jsonify({'success': False, 'message': 'El precio de venta debe ser mayor a 0'}), 400
        
        total = cantidad * costo_unitario
        
        # Verificar presupuesto disponible
        capital, _ = db.obtener_presupuesto()
        if capital < total:
            return jsonify({
                'success': False, 
                'message': f'Presupuesto insuficiente. Disponible: ${capital:.2f}, Necesario: ${total:.2f}'
            }), 400
        
        # Obtener conexión para transacción
        conn = db.get_connection()
        cursor = conn.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Verificar si el producto ya existe
        cursor.execute('SELECT id, cantidad FROM productos WHERE LOWER(nombre) = LOWER(?)', (nombre_producto,))
        producto_existente = cursor.fetchone()
        
        if producto_existente:
            # Actualizar producto existente
            producto_id = producto_existente[0]
            
            cursor.execute('''
                UPDATE productos 
                SET cantidad = cantidad + ?, precio = ?, categoria_id = ?
                WHERE id = ?
            ''', (cantidad, precio_venta, categoria_id, producto_id))
            
            accion = "actualizado"
        else:
            # Crear nuevo producto
            cursor.execute('''
                INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria_id, fecha_agregado)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre_producto, f"Producto agregado por compra", precio_venta, cantidad, categoria_id, fecha))
            
            producto_id = cursor.lastrowid
            accion = "creado"
        
        # Registrar la compra en el historial
        cursor.execute('''
            INSERT INTO compras (producto_id, producto_nombre, cantidad, costo_unitario, total, proveedor, fecha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (producto_id, nombre_producto, cantidad, costo_unitario, total, proveedor, fecha))
        
        compra_id = cursor.lastrowid
        
        # Descontar del presupuesto
        cursor.execute('''
            UPDATE presupuesto 
            SET capital = capital - ?, ultima_actualizacion = ?
            WHERE id = 1
        ''', (total, fecha))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': f'Producto {accion}: {cantidad} unidades de {nombre_producto}',
            'id': compra_id,
            'producto_id': producto_id,
            'accion': accion
        })
        
    except ValueError as ve:
        return jsonify({'success': False, 'message': f'Valores numéricos inválidos: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al procesar compra: {str(e)}'}), 400

@app.route('/api/compras/estadisticas', methods=['GET'])
def get_estadisticas_compras():
    """Obtiene estadísticas de compras"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Total invertido en compras
        cursor.execute('SELECT IFNULL(SUM(total), 0) FROM compras')
        total_invertido = cursor.fetchone()[0]
        
        # Número total de compras
        cursor.execute('SELECT COUNT(*) FROM compras')
        total_compras = cursor.fetchone()[0]
        
        # Compra más grande
        cursor.execute('''
            SELECT producto_nombre, total, fecha 
            FROM compras 
            ORDER BY total DESC 
            LIMIT 1
        ''')
        compra_mayor = cursor.fetchone()
        
        # Proveedor más frecuente
        cursor.execute('''
            SELECT proveedor, COUNT(*) as cantidad
            FROM compras
            GROUP BY proveedor
            ORDER BY cantidad DESC
            LIMIT 1
        ''')
        proveedor_top = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            'total_invertido': total_invertido,
            'total_compras': total_compras,
            'compra_mayor': {
                'producto': compra_mayor[0] if compra_mayor else 'N/A',
                'total': compra_mayor[1] if compra_mayor else 0,
                'fecha': compra_mayor[2] if compra_mayor else 'N/A'
            } if compra_mayor else None,
            'proveedor_frecuente': {
                'nombre': proveedor_top[0] if proveedor_top else 'N/A',
                'cantidad': proveedor_top[1] if proveedor_top else 0
            } if proveedor_top else None
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# ===== RUTAS DE VENTAS =====
@app.route('/api/ventas', methods=['GET'])
def get_ventas():
    """Obtiene el historial de ventas"""
    ventas = db.obtener_ventas(limite=100)
    ventas_list = []
    for v in ventas:
        ventas_list.append({
            'id': v[0],
            'producto_id': v[1],
            'producto_nombre': v[2],
            'cantidad': v[3],
            'precio_unitario': v[4],
            'total': v[5],
            'fecha': v[6]
        })
    return jsonify(ventas_list)

@app.route('/api/ventas', methods=['POST'])
def registrar_venta():
    """Registra una nueva venta"""
    data = request.json
    
    try:
        venta_id, mensaje = db.registrar_venta(
            producto_id=int(data['producto_id']),
            cantidad=int(data['cantidad'])
        )
        
        if venta_id:
            return jsonify({'success': True, 'message': mensaje, 'id': venta_id})
        else:
            return jsonify({'success': False, 'message': mensaje}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# ===== ESTADÍSTICAS =====
@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    """Obtiene estadísticas generales"""
    stats = db.obtener_estadisticas()
    return jsonify(stats)

# ===== PRESUPUESTO =====
@app.route('/api/presupuesto', methods=['GET'])
def get_presupuesto():
    """Obtiene el presupuesto actual"""
    presupuesto = db.obtener_presupuesto()
    return jsonify(presupuesto)

@app.route('/api/presupuesto', methods=['PUT'])
def actualizar_presupuesto():
    """Actualiza el presupuesto manualmente"""
    data = request.json
    try:
        db.actualizar_presupuesto(float(data['capital']))
        return jsonify({'success': True, 'message': 'Presupuesto actualizado'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# ===== GESTIÓN DE ARCHIVOS MENSUALES =====
@app.route('/api/guardar-mes', methods=['POST'])
def guardar_mes_actual():
    """Guarda el archivo de la base de datos actual como backup"""
    data = request.json if request.json else {}
    nombre_archivo = data.get('nombre_archivo', None)
    
    try:
        exito, mensaje, ruta_archivo = db.guardar_mes_actual(nombre_archivo)
        if exito:
            return jsonify({
                'success': True, 
                'message': mensaje,
                'archivo': ruta_archivo
            })
        else:
            return jsonify({'success': False, 'message': mensaje}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/nuevo-mes', methods=['POST'])
def crear_nuevo_mes():
    """Crea una nueva base de datos para el siguiente mes"""
    data = request.json if request.json else {}
    mantener_productos = data.get('mantener_productos', True)
    mantener_presupuesto = data.get('mantener_presupuesto', True)
    
    try:
        exito, mensaje = db.crear_nuevo_mes(mantener_productos, mantener_presupuesto)
        if exito:
            return jsonify({
                'success': True, 
                'message': mensaje
            })
        else:
            return jsonify({'success': False, 'message': mensaje}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/backups', methods=['GET'])
def listar_backups():
    """Lista todos los backups mensuales disponibles"""
    try:
        backups = db.listar_backups()
        return jsonify({
            'success': True,
            'backups': backups,
            'total': len(backups)
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
