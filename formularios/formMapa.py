from tkinter import *
from tkinter import Tk, messagebox
from tkinter.ttk import Checkbutton, Style as ttkCheckbutton, Style
from config import COLOR_CUERPO_PRINCIPAL, COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA
import util.utilEstaciones as utilEstaciones
import util.utilImagenes as utilImagenes
import util.utilClustering as utilClustering
import util.utilInfo as utilInfo
import tkintermapview
import numpy as np
from tkinter import font
import math
import os
from tkinter import filedialog
import json

class FormMapaDesign():

    def __init__(self, panel_principal, menuLateral):
        
        self.panel_principal = panel_principal

        self.frame_mapa = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_mapa.pack(fill="both")

        self.estaciones = utilEstaciones.devolver_estaciones()
        self.df_flotantes = utilEstaciones.generar_flotantes_v2(self.estaciones, 0.005)
        self.df_patinetes = utilEstaciones.generar_patinetes(self.estaciones, 0.005)
        
        #Para poder borrar los mapas de calor
        self.poligonos_estaciones = []
        self.poligonos_flotantes = []
        self.poligonos_centroides = []
        self.poligonos_patinetes = []
        self.poligonos_zonas = {}

        #Para poder borrar el poligono de seleccion
        self.pol_seleccion = None
        self.est_seleccion = None

        self.botones_anadidos = []

        self.maxLon, self.minLon, self.maxLat, self.minLat = utilEstaciones.limites(self.estaciones)

        self.seleccionado_metros = StringVar()
        self.seleccionado_influencia =  StringVar()

        self.cargados_bicicletas = []
        self.cargados_flotantes = []

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
                                                anchor="w", command=self.porcentaje_llenado)
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
        
        checkbox_fijas = BooleanVar()
        self.buttonEstacionesFijas = Checkbutton(frame_submenu, text="\uf3c5 Estaciones fijas", style="Custom.TCheckbutton",
                                                 variable=checkbox_fijas, command= lambda : self.boton_fijas(checkbox_fijas))
        self.buttonEstacionesFijas.pack(side=TOP, pady=5)

        checkbox_flotantes = BooleanVar()
        self.buttonBicicletasFlotantes = Checkbutton(frame_submenu, text=" Bicicletas flotantes", style="Custom.TCheckbutton",
                                                     variable=checkbox_flotantes, command=lambda: self.boton_flotantes(checkbox_flotantes))
        self.buttonBicicletasFlotantes.pack(side=TOP, pady=5)

        checkbox_centroides = BooleanVar()
        self.buttonCentroides = Checkbutton(frame_submenu, text=" Estaciones virtuales", style="Custom.TCheckbutton",
                                                    variable=checkbox_centroides, command=lambda: self.boton_centroides(checkbox_centroides))
        self.buttonCentroides.pack(side=TOP, pady=5)

        checkbox_patinetes = BooleanVar()
        self.buttonPatinetes = Checkbutton(frame_submenu, text=" Patinetes", style="Custom.TCheckbutton",
                                                    variable=checkbox_patinetes, command=lambda: self.boton_patinetes(checkbox_patinetes))
        self.buttonPatinetes.pack(side=TOP, pady=5)

        # Guardar referencias al estado del submenú
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
                                                anchor="w", command=self.porcentaje_llenado)
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
    
    def visualizar_datos_cargados(self):
        ventana_datos = Toplevel(self.frame_mapa)
        ventana_datos.title("Entrada de Mapa de Calor")

        ancho_pantalla = ventana_datos.winfo_screenwidth()
        alto_pantalla = ventana_datos.winfo_screenheight()

        ancho_ventana = 700
        alto_ventana = 350

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        ventana_datos.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        

        ventana_datos.protocol("WM_DELETE_WINDOW", ventana_datos.destroy)

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
            self.dic_mapa_calor = utilEstaciones.crear_diccionario(self.estaciones, None, None,
                    self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                    add_fijas=True, add_flotantes=False, add_patinetes=False, mostrar_huecos=False)
        elif self.clasificacion == "Huecos":
            self.dic_mapa_calor = utilEstaciones.crear_diccionario(self.estaciones, None, None,
                    self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                    add_fijas=False, add_flotantes=False, add_patinetes=False,mostrar_huecos=True)
        else:
            #print(f'Est: {self.checkbox_mapa_estaciones.get()}, Flot: {self.checkbox_mapa_flotantes.get()}')
            self.dic_mapa_calor = utilEstaciones.crear_diccionario(self.estaciones, self.df_flotantes, self.df_patinetes,
                    self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, 
                    add_fijas=self.checkbox_mapa_estaciones.get(), add_flotantes=self.checkbox_mapa_flotantes.get(),
                    add_patinetes=self.checkbox_mapa_patinetes.get(), mostrar_huecos=False)
            
            if self.n == 44: self.alcance = 3
            elif self.n == 54: self.alcance = 5
            elif self.n == 72: self.alcance = 7
            elif self.n == 108: self.alcance = 9
            if self.influencia == 'con':
                self.dic_mapa_calor['cantidades_suavizadas'] = self.aplicar_gaussiana(self.dic_mapa_calor['cantidades'], self.alcance)

        colores = ["#FF3300", "#FF6600", "#FF9933", "#FFCC33", "#FFDD33", "#FFFF00", "#CCFF66", "#99FF66", "#66FF33", "#00FF00"]

        minimo = np.min(self.dic_mapa_calor['cantidades'])
        maximo = np.max(self.dic_mapa_calor['cantidades'])
        index_min = np.argmin(self.dic_mapa_calor['cantidades'])
        index_max = np.argmax(self.dic_mapa_calor['cantidades'])
        print(f'Influencia: {self.influencia}')
        print(f'Min: {minimo}, max: {maximo}')
        print(f'El indice de la menor es: {index_min} y se trata de la zona {self.dic_mapa_calor['ids'][index_min]}')
        print(f'El indice de la mayor es: {index_max} y se trata de la zona {self.dic_mapa_calor['ids'][index_max]}')

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
        if self.checkbox_mapa_estaciones.get()==True:
            mostrados+="estaciones "
        if self.checkbox_mapa_flotantes.get()==True:
            mostrados+="flotantes "
        if self.checkbox_mapa_patinetes.get()==True:
            mostrados+="patinetes "
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
                                            command=self.show_info_zona,
                                            pass_coords=True)
    ###############################################################################################
    
    def cargar_archivo(self, tipo):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json")]
        )
        if archivo:
            try:
                with open(archivo, 'r') as f:
                    data = json.load(f)
                
                if tipo == 'bicicletas':
                    self.cargados_bicicletas.append(data)
                elif tipo == 'patinetes':
                    self.cargados_patinetes.append(data)

                nombre_archivo = os.path.basename(archivo)
                utilInfo.show_info_upload(self, nombre_archivo)

            except Exception as e:
                print(f"Error al cargar el archivo: {e}")
                utilInfo.show_info_upload(self, "Error al cargar el archivo")
   
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
        self.checkbox_mapa_flotantes.get()==False and self.checkbox_mapa_patinetes.get()):
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

    def porcentaje_llenado(self):
        self.borrar_mapacalor()
        self.clasificacion = "Llenado"
        self.pintar_mapa()
    
    def pintar_estaciones(self):
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

        for i in range(len(self.df_flotantes['id'])):

            coord_estacion = self.df_flotantes['coord'][i]
            d = 0.00000001
            #coordinates = [(coord_estacion[0], coord_estacion[1]),
            #                (coord_estacion[0], coord_estacion[1]+ d),
            #                (coord_estacion[0] + d, coord_estacion[1] + d),
            #                (coord_estacion[0] + d, coord_estacion[1])]

            poligono = self.labelMap.set_polygon([coord_estacion],
                                    outline_color="red",
                                    border_width=1,
                                    name=self.df_flotantes['info'][i])
            self.poligonos_flotantes.append(poligono)

    def pintar_flotantes_clusters_dbscan(self):

        coordenadas = self.df_flotantes['coord']
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
            self.coordenadas_flotantes = self.df_flotantes['coord']
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
            self.coordenadas_flotantes = self.df_flotantes['coord']
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

        for i in range(len(self.df_patinetes['id'])):

            coord_patinete = self.df_patinetes['coord'][i]
            d = 0.00000001
            #coordinates = [(coord_estacion[0], coord_estacion[1]),
            #                (coord_estacion[0], coord_estacion[1]+ d),
            #                (coord_estacion[0] + d, coord_estacion[1] + d),
            #                (coord_estacion[0] + d, coord_estacion[1])]

            poligono = self.labelMap.set_polygon([coord_patinete],
                                    outline_color="orange",
                                    border_width=1,
                                    name=self.df_patinetes['info'][i])
            self.poligonos_patinetes.append(poligono)

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

def anadir_mapa(self):
    self.labelMap=tkintermapview.TkinterMapView(self.frame_mapa, width=900, height=700, corner_radius=0)
    self.labelMap.pack(fill="both")
    self.labelMap.config(bg=COLOR_CUERPO_PRINCIPAL)
    
    self.labelMap.set_position(40.4168, -3.7038)
    self.labelMap.set_zoom(12)

    self.labelMap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
    #self.labelMap.set_tile_server("https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png", max_zoom=22)  # black and white

        
def pintar_estaciones_v2(self):
    self.imagenEstacionesFijas = utilImagenes.leer_imagen("./imagenes/green_marker.ico", (15,20))
    for id in self.estaciones:
        self.labelMap.set_marker(self.estaciones[id]['coordinates'][1], self.estaciones[id]['coordinates'][0], 
                                 icon=self.imagenEstacionesFijas)



