// Variables globales
let productos = [];
let ventas = [];
let productoEditando = null;
let presupuestoActual = 0;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    cargarPresupuesto();
    cargarEstadisticas();
    cargarProductos();
    cargarVentas();
    
    // Event listeners
    document.getElementById('form-producto').addEventListener('submit', guardarProducto);
    document.getElementById('form-venta').addEventListener('submit', procesarVenta);
    document.getElementById('form-presupuesto').addEventListener('submit', actualizarPresupuesto);
    document.getElementById('venta-producto').addEventListener('change', actualizarInfoVenta);
    document.getElementById('venta-cantidad').addEventListener('input', actualizarInfoVenta);
    document.getElementById('producto-precio').addEventListener('input', sincronizarCosto);
    
    // Control de música
    const musicToggle = document.getElementById('musicToggle');
    const bgMusic = document.getElementById('bgMusic');
    let musicPlaying = false;
    
    // Establecer volumen inicial
    bgMusic.volume = 0.3; // 30% del volumen
    
    musicToggle.addEventListener('click', function() {
        if (musicPlaying) {
            bgMusic.pause();
            musicToggle.innerHTML = '🎵 Música';
        } else {
            bgMusic.play().then(() => {
                musicToggle.innerHTML = '⏸️ Pausar';
            }).catch(error => {
                console.log('Error al reproducir audio:', error);
                mostrarNotificacion('No se pudo reproducir el audio. Haz clic de nuevo.', 'error');
            });
        }
        musicPlaying = !musicPlaying;
    });
});

function sincronizarCosto() {
    const precio = document.getElementById('producto-precio').value;
    const costoInput = document.getElementById('producto-costo');
    if (costoInput && !costoInput.value) {
        costoInput.value = precio;
    }
}

// ===== NAVEGACIÓN =====
function cambiarTab(tab) {
    // Ocultar todos los contenidos
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    
    // Mostrar el contenido seleccionado
    document.getElementById('content-' + tab).classList.remove('hidden');
    
    // Actualizar botones
    document.querySelectorAll('[id^="tab-"]').forEach(btn => {
        btn.style.opacity = '0.7';
    });
    document.getElementById('tab-' + tab).style.opacity = '1';
    
    // Recargar datos si es necesario
    if (tab === 'historial') {
        cargarVentas();
    }
}

// ===== PRESUPUESTO =====
async function cargarPresupuesto() {
    try {
        const response = await fetch('/api/presupuesto');
        const data = await response.json();
        presupuestoActual = data.capital;
        document.getElementById('presupuesto-display').textContent = presupuestoActual.toFixed(2);
    } catch (error) {
        console.error('Error al cargar presupuesto:', error);
    }
}

function mostrarModalPresupuesto() {
    document.getElementById('presupuesto-actual-modal').textContent = presupuestoActual.toFixed(2);
    document.getElementById('nuevo-presupuesto').value = presupuestoActual;
    document.getElementById('modal-presupuesto').classList.remove('hidden');
}

function cerrarModalPresupuesto() {
    document.getElementById('modal-presupuesto').classList.add('hidden');
}

async function actualizarPresupuesto(e) {
    e.preventDefault();
    
    const nuevoCapital = parseFloat(document.getElementById('nuevo-presupuesto').value);
    
    try {
        const response = await fetch('/api/presupuesto', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ capital: nuevoCapital })
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarNotificacion('Presupuesto actualizado exitosamente', 'success');
            cerrarModalPresupuesto();
            await cargarPresupuesto();
            await cargarEstadisticas();
        } else {
            mostrarNotificacion(result.message, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion('Error al actualizar presupuesto', 'error');
    }
}

// ===== ESTADÍSTICAS =====
async function cargarEstadisticas() {
    try {
        const response = await fetch('/api/estadisticas');
        const stats = await response.json();
        
        const statsHTML = `
            <div class="stat-card rounded-lg p-6 text-center">
                <div class="text-4xl mb-2">📦</div>
                <div class="text-3xl font-bold gold-text">${stats.total_productos}</div>
                <div class="text-yellow-200">Productos</div>
            </div>
            
            <div class="stat-card rounded-lg p-6 text-center">
                <div class="text-4xl mb-2">💰</div>
                <div class="text-3xl font-bold gold-text">${stats.valor_inventario.toFixed(2)}</div>
                <div class="text-yellow-200">Valor Inventario</div>
            </div>
            
            <div class="stat-card rounded-lg p-6 text-center">
                <div class="text-4xl mb-2">🏆</div>
                <div class="text-3xl font-bold gold-text">${stats.total_ventas.toFixed(2)}</div>
                <div class="text-yellow-200">Total Ventas</div>
            </div>
            
            <div class="stat-card rounded-lg p-6 text-center">
                <div class="text-4xl mb-2">💵</div>
                <div class="text-3xl font-bold ${stats.presupuesto_actual > 0 ? 'gold-text' : 'text-red-400'}">${stats.presupuesto_actual.toFixed(2)}</div>
                <div class="text-yellow-200">Balance</div>
            </div>
            
            <div class="stat-card rounded-lg p-6 text-center">
                <div class="text-4xl mb-2">⚠️</div>
                <div class="text-3xl font-bold ${stats.productos_bajo_stock > 0 ? 'text-red-400' : 'gold-text'}">${stats.productos_bajo_stock}</div>
                <div class="text-yellow-200">Stock Bajo</div>
            </div>
        `;
        
        document.getElementById('estadisticas').innerHTML = statsHTML;
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
    }
}

