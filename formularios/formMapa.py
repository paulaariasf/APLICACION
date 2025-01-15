from tkinter import *
from tkinter import Tk, messagebox
from tkinter import ttk
from tkinter.ttk import Checkbutton, Style as ttkCheckbutton, Style
from PIL import ImageTk, Image
from config import COLOR_CUERPO_PRINCIPAL, COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA
import util.utilEstaciones as utilEstaciones
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

class FormMapaDesign():

    def __init__(self, panel_principal, menuLateral):
        
        self.panel_principal = panel_principal

        self.frame_mapa = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_mapa.pack(fill="both")

        
        #Para poder borrar los mapas de calor
        self.poligonos_estaciones = []
        self.poligonos_flotantes = []
        self.poligonos_centroides = []
        self.poligonos_patinetes = []
        self.poligonos_demanda_bicicletas = []
        self.poligonos_demanda_patinetes = []
        self.poligonos_zonas = {}

        #Para poder borrar el poligono de seleccion
        self.pol_seleccion = None
        self.est_seleccion = None

        self.botones_anadidos = []

        self.estaciones = utilEstaciones.devolver_estaciones()

        self.maxLon, self.minLon, self.maxLat, self.minLat = utilEstaciones.limites(self.estaciones)

        self.bicicletas_flotantes = utilEstaciones.generar_flotantes_v2(self.estaciones, 0.005)
        self.patinetes = utilEstaciones.generar_patinetes(self.estaciones, 0.005, self.maxLon, self.minLon, self.maxLat, self.minLat)
        self.solicitudes_bicicletas = 1000
        self.demanda_bicicletas = utilDatos.generar_datos_demanda(self.solicitudes_bicicletas, self.maxLon, self.minLon, self.maxLat, self.minLat)
        self.solicitudes_patinetes = 500
        self.demanda_patinetes = utilDatos.generar_datos_demanda(self.solicitudes_patinetes, self.maxLon, self.minLon, self.maxLat, self.minLat)

        self.seleccionado_metros = StringVar()
        self.seleccionado_influencia =  StringVar()

        self.cargados_estaciones = {}
        self.cargados_estaciones['estaciones_abril2024.json'] = [self.estaciones, True]
        self.selected_archivo_estaciones = StringVar(value='estaciones_abril2024.json')
        self.estaciones_anterior = 'estaciones_abril2024.json'


        self.cargados_bicicletas = {}
        self.cargados_bicicletas['bicicletas_generadas_estaciones.json'] = [self.bicicletas_flotantes, True]
        self.selected_archivo_bicicletas = StringVar(value='bicicletas_generadas_estaciones.json')
        self.bicicletas_anterior = 'bicicletas_generadas_estaciones.json'

        self.cargados_patinetes = {}
        self.cargados_patinetes['patinetes_generados_estaciones.json'] = [self.patinetes, True]
        self.selected_archivo_patinetes = StringVar(value='patinetes_generados_estaciones.json')
        self.patinetes_anterior = 'patinetes_generados_estaciones.json'

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
                        width=200,
                        bg=COLOR_MENU_LATERAL)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        #scrollbar.config(command=canvas.yview)

        scrollable_frame = Frame(canvas, bg=COLOR_MENU_LATERAL, width=200)
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

        self.crear_tipo_transporte()
        self.crear_mapa_calor()
        self.crear_otras_opciones()
        self.crear_carga_datos()
        self.crear_demanda()

        """
        #Botones del menu lateral

        self.labelTipoTransporte = Label(self.scrollable_frame, text="Tipo de transporte", font=fontAwesome)
        self.labelTipoTransporte.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.labelTipoTransporte.pack(side=TOP)

        style = Style()
        style.configure("Custom.TCheckbutton", font=("FontAwesome", 10), anchor="w", background=COLOR_MENU_LATERAL,
                        foreground="white", bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2, indicatorcolor="green")

        checkbox_fijas = BooleanVar()
        self.buttonEstacionesFijas = Checkbutton(self.scrollable_frame, text="\uf3c5 Estaciones fijas", style="Custom.TCheckbutton",
                                                 variable=checkbox_fijas, command= lambda : self.boton_fijas(checkbox_fijas))
        self.buttonEstacionesFijas.pack(side=TOP, pady=5)

        checkbox_flotantes = BooleanVar()
        self.buttonBicicletasFlotantes = Checkbutton(self.scrollable_frame, text=" Bicicletas flotantes", style="Custom.TCheckbutton",
                                                     variable=checkbox_flotantes, command=lambda: self.boton_flotantes(checkbox_flotantes))
        self.buttonBicicletasFlotantes.pack(side=TOP, pady=5)

        checkbox_centroides = BooleanVar()
        self.buttonCentroides = Checkbutton(self.scrollable_frame, text=" Estaciones virtuales", style="Custom.TCheckbutton",
                                                    variable=checkbox_centroides, command=lambda: self.boton_centroides(checkbox_centroides))
        self.buttonCentroides.pack(side=TOP, pady=5)

        checkbox_patinetes = BooleanVar()
        self.buttonPatinetes = Checkbutton(self.scrollable_frame, text=" Patinetes", style="Custom.TCheckbutton",
                                                    variable=checkbox_patinetes, command=lambda: self.boton_patinetes(checkbox_patinetes))
        self.buttonPatinetes.pack(side=TOP, pady=5)

        self.LabelMapaCalor = Label(self.scrollable_frame, text="Mapa de Calor", font=fontAwesome)
        self.LabelMapaCalor.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.LabelMapaCalor.pack(side=TOP)

        self.checkbox_mapa_estaciones = BooleanVar()
        self.buttonMostrarMapaEstaciones = Checkbutton(self.scrollable_frame, text="\uf3c5 Estaciones fijas", style="Custom.TCheckbutton",
                                                       variable=self.checkbox_mapa_estaciones, command=self.mostrar_mapa_general)
        self.buttonMostrarMapaEstaciones.pack(side=TOP, pady=5)

        self.checkbox_mapa_flotantes = BooleanVar()
        self.buttonMostrarMapaFlotantes = Checkbutton(self.scrollable_frame, text=" Bicicletas flotantes", style="Custom.TCheckbutton",
                                                variable=self.checkbox_mapa_flotantes, command= self.mostrar_mapa_general)
        self.buttonMostrarMapaFlotantes.pack(side=TOP, pady=5)

        self.checkbox_mapa_patinetes = BooleanVar()
        self.buttonMostrarMapaPatinetes = Checkbutton(self.scrollable_frame, text=" Patinetes", style="Custom.TCheckbutton",
                                                variable=self.checkbox_mapa_patinetes, command= self.mostrar_mapa_general)
        self.buttonMostrarMapaPatinetes.pack(side=TOP, pady=5)

        self.buttonVecinos = Button(self.scrollable_frame, text=" Cambiar influencia vecinos", font=font.Font(family="FontAwesome", size=10),
                                                anchor="w", command= self.modificar_influencia)
        self.buttonVecinos.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonVecinos.pack(side=TOP)
        self.bindHoverEvents(self.buttonVecinos)

        self.buttonPorcentajeLLenado = Button(self.scrollable_frame, text=" Mapa porcentaje llenado", font=font.Font(family="FontAwesome", size=10), 
                                                anchor="w", command=self.mostrar_mapa_llenado)
        self.buttonPorcentajeLLenado.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonPorcentajeLLenado.pack(side=TOP)
        self.bindHoverEvents(self.buttonPorcentajeLLenado)

        self.buttonMostrarMapaHuecos = Button(self.scrollable_frame, text=" Mostrar mapa huecos", font=font.Font(family="FontAwesome", size=10), 
                                                anchor="w", command=self.mostrar_mapa_huecos)
        self.buttonMostrarMapaHuecos.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonMostrarMapaHuecos.pack(side=TOP)
        self.bindHoverEvents(self.buttonMostrarMapaHuecos)

        self.buttonCambiarN = Button(self.scrollable_frame, text=" Cambiar tamaño cuadrícula", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= self.modificar_cuadricula)
        self.buttonCambiarN.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        #self.buttonCambiarN.pack(side=TOP)
        self.bindHoverEvents(self.buttonCambiarN)

        self.buttonBorrarMapa = Button(self.scrollable_frame, text=" Borrar mapa de calor", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= self.borrar_mapacalor)
        self.buttonBorrarMapa.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        #self.buttonBorrarMapa.pack(side=TOP)
        self.bindHoverEvents(self.buttonBorrarMapa)

        self.labelCargaDatos = Label(self.scrollable_frame, text="Carga de datos", font=fontAwesome)
        self.labelCargaDatos.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.labelCargaDatos.pack(side=TOP)

        self.buttonCargaDatosBicicletas = Button(self.scrollable_frame, text=" Importar datos bicicletas", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= lambda: self.cargar_archivo('bicicletas'))
        self.buttonCargaDatosBicicletas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonCargaDatosBicicletas.pack(side=TOP)
        self.bindHoverEvents(self.buttonCargaDatosBicicletas)

        self.buttonCargaDatosPatinetes = Button(self.scrollable_frame, text=" Importar datos patinetes", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= lambda: self.cargar_archivo('patinetes'))
        self.buttonCargaDatosPatinetes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonCargaDatosPatinetes.pack(side=TOP)
        self.bindHoverEvents(self.buttonCargaDatosPatinetes)

        self.buttonDemanda = Button(self.scrollable_frame, text=" Demanda", font=fontAwesome)
        self.buttonDemanda.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonDemanda.pack(side=TOP)
        self.bindHoverEvents(self.buttonDemanda)"""

    def crear_tipo_transporte(self):

        fontAwesome=font.Font(family="FontAwesome", size=12, weight='bold')
        style = Style()
        style.configure("Custom.TCheckbutton", font=("FontAwesome", 10), anchor="w", background=COLOR_MENU_LATERAL,
                        foreground="white", bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2, indicatorcolor="green")

        frame_opcion = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_opcion.pack(fill=X, pady=2)

        boton_principal = Button(frame_opcion, text='Tipo de Transporte', bg=COLOR_MENU_LATERAL, fg = 'white', relief = FLAT,
                                font=fontAwesome, command=lambda: self.toggle_submenu('Tipo de Transporte'), width=22, height=0)
        boton_principal.pack(fill=X, expand=True)
        self.bindHoverEvents(boton_principal)

        frame_submenu = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_submenu.pack(fill=X, padx=10, pady=2)
        #frame_submenu.pack_forget()
        
        self.checkbox_fijas = BooleanVar()
        self.buttonEstacionesFijas = Checkbutton(frame_submenu, text="\uf3c5 Estaciones fijas", style="Custom.TCheckbutton",
                                                 variable=self.checkbox_fijas, command= lambda : self.boton_fijas(self.checkbox_fijas))
        self.buttonEstacionesFijas.pack(side=TOP, pady=5)

        self.checkbox_flotantes = BooleanVar()
        self.buttonBicicletasFlotantes = Checkbutton(frame_submenu, text=" Bicicletas flotantes", style="Custom.TCheckbutton",
                                                     variable=self.checkbox_flotantes, command=lambda: self.boton_flotantes(self.checkbox_flotantes))
        self.buttonBicicletasFlotantes.pack(side=TOP, pady=5)

        self.checkbox_centroides = BooleanVar()
        self.buttonCentroides = Checkbutton(frame_submenu, text=" Estaciones virtuales", style="Custom.TCheckbutton",
                                                    variable=self.checkbox_centroides, command=lambda: self.boton_centroides(self.checkbox_centroides))
        self.buttonCentroides.pack(side=TOP, pady=5)

        self.checkbox_patinetes = BooleanVar()
        self.buttonPatinetes = Checkbutton(frame_submenu, text=" Patinetes", style="Custom.TCheckbutton",
                                                    variable=self.checkbox_patinetes, command=lambda: self.boton_patinetes(self.checkbox_patinetes))
        self.buttonPatinetes.pack(side=TOP, pady=5)

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
        boton_principal.pack(fill=X)
        self.bindHoverEvents(boton_principal)

        frame_submenu = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_submenu.pack(fill=X, padx=10, pady=2)
        #frame_submenu.pack_forget()
        
        self.checkbox_mapa_estaciones = BooleanVar()
        self.buttonMostrarMapaEstaciones = Checkbutton(frame_submenu, text="\uf3c5 Estaciones fijas", style="Custom.TCheckbutton",
                                                       variable=self.checkbox_mapa_estaciones, command=self.mostrar_mapa_general)
        self.buttonMostrarMapaEstaciones.pack(side=TOP, pady=5)

        self.checkbox_mapa_flotantes = BooleanVar()
        self.buttonMostrarMapaFlotantes = Checkbutton(frame_submenu, text=" Bicicletas flotantes", style="Custom.TCheckbutton",
                                                variable=self.checkbox_mapa_flotantes, command= self.mostrar_mapa_general)
        self.buttonMostrarMapaFlotantes.pack(side=TOP, pady=5)

        self.checkbox_mapa_patinetes = BooleanVar()
        self.buttonMostrarMapaPatinetes = Checkbutton(frame_submenu, text=" Patinetes", style="Custom.TCheckbutton",
                                                variable=self.checkbox_mapa_patinetes, command= self.mostrar_mapa_general)
        self.buttonMostrarMapaPatinetes.pack(side=TOP, pady=5)

        self.submenus['Mapa de Calor'] = {"titulo": boton_principal, "frame_opcion": frame_opcion, 
                                          "frame_submenu": frame_submenu, "visible": True}

    def crear_otras_opciones(self):
        
        fontAwesome=font.Font(family="FontAwesome", size=12, weight='bold')
        style = Style()
        style.configure("Custom.TCheckbutton", font=("FontAwesome", 10), anchor="w", background=COLOR_MENU_LATERAL,
                        foreground="white", bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2, indicatorcolor="green")

        frame_opcion = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_opcion.pack(fill=X, pady=2)

        boton_principal = Button(frame_opcion, text='Otras opciones', bg=COLOR_MENU_LATERAL, fg = 'white', relief = FLAT,
                                font=fontAwesome, command=lambda: self.toggle_submenu('Otras opciones'), width=22, height=0)
        boton_principal.pack(fill=X)
        self.bindHoverEvents(boton_principal)

        frame_submenu = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_submenu.pack(fill=X, padx=10, pady=2)
        #frame_submenu.pack_forget()
        
        self.buttonVecinos = Button(frame_submenu, text=" Cambiar influencia vecinos", font=font.Font(family="FontAwesome", size=10),
                                                anchor="w", command= self.modificar_influencia)
        self.buttonVecinos.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonVecinos.pack(side=TOP)
        self.bindHoverEvents(self.buttonVecinos)

        self.buttonPorcentajeLLenado = Button(frame_submenu, text=" Mapa porcentaje llenado", font=font.Font(family="FontAwesome", size=10), 
                                                anchor="w", command=self.mostrar_mapa_llenado)
        self.buttonPorcentajeLLenado.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonPorcentajeLLenado.pack(side=TOP)
        self.bindHoverEvents(self.buttonPorcentajeLLenado)

        self.buttonMostrarMapaHuecos = Button(frame_submenu, text=" Mostrar mapa huecos", font=font.Font(family="FontAwesome", size=10), 
                                                anchor="w", command=self.mostrar_mapa_huecos)
        self.buttonMostrarMapaHuecos.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonMostrarMapaHuecos.pack(side=TOP)
        self.bindHoverEvents(self.buttonMostrarMapaHuecos)

        self.buttonCambiarN = Button(frame_submenu, text=" Cambiar tamaño cuadrícula", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= self.modificar_cuadricula)
        self.buttonCambiarN.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonCambiarN.pack(side=TOP)
        self.bindHoverEvents(self.buttonCambiarN)

        self.buttonBorrarMapa = Button(frame_submenu, text=" Borrar mapa de calor", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= self.borrar_mapacalor)
        self.buttonBorrarMapa.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonBorrarMapa.pack(side=TOP)
        self.bindHoverEvents(self.buttonBorrarMapa)

        self.submenus['Otras opciones'] = {"titulo": boton_principal, "frame_opcion": frame_opcion, 
                                          "frame_submenu": frame_submenu, "visible": True}
    
    def crear_carga_datos(self):

        fontAwesome=font.Font(family="FontAwesome", size=12, weight="bold")
        style = Style()
        style.configure("Custom.TCheckbutton", font=("FontAwesome", 10), anchor="w", background=COLOR_MENU_LATERAL,
                        foreground="white", bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2, indicatorcolor="green")

        frame_opcion = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_opcion.pack(fill=X, pady=2)

        boton_principal = Button(frame_opcion, text='Carga de datos', bg=COLOR_MENU_LATERAL, fg = 'white', relief = FLAT,
                                font=fontAwesome, command=lambda: self.toggle_submenu('Carga de datos'), width=22, height=0)
        boton_principal.pack(fill=X)
        self.bindHoverEvents(boton_principal)

        frame_submenu = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_submenu.pack(fill=X, padx=10, pady=2)
        #frame_submenu.pack_forget()

        self.buttonVerDatosCargados = Button(frame_submenu, text=" Ver datos cargados", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= self.visualizar_datos_cargados)
        self.buttonVerDatosCargados.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonVerDatosCargados.pack(side=TOP)
        self.bindHoverEvents(self.buttonVerDatosCargados)

        self.buttonCargaDatosEstaciones = Button(frame_submenu, text=" Importar datos estaciones", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= lambda: self.cargar_archivo('estaciones'))
        self.buttonCargaDatosEstaciones.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonCargaDatosEstaciones.pack(side=TOP)
        self.bindHoverEvents(self.buttonCargaDatosEstaciones)
        
        self.buttonCargaDatosBicicletas = Button(frame_submenu, text=" Importar datos bicicletas", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= lambda: self.cargar_archivo('bicicletas'))
        self.buttonCargaDatosBicicletas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonCargaDatosBicicletas.pack(side=TOP)
        self.bindHoverEvents(self.buttonCargaDatosBicicletas)

        self.buttonCargaDatosPatinetes = Button(frame_submenu, text=" Importar datos patinetes", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= lambda: self.cargar_archivo('patinetes'))
        self.buttonCargaDatosPatinetes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonCargaDatosPatinetes.pack(side=TOP)
        self.bindHoverEvents(self.buttonCargaDatosPatinetes)

        self.submenus['Carga de datos'] = {"titulo": boton_principal, "frame_opcion": frame_opcion, 
                                          "frame_submenu": frame_submenu, "visible": True}

    def crear_demanda(self):
        fontAwesome=font.Font(family="FontAwesome", size=12, weight="bold")
        style = Style()
        style.configure("Custom.TCheckbutton", font=("FontAwesome", 10), anchor="w", background=COLOR_MENU_LATERAL,
                        foreground="white", bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2, indicatorcolor="green")

        frame_opcion = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_opcion.pack(fill=X, pady=2)

        boton_principal = Button(frame_opcion, text='Demanda', bg=COLOR_MENU_LATERAL, fg = 'white', relief = FLAT,
                                font=fontAwesome, command=lambda: self.toggle_submenu('Demanda'), width=22, height=0)
        boton_principal.pack(fill=X)
        self.bindHoverEvents(boton_principal)

        frame_submenu = Frame(self.scrollable_frame, bg=COLOR_MENU_LATERAL)
        frame_submenu.pack(fill=X, padx=10, pady=2)
        #frame_submenu.pack_forget()

        self.checkbox_demanda_bicicletas = BooleanVar()
        self.buttonDemandaBicicletas = Checkbutton(frame_submenu, text=" Demanda bicicletas", style="Custom.TCheckbutton",
                                                    variable=self.checkbox_demanda_bicicletas, 
                                                    command=lambda: self.boton_demanda_bicicletas(self.checkbox_demanda_bicicletas))
        self.buttonDemandaBicicletas.pack(side=TOP, pady=5)

        self.checkbox_demanda_patinetes = BooleanVar()
        self.buttonDemandaPatinetes = Checkbutton(frame_submenu, text=" Demanda patinetes", style="Custom.TCheckbutton",
                                                    variable=self.checkbox_demanda_patinetes, 
                                                    command=lambda: self.boton_demanda_patinetes(self.checkbox_demanda_patinetes))
        self.buttonDemandaPatinetes.pack(side=TOP, pady=5)

        self.buttonMapaCalorDemandaBicicletas = Button(frame_submenu, text=" Oferta-demanda bicicletas", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=self.mostrar_mapa_demanda_bicicletas)
        self.buttonMapaCalorDemandaBicicletas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonMapaCalorDemandaBicicletas.pack(side=TOP)
        self.bindHoverEvents(self.buttonMapaCalorDemandaBicicletas)

        self.buttonMapaCalorDemandaPatinetes = Button(frame_submenu, text=" Oferta-demanda patinetes", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=self.mostrar_mapa_demanda_patinetes)
        self.buttonMapaCalorDemandaPatinetes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonMapaCalorDemandaPatinetes.pack(side=TOP)
        self.bindHoverEvents(self.buttonMapaCalorDemandaPatinetes)

        self.buttonGenerarDemandaBicicletas = Button(frame_submenu, text=" Nuevos datos bicicletas", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=self.generar_datos_demanda_bicicletas)
        self.buttonGenerarDemandaBicicletas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonGenerarDemandaBicicletas.pack(side=TOP)
        self.bindHoverEvents(self.buttonGenerarDemandaBicicletas)

        self.buttonGenerarDemandaPatinetes = Button(frame_submenu, text=" Nuevos datos patinetes", font=font.Font(family="FontAwesome", size=10),
                                    anchor='w', command=self.generar_datos_demanda_patinetes)
        self.buttonGenerarDemandaPatinetes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonGenerarDemandaPatinetes.pack(side=TOP)
        self.bindHoverEvents(self.buttonGenerarDemandaPatinetes)

        self.submenus['Demanda'] = {"titulo": boton_principal, "frame_opcion": frame_opcion, 
                                          "frame_submenu": frame_submenu, "visible": True}

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

    def visualizar_datos_cargados(self):
        self.ventana_datos = Toplevel(self.frame_mapa)
        self.ventana_datos.title("Entrada de Mapa de Calor")

        ancho_pantalla = self.ventana_datos.winfo_screenwidth()
        alto_pantalla = self.ventana_datos.winfo_screenheight()

        ancho_ventana = 900
        alto_ventana = 600

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_datos.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.ventana_datos.resizable(False, False)
        self.ventana_datos.config(bg=COLOR_MENU_LATERAL)
        self.ventana_datos.protocol("WM_DELETE_WINDOW", self.ventana_datos.destroy)

        frame_contenedor = Frame(self.ventana_datos, bg=COLOR_MENU_LATERAL)
        frame_contenedor.pack(fill=BOTH, expand=True, padx=20, pady=20)

        titulo_font = Font(family="Arial", size=12, weight="bold")

        ######################## COLUMNA ESTACIONES ######################    

        frame_estaciones = Frame(frame_contenedor, bg=COLOR_MENU_LATERAL, width=300)
        frame_estaciones.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        Label(frame_estaciones, text='Estaciones', font=titulo_font, anchor=W,bg=COLOR_MENU_LATERAL, fg="white").pack(anchor=CENTER, pady=(0, 10))

        texto_cargados = f'Se han cargado un total de {len(self.cargados_estaciones)}\n archivos de estaciones'

        if len(self.cargados_estaciones) != 0: texto_cargados += '\n\nLos archivos cargados son los siguientes:'

        Label(frame_estaciones, text=texto_cargados, bg=COLOR_MENU_LATERAL, fg="white", anchor=W, justify=CENTER).pack(fill=BOTH, padx=5, pady=5)

        frame_radiobuttons_estaciones = Frame(frame_estaciones, bg=COLOR_MENU_LATERAL)
        frame_radiobuttons_estaciones.pack(fill=BOTH, expand=True, padx=5, pady=5)
        #frame_radiobuttons_estaciones = self.anadir_scrollbar_estaciones(frame_radiobuttons_estaciones)

        if len(self.cargados_estaciones) != 0:
            for id, archivo in self.cargados_estaciones.items():
                if archivo[1]:
                    self.selected_archivo_estaciones.set(id)
                Radiobutton(frame_radiobuttons_estaciones, text=id, variable=self.selected_archivo_estaciones,
                    value=id, bg=COLOR_MENU_LATERAL, selectcolor=COLOR_MENU_LATERAL, fg='white', anchor=W, justify=LEFT,
                    command=self.select_button).pack(anchor=W, padx=5, pady=2)

        frame_botones_superior = Frame(frame_estaciones, bg=COLOR_MENU_LATERAL)
        frame_botones_superior.pack(side=TOP, fill=X, pady=10)

        frame_botones_inferior = Frame(frame_estaciones, bg=COLOR_MENU_LATERAL)
        frame_botones_inferior.pack(side=TOP, fill=X, pady=10)

        Button(frame_botones_superior, text="Cargar Archivos", bg='#A4D4EE', fg=COLOR_MENU_LATERAL, 
               command=lambda: self.cargar_archivo('estaciones', visualizador=True)).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_superior, text="Importar datos históricos", bg='#A4D4EE', fg=COLOR_MENU_LATERAL,
            command=lambda: self.selector_fecha()
        ).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_inferior, text="Aplicar Cambios", bg='#A4D4EE', fg=COLOR_MENU_LATERAL,
            command=lambda: self.aplicar_cambios('estaciones')
        ).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_inferior, text="Generar datos aleatorios", bg='#A4D4EE', fg=COLOR_MENU_LATERAL,
            #command=lambda: self.datos_aleatorios('estaciones')
        ).pack(side=LEFT, fill=X, expand=True, padx=5)

        ######################## COLUMNA BICICLETAS ######################

        frame_bicicletas = Frame(frame_contenedor, bg=COLOR_MENU_LATERAL, width=300)
        frame_bicicletas.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        Label(frame_bicicletas, text='Bicicletas', font=titulo_font, anchor=W, bg=COLOR_MENU_LATERAL, fg="white").pack(anchor=CENTER, pady=(0, 10))

        texto_cargados = f'Se han cargado un total de {len(self.cargados_bicicletas)}\n archivos de bicicletas'

        if len(self.cargados_bicicletas) != 0: texto_cargados += '\n\nLos archivos cargados son los siguientes:'

        Label(frame_bicicletas, text=texto_cargados, bg=COLOR_MENU_LATERAL, fg="white", anchor=CENTER, justify=CENTER).pack(fill=BOTH, padx=5, pady=5)

        frame_radiobuttons_bicicletas = Frame(frame_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_radiobuttons_bicicletas.pack(fill=BOTH, expand=True, padx=5, pady=5)

        if len(self.cargados_bicicletas) != 0:
            for id, archivo in self.cargados_bicicletas.items():
                if archivo[1]:
                    self.selected_archivo_bicicletas.set(id)
                Radiobutton(frame_radiobuttons_bicicletas, text=id, variable=self.selected_archivo_bicicletas,
                    value=id, bg=COLOR_MENU_LATERAL, selectcolor=COLOR_MENU_LATERAL, fg="white", anchor=W, justify=LEFT,
                    command=self.select_button).pack(anchor=W, padx=5, pady=2)

        frame_botones_bicicletas = Frame(frame_bicicletas, bg=COLOR_MENU_LATERAL)
        frame_botones_bicicletas.pack(side=BOTTOM, fill=X, pady=10)

        Button(frame_botones_bicicletas, text="Cargar Archivos", bg=COLOR_MENU_CURSOR_ENCIMA, fg='white',
            command=lambda: self.cargar_archivo('bicicletas', visualizador=True)).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_bicicletas, text="Aplicar Cambios", bg=COLOR_MENU_CURSOR_ENCIMA, fg='white',
            command=lambda: self.aplicar_cambios('bicicletas')
        ).pack(side=LEFT, fill=X, expand=True, padx=5)


        ######################## COLUMNA PATINETES ######################

        frame_patinetes = Frame(frame_contenedor, bg=COLOR_MENU_LATERAL, width=300)
        frame_patinetes.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        Label(frame_patinetes, text='Patinetes', font=titulo_font, anchor=W, bg=COLOR_MENU_LATERAL, fg="white").pack(anchor=CENTER, pady=(0, 10))

        texto_cargados = f'Se han cargado un total de {len(self.cargados_patinetes)}\n archivos de patinetes'

        if len(self.cargados_patinetes) != 0: texto_cargados += '\n\nLos archivos cargados son los siguientes:'

        Label(frame_patinetes, text=texto_cargados, bg=COLOR_MENU_LATERAL, fg="white", anchor=CENTER, justify=CENTER).pack(fill=BOTH, padx=5, pady=5)

        frame_radiobuttons_patinetes = Frame(frame_patinetes, bg=COLOR_MENU_LATERAL)
        frame_radiobuttons_patinetes.pack(fill=BOTH, expand=True, padx=5, pady=5)

        if len(self.cargados_patinetes) != 0:
            for id, archivo in self.cargados_patinetes.items():
                if archivo[1]:
                    self.selected_archivo_patinetes.set(id)
                Radiobutton(frame_radiobuttons_patinetes, text=id, variable=self.selected_archivo_patinetes, value=id, 
                    bg=COLOR_MENU_LATERAL, selectcolor=COLOR_MENU_LATERAL, fg="white", anchor=W, justify=LEFT,
                    command=self.select_button).pack(anchor=W, padx=5, pady=2)

        frame_botones_patinetes = Frame(frame_patinetes, bg=COLOR_MENU_LATERAL)
        frame_botones_patinetes.pack(side=BOTTOM, fill=X, pady=10)

        Button(frame_botones_patinetes, text="Cargar Archivos", bg=COLOR_MENU_CURSOR_ENCIMA, fg='white',
            command=lambda: self.cargar_archivo('patinetes', visualizador=True)).pack(side=LEFT, fill=X, expand=True, padx=5)

        Button(frame_botones_patinetes, text="Aplicar Cambios", bg=COLOR_MENU_CURSOR_ENCIMA, fg='white',
            command=lambda: self.aplicar_cambios('patinetes')
        ).pack(side=LEFT, fill=X, expand=True, padx=5)

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

        if self.clasificacion == 'General' and self.checkbox_mapa_estaciones.get()==False and self.checkbox_mapa_flotantes.get()==False \
              and self.checkbox_mapa_patinetes.get()==False:
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
            self.dic_mapa_calor = utilEstaciones.crear_diccionario(
                self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                estaciones=self.estaciones, add_fijas=True)
        elif self.clasificacion == "Huecos":
            self.dic_mapa_calor = utilEstaciones.crear_diccionario(
                    self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                    estaciones=self.estaciones,mostrar_huecos=True)
        elif self.clasificacion == "Demanda Bicicletas":
            self.dic_mapa_calor = utilEstaciones.crear_diccionario(
                    self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                    estaciones=self.estaciones,flotantes= self.bicicletas_flotantes,
                    demanda_bicicletas=self.demanda_bicicletas, demanda_patinetes=self.demanda_patinetes,
                    mostrar_demanda_bicicletas=True, add_fijas=True, add_flotantes=True)
        elif self.clasificacion == "Demanda Patinetes":
            self.dic_mapa_calor = utilEstaciones.crear_diccionario(
                    self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                    patinetes=self.patinetes,
                    demanda_bicicletas=self.demanda_bicicletas, demanda_patinetes=self.demanda_patinetes,
                    mostrar_demanda_patinetes=True, add_patinetes=True)
        else:
            #print(f'Est: {self.checkbox_mapa_estaciones.get()}, Flot: {self.checkbox_mapa_flotantes.get()}')
            self.dic_mapa_calor = utilEstaciones.crear_diccionario(
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
            color = utilEstaciones.get_color(factor_llenado, rangos, colores)
            
            if factor_llenado != 0: #los que son 0 no pintarlos
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
        self.checkbox_mapa_patinetes.get()==False and self.clasificacion=="General":
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
        [self.buttonBicicletasFlotantes.invoke() for _ in range(2)] if self.checkbox_flotantes.get() else None
        [self.buttonCentroides.invoke() for _ in range(2)] if self.checkbox_centroides.get() else None
        [self.buttonPatinetes.invoke() for _ in range(2)] if self.checkbox_patinetes.get() else None
        [self.buttonDemandaBicicletas.invoke() for _ in range(2)] if self.checkbox_demanda_bicicletas.get() else None
        [self.buttonDemandaPatinetes.invoke() for _ in range(2)] if self.checkbox_demanda_patinetes.get() else None

    def select_button(self):
        self.cargados_estaciones[self.estaciones_anterior][1] = False
        self.cargados_estaciones[self.selected_archivo_estaciones.get()][1] = True
        self.estaciones_anterior = self.selected_archivo_estaciones.get()

        self.cargados_bicicletas[self.bicicletas_anterior][1] = False
        self.cargados_bicicletas[self.selected_archivo_bicicletas.get()][1] = True
        self.bicicletas_anterior = self.selected_archivo_bicicletas.get()

        self.cargados_patinetes[self.patinetes_anterior][1] = False
        self.cargados_patinetes[self.selected_archivo_patinetes.get()][1] = True
        self.patinetes_anterior = self.selected_archivo_patinetes.get()

        for clave, valor in self.cargados_estaciones.items():
            print(f"Clave: {clave}, Booleano: {valor[1]}")

        for clave, valor in self.cargados_bicicletas.items():
            print(f"Clave: {clave}, Booleano: {valor[1]}")

        for clave, valor in self.cargados_patinetes.items():
            print(f"Clave: {clave}, Booleano: {valor[1]}")
    
    def cargar_archivo(self, tipo, visualizador=False):
        if tipo == 'estaciones':
            archivo = filedialog.askopenfilename(title="Cargar archivo JSON de estaciones",
                                                 filetypes=[("Archivos JSON", "*.json")])
        elif tipo == 'bicicletas':
            archivo = filedialog.askopenfilename(title="Cargar archivo JSON de bicicletas",
                                                 filetypes=[("Archivos JSON", "*.json")])
        elif tipo == 'patinetes':
            archivo = filedialog.askopenfilename(title="Cargar archivo JSON de patinetes",
                                                 filetypes=[("Archivos JSON", "*.json")])
        if archivo:
            try:
                with open(archivo, 'r', encoding="utf-8") as f:
                    data = json.load(f)

                nombre_archivo = os.path.basename(archivo)
                utilInfo.show_info_upload(self, nombre_archivo)

                if tipo == 'estaciones':
                    if nombre_archivo[:10] == 'estaciones':
                        if nombre_archivo not in self.cargados_estaciones:
                            self.cargados_estaciones[nombre_archivo] = [data, False]
                        else: utilInfo.show_info_upload(self, 'El archivo ya estaba cargado')
                    else: utilInfo.show_info_upload(self, 'Debe introducir un archivo de estaciones')
                elif tipo == 'bicicletas':
                    if nombre_archivo[:10] == 'bicicletas':
                        if nombre_archivo not in self.cargados_bicicletas:
                            self.cargados_bicicletas[nombre_archivo] = [data, False]
                        else: utilInfo.show_info_upload(self, 'El archivo ya estaba cargado')
                    else: utilInfo.show_info_upload(self, 'Debe introducir un archivo de bicicletas')
                elif tipo == 'patinetes':
                    if nombre_archivo[:9] == 'patinetes':
                        if nombre_archivo not in self.cargados_patinetes:
                            self.cargados_patinetes[nombre_archivo] = [data, False]
                        else: utilInfo.show_info_upload(self, 'El archivo ya estaba cargado')
                    else: utilInfo.show_info_upload(self, 'Debe introducir un archivo de patinetes')

            except Exception as e:
                print(f"Error al cargar el archivo: {e}")
                utilInfo.show_info_upload(self, "Error al cargar el archivo")
        if visualizador:
            self.ventana_datos.destroy()
            self.buttonVerDatosCargados.invoke()
    
    def generar_datos_demanda_bicicletas(self):
        self.demanda_bicicletas = utilDatos.generar_datos_demanda(self.solicitudes_bicicletas, self.maxLon, self.minLon, self.maxLat, self.minLat)
    
    def generar_datos_demanda_patinetes(self):
        self.demanda_patinetes = utilDatos.generar_datos_demanda(self.solicitudes_patinetes, self.maxLon, self.minLon, self.maxLat, self.minLat)
    
    def aplicar_cambios(self, cambiado):
        if cambiado == 'estaciones':
            self.estaciones = self.cargados_estaciones[self.selected_archivo_estaciones.get()][0]
        elif cambiado == 'bicicletas':
            self.bicicletas_flotantes = self.cargados_bicicletas[self.selected_archivo_bicicletas.get()][0]
        elif cambiado == 'patinetes':
            self.patinetes = self.cargados_patinetes[self.selected_archivo_patinetes.get()][0]
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
        self.ventana_datos.destroy()
        self.buttonVerDatosCargados.invoke()

    def ventana_informativa(self):
        ventana_info = Toplevel()
        ventana_info.title("Información")

        ancho_pantalla = ventana_info.winfo_screenwidth()
        alto_pantalla = ventana_info.winfo_screenheight()

        ancho_ventana = 300
        alto_ventana = 150

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        ventana_info.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        ventana_info.resizable(False, False)
        ventana_info.config(bg=COLOR_MENU_LATERAL)
        ventana_info.protocol("WM_DELETE_WINDOW", ventana_info.destroy)

        mensaje = Label(ventana_info, text="Los cambios se han \n aplicado correctamente", bg=COLOR_MENU_LATERAL, fg="white", font=("Helvetica", 12))
        mensaje.pack(pady=20)

        boton_cerrar = Button(ventana_info, bg= COLOR_MENU_LATERAL, fg='white', text="Cerrar", command=ventana_info.destroy)
        boton_cerrar.pack(pady=10)

        ventana_info.mainloop()

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

    def mostrar_mapa_general(self):
        self.borrar_mapacalor()
        self.clasificacion = "General"
        #print(f'Est: {self.checkbox_mapa_estaciones.get()}, Flot: {self.checkbox_mapa_flotantes.get()}')
        self.pintar_mapa()
    
    def mostrar_mapa_huecos(self):
        self.borrar_mapacalor()
        self.clasificacion = "Huecos"
        self.pintar_mapa()

    def mostrar_mapa_llenado(self):
        self.borrar_mapacalor()
        self.clasificacion = "Llenado"
        self.pintar_mapa()

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
        if not hasattr(self, 'n') or (self.checkbox_mapa_estaciones.get()==False and \
        self.checkbox_mapa_flotantes.get()==False and self.checkbox_mapa_patinetes.get()):
            messagebox.showwarning("Advertencia", "Debe seleccionar lo que desea incluir en el mapa de calor")
            return
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
        if not hasattr(self, 'n') or (self.checkbox_mapa_estaciones.get()==False and \
        self.checkbox_mapa_flotantes.get()==False and self.checkbox_mapa_patinetes.get()==False):
            messagebox.showwarning("Advertencia", "Debe seleccionar lo que desea incluir en el mapa de calor")
            return
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
    
    def pintar_estaciones(self):
        """
        with open('data/estaciones_abril2024.json', 'w', encoding='utf-8') as archivo:
            json.dump(self.estaciones, archivo, ensure_ascii=False, indent=4)
        """
        strings = []
        for id in self.estaciones:
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
                                    outline_color="blue",
                                    border_width=5,
                                    name=(id, coord_estacion),
                                    command=lambda event: utilInfo.show_info_estacion(self, event))
            self.poligonos_estaciones.append(poligono)
        longest_string = max(strings, key=len)
        max_len = len(longest_string)
        #print(f'número de estaciones fijas: {len(self.estaciones)}')

    def boton_fijas(self, checkbox_fijas):
        if checkbox_fijas.get() == True:
            self.pintar_estaciones()
        elif checkbox_fijas.get() == False:
            for poligono in self.poligonos_estaciones:
                poligono.delete()
      
    def pintar_flotantes(self):
        #cambiar generar_flotantes para usar esto       

        for i in range(len(self.bicicletas_flotantes['id'])):

            coord_estacion = self.bicicletas_flotantes['coord'][i]
            d = 0.00000001
            #coordinates = [(coord_estacion[0], coord_estacion[1]),
            #                (coord_estacion[0], coord_estacion[1]+ d),
            #                (coord_estacion[0] + d, coord_estacion[1] + d),
            #                (coord_estacion[0] + d, coord_estacion[1])]

            poligono = self.labelMap.set_polygon([coord_estacion],
                                    outline_color="red",
                                    border_width=1,
                                    name=self.bicicletas_flotantes['info'][i])
            self.poligonos_flotantes.append(poligono)

    def pintar_flotantes_clusters_dbscan(self):

        coordenadas = self.bicicletas_flotantes['coord']
        eps = 0.008

        # Aplicar el algoritmo de clustering DBSCAN
        clusters = utilClustering.clusters_dbscan(eps, coordenadas)

        n_clusters = 0
        # Añadir los puntos de las bicicletas al mapa
        for i, coord in enumerate(coordenadas):
            cluster_id = clusters[i]
            if cluster_id > n_clusters:
                n_clusters = cluster_id
            color = self.color_map.get(cluster_id, 'black')
            poligono = self.labelMap.set_polygon([coord],
                                            outline_color=color,
                                            border_width=1,
                                            name="Outlier")
            self.poligonos_flotantes.append(poligono)
    
    def pintar_flotantes_clusters_kmeans(self):
        
        if not hasattr(self, 'clusters') and not hasattr(self, 'centroides'):
            self.coordenadas_flotantes = self.bicicletas_flotantes['coord']
            self.clusters, self.centroides = utilClustering.clusters_kmeans(self.coordenadas_flotantes)

        for i, coord in enumerate(self.coordenadas_flotantes):
            cluster_id = self.clusters[i]
            color = self.color_map.get(cluster_id%50, 'black')
            poligono = self.labelMap.set_polygon([coord],
                                                outline_color=color,
                                                border_width=1.5,
                                                name="Outlier")
            self.poligonos_flotantes.append(poligono)

    def pintar_centroides(self):
        if not hasattr(self, 'clusters') and not hasattr(self, 'centroides'):
            self.coordenadas_flotantes = self.bicicletas_flotantes['coord']
            self.clusters, self.centroides = utilClustering.clusters_kmeans(self.coordenadas_flotantes)

        for i, centroide in enumerate(self.centroides):
            d = 0.00000001
            coordinates = [(centroide[0], centroide[1]),
                           (centroide[0], centroide[1]+ d),
                           (centroide[0] + d, centroide[1] + d),
                           (centroide[0] + d, centroide[1])]
            poligono = self.labelMap.set_polygon(coordinates,
                                                outline_color="#ff005d",
                                                border_width=5,
                                                name="Outlier")
            self.poligonos_centroides.append(poligono)

    def pintar_patinetes(self):      

        for i in range(len(self.patinetes['id'])):

            coord_patinete = self.patinetes['coord'][i]
            d = 0.00000001
            #coordinates = [(coord_estacion[0], coord_estacion[1]),
            #                (coord_estacion[0], coord_estacion[1]+ d),
            #                (coord_estacion[0] + d, coord_estacion[1] + d),
            #                (coord_estacion[0] + d, coord_estacion[1])]

            poligono = self.labelMap.set_polygon([coord_patinete],
                                    outline_color="orange",
                                    border_width=1,
                                    name=self.patinetes['info'][i])
            self.poligonos_patinetes.append(poligono)
    
    def pintar_demanda_bicicletas(self):
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

    def pintar_demanda_patinetes(self):
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

    def boton_flotantes(self, checkbox_flotantes):
        if checkbox_flotantes.get() == True:
            labelCargando = Label(self.labelMap, text="Cargando clusters...", bg="#1F71A9", fg="white", font=("Arial", 14))
            labelCargando.place(relx=0.5, rely=0.5, anchor="center")
            self.pintar_flotantes_clusters_kmeans()
            labelCargando.destroy()
        elif checkbox_flotantes.get() == False:
            for poligono in self.poligonos_flotantes:
                poligono.delete()

    def boton_centroides(self, checkbox_centroides):
        if checkbox_centroides.get() == True:
            self.pintar_centroides()
        elif checkbox_centroides.get() == False:
            for poligono in self.poligonos_centroides:
                poligono.delete()

    def boton_patinetes(self, checkbox_patinetes):
        if checkbox_patinetes.get() == True:
            self.pintar_patinetes()
        elif checkbox_patinetes.get() == False:
            for poligono in self.poligonos_patinetes:
                poligono.delete()

    def boton_demanda_bicicletas(self, checkbox_demanda_bicicletas):
        if checkbox_demanda_bicicletas.get() == True:
            self.pintar_demanda_bicicletas()
        elif checkbox_demanda_bicicletas.get() == False:
            for poligono in self.poligonos_demanda_bicicletas:
                poligono.delete()
    
    def boton_demanda_patinetes(self, checkbox_demanda_patinetes):
        if checkbox_demanda_patinetes.get() == True:
            self.pintar_demanda_patinetes()
        elif checkbox_demanda_patinetes.get() == False:
            for poligono in self.poligonos_demanda_patinetes:
                poligono.delete()

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



