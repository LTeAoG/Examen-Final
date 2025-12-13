from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database
import os

app = Flask(__name__)
db = Database()

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