// ===== PRODUCTOS =====
async function cargarProductos() {
    try {
        const response = await fetch('/api/productos');
        productos = await response.json();
        mostrarProductos();
        actualizarSelectProductos();
    } catch (error) {
        console.error('Error al cargar productos:', error);
        mostrarNotificacion('Error al cargar productos', 'error');
    }
}

function mostrarProductos() {
    const tbody = document.getElementById('tabla-productos');
    
    if (productos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-8 text-yellow-300">No hay productos en el inventario</td></tr>';
        return;
    }
    
    tbody.innerHTML = productos.map(p => `
        <tr class="border-b border-yellow-900">
            <td class="px-4 py-3">${p.id}</td>
            <td class="px-4 py-3 font-bold">${p.nombre}</td>
            <td class="px-4 py-3">${p.descripcion || '-'}</td>
            <td class="px-4 py-3">
                <span class="px-3 py-1 rounded-full text-sm" style="background: rgba(218, 165, 32, 0.3);">
                    ${p.categoria}
                </span>
            </td>
            <td class="px-4 py-3 text-right font-bold gold-text">${p.precio.toFixed(2)}</td>
            <td class="px-4 py-3 text-right ${p.cantidad < 10 ? 'text-red-400' : ''}">${p.cantidad}</td>
            <td class="px-4 py-3 text-center">
                <button onclick="editarProducto(${p.id})" class="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm mr-2">
                    ✏️
                </button>
                <button onclick="eliminarProducto(${p.id})" class="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm">
                    🗑️
                </button>
            </td>
        </tr>
    `).join('');
}

function actualizarSelectProductos() {
    const select = document.getElementById('venta-producto');
    select.innerHTML = '<option value="">Selecciona un producto...</option>' +
        productos.filter(p => p.cantidad > 0).map(p => `
            <option value="${p.id}" data-precio="${p.precio}" data-stock="${p.cantidad}">
                ${p.nombre} - Stock: ${p.cantidad} - ${p.precio.toFixed(2)} monedas
            </option>
        `).join('');
}

function mostrarModalProducto(productoId = null) {
    const modal = document.getElementById('modal-producto');
    const form = document.getElementById('form-producto');
    
    // Limpiar formulario
    form.reset();
    document.getElementById('producto-id').value = '';
    productoEditando = null;
    
    if (productoId) {
        // Modo edición
        const producto = productos.find(p => p.id === productoId);
        if (producto) {
            document.getElementById('modal-titulo').textContent = 'Editar Producto';
            document.getElementById('producto-id').value = producto.id;
            document.getElementById('producto-nombre').value = producto.nombre;
            document.getElementById('producto-descripcion').value = producto.descripcion || '';
            document.getElementById('producto-precio').value = producto.precio;
            document.getElementById('producto-costo').value = producto.precio; // Usar precio como costo por defecto
            document.getElementById('producto-cantidad').value = producto.cantidad;
            document.getElementById('producto-categoria').value = producto.categoria;
            productoEditando = producto.id;
        }
    } else {
        document.getElementById('modal-titulo').textContent = 'Agregar Producto';
    }
    
    modal.classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('modal-producto').classList.add('hidden');
    productoEditando = null;
}

