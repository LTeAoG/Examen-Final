"""
InvenBank Pro - Aplicación de Escritorio Mejorada
Sistema Profesional de Gestión de Inventario y Ventas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# Importar módulos del proyecto
from src.models.database_manager import DatabaseManager
from src.utils.helpers import formatear_moneda, formatear_fecha, validar_numero_positivo, validar_entero_no_negativo, exportar_a_csv
from config.settings import COLORS, ICONOS_DISPONIBLES, COLORES_DISPONIBLES, OPCIONES_ORDENAMIENTO, APP_NAME

# Configuración de tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class InvenBankApp:
    def __init__(self):
        self.db = DatabaseManager()
        self.root = ctk.CTk()
        self.root.title(APP_NAME)
        self.root.geometry("1400x850")
        
        # Variables
        self.productos = []
        self.categorias = []
        self.producto_editando = None
        self.categoria_filtro = None
        self.orden_actual = 'orden_visualizacion'
        
        # Construir interfaz
        self.build_ui()
        self.cargar_datos_iniciales()
        
    def build_ui(self):
        """Construye la interfaz principal"""
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=0, fg_color=COLORS['bg_dark'])
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo
        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(pady=30, padx=20)
        
        ctk.CTkLabel(title_frame, text="💼", font=ctk.CTkFont(size=48)).pack()
        ctk.CTkLabel(title_frame, text="InvenBank Pro", font=ctk.CTkFont(size=22, weight="bold"), 
                    text_color=COLORS['text_primary']).pack()
        ctk.CTkLabel(title_frame, text="v2.0", font=ctk.CTkFont(size=11), 
                    text_color=COLORS['text_secondary']).pack()
        
        # Botones de navegación
        self.nav_buttons = []
        self.create_nav_button("📊 Dashboard", "dashboard")
        self.create_nav_button("📦 Productos", "productos")
        self.create_nav_button("📁 Categorías", "categorias")
        self.create_nav_button("💰 Ventas", "ventas")
        self.create_nav_button("📜 Historial", "historial")
        self.create_nav_button("📈 Estadísticas", "estadisticas")
        
        # Info
        ctk.CTkLabel(self.sidebar, text="", height=50).pack(expand=True)
        info = ctk.CTkFrame(self.sidebar, fg_color=COLORS['bg_card'], corner_radius=10)
        info.pack(side="bottom", pady=20, padx=20, fill="x")
        ctk.CTkLabel(info, text=f"© {datetime.now().year}", font=ctk.CTkFont(size=10),
                    text_color=COLORS['text_secondary']).pack(pady=5)
        
        # Contenedor principal
        self.main_container = ctk.CTkFrame(self.root, fg_color=COLORS['bg_dark'], corner_radius=0)
        self.main_container.pack(side="right", fill="both", expand=True)
        
        # Crear frames
        self.frames = {}
        self.create_dashboard_frame()
        self.create_productos_frame()
        self.create_categorias_frame()
        self.create_ventas_frame()
        self.create_historial_frame()
        self.create_estadisticas_frame()
        
        self.show_frame("dashboard")
        
    def create_nav_button(self, text, frame_name):
        btn = ctk.CTkButton(self.sidebar, text=text, font=ctk.CTkFont(size=14, weight="bold"),
                           fg_color="transparent", text_color=COLORS['text_secondary'],
                           hover_color=COLORS['bg_card'], anchor="w", height=50, corner_radius=10,
                           command=lambda: self.show_frame(frame_name))
        btn.pack(pady=5, padx=20, fill="x")
        self.nav_buttons.append((btn, frame_name))
        return btn
        
    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        if frame_name in self.frames:
            self.frames[frame_name].pack(fill="both", expand=True)
        
        for btn, name in self.nav_buttons:
            if name == frame_name:
                btn.configure(fg_color=COLORS['primary'], text_color=COLORS['text_primary'])
            else:
                btn.configure(fg_color="transparent", text_color=COLORS['text_secondary'])
        
        if frame_name == "dashboard":
            self.actualizar_dashboard()
        elif frame_name == "productos":
            self.cargar_productos()
        elif frame_name == "categorias":
            self.cargar_categorias()
        elif frame_name == "historial":
            self.cargar_historial()
        elif frame_name == "estadisticas":
            self.actualizar_estadisticas()
    
    def create_dashboard_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["dashboard"] = frame
        
        header = self.create_header("Dashboard", "Vista general del sistema")
        header.pack(fill="x", padx=30, pady=20)
        
        stats_container = ctk.CTkFrame(frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=30, pady=10)
        
        self.stat_cards = {}
        stats = [
            ("capital", "💰 Capital", "0", COLORS['accent']),
            ("productos", "📦 Productos", "0", COLORS['secondary']),
            ("ventas_hoy", "💵 Ventas Hoy", "0", COLORS['warning']),
            ("ganancia", "📈 Ganancias", "0", COLORS['primary'])
        ]
        
        for i, (key, titulo, valor, color) in enumerate(stats):
            card = self.create_stat_card(stats_container, titulo, valor, color)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            stats_container.grid_columnconfigure(i, weight=1)
            self.stat_cards[key] = card
        
        products_section = ctk.CTkFrame(frame, fg_color=COLORS['bg_card'], corner_radius=15)
        products_section.pack(fill="both", expand=True, padx=30, pady=10)
        
        ctk.CTkLabel(products_section, text="⚠️ Stock Bajo", font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=COLORS['text_primary']).pack(anchor="w", padx=20, pady=15)
        
        self.bajo_stock_tree = self.create_table(products_section, ["ID", "Producto", "Stock", "Precio"], [50, 300, 80, 100])
    
    def create_productos_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["productos"] = frame
        
        header = self.create_header("Gestión de Productos", "Administra tu inventario")
        header.pack(fill="x", padx=30, pady=20)
        
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Panel izquierdo: Formulario
        left = ctk.CTkScrollableFrame(content, fg_color=COLORS['bg_card'], corner_radius=15, width=420)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)
        
        ctk.CTkLabel(left, text="➕ Agregar/Editar Producto", font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=COLORS['text_primary']).pack(pady=20, padx=20, anchor="w")
        
        form = ctk.CTkFrame(left, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.producto_entries = {}
        
        # Campos
        for field, label, tipo in [
            ("nombre", "Nombre *", "entry"),
            ("descripcion", "Descripción", "text"),
            ("categoria", "Categoría *", "combo"),
            ("precio", "Precio de Venta *", "entry"),
            ("costo", "Costo de Compra *", "entry"),
            ("cantidad", "Cantidad *", "entry"),
            ("instrucciones", "Instrucciones de Manejo", "text"),
            ("uso", "Uso Específico", "text"),
            ("notas", "Notas Adicionales", "text")
        ]:
            ctk.CTkLabel(form, text=label, font=ctk.CTkFont(size=12), 
                        text_color=COLORS['text_secondary']).pack(anchor="w", pady=(10, 5))
            
            if tipo == "entry":
                entry = ctk.CTkEntry(form, height=40, corner_radius=10, border_width=0, fg_color=COLORS['bg_dark'])
                entry.pack(fill="x")
                self.producto_entries[field] = entry
            elif tipo == "text":
                entry = ctk.CTkTextbox(form, height=60, corner_radius=10, border_width=0, fg_color=COLORS['bg_dark'])
                entry.pack(fill="x")
                self.producto_entries[field] = entry
            elif tipo == "combo":
                entry = ctk.CTkComboBox(form, values=["Cargando..."], height=40, corner_radius=10, 
                                       border_width=0, fg_color=COLORS['bg_dark'])
                entry.pack(fill="x")
                self.producto_entries[field] = entry
        
        # Botones
        buttons = ctk.CTkFrame(form, fg_color="transparent")
        buttons.pack(fill="x", pady=20)
        
        self.btn_guardar = ctk.CTkButton(buttons, text="💾 Guardar", font=ctk.CTkFont(size=14, weight="bold"),
                                         height=45, corner_radius=10, fg_color=COLORS['accent'], 
                                         hover_color="#059669", command=self.guardar_producto)
        self.btn_guardar.pack(fill="x", pady=5)
        
        ctk.CTkButton(buttons, text="🗑️ Limpiar", font=ctk.CTkFont(size=14, weight="bold"),
                     height=45, corner_radius=10, fg_color=COLORS['bg_dark'], 
                     command=self.limpiar_form_producto).pack(fill="x", pady=5)
        
        # Panel derecho: Lista
        right = ctk.CTkFrame(content, fg_color=COLORS['bg_card'], corner_radius=15)
        right.pack(side="right", fill="both", expand=True)
        
        table_header = ctk.CTkFrame(right, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(table_header, text="📋 Inventario", font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=COLORS['text_primary']).pack(side="left")
        
        # Filtros
        filters = ctk.CTkFrame(table_header, fg_color="transparent")
        filters.pack(side="right")
        
        self.orden_combo = ctk.CTkComboBox(filters, values=list(OPCIONES_ORDENAMIENTO.values()),
                                           width=180, height=35, corner_radius=10, border_width=0,
                                           fg_color=COLORS['bg_dark'], command=self.cambiar_orden)
        self.orden_combo.set("Orden Personalizado")
        self.orden_combo.pack(side="left", padx=5)
        
        ctk.CTkButton(filters, text="🔄", width=35, height=35, corner_radius=10,
                     fg_color=COLORS['primary'], command=self.cargar_productos).pack(side="left")
        
        self.productos_tree = self.create_table(right, ["ID", "Producto", "Categoría", "Precio", "Stock", ""], 
                                               [50, 250, 120, 100, 80, 150])
        self.productos_tree.tree.bind('<Double-1>', lambda e: self.editar_producto_desde_tabla())
    
    def create_categorias_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["categorias"] = frame
        
        header = self.create_header("Gestión de Categorías", "Organiza tus productos en carpetas")
        header.pack(fill="x", padx=30, pady=20)
        
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Formulario
        left = ctk.CTkFrame(content, fg_color=COLORS['bg_card'], corner_radius=15, width=400)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)
        
        ctk.CTkLabel(left, text="📁 Nueva Categoría", font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=COLORS['text_primary']).pack(pady=20, padx=20, anchor="w")
        
        cat_form = ctk.CTkFrame(left, fg_color="transparent")
        cat_form.pack(fill="x", padx=20, pady=10)
        
        self.cat_entries = {}
        
        ctk.CTkLabel(cat_form, text="Nombre *", font=ctk.CTkFont(size=12),
                    text_color=COLORS['text_secondary']).pack(anchor="w", pady=(10, 5))
        self.cat_entries['nombre'] = ctk.CTkEntry(cat_form, height=40, corner_radius=10, 
                                                  border_width=0, fg_color=COLORS['bg_dark'])
        self.cat_entries['nombre'].pack(fill="x")
        
        ctk.CTkLabel(cat_form, text="Descripción", font=ctk.CTkFont(size=12),
                    text_color=COLORS['text_secondary']).pack(anchor="w", pady=(10, 5))
        self.cat_entries['descripcion'] = ctk.CTkTextbox(cat_form, height=80, corner_radius=10,
                                                         border_width=0, fg_color=COLORS['bg_dark'])
        self.cat_entries['descripcion'].pack(fill="x")
        
        ctk.CTkLabel(cat_form, text="Color", font=ctk.CTkFont(size=12),
                    text_color=COLORS['text_secondary']).pack(anchor="w", pady=(10, 5))
        self.cat_entries['color'] = ctk.CTkComboBox(cat_form, values=[c[1] for c in COLORES_DISPONIBLES],
                                                    height=40, corner_radius=10, border_width=0, fg_color=COLORS['bg_dark'])
        self.cat_entries['color'].pack(fill="x")
        
        ctk.CTkLabel(cat_form, text="Icono", font=ctk.CTkFont(size=12),
                    text_color=COLORS['text_secondary']).pack(anchor="w", pady=(10, 5))
        self.cat_entries['icono'] = ctk.CTkComboBox(cat_form, values=ICONOS_DISPONIBLES[:20],
                                                    height=40, corner_radius=10, border_width=0, fg_color=COLORS['bg_dark'])
        self.cat_entries['icono'].pack(fill="x")
        
        ctk.CTkButton(cat_form, text="💾 Guardar Categoría", font=ctk.CTkFont(size=14, weight="bold"),
                     height=45, corner_radius=10, fg_color=COLORS['accent'], 
                     command=self.guardar_categoria).pack(fill="x", pady=20)
        
        # Lista
        right = ctk.CTkFrame(content, fg_color=COLORS['bg_card'], corner_radius=15)
        right.pack(side="right", fill="both", expand=True)
        
        ctk.CTkLabel(right, text="📁 Categorías Creadas", font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=COLORS['text_primary']).pack(anchor="w", padx=20, pady=15)
        
        self.categorias_tree = self.create_table(right, ["ID", "Icono", "Nombre", "Productos", "Acciones"],
                                                [50, 60, 200, 100, 150])
    
    def create_ventas_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["ventas"] = frame
        
        header = self.create_header("Punto de Venta", "Procesar ventas")
        header.pack(fill="x", padx=30, pady=20)
        
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=10)
        
        left = ctk.CTkFrame(content, fg_color=COLORS['bg_card'], corner_radius=15, width=450)
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        ctk.CTkLabel(left, text="🛒 Nueva Venta", font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=COLORS['text_primary']).pack(pady=20, padx=20, anchor="w")
        
        vform = ctk.CTkFrame(left, fg_color="transparent")
        vform.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(vform, text="Producto", font=ctk.CTkFont(size=12),
                    text_color=COLORS['text_secondary']).pack(anchor="w", pady=(0, 5))
        self.venta_producto = ctk.CTkComboBox(vform, values=["Cargando..."], height=45, corner_radius=10,
                                             border_width=0, fg_color=COLORS['bg_dark'],
                                             command=self.actualizar_info_venta)
        self.venta_producto.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(vform, text="Cantidad", font=ctk.CTkFont(size=12),
                    text_color=COLORS['text_secondary']).pack(anchor="w", pady=(0, 5))
        self.venta_cantidad = ctk.CTkEntry(vform, placeholder_text="1", height=45, corner_radius=10,
                                          border_width=0, fg_color=COLORS['bg_dark'])
        self.venta_cantidad.pack(fill="x", pady=(0, 15))
        self.venta_cantidad.bind('<KeyRelease>', lambda e: self.actualizar_info_venta())
        
        info_panel = ctk.CTkFrame(left, fg_color=COLORS['bg_dark'], corner_radius=10)
        info_panel.pack(fill="x", padx=20, pady=10)
        
        self.venta_info = {}
        for key, label, val in [("producto", "Producto:", "-"), ("precio", "Precio:", "$0"),
                                ("stock", "Stock:", "0"), ("total", "TOTAL:", "$0")]:
            item = ctk.CTkFrame(info_panel, fg_color="transparent")
            item.pack(fill="x", padx=15, pady=8)
            ctk.CTkLabel(item, text=label, font=ctk.CTkFont(size=12),
                        text_color=COLORS['text_secondary']).pack(side="left")
            lbl = ctk.CTkLabel(item, text=val, font=ctk.CTkFont(size=14 if key != "total" else 18, weight="bold"),
                              text_color=COLORS['text_primary'] if key != "total" else COLORS['accent'])
            lbl.pack(side="right")
            self.venta_info[key] = lbl
        
        ctk.CTkButton(left, text="✓ PROCESAR VENTA", font=ctk.CTkFont(size=16, weight="bold"),
                     height=55, corner_radius=12, fg_color=COLORS['accent'],
                     command=self.procesar_venta).pack(fill="x", padx=20, pady=20)
        
        right = ctk.CTkFrame(content, fg_color=COLORS['bg_card'], corner_radius=15, width=500)
        right.pack(side="right", fill="both", expand=True)
        right.pack_propagate(False)
        
        ctk.CTkLabel(right, text="📊 Ventas Recientes", font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=COLORS['text_primary']).pack(pady=20, padx=20, anchor="w")
        
        self.ventas_recientes_tree = self.create_table(right, ["Producto", "Cant.", "Total", "Hora"],
                                                      [200, 60, 100, 120])
    
    def create_historial_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["historial"] = frame
        
        header = self.create_header("Historial", "Registro de ventas")
        header.pack(fill="x", padx=30, pady=20)
        
        content = ctk.CTkFrame(frame, fg_color=COLORS['bg_card'], corner_radius=15)
        content.pack(fill="both", expand=True, padx=30, pady=10)
        
        table_header = ctk.CTkFrame(content, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(table_header, text="📜 Todas las Ventas", font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=COLORS['text_primary']).pack(side="left")
        
        btns = ctk.CTkFrame(table_header, fg_color="transparent")
        btns.pack(side="right")
        
        ctk.CTkButton(btns, text="📥 Exportar", width=120, height=35, corner_radius=10,
                     fg_color=COLORS['secondary'], command=self.exportar_historial).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="🔄", width=35, height=35, corner_radius=10,
                     fg_color=COLORS['primary'], command=self.cargar_historial).pack(side="left")
        
        self.historial_tree = self.create_table(content, ["ID", "Producto", "Cant.", "P.Unit", "Total", "Fecha"],
                                               [50, 250, 80, 100, 100, 180])
    
    def create_estadisticas_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["estadisticas"] = frame
        
        header = self.create_header("Estadísticas", "Análisis del negocio")
        header.pack(fill="x", padx=30, pady=20)
        
        grid = ctk.CTkFrame(frame, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=30, pady=10)
        
        self.stat_labels = {}
        
        row1 = ctk.CTkFrame(grid, fg_color="transparent")
        row1.pack(fill="x", pady=10)
        
        self.stat_labels['ganancias'] = self.create_large_card(row1, "💰 Ganancias", "$0", "Total", COLORS['accent'])
        self.stat_labels['ganancias'].pack(side="left", fill="both", expand=True, padx=5)
        
        self.stat_labels['ventas'] = self.create_large_card(row1, "🛍️ Ventas", "0", "transacciones", COLORS['secondary'])
        self.stat_labels['ventas'].pack(side="left", fill="both", expand=True, padx=5)
        
        row2 = ctk.CTkFrame(grid, fg_color="transparent")
        row2.pack(fill="x", pady=10)
        
        self.stat_labels['producto'] = self.create_large_card(row2, "🏆 Top Producto", "-", "0 ventas", COLORS['warning'])
        self.stat_labels['producto'].pack(side="left", fill="both", expand=True, padx=5)
        
        self.stat_labels['capital'] = self.create_large_card(row2, "💵 Capital", "$0", "disponible", COLORS['primary'])
        self.stat_labels['capital'].pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkButton(frame, text="⚙️ Gestionar Presupuesto", font=ctk.CTkFont(size=14, weight="bold"),
                     height=45, corner_radius=10, fg_color=COLORS['primary'],
                     command=self.modal_presupuesto).pack(pady=20)
    
    def create_header(self, title, subtitle):
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        ctk.CTkLabel(header, text=title, font=ctk.CTkFont(size=28, weight="bold"),
                    text_color=COLORS['text_primary']).pack(anchor="w")
        ctk.CTkLabel(header, text=subtitle, font=ctk.CTkFont(size=14),
                    text_color=COLORS['text_secondary']).pack(anchor="w", pady=(5, 0))
        return header
    
    def create_stat_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color=COLORS['bg_card'], corner_radius=15, height=120)
        card.pack_propagate(False)
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(expand=True, padx=20, pady=15)
        ctk.CTkLabel(content, text=title, font=ctk.CTkFont(size=13),
                    text_color=COLORS['text_secondary']).pack(anchor="w")
        card.value_label = ctk.CTkLabel(content, text=value, font=ctk.CTkFont(size=28, weight="bold"),
                                       text_color=color)
        card.value_label.pack(anchor="w", pady=(5, 0))
        return card
    
    def create_large_card(self, parent, title, main, sub, color):
        card = ctk.CTkFrame(parent, fg_color=COLORS['bg_card'], corner_radius=15, height=150)
        card.pack_propagate(False)
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(expand=True, padx=25, pady=20)
        ctk.CTkLabel(content, text=title, font=ctk.CTkFont(size=14),
                    text_color=COLORS['text_secondary']).pack(anchor="w")
        card.main_label = ctk.CTkLabel(content, text=main, font=ctk.CTkFont(size=32, weight="bold"), text_color=color)
        card.main_label.pack(anchor="w", pady=(10, 5))
        card.sub_label = ctk.CTkLabel(content, text=sub, font=ctk.CTkFont(size=12),
                                     text_color=COLORS['text_secondary'])
        card.sub_label.pack(anchor="w")
        return card
    
    def create_table(self, parent, columns, widths):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Modern.Treeview", background=COLORS['bg_dark'], foreground=COLORS['text_primary'],
                       fieldbackground=COLORS['bg_dark'], borderwidth=0, rowheight=40)
        style.configure("Modern.Treeview.Heading", background=COLORS['bg_card'], 
                       foreground=COLORS['text_primary'], borderwidth=0, relief="flat")
        style.map("Modern.Treeview", background=[('selected', COLORS['primary'])],
                 foreground=[('selected', COLORS['text_primary'])])
        
        frame = ctk.CTkFrame(container, fg_color=COLORS['bg_dark'], corner_radius=10)
        frame.pack(fill="both", expand=True)
        
        scroll = ctk.CTkScrollbar(frame)
        scroll.pack(side="right", fill="y")
        
        tree = ttk.Treeview(frame, columns=columns, show="headings", style="Modern.Treeview",
                           yscrollcommand=scroll.set, selectmode="browse")
        scroll.configure(command=tree.yview)
        
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, minwidth=width)
        
        tree.pack(fill="both", expand=True, padx=2, pady=2)
        
        class Wrapper:
            def __init__(self, t):
                self.tree = t
        return Wrapper(tree)
    
    # ========== LÓGICA DE DATOS ==========
    
    def cargar_datos_iniciales(self):
        self.actualizar_dashboard()
        self.cargar_categorias()
        self.cargar_productos()
        self.cargar_combo_categorias()
        self.cargar_combo_productos_venta()
        self.cargar_ventas_recientes()
    
    def actualizar_dashboard(self):
        try:
            capital, _ = self.db.obtener_presupuesto()
            stats = self.db.obtener_estadisticas()
            
            self.stat_cards['capital'].value_label.configure(text=formatear_moneda(capital))
            self.stat_cards['productos'].value_label.configure(text=str(stats['total_productos']))
            self.stat_cards['ventas_hoy'].value_label.configure(text=formatear_moneda(stats['ventas_dia']))
            self.stat_cards['ganancia'].value_label.configure(text=formatear_moneda(stats['ganancia_total']))
            
            bajo_stock = self.db.obtener_productos_bajo_stock()
            tree = self.bajo_stock_tree.tree
            for item in tree.get_children():
                tree.delete(item)
            for p in bajo_stock:
                tree.insert('', 'end', values=(p[0], p[1], p[4], formatear_moneda(p[3])))
        except Exception as e:
            messagebox.showerror("Error", f"Error en dashboard: {e}")
    
    def cargar_productos(self):
        try:
            self.productos = self.db.obtener_productos(self.orden_actual)
            tree = self.productos_tree.tree
            for item in tree.get_children():
                tree.delete(item)
            for p in self.productos:
                cat_nombre = p[11] if p[11] else "Sin categoría"
                tree.insert('', 'end', values=(p[0], p[1], cat_nombre, formatear_moneda(p[3]), p[4], "✏️ 🗑️"))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")
    
    def cargar_categorias(self):
        try:
            self.categorias = self.db.obtener_categorias()
            tree = self.categorias_tree.tree
            for item in tree.get_children():
                tree.delete(item)
            for c in self.categorias:
                prods = self.db.obtener_productos_por_categoria(c[0])
                tree.insert('', 'end', values=(c[0], c[4], c[1], len(prods), "✏️ 🗑️"))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar categorías: {e}")
    
    def cargar_combo_categorias(self):
        categorias = self.db.obtener_categorias()
        nombres = [f"{c[4]} {c[1]}" for c in categorias]
        if nombres:
            self.producto_entries['categoria'].configure(values=nombres)
            self.producto_entries['categoria'].set(nombres[0])
    
    def cargar_combo_productos_venta(self):
        productos = self.db.obtener_productos()
        nombres = [f"{p[1]} (Stock: {p[4]})" for p in productos if p[4] > 0]
        if nombres:
            self.venta_producto.configure(values=nombres)
            self.venta_producto.set(nombres[0])
        else:
            self.venta_producto.configure(values=["Sin productos"])
            self.venta_producto.set("Sin productos")
    
    def cargar_ventas_recientes(self):
        ventas = self.db.obtener_ventas(10)
        tree = self.ventas_recientes_tree.tree
        for item in tree.get_children():
            tree.delete(item)
        for v in ventas:
            fecha = datetime.strptime(v[6], '%Y-%m-%d %H:%M:%S')
            tree.insert('', 'end', values=(v[2], v[3], formatear_moneda(v[5]), fecha.strftime('%H:%M:%S')))
    
    def cargar_historial(self):
        ventas = self.db.obtener_ventas(1000)
        tree = self.historial_tree.tree
        for item in tree.get_children():
            tree.delete(item)
        for v in ventas:
            tree.insert('', 'end', values=(v[0], v[2], v[3], formatear_moneda(v[4]), formatear_moneda(v[5]), v[6]))
    
    def actualizar_estadisticas(self):
        stats = self.db.obtener_estadisticas()
        capital, _ = self.db.obtener_presupuesto()
        
        self.stat_labels['ganancias'].main_label.configure(text=formatear_moneda(stats['ganancia_total']))
        self.stat_labels['ventas'].main_label.configure(text=str(stats['total_ventas']))
        
        prod, cant = self.db.obtener_producto_mas_vendido()
        self.stat_labels['producto'].main_label.configure(text=prod)
        self.stat_labels['producto'].sub_label.configure(text=f"{cant} unidades")
        
        self.stat_labels['capital'].main_label.configure(text=formatear_moneda(capital))
    
    def cambiar_orden(self, seleccion):
        for key, val in OPCIONES_ORDENAMIENTO.items():
            if val == seleccion:
                self.orden_actual = key
                self.cargar_productos()
                break
    
    def guardar_producto(self):
        try:
            nombre = self.producto_entries['nombre'].get().strip()
            desc = self.producto_entries['descripcion'].get("1.0", "end-1c").strip()
            cat_sel = self.producto_entries['categoria'].get()
            precio = float(self.producto_entries['precio'].get())
            costo = float(self.producto_entries['costo'].get())
            cant = int(self.producto_entries['cantidad'].get())
            inst = self.producto_entries['instrucciones'].get("1.0", "end-1c").strip()
            uso = self.producto_entries['uso'].get("1.0", "end-1c").strip()
            notas = self.producto_entries['notas'].get("1.0", "end-1c").strip()
            
            if not nombre:
                messagebox.showwarning("Advertencia", "El nombre es obligatorio")
                return
            
            # Obtener ID de categoría
            cat_id = None
            for c in self.categorias:
                if f"{c[4]} {c[1]}" == cat_sel:
                    cat_id = c[0]
                    break
            
            if self.producto_editando:
                self.db.actualizar_producto(self.producto_editando, nombre, desc, precio, cant, cat_id, inst, uso, notas)
                messagebox.showinfo("Éxito", "Producto actualizado")
            else:
                resultado = self.db.agregar_producto(nombre, desc, precio, cant, cat_id, costo, inst, uso, notas)
                if resultado[0]:
                    messagebox.showinfo("Éxito", "Producto agregado")
                else:
                    messagebox.showerror("Error", resultado[1])
            
            self.limpiar_form_producto()
            self.cargar_productos()
            self.cargar_combo_productos_venta()
            self.actualizar_dashboard()
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def limpiar_form_producto(self):
        self.producto_entries['nombre'].delete(0, 'end')
        self.producto_entries['descripcion'].delete("1.0", "end")
        self.producto_entries['precio'].delete(0, 'end')
        self.producto_entries['costo'].delete(0, 'end')
        self.producto_entries['cantidad'].delete(0, 'end')
        self.producto_entries['instrucciones'].delete("1.0", "end")
        self.producto_entries['uso'].delete("1.0", "end")
        self.producto_entries['notas'].delete("1.0", "end")
        self.producto_editando = None
        self.btn_guardar.configure(text="💾 Guardar")
    
    def editar_producto_desde_tabla(self):
        tree = self.productos_tree.tree
        sel = tree.selection()
        if not sel:
            return
        prod_id = tree.item(sel[0])['values'][0]
        for p in self.productos:
            if p[0] == prod_id:
                self.producto_entries['nombre'].insert(0, p[1])
                self.producto_entries['descripcion'].insert("1.0", p[2] or "")
                self.producto_entries['precio'].insert(0, str(p[3]))
                self.producto_entries['costo'].insert(0, str(p[3]))
                self.producto_entries['cantidad'].insert(0, str(p[4]))
                self.producto_entries['instrucciones'].insert("1.0", p[6] or "")
                self.producto_entries['uso'].insert("1.0", p[7] or "")
                self.producto_entries['notas'].insert("1.0", p[8] or "")
                self.producto_editando = prod_id
                self.btn_guardar.configure(text="✏️ Actualizar")
                self.show_frame("productos")
                break
    
    def guardar_categoria(self):
        try:
            nombre = self.cat_entries['nombre'].get().strip()
            desc = self.cat_entries['descripcion'].get("1.0", "end-1c").strip()
            color_nombre = self.cat_entries['color'].get()
            icono = self.cat_entries['icono'].get()
            
            color_hex = COLORS['secondary']
            for hex_val, nombre_color in COLORES_DISPONIBLES:
                if nombre_color == color_nombre:
                    color_hex = hex_val
                    break
            
            if not nombre:
                messagebox.showwarning("Advertencia", "El nombre es obligatorio")
                return
            
            resultado = self.db.crear_categoria(nombre, desc, color_hex, icono)
            if resultado[0]:
                messagebox.showinfo("Éxito", "Categoría creada")
                self.cat_entries['nombre'].delete(0, 'end')
                self.cat_entries['descripcion'].delete("1.0", "end")
                self.cargar_categorias()
                self.cargar_combo_categorias()
            else:
                messagebox.showerror("Error", resultado[1])
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def actualizar_info_venta(self, *args):
        try:
            sel = self.venta_producto.get()
            if "Sin productos" in sel:
                return
            nombre = sel.split(" (Stock:")[0]
            for p in self.productos:
                if p[1] == nombre:
                    try:
                        cant = int(self.venta_cantidad.get() or 0)
                    except:
                        cant = 0
                    total = p[3] * cant
                    self.venta_info['producto'].configure(text=p[1])
                    self.venta_info['precio'].configure(text=formatear_moneda(p[3]))
                    self.venta_info['stock'].configure(text=str(p[4]))
                    self.venta_info['total'].configure(text=formatear_moneda(total))
                    break
        except:
            pass
    
    def procesar_venta(self):
        try:
            sel = self.venta_producto.get()
            if "Sin productos" in sel:
                messagebox.showwarning("Advertencia", "Selecciona un producto")
                return
            nombre = sel.split(" (Stock:")[0]
            cant = int(self.venta_cantidad.get())
            
            if cant <= 0:
                messagebox.showwarning("Advertencia", "Cantidad inválida")
                return
            
            for p in self.productos:
                if p[1] == nombre:
                    if cant > p[4]:
                        messagebox.showwarning("Advertencia", "Stock insuficiente")
                        return
                    resultado = self.db.registrar_venta(p[0], cant)
                    if resultado[0]:
                        messagebox.showinfo("Éxito", "¡Venta procesada!")
                        self.venta_cantidad.delete(0, 'end')
                        self.venta_cantidad.insert(0, "1")
                        self.cargar_productos()
                        self.cargar_combo_productos_venta()
                        self.cargar_ventas_recientes()
                        self.actualizar_dashboard()
                        self.actualizar_info_venta()
                    else:
                        messagebox.showerror("Error", resultado[1])
                    break
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def exportar_historial(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", 
                                              filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
        if archivo:
            ventas = self.db.obtener_ventas(10000)
            if exportar_a_csv(ventas, ['ID', 'Producto', 'Cantidad', 'Precio', 'Total', 'Fecha'], archivo):
                messagebox.showinfo("Éxito", "Historial exportado")
            else:
                messagebox.showerror("Error", "No se pudo exportar")
    
    def modal_presupuesto(self):
        modal = ctk.CTkToplevel(self.root)
        modal.title("Gestionar Capital")
        modal.geometry("500x350")
        modal.resizable(False, False)
        modal.transient(self.root)
        modal.grab_set()
        
        content = ctk.CTkFrame(modal, fg_color=COLORS['bg_card'])
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content, text="💰 Gestionar Capital", font=ctk.CTkFont(size=24, weight="bold"),
                    text_color=COLORS['text_primary']).pack(pady=20)
        
        capital, _ = self.db.obtener_presupuesto()
        
        info = ctk.CTkFrame(content, fg_color=COLORS['bg_dark'], corner_radius=10)
        info.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(info, text="Capital Actual:", font=ctk.CTkFont(size=14),
                    text_color=COLORS['text_secondary']).pack(pady=(15, 5))
        ctk.CTkLabel(info, text=formatear_moneda(capital), font=ctk.CTkFont(size=28, weight="bold"),
                    text_color=COLORS['accent']).pack(pady=(0, 15))
        
        ctk.CTkLabel(content, text="Nuevo Capital:", font=ctk.CTkFont(size=12),
                    text_color=COLORS['text_secondary']).pack(anchor="w", padx=20, pady=(20, 5))
        entry = ctk.CTkEntry(content, height=45, corner_radius=10, border_width=0, fg_color=COLORS['bg_dark'],
                            font=ctk.CTkFont(size=16))
        entry.pack(fill="x", padx=20, pady=(0, 20))
        entry.insert(0, str(capital))
        
        def actualizar():
            try:
                nuevo = float(entry.get())
                if nuevo < 0:
                    messagebox.showwarning("Advertencia", "No puede ser negativo")
                    return
                self.db.actualizar_presupuesto(nuevo)
                messagebox.showinfo("Éxito", "Capital actualizado")
                modal.destroy()
                self.actualizar_dashboard()
                self.actualizar_estadisticas()
            except ValueError:
                messagebox.showerror("Error", "Valor inválido")
        
        btns = ctk.CTkFrame(content, fg_color="transparent")
        btns.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(btns, text="✓ Actualizar", font=ctk.CTkFont(size=14, weight="bold"), height=45,
                     corner_radius=10, fg_color=COLORS['accent'], command=actualizar).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(btns, text="✕ Cancelar", font=ctk.CTkFont(size=14, weight="bold"), height=45,
                     corner_radius=10, fg_color=COLORS['danger'], command=modal.destroy).pack(side="right", fill="x", expand=True, padx=(5, 0))
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = InvenBankApp()
    app.run()
