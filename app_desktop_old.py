"""
Aplicación de Escritorio - Sistema de Inventario y Ventas
Diseño moderno inspirado en aplicaciones bancarias
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from database import Database
from datetime import datetime
from PIL import Image, ImageTk
import os

# Configuración de tema moderno
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Paleta de colores inspirada en bancos modernos
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

class ModernInventoryApp:
    def __init__(self):
        self.db = Database()
        self.root = ctk.CTk()
        self.root.title("Sistema de Inventario y Ventas")
        self.root.geometry("1400x850")
        
        # Variables de datos
        self.productos = []
        self.ventas_recientes = []
        self.producto_editando = None
        
        # Construir interfaz
        self.build_ui()
        self.cargar_datos_iniciales()
        
    def build_ui(self):
        """Construye la interfaz principal"""
        # Barra lateral de navegación
        self.sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=0, fg_color=COLORS['bg_dark'])
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # Logo/Título en sidebar
        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(pady=30, padx=20)
        
        logo_label = ctk.CTkLabel(
            title_frame, 
            text="💼",
            font=ctk.CTkFont(size=48)
        )
        logo_label.pack()
        
        app_title = ctk.CTkLabel(
            title_frame,
            text="InvenBank",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS['text_primary']
        )
        app_title.pack()
        
        app_subtitle = ctk.CTkLabel(
            title_frame,
            text="Sistema de Gestión",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_secondary']
        )
        app_subtitle.pack()
        
        # Botones de navegación
        self.nav_buttons = []
        
        btn_dashboard = self.create_nav_button("📊 Dashboard", "dashboard")
        btn_productos = self.create_nav_button("📦 Productos", "productos")
        btn_ventas = self.create_nav_button("💰 Ventas", "ventas")
        btn_historial = self.create_nav_button("📜 Historial", "historial")
        btn_estadisticas = self.create_nav_button("📈 Estadísticas", "estadisticas")
        
        # Espaciador
        ctk.CTkLabel(self.sidebar, text="", height=50).pack(expand=True)
        
        # Información del sistema en la parte inferior
        info_frame = ctk.CTkFrame(self.sidebar, fg_color=COLORS['bg_card'], corner_radius=10)
        info_frame.pack(side="bottom", pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(
            info_frame,
            text="Sistema v1.0",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_secondary']
        ).pack(pady=5)
        
        ctk.CTkLabel(
            info_frame,
            text=f"© {datetime.now().year}",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_secondary']
        ).pack(pady=5)
        
        # Contenedor principal
        self.main_container = ctk.CTkFrame(self.root, fg_color=COLORS['bg_dark'], corner_radius=0)
        self.main_container.pack(side="right", fill="both", expand=True)
        
        # Crear todos los frames de contenido
        self.frames = {}
        self.create_dashboard_frame()
        self.create_productos_frame()
        self.create_ventas_frame()
        self.create_historial_frame()
        self.create_estadisticas_frame()
        
        # Mostrar dashboard por defecto
        self.show_frame("dashboard")
        
    def create_nav_button(self, text, frame_name):
        """Crea un botón de navegación moderno"""
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent",
            text_color=COLORS['text_secondary'],
            hover_color=COLORS['bg_card'],
            anchor="w",
            height=50,
            corner_radius=10,
            command=lambda: self.show_frame(frame_name)
        )
        btn.pack(pady=5, padx=20, fill="x")
        self.nav_buttons.append((btn, frame_name))
        return btn
        
    def show_frame(self, frame_name):
        """Muestra el frame seleccionado y actualiza el estilo de los botones"""
        # Ocultar todos los frames
        for frame in self.frames.values():
            frame.pack_forget()
        
        # Mostrar el frame seleccionado
        if frame_name in self.frames:
            self.frames[frame_name].pack(fill="both", expand=True)
        
        # Actualizar estilos de botones
        for btn, name in self.nav_buttons:
            if name == frame_name:
                btn.configure(
                    fg_color=COLORS['primary'],
                    text_color=COLORS['text_primary']
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS['text_secondary']
                )
        
        # Actualizar datos según el frame
        if frame_name == "dashboard":
            self.actualizar_dashboard()
        elif frame_name == "productos":
            self.cargar_productos()
        elif frame_name == "historial":
            self.cargar_historial()
        elif frame_name == "estadisticas":
            self.actualizar_estadisticas()
    
    def create_dashboard_frame(self):
        """Crea el frame de dashboard"""
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["dashboard"] = frame
        
        # Header
        header = self.create_header("Dashboard", "Vista general del sistema")
        header.pack(fill="x", padx=30, pady=20)
        
        # Tarjetas de estadísticas
        stats_container = ctk.CTkFrame(frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=30, pady=10)
        
        # Grid de 4 columnas para las tarjetas
        self.stat_cards = {}
        stat_data = [
            ("capital", "💰 Capital Actual", "0.00", COLORS['accent']),
            ("productos", "📦 Total Productos", "0", COLORS['secondary']),
            ("ventas_hoy", "💵 Ventas Hoy", "0.00", COLORS['warning']),
            ("ganancia", "📈 Ganancia Total", "0.00", COLORS['primary'])
        ]
        
        for i, (key, titulo, valor, color) in enumerate(stat_data):
            card = self.create_stat_card(stats_container, titulo, valor, color)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            stats_container.grid_columnconfigure(i, weight=1)
            self.stat_cards[key] = card
        
        # Sección de productos con bajo stock
        products_section = ctk.CTkFrame(frame, fg_color=COLORS['bg_card'], corner_radius=15)
        products_section.pack(fill="both", expand=True, padx=30, pady=10)
        
        ctk.CTkLabel(
            products_section,
            text="⚠️ Productos con Bajo Stock",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS['text_primary']
        ).pack(anchor="w", padx=20, pady=15)
        
        # Tabla de productos con bajo stock
        self.bajo_stock_tree = self.create_modern_table(
            products_section,
            ["ID", "Producto", "Cantidad", "Precio"],
            [50, 300, 100, 100]
        )
        
    def create_productos_frame(self):
        """Crea el frame de gestión de productos"""
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["productos"] = frame
        
        # Header
        header = self.create_header("Gestión de Productos", "Administra tu inventario")
        header.pack(fill="x", padx=30, pady=20)
        
        # Contenedor principal con dos columnas
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Columna izquierda: Formulario
        left_column = ctk.CTkFrame(content, fg_color=COLORS['bg_card'], corner_radius=15, width=400)
        left_column.pack(side="left", fill="y", padx=(0, 15))
        left_column.pack_propagate(False)
        
        form_title = ctk.CTkLabel(
            left_column,
            text="➕ Agregar Producto",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS['text_primary']
        )
        form_title.pack(pady=20, padx=20, anchor="w")
        
        # Formulario
        form_container = ctk.CTkFrame(left_column, fg_color="transparent")
        form_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.producto_entries = {}
        
        # Campos del formulario
        fields = [
            ("nombre", "Nombre del Producto", "entry"),
            ("descripcion", "Descripción", "text"),
            ("categoria", "Categoría", "combo"),
            ("precio", "Precio de Venta", "entry"),
            ("costo", "Costo de Compra", "entry"),
            ("cantidad", "Cantidad", "entry")
        ]
        
        for field_name, label_text, field_type in fields:
            label = ctk.CTkLabel(
                form_container,
                text=label_text,
                font=ctk.CTkFont(size=12),
                text_color=COLORS['text_secondary']
            )
            label.pack(anchor="w", pady=(10, 5))
            
            if field_type == "entry":
                entry = ctk.CTkEntry(
                    form_container,
                    height=40,
                    corner_radius=10,
                    border_width=0,
                    fg_color=COLORS['bg_dark']
                )
                entry.pack(fill="x", pady=(0, 5))
                self.producto_entries[field_name] = entry
                
            elif field_type == "text":
                entry = ctk.CTkTextbox(
                    form_container,
                    height=80,
                    corner_radius=10,
                    border_width=0,
                    fg_color=COLORS['bg_dark']
                )
                entry.pack(fill="x", pady=(0, 5))
                self.producto_entries[field_name] = entry
                
            elif field_type == "combo":
                entry = ctk.CTkComboBox(
                    form_container,
                    values=["General", "Electrónica", "Ropa", "Alimentos", "Hogar", "Otros"],
                    height=40,
                    corner_radius=10,
                    border_width=0,
                    fg_color=COLORS['bg_dark']
                )
                entry.pack(fill="x", pady=(0, 5))
                self.producto_entries[field_name] = entry
        
        # Botones de acción
        buttons_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)
        
        self.btn_guardar_producto = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar Producto",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color=COLORS['accent'],
            hover_color="#059669",
            command=self.guardar_producto
        )
        self.btn_guardar_producto.pack(fill="x", pady=5)
        
        self.btn_limpiar = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Limpiar Formulario",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color=COLORS['bg_dark'],
            hover_color=COLORS['border'],
            command=self.limpiar_formulario_producto
        )
        self.btn_limpiar.pack(fill="x", pady=5)
        
        # Columna derecha: Lista de productos
        right_column = ctk.CTkFrame(content, fg_color=COLORS['bg_card'], corner_radius=15)
        right_column.pack(side="right", fill="both", expand=True)
        
        # Header de la tabla
        table_header = ctk.CTkFrame(right_column, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            table_header,
            text="📋 Lista de Productos",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS['text_primary']
        ).pack(side="left")
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(table_header, fg_color="transparent")
        search_frame.pack(side="right")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar producto...",
            width=250,
            height=35,
            corner_radius=10,
            border_width=0,
            fg_color=COLORS['bg_dark']
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.buscar_productos())
        
        btn_refresh = ctk.CTkButton(
            search_frame,
            text="🔄",
            width=35,
            height=35,
            corner_radius=10,
            fg_color=COLORS['primary'],
            command=self.cargar_productos
        )
        btn_refresh.pack(side="left")
        
        # Tabla de productos
        self.productos_tree = self.create_modern_table(
            right_column,
            ["ID", "Nombre", "Categoría", "Precio", "Cantidad", "Acciones"],
            [50, 250, 120, 100, 80, 150]
        )
        
        # Bind para doble clic
        self.productos_tree.tree.bind('<Double-1>', lambda e: self.editar_producto_desde_tabla())
    
    def create_ventas_frame(self):
        """Crea el frame de procesamiento de ventas"""
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["ventas"] = frame
        
        # Header
        header = self.create_header("Punto de Venta", "Procesar ventas rápidamente")
        header.pack(fill="x", padx=30, pady=20)
        
        # Contenedor principal
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Panel izquierdo: Selección de producto y cantidad
        left_panel = ctk.CTkFrame(content, fg_color=COLORS['bg_card'], corner_radius=15, width=450)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        ctk.CTkLabel(
            left_panel,
            text="🛒 Nueva Venta",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS['text_primary']
        ).pack(pady=20, padx=20, anchor="w")
        
        # Formulario de venta
        venta_form = ctk.CTkFrame(left_panel, fg_color="transparent")
        venta_form.pack(fill="x", padx=20, pady=10)
        
        # Selección de producto
        ctk.CTkLabel(
            venta_form,
            text="Seleccionar Producto",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_secondary']
        ).pack(anchor="w", pady=(0, 5))
        
        self.venta_producto_combo = ctk.CTkComboBox(
            venta_form,
            values=["Cargando..."],
            height=45,
            corner_radius=10,
            border_width=0,
            fg_color=COLORS['bg_dark'],
            command=self.actualizar_info_venta
        )
        self.venta_producto_combo.pack(fill="x", pady=(0, 15))
        
        # Cantidad
        ctk.CTkLabel(
            venta_form,
            text="Cantidad",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_secondary']
        ).pack(anchor="w", pady=(0, 5))
        
        self.venta_cantidad_entry = ctk.CTkEntry(
            venta_form,
            placeholder_text="1",
            height=45,
            corner_radius=10,
            border_width=0,
            fg_color=COLORS['bg_dark']
        )
        self.venta_cantidad_entry.pack(fill="x", pady=(0, 15))
        self.venta_cantidad_entry.bind('<KeyRelease>', lambda e: self.actualizar_info_venta())
        
        # Panel de información del producto
        info_panel = ctk.CTkFrame(left_panel, fg_color=COLORS['bg_dark'], corner_radius=10)
        info_panel.pack(fill="x", padx=20, pady=10)
        
        self.venta_info_labels = {}
        
        info_items = [
            ("producto_nombre", "Producto:", "-"),
            ("precio_unitario", "Precio Unitario:", "$0.00"),
            ("stock_disponible", "Stock Disponible:", "0"),
            ("total", "TOTAL:", "$0.00")
        ]
        
        for key, label, valor in info_items:
            item_frame = ctk.CTkFrame(info_panel, fg_color="transparent")
            item_frame.pack(fill="x", padx=15, pady=8)
            
            ctk.CTkLabel(
                item_frame,
                text=label,
                font=ctk.CTkFont(size=12),
                text_color=COLORS['text_secondary']
            ).pack(side="left")
            
            valor_label = ctk.CTkLabel(
                item_frame,
                text=valor,
                font=ctk.CTkFont(size=14 if key != "total" else 18, weight="bold"),
                text_color=COLORS['text_primary'] if key != "total" else COLORS['accent']
            )
            valor_label.pack(side="right")
            self.venta_info_labels[key] = valor_label
        
        # Botón de procesar venta
        btn_procesar = ctk.CTkButton(
            left_panel,
            text="✓ PROCESAR VENTA",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=55,
            corner_radius=12,
            fg_color=COLORS['accent'],
            hover_color="#059669",
            command=self.procesar_venta
        )
        btn_procesar.pack(fill="x", padx=20, pady=20)
        
        # Panel derecho: Ventas recientes
        right_panel = ctk.CTkFrame(content, fg_color=COLORS['bg_card'], corner_radius=15, width=500)
        right_panel.pack(side="right", fill="both", expand=True)
        right_panel.pack_propagate(False)
        
        ctk.CTkLabel(
            right_panel,
            text="📊 Ventas Recientes",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS['text_primary']
        ).pack(pady=20, padx=20, anchor="w")
        
        # Tabla de ventas recientes
        self.ventas_recientes_tree = self.create_modern_table(
            right_panel,
            ["Producto", "Cant.", "Total", "Hora"],
            [200, 60, 100, 120]
        )
    
    def create_historial_frame(self):
        """Crea el frame de historial de ventas"""
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["historial"] = frame
        
        # Header
        header = self.create_header("Historial de Ventas", "Registro completo de transacciones")
        header.pack(fill="x", padx=30, pady=20)
        
        # Contenedor
        content = ctk.CTkFrame(frame, fg_color=COLORS['bg_card'], corner_radius=15)
        content.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Header de la tabla
        table_header = ctk.CTkFrame(content, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            table_header,
            text="📜 Todas las Ventas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS['text_primary']
        ).pack(side="left")
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(table_header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        btn_exportar = ctk.CTkButton(
            btn_frame,
            text="📥 Exportar",
            width=120,
            height=35,
            corner_radius=10,
            fg_color=COLORS['secondary'],
            command=self.exportar_historial
        )
        btn_exportar.pack(side="left", padx=5)
        
        btn_refresh = ctk.CTkButton(
            btn_frame,
            text="🔄 Actualizar",
            width=120,
            height=35,
            corner_radius=10,
            fg_color=COLORS['primary'],
            command=self.cargar_historial
        )
        btn_refresh.pack(side="left", padx=5)
        
        # Tabla de historial
        self.historial_tree = self.create_modern_table(
            content,
            ["ID", "Producto", "Cantidad", "Precio Unit.", "Total", "Fecha"],
            [50, 250, 100, 120, 120, 180]
        )
    
    def create_estadisticas_frame(self):
        """Crea el frame de estadísticas y reportes"""
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["estadisticas"] = frame
        
        # Header
        header = self.create_header("Estadísticas y Reportes", "Análisis del negocio")
        header.pack(fill="x", padx=30, pady=20)
        
        # Grid de tarjetas de estadísticas
        stats_grid = ctk.CTkFrame(frame, fg_color="transparent")
        stats_grid.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Primera fila
        row1 = ctk.CTkFrame(stats_grid, fg_color="transparent")
        row1.pack(fill="x", pady=10)
        
        self.stat_labels = {}
        
        # Ganancias totales
        ganancia_card = self.create_large_stat_card(
            row1,
            "💰 Ganancias Totales",
            "$0.00",
            "+0% este mes",
            COLORS['accent']
        )
        ganancia_card.pack(side="left", fill="both", expand=True, padx=5)
        self.stat_labels['ganancias'] = ganancia_card
        
        # Ventas totales
        ventas_card = self.create_large_stat_card(
            row1,
            "🛍️ Ventas Totales",
            "0",
            "transacciones",
            COLORS['secondary']
        )
        ventas_card.pack(side="left", fill="both", expand=True, padx=5)
        self.stat_labels['ventas_totales'] = ventas_card
        
        # Segunda fila
        row2 = ctk.CTkFrame(stats_grid, fg_color="transparent")
        row2.pack(fill="x", pady=10)
        
        # Producto más vendido
        mas_vendido_card = self.create_large_stat_card(
            row2,
            "🏆 Producto Más Vendido",
            "-",
            "0 unidades",
            COLORS['warning']
        )
        mas_vendido_card.pack(side="left", fill="both", expand=True, padx=5)
        self.stat_labels['mas_vendido'] = mas_vendido_card
        
        # Capital disponible
        capital_card = self.create_large_stat_card(
            row2,
            "💵 Capital Disponible",
            "$0.00",
            "Presupuesto actual",
            COLORS['primary']
        )
        capital_card.pack(side="left", fill="both", expand=True, padx=5)
        self.stat_labels['capital'] = capital_card
        
        # Botón para gestionar presupuesto
        btn_gestionar = ctk.CTkButton(
            frame,
            text="⚙️ Gestionar Presupuesto",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color=COLORS['primary'],
            command=self.mostrar_modal_presupuesto
        )
        btn_gestionar.pack(pady=20)
    
    def create_header(self, title, subtitle):
        """Crea un header moderno para las secciones"""
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        
        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            header,
            text=subtitle,
            font=ctk.CTkFont(size=14),
            text_color=COLORS['text_secondary']
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        return header
    
    def create_stat_card(self, parent, title, value, color):
        """Crea una tarjeta de estadística"""
        card = ctk.CTkFrame(parent, fg_color=COLORS['bg_card'], corner_radius=15, height=120)
        card.pack_propagate(False)
        
        # Contenido
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(expand=True, padx=20, pady=15)
        
        # Título
        title_label = ctk.CTkLabel(
            content,
            text=title,
            font=ctk.CTkFont(size=13),
            text_color=COLORS['text_secondary']
        )
        title_label.pack(anchor="w")
        
        # Valor
        value_label = ctk.CTkLabel(
            content,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=color
        )
        value_label.pack(anchor="w", pady=(5, 0))
        
        # Guardar referencia al label del valor
        card.value_label = value_label
        
        return card
    
    def create_large_stat_card(self, parent, title, main_value, sub_value, color):
        """Crea una tarjeta de estadística grande"""
        card = ctk.CTkFrame(parent, fg_color=COLORS['bg_card'], corner_radius=15, height=150)
        card.pack_propagate(False)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(expand=True, padx=25, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            content,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color=COLORS['text_secondary']
        )
        title_label.pack(anchor="w")
        
        # Valor principal
        main_label = ctk.CTkLabel(
            content,
            text=main_value,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=color
        )
        main_label.pack(anchor="w", pady=(10, 5))
        
        # Valor secundario
        sub_label = ctk.CTkLabel(
            content,
            text=sub_value,
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_secondary']
        )
        sub_label.pack(anchor="w")
        
        # Guardar referencias
        card.main_label = main_label
        card.sub_label = sub_label
        
        return card
    
    def create_modern_table(self, parent, columns, widths):
        """Crea una tabla moderna con Treeview"""
        # Contenedor para la tabla
        table_container = ctk.CTkFrame(parent, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Estilo personalizado
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configurar colores
        style.configure(
            "Modern.Treeview",
            background=COLORS['bg_dark'],
            foreground=COLORS['text_primary'],
            fieldbackground=COLORS['bg_dark'],
            borderwidth=0,
            rowheight=40
        )
        
        style.configure(
            "Modern.Treeview.Heading",
            background=COLORS['bg_card'],
            foreground=COLORS['text_primary'],
            borderwidth=0,
            relief="flat"
        )
        
        style.map(
            "Modern.Treeview",
            background=[('selected', COLORS['primary'])],
            foreground=[('selected', COLORS['text_primary'])]
        )
        
        # Frame para tree y scrollbar
        tree_frame = ctk.CTkFrame(table_container, fg_color=COLORS['bg_dark'], corner_radius=10)
        tree_frame.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Modern.Treeview",
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )
        
        scrollbar.configure(command=tree.yview)
        
        # Configurar columnas
        for i, (col, width) in enumerate(zip(columns, widths)):
            tree.heading(col, text=col)
            tree.column(col, width=width, minwidth=width)
        
        tree.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Objeto contenedor con referencia al tree
        class TableWrapper:
            def __init__(self, tree):
                self.tree = tree
                
        return TableWrapper(tree)
    
    # ========== FUNCIONES DE DATOS ==========
    
    def cargar_datos_iniciales(self):
        """Carga todos los datos iniciales"""
        self.actualizar_dashboard()
        self.cargar_productos()
        self.cargar_productos_combo()
        self.cargar_ventas_recientes()
    
    def actualizar_dashboard(self):
        """Actualiza las estadísticas del dashboard"""
        try:
            # Obtener presupuesto
            presupuesto_data = self.db.obtener_presupuesto()
            capital = presupuesto_data[0] if presupuesto_data else 0
            
            # Obtener estadísticas
            stats = self.db.obtener_estadisticas()
            
            # Actualizar tarjetas
            self.stat_cards['capital'].value_label.configure(text=f"${capital:,.2f}")
            self.stat_cards['productos'].value_label.configure(text=str(stats['total_productos']))
            self.stat_cards['ventas_hoy'].value_label.configure(text=f"${stats['ventas_dia']:,.2f}")
            self.stat_cards['ganancia'].value_label.configure(text=f"${stats['ganancia_total']:,.2f}")
            
            # Cargar productos con bajo stock
            productos_bajo_stock = self.db.obtener_productos_bajo_stock()
            tree = self.bajo_stock_tree.tree
            
            # Limpiar tabla
            for item in tree.get_children():
                tree.delete(item)
            
            # Llenar tabla
            for p in productos_bajo_stock:
                tree.insert('', 'end', values=(
                    p[0],  # ID
                    p[1],  # Nombre
                    p[4],  # Cantidad
                    f"${p[3]:,.2f}"  # Precio
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar dashboard: {str(e)}")
    
    def cargar_productos(self):
        """Carga la lista de productos"""
        try:
            self.productos = self.db.obtener_productos()
            tree = self.productos_tree.tree
            
            # Limpiar tabla
            for item in tree.get_children():
                tree.delete(item)
            
            # Llenar tabla
            for p in self.productos:
                tree.insert('', 'end', values=(
                    p[0],  # ID
                    p[1],  # Nombre
                    p[5],  # Categoría
                    f"${p[3]:,.2f}",  # Precio
                    p[4],  # Cantidad
                    "✏️ 🗑️"  # Acciones
                ), tags=('producto',))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")
    
    def buscar_productos(self):
        """Busca productos por nombre"""
        termino = self.search_entry.get().lower()
        tree = self.productos_tree.tree
        
        # Limpiar tabla
        for item in tree.get_children():
            tree.delete(item)
        
        # Filtrar y mostrar
        for p in self.productos:
            if termino in p[1].lower():
                tree.insert('', 'end', values=(
                    p[0], p[1], p[5], f"${p[3]:,.2f}", p[4], "✏️ 🗑️"
                ))
    
    def cargar_productos_combo(self):
        """Carga los productos en el combo de ventas"""
        try:
            productos = self.db.obtener_productos()
            nombres = [f"{p[1]} (Stock: {p[4]})" for p in productos if p[4] > 0]
            
            if nombres:
                self.venta_producto_combo.configure(values=nombres)
                self.venta_producto_combo.set(nombres[0])
            else:
                self.venta_producto_combo.configure(values=["Sin productos disponibles"])
                self.venta_producto_combo.set("Sin productos disponibles")
                
        except Exception as e:
            print(f"Error al cargar combo: {e}")
    
    def cargar_ventas_recientes(self):
        """Carga las ventas recientes"""
        try:
            ventas = self.db.obtener_ventas(limite=10)
            tree = self.ventas_recientes_tree.tree
            
            # Limpiar
            for item in tree.get_children():
                tree.delete(item)
            
            # Llenar
            for v in ventas:
                fecha = datetime.strptime(v[6], '%Y-%m-%d %H:%M:%S')
                hora = fecha.strftime('%H:%M:%S')
                
                tree.insert('', 'end', values=(
                    v[2],  # Nombre producto
                    v[3],  # Cantidad
                    f"${v[5]:,.2f}",  # Total
                    hora  # Hora
                ))
                
        except Exception as e:
            print(f"Error al cargar ventas recientes: {e}")
    
    def cargar_historial(self):
        """Carga el historial completo de ventas"""
        try:
            ventas = self.db.obtener_ventas(limite=1000)
            tree = self.historial_tree.tree
            
            # Limpiar
            for item in tree.get_children():
                tree.delete(item)
            
            # Llenar
            for v in ventas:
                tree.insert('', 'end', values=(
                    v[0],  # ID
                    v[2],  # Nombre producto
                    v[3],  # Cantidad
                    f"${v[4]:,.2f}",  # Precio unitario
                    f"${v[5]:,.2f}",  # Total
                    v[6]  # Fecha
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar historial: {str(e)}")
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas completas"""
        try:
            stats = self.db.obtener_estadisticas()
            presupuesto_data = self.db.obtener_presupuesto()
            capital = presupuesto_data[0] if presupuesto_data else 0
            
            # Actualizar tarjetas
            self.stat_labels['ganancias'].main_label.configure(
                text=f"${stats['ganancia_total']:,.2f}"
            )
            
            self.stat_labels['ventas_totales'].main_label.configure(
                text=str(stats['total_ventas'])
            )
            self.stat_labels['ventas_totales'].sub_label.configure(
                text="transacciones realizadas"
            )
            
            # Producto más vendido
            mas_vendido = self.db.obtener_producto_mas_vendido()
            if mas_vendido:
                self.stat_labels['mas_vendido'].main_label.configure(
                    text=mas_vendido[0]
                )
                self.stat_labels['mas_vendido'].sub_label.configure(
                    text=f"{mas_vendido[1]} unidades vendidas"
                )
            
            self.stat_labels['capital'].main_label.configure(
                text=f"${capital:,.2f}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estadísticas: {str(e)}")
    
    # ========== FUNCIONES DE PRODUCTOS ==========
    
    def guardar_producto(self):
        """Guarda o actualiza un producto"""
        try:
            # Obtener valores
            nombre = self.producto_entries['nombre'].get().strip()
            descripcion = self.producto_entries['descripcion'].get("1.0", "end-1c").strip()
            categoria = self.producto_entries['categoria'].get()
            precio = float(self.producto_entries['precio'].get())
            costo = float(self.producto_entries['costo'].get())
            cantidad = int(self.producto_entries['cantidad'].get())
            
            # Validar
            if not nombre:
                messagebox.showwarning("Advertencia", "El nombre es obligatorio")
                return
            
            if precio <= 0 or costo <= 0 or cantidad < 0:
                messagebox.showwarning("Advertencia", "Valores inválidos")
                return
            
            # Guardar o actualizar
            if self.producto_editando:
                self.db.actualizar_producto(
                    self.producto_editando,
                    nombre, descripcion, precio, cantidad, categoria
                )
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                self.producto_editando = None
                self.btn_guardar_producto.configure(text="💾 Guardar Producto")
            else:
                resultado = self.db.agregar_producto(
                    nombre, descripcion, precio, cantidad, categoria, costo
                )
                if resultado[0]:
                    messagebox.showinfo("Éxito", "Producto agregado correctamente")
                else:
                    messagebox.showerror("Error", resultado[1])
            
            # Limpiar y recargar
            self.limpiar_formulario_producto()
            self.cargar_productos()
            self.cargar_productos_combo()
            self.actualizar_dashboard()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def limpiar_formulario_producto(self):
        """Limpia el formulario de productos"""
        self.producto_entries['nombre'].delete(0, 'end')
        self.producto_entries['descripcion'].delete("1.0", "end")
        self.producto_entries['categoria'].set("General")
        self.producto_entries['precio'].delete(0, 'end')
        self.producto_entries['costo'].delete(0, 'end')
        self.producto_entries['cantidad'].delete(0, 'end')
        self.producto_editando = None
        self.btn_guardar_producto.configure(text="💾 Guardar Producto")
    
    def editar_producto_desde_tabla(self):
        """Edita un producto desde la tabla"""
        tree = self.productos_tree.tree
        selection = tree.selection()
        
        if not selection:
            return
        
        item = tree.item(selection[0])
        producto_id = item['values'][0]
        
        # Buscar producto completo
        for p in self.productos:
            if p[0] == producto_id:
                # Llenar formulario
                self.producto_entries['nombre'].delete(0, 'end')
                self.producto_entries['nombre'].insert(0, p[1])
                
                self.producto_entries['descripcion'].delete("1.0", "end")
                self.producto_entries['descripcion'].insert("1.0", p[2] if p[2] else "")
                
                self.producto_entries['categoria'].set(p[5] if p[5] else "General")
                
                self.producto_entries['precio'].delete(0, 'end')
                self.producto_entries['precio'].insert(0, str(p[3]))
                
                self.producto_entries['costo'].delete(0, 'end')
                self.producto_entries['costo'].insert(0, str(p[3]))
                
                self.producto_entries['cantidad'].delete(0, 'end')
                self.producto_entries['cantidad'].insert(0, str(p[4]))
                
                self.producto_editando = producto_id
                self.btn_guardar_producto.configure(text="✏️ Actualizar Producto")
                
                # Cambiar a tab de productos
                self.show_frame("productos")
                break
    
    # ========== FUNCIONES DE VENTAS ==========
    
    def actualizar_info_venta(self, *args):
        """Actualiza la información de la venta"""
        try:
            seleccion = self.venta_producto_combo.get()
            if not seleccion or "Sin productos" in seleccion:
                return
            
            # Extraer nombre del producto
            nombre_producto = seleccion.split(" (Stock:")[0]
            
            # Buscar producto
            for p in self.productos:
                if p[1] == nombre_producto:
                    # Obtener cantidad
                    try:
                        cantidad = int(self.venta_cantidad_entry.get() or 0)
                    except:
                        cantidad = 0
                    
                    # Calcular total
                    total = p[3] * cantidad
                    
                    # Actualizar labels
                    self.venta_info_labels['producto_nombre'].configure(text=p[1])
                    self.venta_info_labels['precio_unitario'].configure(text=f"${p[3]:,.2f}")
                    self.venta_info_labels['stock_disponible'].configure(text=str(p[4]))
                    self.venta_info_labels['total'].configure(text=f"${total:,.2f}")
                    break
                    
        except Exception as e:
            print(f"Error al actualizar info venta: {e}")
    
    def procesar_venta(self):
        """Procesa una nueva venta"""
        try:
            seleccion = self.venta_producto_combo.get()
            if not seleccion or "Sin productos" in seleccion:
                messagebox.showwarning("Advertencia", "Selecciona un producto")
                return
            
            # Extraer nombre del producto
            nombre_producto = seleccion.split(" (Stock:")[0]
            
            # Obtener cantidad
            try:
                cantidad = int(self.venta_cantidad_entry.get())
            except:
                messagebox.showwarning("Advertencia", "Ingresa una cantidad válida")
                return
            
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            # Buscar producto y procesar venta
            for p in self.productos:
                if p[1] == nombre_producto:
                    if cantidad > p[4]:
                        messagebox.showwarning("Advertencia", "Stock insuficiente")
                        return
                    
                    # Registrar venta
                    resultado = self.db.registrar_venta(p[0], cantidad)
                    
                    if resultado[0]:
                        messagebox.showinfo("Éxito", "¡Venta procesada correctamente!")
                        
                        # Limpiar formulario
                        self.venta_cantidad_entry.delete(0, 'end')
                        self.venta_cantidad_entry.insert(0, "1")
                        
                        # Actualizar datos
                        self.cargar_productos()
                        self.cargar_productos_combo()
                        self.cargar_ventas_recientes()
                        self.actualizar_dashboard()
                        self.actualizar_info_venta()
                    else:
                        messagebox.showerror("Error", resultado[1])
                    break
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar venta: {str(e)}")
    
    # ========== OTRAS FUNCIONES ==========
    
    def exportar_historial(self):
        """Exporta el historial a CSV"""
        try:
            import csv
            from tkinter import filedialog
            
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if archivo:
                ventas = self.db.obtener_ventas(limite=10000)
                
                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['ID', 'Producto', 'Cantidad', 'Precio Unitario', 'Total', 'Fecha'])
                    
                    for v in ventas:
                        writer.writerow([v[0], v[2], v[3], v[4], v[5], v[6]])
                
                messagebox.showinfo("Éxito", "Historial exportado correctamente")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def mostrar_modal_presupuesto(self):
        """Muestra un modal para actualizar el presupuesto"""
        # Crear ventana modal
        modal = ctk.CTkToplevel(self.root)
        modal.title("Gestionar Presupuesto")
        modal.geometry("500x350")
        modal.resizable(False, False)
        
        # Centrar ventana
        modal.transient(self.root)
        modal.grab_set()
        
        # Contenido
        content = ctk.CTkFrame(modal, fg_color=COLORS['bg_card'])
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content,
            text="💰 Gestionar Capital",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS['text_primary']
        ).pack(pady=20)
        
        # Presupuesto actual
        presupuesto_data = self.db.obtener_presupuesto()
        capital_actual = presupuesto_data[0] if presupuesto_data else 0
        
        info_frame = ctk.CTkFrame(content, fg_color=COLORS['bg_dark'], corner_radius=10)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="Capital Actual:",
            font=ctk.CTkFont(size=14),
            text_color=COLORS['text_secondary']
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            info_frame,
            text=f"${capital_actual:,.2f}",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS['accent']
        ).pack(pady=(0, 15))
        
        # Nuevo presupuesto
        ctk.CTkLabel(
            content,
            text="Nuevo Capital:",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_secondary']
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        entry_presupuesto = ctk.CTkEntry(
            content,
            height=45,
            corner_radius=10,
            border_width=0,
            fg_color=COLORS['bg_dark'],
            font=ctk.CTkFont(size=16)
        )
        entry_presupuesto.pack(fill="x", padx=20, pady=(0, 20))
        entry_presupuesto.insert(0, str(capital_actual))
        
        # Botones
        def actualizar():
            try:
                nuevo_capital = float(entry_presupuesto.get())
                if nuevo_capital < 0:
                    messagebox.showwarning("Advertencia", "El capital no puede ser negativo")
                    return
                
                self.db.actualizar_presupuesto(nuevo_capital)
                messagebox.showinfo("Éxito", "Capital actualizado correctamente")
                modal.destroy()
                self.actualizar_dashboard()
                self.actualizar_estadisticas()
                
            except ValueError:
                messagebox.showerror("Error", "Ingresa un valor válido")
        
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="✓ Actualizar",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color=COLORS['accent'],
            hover_color="#059669",
            command=actualizar
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(
            buttons_frame,
            text="✕ Cancelar",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color=COLORS['danger'],
            hover_color="#DC2626",
            command=modal.destroy
        ).pack(side="right", fill="x", expand=True, padx=(5, 0))
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernInventoryApp()
    app.run()