async function guardarProducto(e) {
    e.preventDefault();
    
    const producto = {
        nombre: document.getElementById('producto-nombre').value,
        descripcion: document.getElementById('producto-descripcion').value,
        precio: parseFloat(document.getElementById('producto-precio').value),
        cantidad: parseInt(document.getElementById('producto-cantidad').value),
        categoria: document.getElementById('producto-categoria').value,
        costo_compra: parseFloat(document.getElementById('producto-costo').value)
    };
    
    try {
        let response;
        if (productoEditando) {
            // Actualizar
            response = await fetch(`/api/productos/${productoEditando}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(producto)
            });
        } else {
            // Crear nuevo
            response = await fetch('/api/productos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(producto)
            });
        }
        
        const result = await response.json();
        
        if (result.success) {
            mostrarNotificacion(result.message, 'success');
            cerrarModal();
            await cargarProductos();
            await cargarPresupuesto();
            await cargarEstadisticas();
        } else {
            mostrarNotificacion(result.message, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion('Error al guardar producto', 'error');
    }
}

function editarProducto(id) {
    mostrarModalProducto(id);
}

async function eliminarProducto(id) {
    const producto = productos.find(p => p.id === id);
    if (!confirm(`¿Estás seguro de eliminar "${producto.nombre}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/productos/${id}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarNotificacion(result.message, 'success');
            await cargarProductos();
            await cargarEstadisticas();
        } else {
            mostrarNotificacion(result.message, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion('Error al eliminar producto', 'error');
    }
}

// ===== VENTAS =====
function actualizarInfoVenta() {
    const select = document.getElementById('venta-producto');
    const cantidadInput = document.getElementById('venta-cantidad');
    const infoDiv = document.getElementById('venta-info');
    
    if (!select.value || !cantidadInput.value) {
        infoDiv.classList.add('hidden');
        return;
    }
    
    const productoId = parseInt(select.value);
    const cantidad = parseInt(cantidadInput.value);
    const producto = productos.find(p => p.id === productoId);
    
    if (producto) {
        const total = producto.precio * cantidad;
        
        document.getElementById('venta-precio').textContent = producto.precio.toFixed(2);
        document.getElementById('venta-stock').textContent = producto.cantidad;
        document.getElementById('venta-total').textContent = total.toFixed(2);
        
        infoDiv.classList.remove('hidden');
        
        // Validar stock
        if (cantidad > producto.cantidad) {
            cantidadInput.setCustomValidity('Stock insuficiente');
        } else {
            cantidadInput.setCustomValidity('');
        }
    }
}

async function procesarVenta(e) {
    e.preventDefault();
    
    const venta = {
        producto_id: parseInt(document.getElementById('venta-producto').value),
        cantidad: parseInt(document.getElementById('venta-cantidad').value)
    };
    
    try {
        const response = await fetch('/api/ventas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(venta)
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarNotificacion('¡Venta registrada exitosamente! 💰', 'success');
            document.getElementById('form-venta').reset();
            document.getElementById('venta-info').classList.add('hidden');
            await cargarProductos();
            await cargarPresupuesto();
            await cargarEstadisticas();
            await cargarVentas();
        } else {
            mostrarNotificacion(result.message, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion('Error al registrar venta', 'error');
    }
}

async function cargarVentas() {
    try {
        const response = await fetch('/api/ventas');
        ventas = await response.json();
        mostrarVentas();
    } catch (error) {
        console.error('Error al cargar ventas:', error);
        mostrarNotificacion('Error al cargar historial', 'error');
    }
}

function mostrarVentas() {
    const tbody = document.getElementById('tabla-ventas');
    
    if (ventas.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-8 text-yellow-300">No hay ventas registradas</td></tr>';
        return;
    }
    
    tbody.innerHTML = ventas.map(v => `
        <tr class="border-b border-yellow-900">
            <td class="px-4 py-3">${v.id}</td>
            <td class="px-4 py-3 font-bold">${v.producto_nombre}</td>
            <td class="px-4 py-3 text-right">${v.cantidad}</td>
            <td class="px-4 py-3 text-right gold-text">${v.precio_unitario.toFixed(2)}</td>
            <td class="px-4 py-3 text-right font-bold gold-text">${v.total.toFixed(2)}</td>
            <td class="px-4 py-3">${formatearFecha(v.fecha)}</td>
        </tr>
    `).join('');
}

// ===== UTILIDADES =====
function formatearFecha(fecha) {
    const date = new Date(fecha);
    return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function mostrarNotificacion(mensaje, tipo = 'info') {
    const colores = {
        success: 'bg-green-600',
        error: 'bg-red-600',
        info: 'bg-blue-600'
    };
    
    const notif = document.createElement('div');
    notif.className = `fixed top-4 right-4 ${colores[tipo]} text-white px-6 py-4 rounded-lg shadow-lg z-50 animate-fade-in`;
    notif.textContent = mensaje;
    
    document.body.appendChild(notif);
    
    setTimeout(() => {
        notif.remove();
    }, 3000);
}

// Inicializar en la pestaña de inventario
cambiarTab('inventario');
