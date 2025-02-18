from tkinter import *
from tkinter import Tk, messagebox
from tkinter import ttk
from tkinter.ttk import Checkbutton, Style as ttkCheckbutton, Style
from PIL import ImageTk, Image
from config import COLOR_CUERPO_PRINCIPAL, COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA
import util.utilTransportes as utilTransportes
import util.utilImagenes as utilImagenes
import util.utilClustering as utilClustering
import util.utilDatos as utilDatos
import util.utilInfo as utilInfo
import tkintermapview
import numpy as np
from tkinter import font
import math
import os
from tkinter import filedialog
import json
from tkinter.font import Font
import random
import re
import requests
import webbrowser

class FormMapaDesign():

    def __init__(self, panel_principal, menuLateral):
        
        self.panel_principal = panel_principal

        self.frame_mapa = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_mapa.pack(fill="both")

        
        #Para poder borrar los mapas de calor
        self.poligonos_estaciones = []
        self.poligonos_estaciones_ocupacion = []
        self.poligonos_bicicletas = []
        self.poligonos_bicicletas_clusters = []
        self.poligonos_centroides_bicicletas = []
        self.poligonos_patinetes = []
        self.poligonos_patinetes_clusters = []
        self.poligonos_centroides_patinetes = []
        self.poligonos_demanda_bicicletas = []
        self.poligonos_demanda_patinetes = []
        self.poligonos_zonas = {}

        #Para poder borrar el poligono de seleccion
        self.pol_seleccion = None
        self.est_seleccion = None

        self.botones_anadidos = []

        self.estaciones = utilTransportes.devolver_estaciones()

        self.maxLon, self.minLon, self.maxLat, self.minLat = utilTransportes.limites(self.estaciones)

        self.bicicletas_flotantes = utilTransportes.generar_flotantes_v2(self.estaciones, 0.005)
        self.patinetes = utilTransportes.generar_patinetes(self.estaciones, 0.005, self.maxLon, self.minLon, self.maxLat, self.minLat)
        self.solicitudes_bicicletas = 1000
        self.demanda_bicicletas = utilDatos.generar_datos_demanda(self.solicitudes_bicicletas, self.maxLon, self.minLon, self.maxLat, self.minLat)
        self.solicitudes_patinetes = 500
        self.demanda_patinetes = utilDatos.generar_datos_demanda(self.solicitudes_patinetes, self.maxLon, self.minLon, self.maxLat, self.minLat)

        #Variables radiobutton
        self.seleccionado_metros = StringVar()
        self.seleccionado_influencia =  StringVar()
        self.tipo_mapa_anterior = 'General'
        self.tipo_mapa = StringVar(value='General')

        #Clustering
        self.clustering_bicicletas = {}
        self.clustering_patinetes = {}

        #Inicio sesion api
        self.sesion_iniciada = False
        self.token = ''

        self.cargados_estaciones = {}
        self.cargados_estaciones['Tomar datos en tiempo real'] = [None, False]
        self.cargados_estaciones['estaciones_16-04-2024_23h.json'] = [self.estaciones, True]
        self.selected_archivo_estaciones = StringVar(value='estaciones_16-04-2024_23h.json')
        self.estaciones_anterior = 'estaciones_16-04-2024_23h.json'
        self.num_archivos_aleatorios_est = 0

        self.cargados_bicicletas = {}
        self.cargados_bicicletas['bicicletas_generadas_estaciones.json'] = [self.bicicletas_flotantes, True]
        self.clustering_bicicletas['bicicletas_generadas_estaciones.json'] = {'clusters': np.array([]), 'centroides': np.array([])}
        self.selected_archivo_bicicletas = StringVar(value='bicicletas_generadas_estaciones.json')
        self.bicicletas_anterior = 'bicicletas_generadas_estaciones.json'
        self.num_archivos_aleatorios_bic = 0

        self.cargados_patinetes = {}
        self.cargados_patinetes['patinetes_generados_estaciones.json'] = [self.patinetes, True]
        self.clustering_patinetes['patinetes_generados_estaciones.json'] = {'clusters': np.array([]), 'centroides': np.array([])}
        self.selected_archivo_patinetes = StringVar(value='patinetes_generados_estaciones.json')
        self.patinetes_anterior = 'patinetes_generados_estaciones.json'
        self.num_archivos_aleatorios_pat = 0

        self.cargados_demanda_bicicletas = {}
        self.cargados_demanda_bicicletas['solicitudes_1000_bicicletas.json'] = [self.demanda_bicicletas, True]
        self.selected_archivo_solicitudes_bicicletas = StringVar(value='solicitudes_1000_bicicletas.json')
        self.bicicletas_solicitudes_anterior = 'solicitudes_1000_bicicletas.json'

        self.cargados_demanda_patinetes = {}
        self.cargados_demanda_patinetes['solicitudes_500_patinetes.json'] = [self.demanda_patinetes, True]
        self.selected_archivo_solicitudes_patinetes = StringVar(value='solicitudes_500_patinetes.json')
        self.patinetes_solicitudes_anterior = 'solicitudes_500_patinetes.json'

        self.color_map = {
            0: '#FF0000',   # Rojo
            1: '#00FF00',   # Verde
            2: '#0000FF',   # Azul
            3: '#FFFF00',   # Amarillo
            4: '#FF00FF',   # Magenta
            5: '#00FFFF',   # Cian
            6: '#FFA500',   # Naranja
            7: '#800080',   # Púrpura
            8: '#FFC0CB',   # Rosa
            9: '#A52A2A',   # Marrón
            10: '#808080',  # Gris
            11: '#FFD700',  # Dorado
            12: '#ADFF2F',  # Verde Lima
            13: '#000080',  # Azul Marino
            14: '#4682B4',  # Azul Acero
            15: '#5F9EA0',  # Verde Cadete
            16: '#D2691E',  # Chocolate
            17: '#FF4500',  # Naranja Rojo
            18: '#2E8B57',  # Verde Mar
            19: '#6A5ACD',  # Azul Pizarra
            20: '#7FFF00',  # Chartreuse
            21: '#FF1493',  # Rosa Profundo
            22: '#B0C4DE',  # Azul Claro
            23: '#32CD32',  # Verde Lima
            24: '#FF6347',  # Tomate
            25: '#FF8C00',  # Naranja Oscuro
            26: '#1E90FF',  # Azul Dodger
            27: '#FFDAB9',  # Durazno
            28: '#C71585',  # Rosa Medio
            29: '#191970',  # Azul Medianoche
            30: '#B22222',  # Rojo Fuego
            31: '#7FFF00',  # Verde Lima
            32: '#20B2AA',  # Verde Claro
            33: '#FF69B4',  # Rosa Hot
            34: '#CD5C5C',  # Coral
            35: '#A9A9A9',  # Gris Oscuro
            36: '#B8860B',  # Dorado Oscuro
            37: '#F0E68C',  # Amarillo Khaaki
            38: '#FFB6C1',  # Rosa Claro
            39: '#BDB76B',  # Oliva
            40: '#228B22',  # Verde Bosque
            41: '#8B008B',  # Púrpura Oscuro
            42: '#FF7F50',  # Coral
            43: '#FFD700',  # Dorado
            44: '#FF4500',  # Naranja Rojo
            45: '#00FA9A',  # Verde Medio
            46: '#9370DB',  # Púrpura Medio
            47: '#DDA0DD',  # Púrpura Claro
            48: '#B0E0E6',  # Azul Pálido
            49: '#800000',  # Rojo Marrón
            -1: '#000000'   # Ruido en negro
        }
        
        #Ajustes por defecto mapa de calor
        self.influencia = 'con'
        self.clasificacion = "General"

        anadir_mapa(self)

        self.menuLateral = menuLateral
        self.menu_lateral()

        #creacion_paneles_info(self, panel_principal)

    def anadir_scrollbar(self):
        #scrollbar = Scrollbar(self.menuLateral, orient=VERTICAL)
        #scrollbar.pack(side=RIGHT, fill=Y)

        canvas = Canvas(self.menuLateral, 
                        #yscrollcommand=scrollbar.set, 
                        yscrollcommand=None,
                        width=225,
                        bg=COLOR_MENU_LATERAL)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        #scrollbar.config(command=canvas.yview)

        scrollable_frame = Frame(canvas, bg=COLOR_MENU_LATERAL, width=225)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind("<Configure>", lambda event: self.actualizar_scrollregion(canvas))

        canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas(event,canvas))

        return scrollable_frame

    def actualizar_scrollregion(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def scroll_canvas(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def menu_lateral(self):
        self.scrollable_frame = self.anadir_scrollbar()
        #ya se habia creado el menu anteriormente, se termina la funcion
        if hasattr(self, 'labelTipoTransporte'):
            return
        self.submenus = {}

        self.crear_carga_datos()
        self.crear_tipo_transporte()
        self.crear_mapa_calor()
        #self.crear_otras_opciones()
        self.crear_demanda()

    def crear_carga_datos(self):
        fontAwesome=font.Font(family="FontAwesome", size=12, weight="bold")
        style = Style()
        style.configure("Custom.TCheckbutton", font=("FontAwesome", 10), anchor="w", background=COLOR_MENU_LATERAL,
                        foreground="white", bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2, indicatorcolor="green")

        frame_opcion = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_opcion.pack(fill=X, pady=4)

        frame_submenu = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_submenu.pack(fill=X, padx=10, pady=2)

        boton_principal = Button(frame_opcion, text='Gestor de datos', bg=COLOR_MENU_LATERAL, fg = 'white', relief = FLAT,
                                font=fontAwesome, command=lambda: self.toggle_submenu('Gestor de datos'), width=22, height=0)
        boton_principal.pack(fill=X)
        self.bindHoverEvents(boton_principal)

        self.buttonGestorEstaciones = Button(frame_submenu, text="\uf3c5    Gestor de estaciones", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=lambda: self.gestor_estaciones())
        self.buttonGestorEstaciones.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=22, height=2)
        self.buttonGestorEstaciones.pack(side=TOP)
        self.bindHoverEvents(self.buttonGestorEstaciones)

        self.buttonGestorBicicletas = Button(frame_submenu, text="    Gestor de bicicletas", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=lambda: self.gestor_bicicletas())
        self.buttonGestorBicicletas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=22, height=2)
        self.buttonGestorBicicletas.pack(side=TOP)
        self.bindHoverEvents(self.buttonGestorBicicletas)

        self.buttonGestorPatinetes = Button(frame_submenu, text="    Gestor de patinetes", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=lambda: self.gestor_patinetes())
        self.buttonGestorPatinetes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=22, height=2)
        self.buttonGestorPatinetes.pack(side=TOP)
        self.bindHoverEvents(self.buttonGestorPatinetes)

        self.submenus['Gestor de datos'] = {"titulo": boton_principal, "frame_opcion": frame_opcion,
                                               "frame_submenu": frame_submenu, "visible": True}

    def crear_tipo_transporte(self):

        fontAwesome=font.Font(family="FontAwesome", size=12, weight='bold')
        style = Style()
        style.configure("Custom.TCheckbutton", font=("FontAwesome", 10), anchor="w", background=COLOR_MENU_LATERAL,
                        foreground="white", bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2, indicatorcolor="green")

        frame_opcion = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_opcion.pack(fill=X, pady=2)

        boton_principal = Button(frame_opcion, text='Visualización Transportes', bg=COLOR_MENU_LATERAL, fg = 'white', relief = FLAT,
                                font=fontAwesome, command=lambda: self.toggle_submenu('Tipo de Transporte'), width=22, height=0)
        boton_principal.pack(fill=X, expand=True)
        self.bindHoverEvents(boton_principal)

        frame_submenu = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_submenu.pack(fill=X, padx=10, pady=2)
        #frame_submenu.pack_forget()

        frame_submenu_fijas = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_submenu_fijas.pack(fill=X, padx=10, pady=1)

        frame_subopciones_fijas = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_subopciones_fijas.pack(fill=X, padx=10, pady=2)
        
        self.checkbox_fijas = BooleanVar()
        self.buttonEstacionesFijas = Checkbutton(frame_submenu_fijas, text="\uf3c5 Estaciones fijas", style="Custom.TCheckbutton",
                                                 variable=self.checkbox_fijas, command= lambda : self.boton_fijas(self.checkbox_fijas))
        self.buttonEstacionesFijas.pack(side=LEFT, pady=5)

        self.checkbox_ocupacion = BooleanVar()
        self.buttonEstacionesOcupacion = Checkbutton(frame_subopciones_fijas, text="Nivel de ocupación", 
            style="Custom.TCheckbutton", variable=self.checkbox_ocupacion, 
            command=lambda: self.boton_fijas_ocupacion(self.checkbox_ocupacion))
        self.buttonEstacionesOcupacion.pack(side=TOP, pady=5)

        frame_submenu_bicicletas = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_submenu_bicicletas.pack(fill=X, padx=10, pady=2)

        frame_subopciones_bicicletas = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_subopciones_bicicletas.pack(fill=X, padx=10, pady=2)

        self.checkbox_bicicletas = BooleanVar()
        self.buttonBicicletasFlotantes = Checkbutton(frame_submenu_bicicletas, text=" Bicicletas flotantes", 
            style="Custom.TCheckbutton", variable=self.checkbox_bicicletas, 
            command=lambda: self.boton_bicicletas(self.checkbox_bicicletas, clusters=False))
        self.buttonBicicletasFlotantes.pack(side=LEFT, pady=5)

        frame_agruparB = Frame(frame_subopciones_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_agruparB.pack(fill=X, side=TOP)

        frame_centroidesB = Frame(frame_subopciones_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_centroidesB.pack(fill=X, side=TOP)

        self.checkbox_agrupar_bicicletas = BooleanVar()
        self.buttonAgruparBicicletas = Checkbutton(frame_agruparB, text="Agrupar en clusters",
            style="Custom.TCheckbutton",variable=self.checkbox_agrupar_bicicletas,
            command=lambda: self.boton_bicicletas(self.checkbox_agrupar_bicicletas, clusters=True))
        self.buttonAgruparBicicletas.pack(side=TOP, pady=5)

        self.checkbox_centroides_bicicletas = BooleanVar()
        self.buttonCentroidesBicicletas = Checkbutton(frame_centroidesB, text="Estaciones virtuales",
            style="Custom.TCheckbutton",variable=self.checkbox_centroides_bicicletas,
            command=lambda: self.boton_centroides_bicicletas(self.checkbox_centroides_bicicletas))
        self.buttonCentroidesBicicletas.pack(side=TOP, pady=5)

        frame_submenu_patinetes = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_submenu_patinetes.pack(fill=X, padx=10, pady=2)

        frame_subopciones_patinetes = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_subopciones_patinetes.pack(fill=X, padx=10, pady=2)

        self.checkbox_patinetes = BooleanVar()
        self.buttonPatinetes = Checkbutton(frame_submenu_patinetes, text=" Patinetes", style="Custom.TCheckbutton",
                                                    variable=self.checkbox_patinetes, command=lambda: self.boton_patinetes(self.checkbox_patinetes, clusters=False))
        self.buttonPatinetes.pack(side=LEFT, pady=5)

        frame_agruparP = Frame(frame_subopciones_patinetes, bg=COLOR_MENU_LATERAL)
        frame_agruparP.pack(fill=X, side=TOP)

        frame_centroidesP = Frame(frame_subopciones_patinetes, bg=COLOR_MENU_LATERAL)
        frame_centroidesP.pack(fill=X, side=TOP)

        self.checkbox_agrupar_patinetes = BooleanVar()
        self.buttonAgruparPatinetes = Checkbutton(frame_agruparP, text="Agrupar en clusters",
            style="Custom.TCheckbutton",variable=self.checkbox_agrupar_patinetes,
            command=lambda: self.boton_patinetes(self.checkbox_agrupar_patinetes, clusters=True))
        self.buttonAgruparPatinetes.pack(side=TOP, pady=5)

        self.checkbox_centroides_patinetes = BooleanVar()
        self.buttonCentroidesPatinetes = Checkbutton(frame_centroidesP, text="Estaciones virtuales",
            style="Custom.TCheckbutton",variable=self.checkbox_centroides_patinetes,
            command=lambda: self.boton_centroides_patinetes(self.checkbox_centroides_patinetes))
        self.buttonCentroidesPatinetes.pack(side=TOP, pady=5)

        self.submenus['Tipo de Transporte'] = {"titulo": boton_principal, "frame_opcion": frame_opcion,
                                               "frame_submenu": frame_submenu, "visible": True}

    def crear_mapa_calor(self):
        
        fontAwesome=font.Font(family="FontAwesome", size=12, weight='bold')
        style = Style()
        style.configure("Custom.TCheckbutton", font=("FontAwesome", 10), anchor="w", background=COLOR_MENU_LATERAL,
                        foreground="white", bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2, indicatorcolor="green")

        frame_opcion = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_opcion.pack(fill=X, pady=2)

        boton_principal = Button(frame_opcion, text='Mapa de Calor', bg=COLOR_MENU_LATERAL, fg = 'white', relief = FLAT,
                                font=fontAwesome, command=lambda: self.toggle_submenu('Mapa de Calor'), width=18, height=0)
        boton_principal.pack(fill=X, side=LEFT)
        self.bindHoverEvents(boton_principal)

        frame_submenu = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_submenu.pack(fill=X, padx=10, pady=2)
        #frame_submenu.pack_forget()

        
        self.frame_mostrar_mapa_estaciones = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        self.frame_mostrar_mapa_estaciones.pack(fill=X, padx=10, pady=2, side=TOP)
        self.checkbox_mapa_estaciones = BooleanVar()
        self.buttonMostrarMapaEstaciones = Checkbutton(self.frame_mostrar_mapa_estaciones, text="\uf3c5 Estaciones fijas", style="Custom.TCheckbutton",
                                                       variable=self.checkbox_mapa_estaciones, command=self.mostrar_mapa)
        self.buttonMostrarMapaEstaciones.pack(side=LEFT, pady=5)

        self.frame_mostrar_mapa_bicicletas = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        self.frame_mostrar_mapa_bicicletas.pack(fill=X, padx=10, pady=2, side=TOP)
        self.checkbox_mapa_flotantes = BooleanVar()
        self.buttonMostrarMapaFlotantes = Checkbutton(self.frame_mostrar_mapa_bicicletas, text=" Bicicletas flotantes", style="Custom.TCheckbutton",
                                                variable=self.checkbox_mapa_flotantes, command= self.mostrar_mapa)
        self.buttonMostrarMapaFlotantes.pack(side=LEFT, pady=5)

        self.frame_mostrar_mapa_patinetes = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        self.frame_mostrar_mapa_patinetes.pack(fill=X, padx=10, pady=2, side=TOP)
        self.checkbox_mapa_patinetes = BooleanVar()
        self.buttonMostrarMapaPatinetes = Checkbutton(self.frame_mostrar_mapa_patinetes, text=" Patinetes", style="Custom.TCheckbutton",
                                                variable=self.checkbox_mapa_patinetes, command= self.mostrar_mapa)
        self.buttonMostrarMapaPatinetes.pack(side=LEFT, pady=5)

        self.submenus['Mapa de Calor'] = {"titulo": boton_principal, "frame_opcion": frame_opcion, 
                                          "frame_submenu": frame_submenu, "visible": True}

        frame_opcion = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_opcion.pack(fill=X, pady=2)

        boton_principal = Button(frame_opcion, text='Tipo de Mapa', bg=COLOR_MENU_LATERAL, fg = 'white', relief = FLAT,
                                font=font.Font(family="FontAwesome", size=11, weight='bold'), command=lambda: self.toggle_submenu('Tipo de Mapa'), width=18, height=0)
        boton_principal.pack(fill=X)
        self.bindHoverEvents(boton_principal)

        frame_tipos = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_tipos.pack(fill=X, padx=10, pady=2)
        #frame_tipos.pack_forget()

        ################################## Mapa General ######################################

        frame_general_titulo = Frame(frame_tipos, bg=COLOR_MENU_LATERAL)
        frame_general_titulo.pack(fill=X, padx=5, pady=2)

        frame_general_subopciones = Frame(frame_tipos, bg=COLOR_MENU_LATERAL)
        frame_general_subopciones.pack(fill=X, padx=5, pady=2)

        radiobutton_general = Radiobutton(frame_general_titulo, text="Mapa General", variable=self.tipo_mapa,
            value="General", font=("FontAwesome", 10), background=COLOR_MENU_LATERAL, foreground="white",
            selectcolor=COLOR_MENU_LATERAL, fg='white', anchor=W, justify=LEFT, command=lambda: self.cambiar_tipo())
        radiobutton_general.pack(anchor="w", padx=5, pady=2)

        frame_general_cambios = Frame(frame_general_subopciones, bg=COLOR_MENU_LATERAL)
        frame_general_cambios.pack(fill=X, padx=5, pady=2, side=TOP)

        Button(frame_general_cambios, text="Modificar influencia", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
            command=lambda: self.modificar_influencia()).pack(side=RIGHT, expand=True, padx=5)
        
        frame_general_cambios = Frame(frame_general_subopciones, bg=COLOR_MENU_LATERAL)
        frame_general_cambios.pack(fill=X, padx=5, pady=2, side=TOP)
        
        Button(frame_general_cambios, text="Modificar cuadrícula", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
            command=lambda: self.modificar_cuadricula()).pack(side=RIGHT, expand=True, padx=5)
        
        self.submenus['Mapa General'] = {"titulo": radiobutton_general, "frame_opcion": frame_general_titulo, 
                                          "frame_submenu": frame_general_subopciones, "visible": True}

        ################################## Mapa Porcentaje Llenado ######################################

        frame_llenado_titulo = Frame(frame_tipos, bg=COLOR_MENU_LATERAL)
        frame_llenado_titulo.pack(fill=X, padx=5, pady=2)

        frame_llenado_subopciones = Frame(frame_tipos, bg=COLOR_MENU_LATERAL)
        frame_llenado_subopciones.pack(fill=X, padx=5, pady=2)
        frame_llenado_subopciones.pack_forget()

        radiobutton_llenado = Radiobutton(frame_llenado_titulo, text="Mapa Porcentaje Llenado", variable=self.tipo_mapa, 
            value="Llenado", font=("FontAwesome", 10), background=COLOR_MENU_LATERAL, foreground="white",
            selectcolor=COLOR_MENU_LATERAL, fg='white', anchor=W, justify=LEFT, command=lambda: self.cambiar_tipo())
        radiobutton_llenado.pack(anchor="w", padx=5, pady=2)
        
        frame_llenado_cambios1 = Frame(frame_llenado_subopciones, bg=COLOR_MENU_LATERAL)
        frame_llenado_cambios1.pack(fill=X, padx=5, pady=2, side=TOP)
        
        Button(frame_llenado_cambios1, text="Modificar cuadrícula", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
            command=lambda: self.modificar_cuadricula()).pack(side=RIGHT, expand=True, padx=5)
        
        self.submenus['Mapa Llenado'] = {"titulo": radiobutton_llenado, "frame_opcion": frame_llenado_titulo, 
                                          "frame_submenu": frame_llenado_subopciones, "visible": False}

        ################################## Mapa Huecos ######################################

        frame_huecos_titulo = Frame(frame_tipos, bg=COLOR_MENU_LATERAL)
        frame_huecos_titulo.pack(fill=X, padx=5, pady=2)

        frame_huecos_subopciones = Frame(frame_tipos, bg=COLOR_MENU_LATERAL)
        frame_huecos_subopciones.pack(fill=X, padx=5, pady=2)
        frame_huecos_subopciones.pack_forget()

        radiobutton_huecos = Radiobutton(frame_huecos_titulo, text="Mapa de Huecos", variable=self.tipo_mapa, 
            value="Huecos", font=("FontAwesome", 10), background=COLOR_MENU_LATERAL, foreground="white",
            selectcolor=COLOR_MENU_LATERAL, fg='white', anchor=W, justify=LEFT, command=lambda: self.cambiar_tipo())
        radiobutton_huecos.pack(anchor="w", padx=5, pady=2)

        frame_huecos_cambios = Frame(frame_huecos_subopciones, bg=COLOR_MENU_LATERAL)
        frame_huecos_cambios.pack(fill=X, padx=5, pady=2, side=TOP)

        Button(frame_huecos_cambios, text="Modificar influencia", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
            command=lambda: self.modificar_influencia()).pack(side=RIGHT, expand=True, padx=5)
        
        frame_huecos_cambios = Frame(frame_huecos_subopciones, bg=COLOR_MENU_LATERAL)
        frame_huecos_cambios.pack(fill=X, padx=5, pady=2, side=TOP)
        
        Button(frame_huecos_cambios, text="Modificar cuadrícula", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
            command=lambda: self.modificar_cuadricula()).pack(side=RIGHT, expand=True, padx=5)
        
        self.submenus['Mapa Huecos'] = {"titulo": radiobutton_huecos, "frame_opcion": frame_huecos_titulo, 
                                          "frame_submenu": frame_huecos_subopciones, "visible": False}

        self.submenus['Tipo de Mapa'] = {"titulo": boton_principal, "frame_opcion": frame_opcion, 
                                          "frame_submenu": frame_tipos, "visible": True}
        
        Button(frame_tipos, text="Confirmar", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA, 
               command=lambda: self.confirmar_tipo()).pack(expand=True, padx=5)

    def crear_demanda(self):
        fontAwesome=font.Font(family="FontAwesome", size=12, weight="bold")
        style = Style()
        style.configure("Custom.TCheckbutton", font=("FontAwesome", 10), anchor="w", background=COLOR_MENU_LATERAL,
                        foreground="white", bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=23, height=2, indicatorcolor="green")

        frame_opcion = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_opcion.pack(fill=X, pady=2)

        boton_principal = Button(frame_opcion, text='Demanda', bg=COLOR_MENU_LATERAL, fg = 'white', relief = FLAT,
                                font=fontAwesome, command=lambda: self.toggle_submenu('Demanda'), width=22, height=0)
        boton_principal.pack(fill=X)
        self.bindHoverEvents(boton_principal)

        frame_submenu = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_submenu.pack(fill=X, padx=10, pady=2)
        #frame_submenu.pack_forget()

        self.submenus['Demanda'] = {"titulo": boton_principal, "frame_opcion": frame_opcion, 
                                          "frame_submenu": frame_submenu, "visible": True}

        frame_solicitudes= Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_solicitudes.pack(side=TOP, fill=X, pady=2)

        self.buttonSolicitudes = Button(frame_solicitudes, text="Solicitudes", font=font.Font(family="FontAwesome", size=11, weight="bold"),
                                    command=lambda: self.toggle_submenu('Solicitudes'))
        self.buttonSolicitudes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonSolicitudes.pack(side=TOP)
        self.bindHoverEvents(self.buttonSolicitudes)

        frame_submenu_solicitudes = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_submenu_solicitudes.pack(fill=X, pady=2)

        frame_bicicletas = Frame(frame_submenu_solicitudes, bg=COLOR_MENU_LATERAL)
        frame_bicicletas.pack(pady=0)

        self.checkbox_demanda_bicicletas = BooleanVar()
        self.buttonDemandaBicicletas = Checkbutton(frame_bicicletas, text=" Solicitudes de Bicicletas", style="Custom.TCheckbutton",
                                                    variable=self.checkbox_demanda_bicicletas, 
                                                    command=lambda: self.boton_demanda_bicicletas(self.checkbox_demanda_bicicletas))
        self.buttonDemandaBicicletas.pack(side=LEFT, padx=2, pady=0, anchor=CENTER)

        """self.buttonGenerarDemandaBicicletas = Button(frame_bicicletas, text="", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=self.generar_datos_demanda_bicicletas)
        self.buttonGenerarDemandaBicicletas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=2, height=2)
        self.buttonGenerarDemandaBicicletas.pack(side=LEFT, padx=2, pady=0, anchor=CENTER)"""

        self.buttonGestorDemandaBicicletas = Button(frame_bicicletas, text="", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=self.gestor_demanda_bicicletas)
        self.buttonGestorDemandaBicicletas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=2, height=2)
        self.buttonGestorDemandaBicicletas.pack(side=LEFT, padx=2, pady=0, anchor=CENTER)

        frame_patinetes = Frame(frame_submenu_solicitudes, bg=COLOR_MENU_LATERAL)
        frame_patinetes.pack(pady=0)

        self.checkbox_demanda_patinetes = BooleanVar()
        self.buttonDemandaPatinetes = Checkbutton(frame_patinetes, text=" Solicitudes de Patinetes", style="Custom.TCheckbutton",
                                                    variable=self.checkbox_demanda_patinetes, 
                                                    command=lambda: self.boton_demanda_patinetes(self.checkbox_demanda_patinetes))
        self.buttonDemandaPatinetes.pack(side=LEFT, padx=2, pady=0, anchor=CENTER)

        self.buttonGenerarDemandaPatinetes = Button(frame_patinetes, text="", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=self.generar_datos_demanda_patinetes)
        self.buttonGenerarDemandaPatinetes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=2, height=2)
        self.buttonGenerarDemandaPatinetes.pack(side=LEFT, padx=2, pady=0, anchor=CENTER)

        self.submenus['Solicitudes'] = {"titulo": self.buttonSolicitudes, "frame_opcion": frame_solicitudes, 
                                          "frame_submenu": frame_submenu_solicitudes, "visible": True}
        
        frame_ofertademanda = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_ofertademanda.pack(side=TOP, fill=X, pady=2)

        self.buttonOfertaDemanda = Button(frame_ofertademanda, text="Mapa de oferta-demanda", font=font.Font(family="FontAwesome", size=11, weight="bold"),
                                    anchor='w', command=lambda: self.toggle_submenu('Oferta Demanda'))
        self.buttonOfertaDemanda.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonOfertaDemanda.pack(side=TOP)
        self.bindHoverEvents(self.buttonOfertaDemanda)

        frame_opciones_ofertademanda = Frame(frame_submenu, bg=COLOR_MENU_LATERAL)
        frame_opciones_ofertademanda.pack(side=TOP, fill=X, pady=2)

        self.buttonMapaCalorDemandaBicicletas = Button(frame_opciones_ofertademanda, text=" Oferta-demanda bicicletas", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=self.mostrar_mapa_demanda_bicicletas)
        self.buttonMapaCalorDemandaBicicletas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=22, height=2)
        self.buttonMapaCalorDemandaBicicletas.pack(side=TOP)
        self.bindHoverEvents(self.buttonMapaCalorDemandaBicicletas)

        self.buttonMapaCalorDemandaPatinetes = Button(frame_opciones_ofertademanda, text=" Oferta-demanda patinetes", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=self.mostrar_mapa_demanda_patinetes)
        self.buttonMapaCalorDemandaPatinetes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=22, height=2)
        self.buttonMapaCalorDemandaPatinetes.pack(side=TOP)
        self.bindHoverEvents(self.buttonMapaCalorDemandaPatinetes)

        self.buttonBorrarMapa = Button(frame_opciones_ofertademanda, text=" Borrar mapa de calor", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= self.borrar_mapacalor)
        self.buttonBorrarMapa.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonBorrarMapa.pack(side=TOP)
        self.bindHoverEvents(self.buttonBorrarMapa)

        self.submenus['Oferta Demanda'] = {"titulo": self.buttonOfertaDemanda, "frame_opcion": frame_ofertademanda, 
                                          "frame_submenu": frame_opciones_ofertademanda, "visible": True}

    def toggle_submenu(self, texto_opcion):
        submenu = self.submenus[texto_opcion]
        if submenu["visible"]:
            submenu["frame_submenu"].pack_forget()
            submenu["visible"] = False
            #submenu['titulo'] = submenu['titulo'].config(text="▶" + submenu['titulo'].cget("text"))
        else:
            submenu["frame_submenu"].pack(after=submenu["frame_opcion"], fill=X)
            submenu["visible"] = True
            #submenu['titulo'] = submenu['titulo'].config(text="▼" + submenu['titulo'].cget("text"))
    
    def anadir_scrollbar_estaciones(self, frame):
        #scrollbar = Scrollbar(self.menuLateral, orient=VERTICAL)
        #scrollbar.pack(side=RIGHT, fill=Y)

        canvas = Canvas(frame, 
                        #yscrollcommand=scrollbar.set, 
                        yscrollcommand=None,
                        width=200,
                        bg=COLOR_MENU_LATERAL)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        #scrollbar.config(command=canvas.yview)

        scrollable_frame = Frame(canvas, bg=COLOR_MENU_LATERAL, width=200)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind("<Configure>", lambda event: self.actualizar_scrollregion_estaciones(canvas))

        canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas_estaciones(event,canvas))

        return scrollable_frame

    def actualizar_scrollregion_estaciones(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def scroll_canvas_estaciones(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def gestor_estaciones(self):
        self.ventana_gestor_estaciones = Toplevel(self.frame_mapa)
        self.ventana_gestor_estaciones.title("Gestor datos estaciones")

        ancho_pantalla = self.ventana_gestor_estaciones.winfo_screenwidth()
        alto_pantalla = self.ventana_gestor_estaciones.winfo_screenheight()

        ancho_ventana = 350
        alto_ventana = 400

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_gestor_estaciones.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.ventana_gestor_estaciones.resizable(False, False)
        self.ventana_gestor_estaciones.config(bg=COLOR_MENU_LATERAL)
        self.ventana_gestor_estaciones.protocol("WM_DELETE_WINDOW", self.ventana_gestor_estaciones.destroy)

        frame_estaciones = Frame(self.ventana_gestor_estaciones, bg=COLOR_MENU_LATERAL)
        frame_estaciones.pack(fill=BOTH, expand=True, padx=20, pady=20)

        titulo_font = Font(family="Arial", size=12, weight="bold")

        ######################## COLUMNA ESTACIONES ######################    

        Label(frame_estaciones, text='Estaciones', font=titulo_font, anchor=W,bg=COLOR_MENU_LATERAL, fg="white").pack(anchor=CENTER, pady=(0, 10))

        texto_cargados = 'Seleccione la fuente de datos:'

        Label(frame_estaciones, text=texto_cargados, bg=COLOR_MENU_LATERAL, fg="white", anchor=CENTER, justify=CENTER).pack(fill=BOTH, padx=5, pady=5)

        frame_radiobuttons_estaciones = Frame(frame_estaciones, bg=COLOR_MENU_LATERAL)
        frame_radiobuttons_estaciones.pack(fill=BOTH, expand=True, padx=5, pady=5)
        #frame_radiobuttons_estaciones = self.anadir_scrollbar_estaciones(frame_radiobuttons_estaciones)

        if len(self.cargados_estaciones) != 0:
            for id, archivo in self.cargados_estaciones.items():
                if archivo[1]:
                    self.selected_archivo_estaciones.set(id)

                fila_frame = Frame(frame_radiobuttons_estaciones, bg=COLOR_MENU_LATERAL)
                fila_frame.pack(fill="x", padx=5, pady=2, anchor="w")

                Radiobutton(fila_frame, text=id, variable=self.selected_archivo_estaciones,
                    value=id, bg=COLOR_MENU_LATERAL, selectcolor=COLOR_MENU_LATERAL,
                    fg='white', anchor="w", justify="left",
                    command=self.select_button
                ).pack(side="left", padx=5, pady=2)

                if id != 'Tomar datos en tiempo real':
                    boton_descarga = Button(fila_frame, text="", font=Font(family="FontAwesome", size=10), fg="white", 
                        bg=COLOR_MENU_LATERAL, command=lambda: utilDatos.guardar_json(id, archivo[0])
                    )
                    boton_descarga.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=2, height=2)
                    boton_descarga.pack(side="left", padx=5)
                


        frame_botones_superior = Frame(frame_estaciones, bg=COLOR_MENU_LATERAL)
        frame_botones_superior.pack(side=TOP, fill=X, pady=5)

        frame_botones_inferior = Frame(frame_estaciones, bg=COLOR_MENU_LATERAL)
        frame_botones_inferior.pack(side=TOP, fill=X, pady=5)

        Button(frame_botones_superior, text="Cargar Archivos", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA, 
               command=lambda: self.cargar_archivo('estaciones', visualizador=True)).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_superior, text="Importar datos históricos", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
            command=lambda: self.selector_fecha()).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_inferior, text="Aplicar Cambios", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
            command=lambda: self.aplicar_cambios('estaciones')).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_inferior, text="Generar datos aleatorios", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
            command=lambda: self.ventana_datos_aleatorios('estaciones')
        ).pack(side=LEFT, fill=X, expand=True, padx=5)

    def gestor_bicicletas(self):
        self.ventana_gestor_bicicletas = Toplevel(self.frame_mapa)
        self.ventana_gestor_bicicletas.title("Gestor datos bicicletas")

        ancho_pantalla = self.ventana_gestor_bicicletas.winfo_screenwidth()
        alto_pantalla = self.ventana_gestor_bicicletas.winfo_screenheight()

        ancho_ventana = 350
        alto_ventana = 400

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_gestor_bicicletas.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.ventana_gestor_bicicletas.resizable(False, False)
        self.ventana_gestor_bicicletas.config(bg=COLOR_MENU_LATERAL)
        self.ventana_gestor_bicicletas.protocol("WM_DELETE_WINDOW", self.ventana_gestor_bicicletas.destroy)

        frame_bicicletas = Frame(self.ventana_gestor_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_bicicletas.pack(fill=BOTH, expand=True, padx=20, pady=20)

        titulo_font = Font(family="Arial", size=12, weight="bold")

        Label(frame_bicicletas, text='Bicicletas', font=titulo_font, anchor=W, bg=COLOR_MENU_LATERAL, fg="white").pack(anchor=CENTER, pady=(0, 10))

        texto_cargados = 'Seleccione la fuente de datos:'

        Label(frame_bicicletas, text=texto_cargados, bg=COLOR_MENU_LATERAL, fg="white", anchor=CENTER, justify=CENTER).pack(fill=BOTH, padx=5, pady=5)

        frame_radiobuttons_bicicletas = Frame(frame_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_radiobuttons_bicicletas.pack(fill=BOTH, expand=True, padx=5, pady=5)

        if len(self.cargados_bicicletas) != 0:
            for id, archivo in self.cargados_bicicletas.items():
                if archivo[1]:
                    self.selected_archivo_bicicletas.set(id)

                fila_frame = Frame(frame_radiobuttons_bicicletas, bg=COLOR_MENU_LATERAL)
                fila_frame.pack(fill="x", padx=5, pady=2, anchor="w")

                Radiobutton(fila_frame, text=id, variable=self.selected_archivo_bicicletas, value=id, 
                    bg=COLOR_MENU_LATERAL, selectcolor=COLOR_MENU_LATERAL, fg='white', anchor="w",
                    justify="left", command=self.select_button).pack(side="left", padx=5, pady=2)

                boton_descarga = Button(fila_frame, text="", font=Font(family="FontAwesome", size=10), fg="white", 
                    bg=COLOR_MENU_LATERAL, command=lambda id=id, archivo=archivo: utilDatos.guardar_json(id, archivo[0])
                )
                boton_descarga.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=2, height=2)
                boton_descarga.pack(side="left", padx=5)
                

        frame_botones_superior = Frame(frame_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_botones_superior.pack(side=TOP, fill=X, pady=5)

        frame_botones_inferior = Frame(frame_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_botones_inferior.pack(side=TOP, fill=X, pady=5)

        Button(frame_botones_superior, text="Cargar Archivos", bg=COLOR_MENU_CURSOR_ENCIMA, fg='white',
            command=lambda: self.cargar_archivo('bicicletas', visualizador=True)).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_superior, text="Aplicar Cambios", bg=COLOR_MENU_CURSOR_ENCIMA, fg='white',
            command=lambda: self.aplicar_cambios('bicicletas')
        ).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_inferior, text="Generar datos aleatorios", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
            command=lambda: self.ventana_datos_aleatorios('bicicletas')
        ).pack(side=LEFT, fill=X, expand=True, padx=5)
    
    def gestor_patinetes(self):
        self.ventana_gestor_patinetes = Toplevel(self.frame_mapa)
        self.ventana_gestor_patinetes.title("Ventana datos patinetes")

        ancho_pantalla = self.ventana_gestor_patinetes.winfo_screenwidth()
        alto_pantalla = self.ventana_gestor_patinetes.winfo_screenheight()

        ancho_ventana = 350
        alto_ventana = 400

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_gestor_patinetes.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.ventana_gestor_patinetes.resizable(False, False)
        self.ventana_gestor_patinetes.config(bg=COLOR_MENU_LATERAL)
        self.ventana_gestor_patinetes.protocol("WM_DELETE_WINDOW", self.ventana_gestor_patinetes.destroy)

        frame_patinetes = Frame(self.ventana_gestor_patinetes, bg=COLOR_MENU_LATERAL)
        frame_patinetes.pack(fill=BOTH, expand=True, padx=20, pady=20)

        titulo_font = Font(family="Arial", size=12, weight="bold")

        Label(frame_patinetes, text='Patinetes', font=titulo_font, anchor=W, bg=COLOR_MENU_LATERAL, fg="white").pack(anchor=CENTER, pady=(0, 10))

        texto_cargados = '\n\nSeleccione la fuente de datos:'

        Label(frame_patinetes, text=texto_cargados, bg=COLOR_MENU_LATERAL, fg="white", anchor=CENTER, justify=CENTER).pack(fill=BOTH, padx=5, pady=5)

        frame_radiobuttons_patinetes = Frame(frame_patinetes, bg=COLOR_MENU_LATERAL)
        frame_radiobuttons_patinetes.pack(fill=BOTH, expand=True, padx=5, pady=5)

        if len(self.cargados_patinetes) != 0:
            for id, archivo in self.cargados_patinetes.items():
                if archivo[1]:
                    self.selected_archivo_patinetes.set(id)
                
                fila_frame = Frame(frame_radiobuttons_patinetes, bg=COLOR_MENU_LATERAL)
                fila_frame.pack(fill="x", padx=5, pady=2, anchor="w")

                Radiobutton(fila_frame, text=id, variable=self.selected_archivo_patinetes,
                    value=id, bg=COLOR_MENU_LATERAL, selectcolor=COLOR_MENU_LATERAL,fg='white', 
                    anchor="w", justify="left", command=self.select_button).pack(side="left", padx=5, pady=2)
                
                boton_descarga = Button(fila_frame, text="", font=Font(family="FontAwesome", size=10), fg="white", 
                    bg=COLOR_MENU_LATERAL, command=lambda: utilDatos.guardar_json(id, archivo[0])
                )
                boton_descarga.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=2, height=2)
                boton_descarga.pack(side="left", padx=5)

        frame_botones_superior = Frame(frame_patinetes, bg=COLOR_MENU_LATERAL)
        frame_botones_superior.pack(side=TOP, fill=X, pady=5)

        frame_botones_inferior = Frame(frame_patinetes, bg=COLOR_MENU_LATERAL)
        frame_botones_inferior.pack(side=TOP, fill=X, pady=5)

        Button(frame_botones_superior, text="Cargar Archivos", bg=COLOR_MENU_CURSOR_ENCIMA, fg='white',
            command=lambda: self.cargar_archivo('patinetes', visualizador=True)).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_superior, text="Aplicar Cambios", bg=COLOR_MENU_CURSOR_ENCIMA, fg='white',
            command=lambda: self.aplicar_cambios('patinetes')
        ).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_inferior, text="Generar datos aleatorios", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
            command=lambda: self.ventana_datos_aleatorios('patinetes')
        ).pack(side=LEFT, fill=X, expand=True, padx=5)
    
    def gestor_demanda_bicicletas(self):
        self.ventana_gestor_demanda_bicicletas = Toplevel(self.frame_mapa)
        self.ventana_gestor_demanda_bicicletas.title("Gestor datos demanda bicicletas")

        ancho_pantalla = self.ventana_gestor_demanda_bicicletas.winfo_screenwidth()
        alto_pantalla = self.ventana_gestor_demanda_bicicletas.winfo_screenheight()

        ancho_ventana = 350
        alto_ventana = 400

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_gestor_demanda_bicicletas.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.ventana_gestor_demanda_bicicletas.resizable(False, False)
        self.ventana_gestor_demanda_bicicletas.config(bg=COLOR_MENU_LATERAL)
        self.ventana_gestor_demanda_bicicletas.protocol("WM_DELETE_WINDOW", self.ventana_gestor_demanda_bicicletas.destroy)

        frame_demanda_bicicletas = Frame(self.ventana_gestor_demanda_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_demanda_bicicletas.pack(fill=BOTH, expand=True, padx=20, pady=20)

        titulo_font = Font(family="Arial", size=12, weight="bold")

        Label(frame_demanda_bicicletas, text='Demanda de Bicicletas', font=titulo_font, anchor=W, bg=COLOR_MENU_LATERAL, fg="white").pack(anchor=CENTER, pady=(0, 10))

        texto_cargados = 'Seleccione la fuente de datos:'

        Label(frame_demanda_bicicletas, text=texto_cargados, bg=COLOR_MENU_LATERAL, fg="white", anchor=CENTER, justify=CENTER).pack(fill=BOTH, padx=5, pady=5)

        frame_radiobuttons_bicicletas = Frame(frame_demanda_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_radiobuttons_bicicletas.pack(fill=BOTH, expand=True, padx=5, pady=5)

        if len(self.cargados_demanda_bicicletas) != 0:
            for id, archivo in self.cargados_demanda_bicicletas.items():
                if archivo[1]:
                    self.selected_archivo_solicitudes_bicicletas.set(id)

                fila_frame = Frame(frame_radiobuttons_bicicletas, bg=COLOR_MENU_LATERAL)
                fila_frame.pack(fill="x", padx=5, pady=2, anchor="w")

                Radiobutton(fila_frame, text=id, variable=self.selected_archivo_solicitudes_bicicletas, value=id, 
                    bg=COLOR_MENU_LATERAL, selectcolor=COLOR_MENU_LATERAL, fg='white', anchor="w",
                    justify="left", command=self.select_button).pack(side="left", padx=5, pady=2)

                boton_descarga = Button(fila_frame, text="", font=Font(family="FontAwesome", size=10), fg="white", 
                    bg=COLOR_MENU_LATERAL, command=lambda id=id, archivo=archivo: utilDatos.guardar_json(id, archivo[0])
                )
                boton_descarga.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=2, height=2)
                boton_descarga.pack(side="left", padx=5)
                

        frame_botones_superior = Frame(frame_demanda_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_botones_superior.pack(side=TOP, fill=X, pady=5)

        frame_botones_inferior = Frame(frame_demanda_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_botones_inferior.pack(side=TOP, fill=X, pady=5)

        Button(frame_botones_superior, text="Cargar Archivos", bg=COLOR_MENU_CURSOR_ENCIMA, fg='white',
            command=lambda: self.cargar_archivo('demanda bicicletas', visualizador=True)).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_superior, text="Aplicar Cambios", bg=COLOR_MENU_CURSOR_ENCIMA, fg='white',
            command=lambda: self.aplicar_cambios('demanda bicicletas')
        ).pack(side=LEFT, fill=X, expand=True, padx=5)

        #Button(frame_botones_inferior, text="Generar datos aleatorios", fg='white', bg=COLOR_MENU_CURSOR_ENCIMA,
        #    command=lambda: self.generar_datos_demanda_bicicletas
        #).pack(side=LEFT, fill=X, expand=True, padx=5)
    
    def bindHoverEvents(self, button):
        #Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        #Cambiar el estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg="white")
        
    def on_leave(self, event, button):
        #Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg="white")
        
    def pintar_mapa(self):
        utilInfo.close_infozona(self)
        if hasattr (self, "frame_leyenda"):
            self.frame_leyenda.destroy()

        if self.checkbox_mapa_estaciones.get()==False and self.checkbox_mapa_flotantes.get()==False \
            and self.checkbox_mapa_patinetes.get()==False \
            and self.clasificacion != 'Demanda Bicicletas' and self.clasificacion != 'Demanda Patinetes':
            return
        
        if not hasattr(self, 'influencia'):
            self.influencia = 'con'

        if not hasattr(self, 'n'):
            metros = 500
            lon_objetivo = metros/(111320*math.cos(40.4))
            lat_objetivo = metros/111320 
            n_lon = abs(self.maxLon - self.minLon) / lon_objetivo
            n_lat = abs(self.maxLat - self.minLat) / lat_objetivo
            self.n = math.ceil(max(n_lon, n_lat))
       
        self.lon_celda = (self.maxLon - self.minLon) / self.n
        self.lat_celda = (self.maxLat - self.minLat) / self.n


        if self.clasificacion == "Llenado":
            self.dic_mapa_calor = utilTransportes.crear_diccionario(
                self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                estaciones=self.estaciones, add_fijas=True)
        elif self.clasificacion == "Huecos":
            self.dic_mapa_calor = utilTransportes.crear_diccionario(
                    self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                    estaciones=self.estaciones,mostrar_huecos=True)
        elif self.clasificacion == "Demanda Bicicletas":
            self.dic_mapa_calor = utilTransportes.crear_diccionario(
                    self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                    estaciones=self.estaciones,flotantes= self.bicicletas_flotantes,
                    demanda_bicicletas=self.demanda_bicicletas, demanda_patinetes=self.demanda_patinetes,
                    mostrar_demanda_bicicletas=True, add_fijas=True, add_flotantes=True)
        elif self.clasificacion == "Demanda Patinetes":
            self.dic_mapa_calor = utilTransportes.crear_diccionario(
                    self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                    patinetes=self.patinetes,
                    demanda_bicicletas=self.demanda_bicicletas, demanda_patinetes=self.demanda_patinetes,
                    mostrar_demanda_patinetes=True, add_patinetes=True)
        else:
            #print(f'Est: {self.checkbox_mapa_estaciones.get()}, Flot: {self.checkbox_mapa_flotantes.get()}')
            self.dic_mapa_calor = utilTransportes.crear_diccionario(
                    self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda,
                    estaciones=self.estaciones, flotantes=self.bicicletas_flotantes, patinetes=self.patinetes,
                    add_fijas=self.checkbox_mapa_estaciones.get(), add_flotantes=self.checkbox_mapa_flotantes.get(),
                    add_patinetes=self.checkbox_mapa_patinetes.get())
            
            if self.n == 44: self.alcance = 3
            elif self.n == 54: self.alcance = 5
            elif self.n == 72: self.alcance = 7
            elif self.n == 108: self.alcance = 9
            if self.influencia == 'con':
                self.dic_mapa_calor['cantidades_suavizadas'] = self.aplicar_gaussiana(self.dic_mapa_calor['cantidades'], self.alcance)
        with open('diccionario_demanda.json', 'w', encoding='utf-8') as archivo:
            json.dump(self.dic_mapa_calor, archivo, ensure_ascii=False, indent=4)
        colores = ["#FF3300", "#FF6600", "#FF9933", "#FFCC33", "#FFDD33", "#FFFF00", "#CCFF66", "#99FF66", "#66FF33", "#00FF00"]
        
        """minimo = np.min(self.dic_mapa_calor['factor_oferta_demanda_bicicletas'])
        maximo = np.max(self.dic_mapa_calor['factor_oferta_demanda_bicicletas'])
        index_min = np.argmin(self.dic_mapa_calor['factor_oferta_demanda_bicicletas'])
        index_max = np.argmax(self.dic_mapa_calor['factor_oferta_demanda_bicicletas'])
        print(f'Influencia: {self.influencia}')
        print(f'Min: {minimo}, max: {maximo}')
        print(f'El indice de la menor es: {index_min} y se trata de la zona {self.dic_mapa_calor['ids'][index_min]}')
        print(f'El indice de la mayor es: {index_max} y se trata de la zona {self.dic_mapa_calor['ids'][index_max]}')
        """
        for i in range(pow(self.n, 2)):
            if self.clasificacion == 'General' and self.influencia=='con':
                factor_llenado = self.dic_mapa_calor['cantidades_suavizadas'][i]
                contador = sum([self.checkbox_mapa_estaciones.get(),
                                self.checkbox_mapa_flotantes.get(),
                                self.checkbox_mapa_patinetes.get()])
                if contador==3: # Si hay tres medios seleccionados, los rangos son de 0-100 aprox
                    rangos = [0, 2, 10, 18, 26, 34, 44, 56, 70, 84, 1000]
                elif contador==2: # Si hay dos medios seleccionados, los rangos son de 0-65 aprox 
                    rangos = [0, 1, 6, 12, 18, 24, 30, 36, 42, 50, 1000]
                elif contador==1: # Si hay uno , los rangos son de 0-33 aprox 
                    rangos = [0, 1, 4, 7, 10, 13, 16, 19, 22, 25, 1000]

            elif self.clasificacion == 'General' and self.influencia=='sin':
                factor_llenado = self.dic_mapa_calor['cantidades'][i]
                contador = sum([self.checkbox_mapa_estaciones.get(),
                                self.checkbox_mapa_flotantes.get(),
                                self.checkbox_mapa_patinetes.get()])
                if contador==3: # Si hay tres medios seleccionados, los rangos son de ????? aprox
                    rangos = [0, 8, 20, 34, 48, 64, 82, 100, 120, 142, 1000]
                elif contador==2: # Si hay dos medios seleccionados, los rangos son de 0-92/106 aprox 
                    rangos = [0, 4, 12, 20, 28, 38, 48, 60, 72, 84, 1000]
                elif contador==1: # Si hay uno , los rangos son de 0-61/46 aprox 
                    rangos = [0, 1, 6, 12, 18, 24, 30, 36, 42, 50, 1000]

            elif self.clasificacion == 'Llenado' or self.clasificacion == 'Huecos':
                rangos = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                if self.dic_mapa_calor['capacidades'][i] != 0:
                    factor_llenado = (self.dic_mapa_calor['cantidades'][i]/self.dic_mapa_calor['capacidades'][i])*100
                else: factor_llenado = 0
            elif self.clasificacion == 'Demanda Bicicletas':
                rangos = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                bicicletas_disponibles = self.dic_mapa_calor['cantidades'][i]
                solicitudes =  self.dic_mapa_calor['demanda_bicicletas'][i]
                factor_llenado=100*(bicicletas_disponibles-solicitudes)/(bicicletas_disponibles+solicitudes+5)
            elif self.clasificacion == 'Demanda Patinetes':
                rangos = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                patinetes_disponibles = self.dic_mapa_calor['cantidades'][i]
                solicitudes =  self.dic_mapa_calor['demanda_patinetes'][i]
                factor_llenado=100*(patinetes_disponibles-solicitudes)/(patinetes_disponibles+solicitudes+5)
            color = utilTransportes.get_color(factor_llenado, rangos, colores)
            
            if factor_llenado != 0 and (not self.clasificacion == 'Llenado' or self.checkbox_mapa_estaciones.get()): #los que son 0 no pintarlos
                poligono = self.labelMap.set_polygon(self.dic_mapa_calor['coordenadas'][i],
                                        fill_color=color,
                                        outline_color=None,
                                        #outline_color="grey",
                                        #border_width=1,
                                        name=f'Zona {self.dic_mapa_calor['ids'][i]}')
                if self.n in self.poligonos_zonas:
                    self.poligonos_zonas[self.n].append(poligono)
                else:
                    self.poligonos_zonas[self.n] = [poligono]

        ############################       Leyenda     ##############################
        self.frame_leyenda = Frame(self.panel_principal, width=20, height=100, bg=None)
        self.frame_leyenda.place(relx=0.9, rely=0.3, width=50, height=210)
        
        i=10
        for color in colores[::-1]:
            if self.clasificacion == 'General':
                rangos[-1]='...'
                color_label = Label(self.frame_leyenda, width=50, height=1, bg=color, text=f"{rangos[i-1]}-{rangos[i]}")
            else:
                color_label = Label(self.frame_leyenda, width=50, height=1, bg=color, text=f"{rangos[i-1]}-{rangos[i]}%")
            color_label.pack()
            i=i-1

        if self.checkbox_mapa_estaciones.get()==False and \
        self.checkbox_mapa_flotantes.get()==False and \
        self.checkbox_mapa_patinetes.get()==False and \
        self.clasificacion != 'Demanda Bicicletas' and self.clasificacion != 'Demanda Patinetes':
            self.frame_leyenda.destroy()
        ###############################################################################

        ##################################### BOTONES RIGHT CLICK ##################################
        mostrados=""
        if self.checkbox_mapa_estaciones.get()==True:   mostrados+="estaciones "
        if self.checkbox_mapa_flotantes.get()==True:    mostrados+="flotantes "
        if self.checkbox_mapa_patinetes.get()==True:    mostrados+="patinetes "
        tipo_mapa = (self.n, self.clasificacion, mostrados)
        if not tipo_mapa in self.botones_anadidos:
            self.botones_anadidos.append(tipo_mapa)
            if self.n == 44: metros=500
            elif self.n == 54: metros=400
            elif self.n == 72: metros=300
            elif self.n == 108: metros=200
            if self.clasificacion=="General":
                self.labelMap.add_right_click_menu_command(label=f"Info zona con {metros}m mapa {mostrados}",
                                            command=lambda event: utilInfo.show_info_zona(self, coords=(event[0], event[1])),
                                            pass_coords=True)
            else:
                self.labelMap.add_right_click_menu_command(label=f"Info zona con {metros}m mapa {self.clasificacion}",
                                            command=lambda event: utilInfo.show_info_zona(self, coords=(event[0], event[1])),
                                            pass_coords=True)
        ###############################################################################################
        #Reestablecer transporte por encima del mapa
        [self.buttonEstacionesFijas.invoke() for _ in range(2)] if self.checkbox_fijas.get() else None
        [self.buttonBicicletasFlotantes.invoke() for _ in range(2)] if self.checkbox_bicicletas.get() else None
        [self.buttonAgruparBicicletas.invoke() for _ in range(2)] if self.checkbox_agrupar_bicicletas.get() else None
        [self.buttonCentroidesBicicletas.invoke() for _ in range(2)] if self.checkbox_centroides_bicicletas.get() else None
        [self.buttonPatinetes.invoke() for _ in range(2)] if self.checkbox_patinetes.get() else None
        [self.buttonAgruparPatinetes.invoke() for _ in range(2)] if self.checkbox_agrupar_patinetes.get() else None
        [self.buttonCentroidesPatinetes.invoke() for _ in range(2)] if self.checkbox_centroides_patinetes.get() else None
        [self.buttonDemandaBicicletas.invoke() for _ in range(2)] if self.checkbox_demanda_bicicletas.get() else None
        [self.buttonDemandaPatinetes.invoke() for _ in range(2)] if self.checkbox_demanda_patinetes.get() else None

    def select_button(self):
        if self.selected_archivo_estaciones.get() == 'Tomar datos en tiempo real' and not self.sesion_iniciada:
            self.verificar_credenciales()
        else:
            self.cargados_estaciones[self.estaciones_anterior][1] = False
            self.cargados_estaciones[self.selected_archivo_estaciones.get()][1] = True
            self.estaciones_anterior = self.selected_archivo_estaciones.get()

        self.cargados_bicicletas[self.bicicletas_anterior][1] = False
        self.cargados_bicicletas[self.selected_archivo_bicicletas.get()][1] = True
        self.bicicletas_anterior = self.selected_archivo_bicicletas.get()

        self.cargados_patinetes[self.patinetes_anterior][1] = False
        self.cargados_patinetes[self.selected_archivo_patinetes.get()][1] = True
        self.patinetes_anterior = self.selected_archivo_patinetes.get()

        self.cargados_demanda_bicicletas[self.bicicletas_solicitudes_anterior][1] = False
        self.cargados_demanda_bicicletas[self.selected_archivo_solicitudes_bicicletas.get()][1] = True
        self.bicicletas_solicitudes_anterior = self.selected_archivo_solicitudes_bicicletas.get()

        self.cargados_demanda_patinetes[self.patinetes_solicitudes_anterior][1] = False
        self.cargados_demanda_patinetes[self.selected_archivo_solicitudes_patinetes.get()][1] = True
        self.patinetes_solicitudes_anterior = self.selected_archivo_solicitudes_patinetes.get()

        for clave, valor in self.cargados_estaciones.items():
            print(f"Clave: {clave}, Booleano: {valor[1]}")

        for clave, valor in self.cargados_bicicletas.items():
            print(f"Clave: {clave}, Booleano: {valor[1]}")

        for clave, valor in self.cargados_patinetes.items():
            print(f"Clave: {clave}, Booleano: {valor[1]}")
    
    def cargar_archivo(self, tipo, visualizador=False):
        ruta_relativa = os.path.join(os.getcwd(), "data")
        if tipo == 'estaciones':
            archivo = filedialog.askopenfilename(title="Cargar archivo JSON de estaciones",
                                                 filetypes=[("Archivos JSON", "*.json")],
                                                 initialdir=ruta_relativa)
        elif tipo == 'bicicletas':
            archivo = filedialog.askopenfilename(title="Cargar archivo JSON de bicicletas",
                                                 filetypes=[("Archivos JSON", "*.json")],
                                                 initialdir=ruta_relativa)
        elif tipo == 'patinetes':
            archivo = filedialog.askopenfilename(title="Cargar archivo JSON de patinetes",
                                                 filetypes=[("Archivos JSON", "*.json")],
                                                 initialdir=ruta_relativa)
        elif tipo == 'demanda bicicletas':
            archivo = filedialog.askopenfilename(title="Cargar archivo JSON de demanda de bicicletas",
                                                 filetypes=[("Archivos JSON", "*.json")],
                                                 initialdir=ruta_relativa)
        elif tipo == 'demanda_patinetes':
            archivo = filedialog.askopenfilename(title="Cargar archivo JSON de demanda de bicicletas",
                                                 filetypes=[("Archivos JSON", "*.json")],
                                                 initialdir=ruta_relativa)
        if archivo:
            try:
                with open(archivo, 'r', encoding="utf-8") as f:
                    data = json.load(f)

                nombre_archivo = os.path.basename(archivo)
                #utilInfo.show_info_upload(self, nombre_archivo)

                if tipo == 'estaciones':
                    if nombre_archivo not in self.cargados_estaciones:
                        if self.validar_estructura_estaciones(data):
                            self.cargados_estaciones[nombre_archivo] = [data, False]
                        else: messagebox.showwarning("Aviso",  'Debe introducir un archivo con el formato correcto')
                    else: messagebox.showwarning("Aviso",  'El archivo ya estaba cargado')
                elif tipo == 'bicicletas':
                    if self.validar_estructura_flotantes(data):
                        if nombre_archivo not in self.cargados_bicicletas:
                            self.cargados_bicicletas[nombre_archivo] = [data, False]
                        else: messagebox.showwarning('Aviso', 'El archivo ya estaba cargado')
                        if nombre_archivo not in self.clustering_bicicletas:
                            self.clustering_bicicletas[nombre_archivo] = {'clusters': np.array([]), 'centroides': np.array([])}
                    else: messagebox.showwarning('Aviso', 'Debe introducir un archivo con el formato correcto')
                elif tipo == 'patinetes':
                    if self.validar_estructura_flotantes(data):
                        if nombre_archivo not in self.cargados_patinetes:
                            self.cargados_patinetes[nombre_archivo] = [data, False]
                        if nombre_archivo not in self.clustering_patinetes:
                            self.clustering_patinetes[nombre_archivo] = {'clusters': np.array([]), 'centroides': np.array([])}
                        else: messagebox.showwarning('Aviso', 'El archivo ya estaba cargado')
                    else: messagebox.showwarning('Aviso', 'Debe introducir un archivo con el formato correcto')
                elif tipo == 'demanda bicicletas':
                    if self.validar_estructura_demanda(data):
                        if nombre_archivo not in self.cargados_demanda_bicicletas:
                            self.cargados_demanda_bicicletas[nombre_archivo] = [data, False]
                        else: messagebox.showwarning('Aviso', 'El archivo ya estaba cargado')
                    else: messagebox.showwarning('Aviso', 'Debe introducir un archivo con el formato correcto')
                elif tipo == 'demanda patinetes':
                    if self.validar_estructura_demanda(data):
                        if nombre_archivo not in self.cargados_demanda_patinetes:
                            self.cargados_demanda_patinetes[nombre_archivo] = [data, False]
                        else: messagebox.showwarning('Aviso', 'El archivo ya estaba cargado')
                    else: messagebox.showwarning('Aviso', 'Debe introducir un archivo con el formato correcto')

            except Exception as e:
                print(f"Error al cargar el archivo: {e}")
                messagebox.showerror('Error', "Error al cargar el archivo")
        if visualizador:
            if tipo == 'estaciones' and hasattr(self, "ventana_gestor_estaciones"):
                self.ventana_gestor_estaciones.destroy()
                self.gestor_estaciones()
            elif tipo == 'bicicletas' and hasattr(self, "ventana_gestor_bicicletas"):
                self.ventana_gestor_bicicletas.destroy()
                self.gestor_bicicletas()
            elif tipo == 'patinetes' and hasattr(self, "ventana_gestor_patinetes"):
                self.ventana_gestor_patinetes.destroy()
                self.gestor_patinetes()
            elif tipo == 'demanda bicicletas' and hasattr(self, "ventana_gestor_demanda_bicicletas"):
                self.ventana_gestor_demanda_bicicletas.destroy()
                self.gestor_demanda_bicicletas()
            elif tipo == 'demanda patinetes' and hasattr(self, "ventana_gestor_demanda_patinetes"):
                self.ventana_gestor_demanda_patinetes.destroy()
                self.gestor_demanda_patinetes()
    
    def validar_estructura_estaciones(self, diccionario):
        if not isinstance(diccionario, dict):
            return False
        
        for clave, valor in diccionario.items():
            if not isinstance(clave, str) or not clave.isdigit():
                return False
            if not isinstance(valor, dict):
                return False
            
            claves_esperadas = {"name", "coordinates", "bike_bases", "free_bases", "light"}
            if set(valor.keys()) != claves_esperadas:
                return False
            
            if not isinstance(valor["name"], str):
                return False
            if not (isinstance(valor["coordinates"], list) and 
                    len(valor["coordinates"]) == 2 and 
                    all(isinstance(coord, (int, float)) for coord in valor["coordinates"])):
                return False
            if not isinstance(valor["bike_bases"], int):
                return False
            if not isinstance(valor["free_bases"], int):
                return False
            if not isinstance(valor["light"], int):
                return False
        return True

    def validar_estructura_flotantes(self, diccionario):
        if not isinstance(diccionario, dict):
            return False

        claves_esperadas = {"id", "coord", "zona"}
        if set(diccionario.keys()) != claves_esperadas:
            return False

        if not (isinstance(diccionario["id"], list) and 
                all(isinstance(i, int) for i in diccionario["id"])):
            return False

        if not (isinstance(diccionario["coord"], list) and 
                all(isinstance(coord, list) and len(coord) == 2 and 
                    all(isinstance(num, (int, float)) for num in coord)
                    for coord in diccionario["coord"])):
            return False

        if not isinstance(diccionario["zona"], list):
            return False

        return True

    def validar_estructura_demanda(self, diccionario):
        if not isinstance(diccionario, dict):
            return False
    
        if "coordenadas" not in diccionario or "zona" not in diccionario:
            return False

        if not isinstance(diccionario["coordenadas"], list) or not all(
            isinstance(coord, list) and len(coord) == 2 and all(isinstance(num, (int, float)) for num in coord)
            for coord in diccionario["coordenadas"]
        ):
            return False

        if not isinstance(diccionario["zona"], list) or not all(isinstance(z, (int, float)) for z in diccionario["zona"]):
            return False

        if len(diccionario["coordenadas"]) != len(diccionario["zona"]):
            return False

        return True

    def generar_datos_demanda_bicicletas(self):
        self.demanda_bicicletas = utilDatos.generar_datos_demanda(self.solicitudes_bicicletas, self.maxLon, self.minLon, self.maxLat, self.minLat)
        if self.checkbox_demanda_bicicletas.get():
            self.boton_demanda_bicicletas(self.checkbox_demanda_bicicletas)
    
    def generar_datos_demanda_patinetes(self):
        self.demanda_patinetes = utilDatos.generar_datos_demanda(self.solicitudes_patinetes, self.maxLon, self.minLon, self.maxLat, self.minLat)
        if self.checkbox_demanda_patinetes.get():
            self.boton_demanda_patinetes(self.checkbox_demanda_patinetes)
    
    def aplicar_cambios(self, cambiado):
        if self.selected_archivo_estaciones.get() == 'Tomar datos en tiempo real' and not self.sesion_iniciada:
            self.verificar_credenciales()
        elif self.selected_archivo_estaciones.get() == 'Tomar datos en tiempo real' and self.sesion_iniciada:
            self.select_button()
            self.datos_estaciones_api()
        elif cambiado == 'estaciones':
            self.estaciones = self.cargados_estaciones[self.selected_archivo_estaciones.get()][0]
            self.ventana_informativa()
            #self.ventana_gestor_estaciones.destroy()
        elif cambiado == 'bicicletas':
            self.bicicletas_flotantes = self.cargados_bicicletas[self.selected_archivo_bicicletas.get()][0]
            self.ventana_informativa()
            #self.ventana_gestor_bicicletas.destroy()
        elif cambiado == 'patinetes':
            self.patinetes = self.cargados_patinetes[self.selected_archivo_patinetes.get()][0]
            self.ventana_informativa()
            #self.ventana_gestor_patinetes.destroy()
        elif cambiado == 'demanda bicicletas':
            self.demanda_bicicletas = self.cargados_demanda_bicicletas[self.selected_archivo_solicitudes_bicicletas.get()][0]
            self.ventana_informativa()
        elif cambiado == 'demanda patinetes':
            self.demanda_patinetes = self.cargados_demanda_patinetes[self.selected_archivo_patinetes.get()][0]
            self.ventana_informativa()

    def selector_fecha(self):
        self.ventana_fecha = Toplevel(self.frame_mapa)
        self.ventana_fecha.title("Entrada de Mapa de Calor")

        ancho_pantalla = self.ventana_fecha.winfo_screenwidth()
        alto_pantalla = self.ventana_fecha.winfo_screenheight()

        ancho_ventana = 220
        alto_ventana = 180

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_fecha.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.ventana_fecha.resizable(False, False)
        self.ventana_fecha.config(bg=COLOR_MENU_LATERAL)
        self.ventana_fecha.protocol("WM_DELETE_WINDOW", self.ventana_fecha.destroy)


        dia = [str(i) for i in range(1, 32)]
        mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        ano = [str(i) for i in range(2018, 2022)]
        hora = [str(i).zfill(2) for i in range(24)]

        label_ano = Label(self.ventana_fecha, text="Año:", bg=COLOR_MENU_LATERAL, fg="white")
        label_ano.grid(row=0, column=0, padx=10, pady=5)

        combo_ano = ttk.Combobox(self.ventana_fecha, values=ano, state="readonly")
        combo_ano.grid(row=0, column=1, padx=10, pady=5)
        combo_ano.set(ano[1])
        combo_ano.bind("<<ComboboxSelected>>", lambda event: self.actualizar_mes(event=event, combo_ano=combo_ano, combo_mes=combo_mes))

        label_mes = Label(self.ventana_fecha, text="Mes:", bg=COLOR_MENU_LATERAL, fg="white")
        label_mes.grid(row=1, column=0, padx=10, pady=5)

        combo_mes = ttk.Combobox(self.ventana_fecha, values=mes, state="readonly")
        combo_mes.grid(row=1, column=1, padx=10, pady=5)
        combo_mes.set(mes[0])
        combo_mes.bind("<<ComboboxSelected>>", lambda event: self.actualizar_dias(event=event,combo_mes=combo_mes, combo_ano=combo_ano, combo_dia=combo_dia))

        label_dia = Label(self.ventana_fecha, text="Día:", bg=COLOR_MENU_LATERAL, fg="white")
        label_dia.grid(row=2, column=0, padx=10, pady=5)

        combo_dia = ttk.Combobox(self.ventana_fecha, values=dia, state="readonly")
        combo_dia.grid(row=2, column=1, padx=10, pady=5)
        combo_dia.set("1") 

        label_hora = Label(self.ventana_fecha, text="Hora:", bg=COLOR_MENU_LATERAL, fg="white")
        label_hora.grid(row=3, column=0, padx=10, pady=5)

        combo_hora = ttk.Combobox(self.ventana_fecha, values=hora, state="readonly")
        combo_hora.grid(row=3, column=1, padx=10, pady=5)
        combo_hora.set(hora[0])

        boton_cargar = Button(self.ventana_fecha, text="Cargar archivo", bg=COLOR_MENU_LATERAL, fg="white",
                               command=lambda: self.cargar_archivo_historico(combo_dia.get(), 
                                combo_mes.get(), combo_ano.get(), combo_hora.get()))
        boton_cargar.grid(row=5, column=0, columnspan=2, pady=10)

    def actualizar_dias(self, combo_ano, combo_mes, combo_dia, event=None):
        dias_por_mes = {
            "Enero": 31, "Febrero": 28, "Marzo": 31, "Abril": 30, "Mayo": 31,
            "Junio": 30, "Julio": 31, "Agosto": 31, "Septiembre": 30,
            "Octubre": 31, "Noviembre": 30, "Diciembre": 31
        }

        if int(combo_ano.get()) % 4 == 0 and (int(combo_ano.get()) % 100 != 0 or int(combo_ano.get()) % 400 == 0):
            dias_por_mes["Febrero"] = 29
        
        num_dias = dias_por_mes[combo_mes.get()]
        
        dias = [str(i) for i in range(1, num_dias + 1)]
        combo_dia['values'] = dias
        if int(combo_dia.get()) > num_dias:
            combo_dia.set(str(num_dias))
    
    def actualizar_mes(self, event, combo_ano, combo_mes):
        año_seleccionado = combo_ano.get()

        combo_mes.set('')

        if año_seleccionado == '2018':
            meses_disponibles = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            combo_mes['values'] = meses_disponibles
            combo_mes.set('Julio')
        else:
            combo_mes.set('Enero')

    def cargar_archivo_historico(self, dia, mes, ano, hora):
        #utilDatos.cargar_datos(int(ano), int(mes), int(dia), int(hora))
        if mes == 'Enero': mes=1
        elif mes== 'Febrero': mes=2
        elif mes== 'Marzo': mes=3
        elif mes== 'Abril': mes=4
        elif mes== 'Mayo': mes=5
        elif mes== 'Junio': mes=6
        elif mes== 'Julio': mes=7
        elif mes== 'Agosto': mes=8
        elif mes== 'Septiembre': mes=9
        elif mes== 'Octubre': mes=10
        elif mes== 'Noviembre': mes=11
        elif mes== 'Diciembre': mes=12

        nombre, df = utilDatos.cargar_datos(str(ano), str(mes), str(dia), str(hora))
        if nombre not in self.cargados_estaciones:
            self.cargados_estaciones[nombre] = [df, False]
        else: utilInfo.show_info_upload(self, 'El archivo ya estaba cargado')

        self.ventana_fecha.destroy()
        self.ventana_gestor_estaciones.destroy()
        self.gestor_estaciones()

    def ventana_informativa(self):
        ventana_info = Toplevel()
        ventana_info.title("Información")

        ancho_pantalla = ventana_info.winfo_screenwidth()
        alto_pantalla = ventana_info.winfo_screenheight()

        ancho_ventana = 300
        alto_ventana = 100

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        ventana_info.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        ventana_info.resizable(False, False)
        ventana_info.config(bg=COLOR_MENU_LATERAL)
        ventana_info.protocol("WM_DELETE_WINDOW", ventana_info.destroy)

        mensaje = Label(ventana_info, text="Los cambios se han \n aplicado correctamente", bg=COLOR_MENU_LATERAL, fg="white", font=("Arial", 12))
        mensaje.pack(pady=5)

        boton_cerrar = Button(ventana_info, bg= COLOR_MENU_LATERAL, fg='white', text="Cerrar", command=ventana_info.destroy)
        boton_cerrar.pack(pady=5)

        ventana_info.mainloop()

    def ventana_datos_aleatorios(self, tipo):
        self.ventana_aleatorios = Toplevel(self.frame_mapa)
        self.ventana_aleatorios.title("Generación de datos aleatorios")

        ancho_pantalla = self.ventana_aleatorios.winfo_screenwidth()
        alto_pantalla = self.ventana_aleatorios.winfo_screenheight()

        ancho_ventana = 400
        alto_ventana = 150

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_aleatorios.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        if tipo == 'estaciones':
            seleccionado = StringVar(value='est_num_bicicletas')
            texto1, value1 = "Generar aleatoriamente el número de bicicletas por estación", 'est_num_bicicletas'
            texto2, value2 = "Generar la ubicación de las estaciones uniformemente", 'est_uniforme'
            texto3, value3 = "Generar la ubicación de las estaciones centrada", 'est_centrado'
        elif tipo == 'bicicletas':
            seleccionado = StringVar(value='bic_estaciones')
            texto1, value1 = "Generar las bicicletas flotantes en función de los datos de las estaciones", 'bic_estaciones'
            texto2, value2 = "Generar la ubicación de las bicicletas uniformemente", 'bic_uniforme'
            texto3, value3 = "Generar la ubicación de las bicicletas centrada", 'bic_centrado'
        elif tipo == 'patinetes':
            seleccionado = StringVar(value='pat_estaciones')
            texto1, value1 = "Generar los patinetes en función de los datos de las estaciones", 'pat_estaciones'
            texto2, value2 = "Generar la ubicación de los patinetes uniformemente", 'pat_uniforme'
            texto3, value3 = "Generar la ubicación de los patinetes centrada", 'pat_centrado'

        num_transportes = IntVar(value=100)
        frame_entry = Frame(self.ventana_aleatorios)
        frame_entry.pack(padx=5, pady=5, fill="x")
        if tipo == 'bicicletas' or tipo == 'patinetes':
            Label(frame_entry, text="Número de transportes a generar:").pack(side="left", padx=5)

            num_transportes = IntVar(value=100)
            entry_num_transportes = Entry(frame_entry, textvariable=num_transportes, width=5)
            entry_num_transportes.pack(side="left", padx=5)
        
        radio1 = Radiobutton(self.ventana_aleatorios, text=texto1, variable=seleccionado, value=value1, 
                            #command=lambda: self.solicitar_numero_transportes(tipo, frame_entry, False)
                            )
        radio1.pack(anchor=W)

        radio2 = Radiobutton(self.ventana_aleatorios, text=texto2, variable=seleccionado, value=value2, 
                            #command=lambda: self.solicitar_numero_transportes(tipo, frame_entry, True)
                            )
        radio2.pack(anchor=W)

        radio3 = Radiobutton(self.ventana_aleatorios, text=texto3, variable=seleccionado, value=value3, 
                            #command=lambda:self.solicitar_numero_transportes(tipo, frame_entry, True)
                            )
        radio3.pack(anchor=W)

        submit_button = Button(self.ventana_aleatorios, text="Generar", command=lambda: self.aceptar_aleatorios(tipo, seleccionado, num_transportes))
        submit_button.pack(pady=5)

        self.ventana_aleatorios.protocol("WM_DELETE_WINDOW", self.ventana_aleatorios.destroy)
    """
    def solicitar_numero_transportes(self, tipo, frame_entry, mostrado):
        if tipo == 'bicicletas' or tipo == 'patinetes' and mostrado:
            frame_entry.pack(padx=5, pady=5, fill="x")
        elif tipo == 'bicicletas' or tipo == 'patinetes' and not mostrado:
            frame_entry.pack_forget()
    """
        
    def aceptar_aleatorios(self, tipo, seleccionado, num_transportes = None):
        if num_transportes.get() < 0 or num_transportes.get() > 5000:
            messagebox.showwarning("Límite excedido", "El máximo número de transportes a generar es 5000.")
            return

        if tipo == 'estaciones':
            nombre_aleatorios = 'estaciones_aleatorios_'
            if seleccionado.get() == 'est_num_bicicletas':
                nombre_aleatorios+=f'num_bicicletas_{self.num_archivos_aleatorios_est}'
                self.num_archivos_aleatorios_est+=1
                datos = utilDatos.generar_aleatorios_estaciones_num_bicicletas(self.estaciones)
            elif seleccionado.get() == 'est_uniforme':
                nombre_aleatorios+=f'uniforme_{self.num_archivos_aleatorios_est}'
                self.num_archivos_aleatorios_est+=1
                datos = utilDatos.generar_aleatorios_estaciones_uniformes(len(self.estaciones)-1, self.maxLon, self.minLon, self.maxLat, self.minLat)
            elif seleccionado.get() == 'est_centrado':
                nombre_aleatorios+=f'centrado_{self.num_archivos_aleatorios_est}'
                self.num_archivos_aleatorios_est+=1
                datos = utilDatos.generar_aleatorios_estaciones_centrados(len(self.estaciones)-1, self.maxLon, self.minLon, self.maxLat, self.minLat)
            self.cargados_estaciones[nombre_aleatorios] = [datos, False]

            self.ventana_aleatorios.destroy()
            self.ventana_gestor_estaciones.destroy()
            self.gestor_estaciones()
        
        elif tipo == 'bicicletas':
            nombre_aleatorios = 'bicicletas_aleatorias_'
            if seleccionado.get() == 'bic_estaciones':
                nombre_aleatorios+=f'estaciones_{self.num_archivos_aleatorios_bic}'
                self.num_archivos_aleatorios_bic+=1
                datos = utilDatos.generar_aleatorios_flotantes_estaciones(self.estaciones)
            elif seleccionado.get() == 'bic_uniforme':
                nombre_aleatorios+=f'uniforme_{self.num_archivos_aleatorios_bic}'
                self.num_archivos_aleatorios_bic+=1
                datos = utilDatos.generar_aleatorios_flotantes_uniforme(num_transportes, self.maxLon, self.minLon, self.maxLat, self.minLat)
            elif seleccionado.get() == 'bic_centrado':
                nombre_aleatorios+=f'centrado_{self.num_archivos_aleatorios_bic}'
                self.num_archivos_aleatorios_bic+=1
                datos = utilDatos.generar_aleatorios_flotantes_centrado(num_transportes, self.maxLon, self.minLon, self.maxLat, self.minLat)
            self.cargados_bicicletas[nombre_aleatorios] = [datos, False]
            self.clustering_bicicletas[nombre_aleatorios] = {'clusters': np.array([]), 'centroides': np.array([])}

            self.ventana_aleatorios.destroy()
            self.ventana_gestor_bicicletas.destroy()
            self.gestor_bicicletas()

        elif tipo == 'patinetes':
            nombre_aleatorios = 'patinetes_aleatorios_'
            if seleccionado.get() == 'pat_estaciones':
                nombre_aleatorios+=f'estaciones_{self.num_archivos_aleatorios_pat}'
                self.num_archivos_aleatorios_pat+=1
                datos = utilDatos.generar_aleatorios_flotantes_estaciones(self.estaciones)
            elif seleccionado.get() == 'pat_uniforme':
                nombre_aleatorios+=f'uniforme_{self.num_archivos_aleatorios_pat}'
                self.num_archivos_aleatorios_pat+=1
                datos = utilDatos.generar_aleatorios_flotantes_uniforme(num_transportes, self.maxLon, self.minLon, self.maxLat, self.minLat)
            elif seleccionado.get() == 'pat_centrado':
                nombre_aleatorios+=f'centrado_{self.num_archivos_aleatorios_pat}'
                self.num_archivos_aleatorios_pat+=1
                datos = utilDatos.generar_aleatorios_flotantes_centrado(num_transportes, self.maxLon, self.minLon, self.maxLat, self.minLat)
            self.cargados_patinetes[nombre_aleatorios] = [datos, False]
            self.clustering_patinetes[nombre_aleatorios] = {'clusters': np.array([]), 'centroides': np.array([])}

            self.ventana_aleatorios.destroy()
            self.ventana_gestor_patinetes.destroy()
            self.gestor_patinetes()

    def verificar_credenciales(self):
        url_login = "https://openapi.emtmadrid.es/v1/mobilitylabs/user/login/"
        headers_login = {'email': 'paulariasfer01@gmail.com', 'password': 'passwordEMT2025'}

        response_login = requests.get(url_login, headers=headers_login)
        datos_login = json.loads(response_login.content)
        if datos_login['code'] == '01':
            self.token = datos_login['data'][0]['accessToken']
            self.sesion_iniciada = True
        else:
            messagebox.showinfo('Credenciales incorrectas', 'Debe crear una cuenta antes de intentar iniciar sesion')
            return

        self.datos_estaciones_api()

    def datos_estaciones_api(self):

        #Tomo información sobre las estaciones

        url_stations = "http://openapi.emtmadrid.es/v1/transport/bicimad/stations/"
        headers_stations = {'accessToken': self.token}

        response_stations = requests.get(url_stations, headers=headers_stations)
        datos_stations = json.loads(response_stations.content)

        stations = {}
        for station in datos_stations['data']:
            if station['no_available'] == 0:
                stations[station['id']] = {
                    "name": station['name'],
                    "free_bases": station['free_bases'],
                    "bike_bases": station['dock_bikes'],
                    "coordinates": station['geometry']['coordinates'],
                    "light": station['light']
                }
        self.estaciones = stations

    def aplicar_gaussiana(self, cantidades, alcance, sigma=1):
        # Convertimos la lista a una matriz
        matriz = np.array(cantidades).reshape(self.n, self.n)
        matriz_suavizada = np.zeros_like(matriz, dtype=float)
        
        mitad_alcance = alcance // 2

        matriz_influencia = np.zeros((alcance, alcance))
        for i in range(alcance):
            for j in range(alcance):
                distancia = max(abs(i - mitad_alcance), abs(j - mitad_alcance))       # Igual en vecinos horizontales, verticales y diagonales
                matriz_influencia[i, j] = np.exp(-distancia ** 2 / (2 * sigma ** 2))    #funcion gaussiana
        
        # Normalizamos para que la suma sea 1
        matriz_influencia /= np.sum(matriz_influencia)

        for i in range(self.n):
            for j in range(self.n):
                sumatoria = 0
                for fi in range(-mitad_alcance, mitad_alcance + 1):
                    for fj in range(-mitad_alcance, mitad_alcance + 1):
                        ni, nj = i + fi, j + fj  # Coordenadas del vecino
                        if 0 <= ni < self.n and 0 <= nj < self.n:
                            sumatoria += matriz[ni, nj] * matriz_influencia[fi + mitad_alcance, fj + mitad_alcance]
                matriz_suavizada[i, j] = sumatoria
        
        """minimo = np.min(matriz_suavizada)
        maximo = np.max(matriz_suavizada)
        index_min = np.argmin(matriz_suavizada)
        index_max = np.argmax(matriz_suavizada)
        print(f'Min: {minimo}, max: {maximo}')
        print(f'El indice de la menor es: {index_min} y se trata de la zona {self.dic_mapa_calor['ids'][index_min]}')
        print(f'El indice de la mayor es: {index_max} y se trata de la zona {self.dic_mapa_calor['ids'][index_max]}')
        """
        return matriz_suavizada.flatten().tolist()
        """
        ################## NORMALIZACION ######################
        rango_min = 0
        rango_max = 100
        matriz_suavizada_normalizada = rango_min + (matriz_suavizada - np.min(matriz_suavizada)) * (rango_max - rango_min) / (np.max(matriz_suavizada) - np.min(matriz_suavizada))
        """

        return matriz_suavizada_normalizada.flatten().tolist()

    def mostrar_mapa(self):
        self.borrar_mapacalor()
        self.pintar_mapa()

    def confirmar_tipo(self):        
        self.borrar_mapacalor()
        self.clasificacion = self.tipo_mapa.get()
        if self.clasificacion == 'Llenado' or self.clasificacion == 'Huecos':
            self.frame_mostrar_mapa_bicicletas.pack_forget()
            self.frame_mostrar_mapa_patinetes.pack_forget()
        if self.clasificacion == 'General':
            self.frame_mostrar_mapa_bicicletas.pack(after=self.frame_mostrar_mapa_estaciones, fill=X, padx=10, pady=2, side=TOP)
            self.frame_mostrar_mapa_patinetes.pack(after=self.frame_mostrar_mapa_bicicletas, fill=X, padx=10, pady=2, side=TOP)
        self.pintar_mapa()
        utilInfo.show_info_cambio_tipo(self)
        self.tipo_mapa_anterior == self.tipo_mapa.get()

    def cambiar_tipo(self):
        self.toggle_submenu(f'Mapa {self.tipo_mapa_anterior}')
        self.toggle_submenu(f'Mapa {self.tipo_mapa.get()}')
        self.tipo_mapa_anterior = self.tipo_mapa.get()

    def mostrar_mapa_demanda_bicicletas(self):
        self.borrar_mapacalor()
        self.clasificacion = "Demanda Bicicletas"
        self.pintar_mapa()

    def mostrar_mapa_demanda_patinetes(self):
        self.borrar_mapacalor()
        self.clasificacion = "Demanda Patinetes"
        self.pintar_mapa()

    def borrar_mapacalor(self):
        if hasattr(self, "n"):
            poligonos = self.poligonos_zonas[self.n]
            if len(poligonos) != 0:
                for poligono in poligonos:
                    poligono.delete()
            self.frame_leyenda.destroy()
    
    def modificar_cuadricula(self):
        """if not hasattr(self, 'n') or (self.checkbox_mapa_estaciones.get()==False and \
        self.checkbox_mapa_flotantes.get()==False and self.checkbox_mapa_patinetes.get()):
            messagebox.showwarning("Advertencia", "Debe seleccionar lo que desea incluir en el mapa de calor")
            return"""
        self.ventana_mod = Toplevel(self.frame_mapa)
        self.ventana_mod.title("Entrada de Mapa de Calor")

        ancho_pantalla = self.ventana_mod.winfo_screenwidth()
        alto_pantalla = self.ventana_mod.winfo_screenheight()

        ancho_ventana = 300
        alto_ventana = 150

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_mod.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        if self.n == 44: self.seleccionado_metros.set(500)
        elif self.n == 51: self.seleccionado_metros.set(400)
        elif self.n == 68: self.seleccionado_metros.set(300)
        elif self.n == 102: self.seleccionado_metros.set(200)

        # Crear RadioButtons
        radio500 = Radiobutton(self.ventana_mod, text="500 metros", variable=self.seleccionado_metros, value=500)
        radio500.pack(anchor=W)

        radio400 = Radiobutton(self.ventana_mod, text="400 metros", variable=self.seleccionado_metros, value=400)
        radio400.pack(anchor=W)

        radio300 = Radiobutton(self.ventana_mod, text="300 metros", variable=self.seleccionado_metros, value=300)
        radio300.pack(anchor=W)

        radio200 = Radiobutton(self.ventana_mod, text="200 metros", variable=self.seleccionado_metros, value=200)
        radio200.pack(anchor=W)

        submit_button = Button(self.ventana_mod, text="Mostrar", command=self.enviar_tamano_cuadricula)
        submit_button.pack(pady=5)

        self.ventana_mod.protocol("WM_DELETE_WINDOW", self.ventana_mod.destroy)

    def modificar_influencia(self):
        """if not hasattr(self, 'n') or (self.checkbox_mapa_estaciones.get()==False and \
        self.checkbox_mapa_flotantes.get()==False and self.checkbox_mapa_patinetes.get()==False):
            messagebox.showwarning("Advertencia", "Debe seleccionar lo que desea incluir en el mapa de calor")
            return"""
        self.ventana_mod = Toplevel(self.frame_mapa)
        self.ventana_mod.title("Modificación de la Influencia de Zonas Vecinas")

        ancho_pantalla = self.ventana_mod.winfo_screenwidth()
        alto_pantalla = self.ventana_mod.winfo_screenheight()

        ancho_ventana = 300
        alto_ventana = 100

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_mod.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        self.seleccionado_influencia.set(self.influencia)

        # Crear RadioButtons
        radio_con_influencia = Radiobutton(self.ventana_mod, text="Con influencia de vecinos", variable=self.seleccionado_influencia, value='con')
        radio_con_influencia.pack(anchor=W)

        radio_sin_influencia = Radiobutton(self.ventana_mod, text="Sin influencia de vecinos", variable=self.seleccionado_influencia, value='sin')
        radio_sin_influencia.pack(anchor=W)

        submit_button = Button(self.ventana_mod, text="Cambiar", command=self.enviar_influencia)
        submit_button.pack(pady=5)

        self.ventana_mod.protocol("WM_DELETE_WINDOW", self.ventana_mod.destroy)

    def enviar_tamano_cuadricula(self):        
        self.borrar_mapacalor()
        self.ventana_mod.destroy()

        
        metros = float(self.seleccionado_metros.get())
        lon_objetivo = metros/(111320*math.cos(40.4))
        lat_objetivo = metros/111320 
        n_lon = abs(self.maxLon - self.minLon) / lon_objetivo
        n_lat = abs(self.maxLat - self.minLat) / lat_objetivo
        self.n = math.ceil(max(n_lon, n_lat))

        if not hasattr(self, 'clasificacion'):
            self.clasificacion = "General"

        self.pintar_mapa()

    def enviar_influencia(self):        
        self.borrar_mapacalor()
        self.ventana_mod.destroy()

        if not hasattr(self, 'clasificacion'):
            self.clasificacion = "General"
        self.influencia = self.seleccionado_influencia.get()
        self.pintar_mapa()
    
    def pintar_estaciones(self, ocupacion=False):
        if ocupacion and self.checkbox_fijas.get():
            self.buttonEstacionesFijas.invoke()
        if not ocupacion and self.checkbox_ocupacion.get():
            self.buttonEstacionesOcupacion.invoke()
        strings = []
        for id in self.estaciones:
            if ocupacion:
                if self.estaciones[id]['light'] == 0: color = "red"
                elif self.estaciones[id]['light'] == 1: color = "#68ca3d"
                elif self.estaciones[id]['light'] == 2: color = "orange"
                elif self.estaciones[id]['light'] == 3: color = "black"
            else: color = "blue"
            strings.append(self.estaciones[id]['name'])
            coord_estacion = tuple(self.estaciones[id]['coordinates'][::-1])
            d = 0.00000001
            coordinates = [(coord_estacion[0], coord_estacion[1]),
                           (coord_estacion[0], coord_estacion[1]+ d),
                           (coord_estacion[0] + d, coord_estacion[1] + d),
                           (coord_estacion[0] + d, coord_estacion[1])]
            """poligono = self.labelMap.set_polygon(coordinates,
                                    outline_color="blue",
                                    border_width=5,
                                    name=(id, coord_estacion),
                                    command=self.show_info_estacion,
                                    )"""
            poligono = self.labelMap.set_polygon(coordinates,
                                    outline_color=color,
                                    border_width=5,
                                    name=(id, coord_estacion),
                                    command=lambda event: utilInfo.show_info_estacion(self, event))
            if ocupacion: self.poligonos_estaciones_ocupacion.append(poligono)
            else: self.poligonos_estaciones.append(poligono)
        longest_string = max(strings, key=len)
        max_len = len(longest_string)
        #print(f'número de estaciones fijas: {len(self.estaciones)}')

    def boton_fijas(self, checkbox_fijas):
        if checkbox_fijas.get() == True:
            self.pintar_estaciones()
        elif checkbox_fijas.get() == False:
            utilInfo.close_infoest(self)
            for poligono in self.poligonos_estaciones:
                poligono.delete()
      
    def pintar_flotantes(self):
        if self.checkbox_agrupar_bicicletas.get():
            self.buttonAgruparBicicletas.invoke()
        for i in range(len(self.bicicletas_flotantes['id'])):

            coord_bici = self.bicicletas_flotantes['coord'][i]
            d = 0.00000001
            coordinates = [(coord_bici[0], coord_bici[1]),
                           (coord_bici[0], coord_bici[1]+ d),
                           (coord_bici[0] + d, coord_bici[1] + d),
                           (coord_bici[0] + d, coord_bici[1])]

            poligono = self.labelMap.set_polygon(coordinates,
                                    outline_color="#991010",
                                    border_width=5,
                                    )
            self.poligonos_bicicletas.append(poligono)
    
    def pintar_bicicletas_clusters_kmeans(self):
        if self.checkbox_bicicletas.get():
            self.buttonBicicletasFlotantes.invoke()
        if self.clustering_bicicletas[self.selected_archivo_bicicletas.get()]['clusters'].size == 0 and \
            self.clustering_bicicletas[self.selected_archivo_bicicletas.get()]['centroides'].size == 0:

            self.clustering_bicicletas[self.selected_archivo_bicicletas.get()]['clusters'], self.clustering_bicicletas[self.selected_archivo_bicicletas.get()]['centroides'] = utilClustering.clusters_kmeans(self.bicicletas_flotantes['coord'])

        for i, coord in enumerate(self.bicicletas_flotantes['coord']):
            cluster_id = self.clustering_bicicletas[self.selected_archivo_bicicletas.get()]['clusters'][i]
            color = self.color_map.get(cluster_id%50, 'black')
            poligono = self.labelMap.set_polygon([coord],
                                                outline_color=color,
                                                border_width=1.5,
                                                name="Outlier")
            self.poligonos_bicicletas_clusters.append(poligono)
    
    def pintar_centroides_bicicletas(self):
        if self.clustering_bicicletas[self.selected_archivo_bicicletas.get()]['clusters'].size == 0 and \
            self.clustering_bicicletas[self.selected_archivo_bicicletas.get()]['centroides'].size == 0:
            
            self.clustering_bicicletas[self.selected_archivo_bicicletas.get()]['clusters'], self.clustering_bicicletas[self.selected_archivo_bicicletas.get()]['centroides'] = utilClustering.clusters_kmeans(self.bicicletas_flotantes['coord'])

        for i, centroide in enumerate(self.clustering_bicicletas[self.selected_archivo_bicicletas.get()]['centroides']):
            d = 0.00000001
            coordinates = [(centroide[0], centroide[1]),
                           (centroide[0], centroide[1]+ d),
                           (centroide[0] + d, centroide[1] + d),
                           (centroide[0] + d, centroide[1])]
            poligono = self.labelMap.set_polygon(coordinates,
                                                outline_color="#ff005d",
                                                border_width=5,
                                                name="Outlier")
            self.poligonos_centroides_bicicletas.append(poligono)

    def pintar_patinetes_clusters_kmeans(self):
        if self.checkbox_patinetes.get():
            self.buttonPatinetes.invoke()
        if self.clustering_patinetes[self.selected_archivo_patinetes.get()]['clusters'].size == 0 and \
            self.clustering_patinetes[self.selected_archivo_patinetes.get()]['centroides'].size == 0:

            self.clustering_patinetes[self.selected_archivo_patinetes.get()]['clusters'], self.clustering_patinetes[self.selected_archivo_patinetes.get()]['centroides'] = utilClustering.clusters_kmeans(self.patinetes['coord'])
        
        for i, coord in enumerate(self.patinetes['coord']):
            cluster_id = self.clustering_patinetes[self.selected_archivo_patinetes.get()]['clusters'][i]
            color = self.color_map.get(cluster_id%50, 'black')
            poligono = self.labelMap.set_polygon([coord],
                                                outline_color=color,
                                                border_width=1.5,
                                                name="Outlier")
            self.poligonos_patinetes_clusters.append(poligono)
    
    def pintar_centroides_patinetes(self):
        if self.clustering_patinetes[self.selected_archivo_patinetes.get()]['clusters'].size == 0 and \
            self.clustering_patinetes[self.selected_archivo_patinetes.get()]['centroides'].size == 0:
            
            self.clustering_patinetes[self.selected_archivo_patinetes.get()]['clusters'], self.clustering_patinetes[self.selected_archivo_patinetes.get()]['centroides'] = utilClustering.clusters_kmeans(self.patinetes_flotantes['coord'])

        for i, centroide in enumerate(self.clustering_patinetes[self.selected_archivo_patinetes.get()]['centroides']):
            d = 0.00000001
            coordinates = [(centroide[0], centroide[1]),
                           (centroide[0], centroide[1]+ d),
                           (centroide[0] + d, centroide[1] + d),
                           (centroide[0] + d, centroide[1])]
            poligono = self.labelMap.set_polygon(coordinates,
                                                outline_color="#ff005d",
                                                border_width=5,
                                                name="Outlier")
            self.poligonos_centroides_patinetes.append(poligono)

    def pintar_patinetes(self):
        if self.checkbox_agrupar_patinetes.get():
            self.buttonAgruparPatinetes.invoke()
        for i in range(len(self.patinetes['id'])):

            coord_patinete = self.patinetes['coord'][i]
            d = 0.00000001
            coordinates = [(coord_patinete[0], coord_patinete[1]),
                           (coord_patinete[0], coord_patinete[1]+ d),
                           (coord_patinete[0] + d, coord_patinete[1] + d),
                           (coord_patinete[0] + d, coord_patinete[1])]

            poligono = self.labelMap.set_polygon(coordinates,
                                    outline_color="orange",
                                    border_width=5,
                                    #name=self.patinetes['info'][i]
                                    )
            self.poligonos_patinetes.append(poligono)
    
    def pintar_demanda_bicicletas(self):
        self.borrar_demanda_bicicletas()
        """
        current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        bycicle_img = ImageTk.PhotoImage(Image.open("bycicle.png").resize((15, 15)))
        for punto in self.demanda_bicicletas:
            marcador = self.labelMap.set_marker(punto[0], punto[1], icon=bycicle_img, image_zoom_visibility = (14, 15))
            self.poligonos_demanda_bicicletas.append(marcador)"""
        for punto in self.demanda_bicicletas['coordenadas']:
            d = 0.00000001
            coordinates = [(punto[0], punto[1]),
                           (punto[0], punto[1]+ d),
                           (punto[0] + d, punto[1] + d),
                           (punto[0] + d, punto[1])]
            poligono = self.labelMap.set_polygon(coordinates,
                                                outline_color="#27ae60",
                                                border_width=5)
            self.poligonos_demanda_bicicletas.append(poligono)
    
    def borrar_demanda_bicicletas(self):
        if self.poligonos_demanda_bicicletas != []:
            for poligono in self.poligonos_demanda_bicicletas:
                poligono.delete()

    def pintar_demanda_patinetes(self):
        self.borrar_demanda_patinetes()
        for punto in self.demanda_patinetes['coordenadas']:
            d = 0.00000001
            coordinates = [(punto[0], punto[1]),
                           (punto[0], punto[1]+ d),
                           (punto[0] + d, punto[1] + d),
                           (punto[0] + d, punto[1])]
            poligono = self.labelMap.set_polygon(coordinates,
                                                outline_color="#f1c40f",
                                                border_width=5)
            self.poligonos_demanda_patinetes.append(poligono)

    def borrar_demanda_patinetes(self):
        if self.poligonos_demanda_patinetes != []:
            for poligono in self.poligonos_demanda_patinetes:
                poligono.delete()

    def boton_bicicletas(self, checkbox_bicicletas, clusters=False):
        if checkbox_bicicletas.get() and not clusters:
            self.pintar_flotantes()
        elif checkbox_bicicletas.get() and clusters:
            self.pintar_bicicletas_clusters_kmeans()
        elif not checkbox_bicicletas.get() and clusters:
            for poligono in self.poligonos_bicicletas_clusters:
                poligono.delete()
        elif not checkbox_bicicletas.get() and not clusters:
            for poligono in self.poligonos_bicicletas:
                poligono.delete()
    
    def boton_fijas_ocupacion(self, checkbox_ocupacion):
        if checkbox_ocupacion.get() == True:
            self.pintar_estaciones(ocupacion=True)
        elif checkbox_ocupacion.get() == False:
            utilInfo.close_infoest(self)
            for poligono in self.poligonos_estaciones_ocupacion:
                poligono.delete()
    
    def boton_centroides_bicicletas(self, checkbox_centroides):
        if checkbox_centroides.get() == True:
            self.pintar_centroides_bicicletas()
        elif checkbox_centroides.get() == False:
            for poligono in self.poligonos_centroides_bicicletas:
                poligono.delete()

    def boton_patinetes(self, checkbox_patinetes, clusters=False):
        if checkbox_patinetes.get() and not clusters:
            self.pintar_patinetes()
        elif checkbox_patinetes.get() and clusters:
            self.pintar_patinetes_clusters_kmeans()
        elif not checkbox_patinetes.get() and clusters:
            for poligono in self.poligonos_patinetes_clusters:
                poligono.delete()
        elif not checkbox_patinetes.get() and not clusters:
            for poligono in self.poligonos_patinetes:
                poligono.delete()

    def boton_centroides_patinetes(self, checkbox_centroides):
        if checkbox_centroides.get() == True:
            self.pintar_centroides_patinetes()
        elif checkbox_centroides.get() == False:
            for poligono in self.poligonos_centroides_patinetes:
                poligono.delete()

    def boton_demanda_bicicletas(self, checkbox_demanda_bicicletas):
        if checkbox_demanda_bicicletas.get() == True:
            self.pintar_demanda_bicicletas()
        elif checkbox_demanda_bicicletas.get() == False:
            self.borrar_demanda_bicicletas()
    
    def boton_demanda_patinetes(self, checkbox_demanda_patinetes):
        if checkbox_demanda_patinetes.get() == True:
            self.pintar_demanda_patinetes()
        elif checkbox_demanda_patinetes.get() == False:
            self.borrar_demanda_patinetes()
def anadir_mapa(self):
    self.labelMap=tkintermapview.TkinterMapView(self.frame_mapa, width=900, height=700, corner_radius=0)
    self.labelMap.pack(fill="both")
    self.labelMap.config(bg=COLOR_CUERPO_PRINCIPAL)
    
    self.labelMap.set_position(40.4168, -3.7038)
    self.labelMap.set_zoom(12)

    #self.labelMap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
    #self.labelMap.set_tile_server("https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png", max_zoom=22)  # black and white

        
def pintar_estaciones_v2(self):
    self.imagenEstacionesFijas = utilImagenes.leer_imagen("./imagenes/green_marker.ico", (15,20))
    for id in self.estaciones:
        self.labelMap.set_marker(self.estaciones[id]['coordinates'][1], self.estaciones[id]['coordinates'][0], 
                                 icon=self.imagenEstacionesFijas)



