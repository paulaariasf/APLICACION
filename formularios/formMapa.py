from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL, COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA
import util.utilEstaciones as utilEstaciones
import util.utilImagenes as utilImagenes
import tkintermapview
from tkinter import messagebox
import numpy as np
from tkinter import font
import json
import math

class FormMapaDesign():

    def __init__(self, panel_principal, menuLateral):
        
        self.panel_principal = panel_principal

        self.frame_mapa = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_mapa.pack(fill="both")

        self.estaciones = utilEstaciones.devolver_estaciones()
        
        self.poligonos_estaciones = []
        self.poligonos_flotantes = []
        self.poligonos_zonas = {}

        self.pol_seleccion = None
        self.est_seleccion = None

        self.maxLon, self.minLon, self.maxLat, self.minLat = utilEstaciones.limites(self.estaciones)

        self.seleccionado = StringVar()

        anadir_mapa(self)
        self.menu_lateral(menuLateral)

        #creacion_paneles_info(self, panel_principal)

    def menu_lateral(self, menuLateral):
        self.menuLateral = menuLateral

        #Controles menu lateral
        fontAwesome=font.Font(family="FontAwesome", size=15)

        #Botones del menu lateral

        self.labelTipoTransporte = Label(self.menuLateral, text="Tipo de transporte", font=fontAwesome)
        self.labelTipoTransporte.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.labelTipoTransporte.pack(side=TOP)

        checkbox_fijas = BooleanVar()
        self.buttonEstacionesFijas = Checkbutton(self.menuLateral, text="\uf3c5    Estaciones fijas", font=font.Font(family="FontAwesome", size=10), 
                                                 variable=checkbox_fijas, anchor="w", command= lambda : self.boton_fijas(checkbox_fijas))
        self.buttonEstacionesFijas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonEstacionesFijas.pack(side=TOP)

        checkbox_flotantes = BooleanVar()
        self.buttonBicicletasFlotantes = Checkbutton(self.menuLateral, text="    Bicicletas flotantes", font=font.Font(family="FontAwesome", size=10),
                                                     variable=checkbox_flotantes, anchor="w", command=lambda: self.boton_flotantes(checkbox_flotantes))
        self.buttonBicicletasFlotantes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonBicicletasFlotantes.pack(side=TOP)
        self.bindHoverEvents(self.buttonBicicletasFlotantes)

        self.LabelMapaCalor_menu = Label(self.menuLateral, text="Mapa de Calor", font=fontAwesome)
        self.LabelMapaCalor_menu.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.LabelMapaCalor_menu.pack(side=TOP)

        self.buttonMostrarMapa_menu = Button(self.menuLateral, text=" Mostrar mapa de calor", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= self.mostrar_mapapordefecto)
        self.buttonMostrarMapa_menu.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonMostrarMapa_menu.pack(side=TOP)
        self.bindHoverEvents(self.buttonMostrarMapa_menu)

        self.buttonPorcentajeLLenado_menu = Button(self.menuLateral, text=" Mapa con porcentaje de llenado", font=font.Font(family="FontAwesome", size=8), 
                                                 anchor="w", command= self.porcentaje_llenado)
        self.buttonPorcentajeLLenado_menu.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonPorcentajeLLenado_menu.pack(side=TOP)
        self.bindHoverEvents(self.buttonPorcentajeLLenado_menu)

        self.buttonCambiarN_menu = Button(self.menuLateral, text=" Modificar cuadrícula", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= self.modificar_cuadricula)
        self.buttonCambiarN_menu.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonCambiarN_menu.pack(side=TOP)
        self.bindHoverEvents(self.buttonCambiarN_menu)

        self.buttonBorrarMapa_menu = Button(self.menuLateral, text=" Borrar mapa de calor", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="w", command= self.borrar_mapacalor)
        self.buttonBorrarMapa_menu.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonBorrarMapa_menu.pack(side=TOP)
        self.bindHoverEvents(self.buttonBorrarMapa_menu)

        self.buttonIntegracion = Button(self.menuLateral, text=" Integración", font=fontAwesome)
        self.buttonIntegracion.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonIntegracion.pack(side=TOP)
        self.bindHoverEvents(self.buttonIntegracion)

        self.buttonDemanda = Button(self.menuLateral, text=" Demanda", font=fontAwesome)
        self.buttonDemanda.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonDemanda.pack(side=TOP)
        self.bindHoverEvents(self.buttonDemanda)

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
    
    def close_infozona(self):
        if self.pol_seleccion is not None:
            self.pol_seleccion.delete()
        if hasattr(self, 'infozona_frame'):
            self.infozona_frame.destroy()

    def show_info_zona(self, coords):
        self.close_infozona()

        self.infozona_frame = Frame(self.panel_principal, bg="white", borderwidth=1, relief="solid")
        self.infozona_frame.place(relx=0.8, rely=0.75)
        
        zona = utilEstaciones.clasificar_punto(self.n, (coords[0], coords[1]), self.lon_celda, self.lat_celda, self.minLon, self.maxLat, self.idMap)
        fila = (zona-1)//self.n
        columna =((zona-1)%self.n)

        if self.clasificacion == "General":
            texto=f"Zona seleccionada: {zona} de {self.n**2}\nNúmero de estaciones:{self.diccionario['num_estaciones'][zona-1]}\nCantidad de bicis: {self.diccionario['cantidades'][zona-1]} de {self.diccionario['cantidad_maxima']}"
        elif self.clasificacion == "Llenado":
            texto=f"Zona seleccionada: {zona} de {self.n**2}\nNúmero de estaciones:{self.diccionario['num_estaciones'][zona-1]}\nCantidad de bicis: {self.diccionario['cantidades'][zona-1]} de {self.diccionario['capacidades'][zona-1]}"

        info_label = Label(self.infozona_frame, text=texto, bg="white")
        info_label.pack(side="left", padx=5, pady=5)

        #Resaltar zona seleccionada
        self.pol_seleccion =self.labelMap.set_polygon(self.diccionario['coordenadas'][zona-1],
                                    fill_color="#1F71A9",
                                    outline_color="#1F71A9",
                                    border_width=3)

        close_button = Button(self.infozona_frame, text="x", command=lambda: self.close_infozona(), bg="white", fg="red", borderwidth=0)
        close_button.pack(side="right", padx=5, pady=5)

    def pintar_mapa_calor(self):
        if hasattr (self, "frame_leyenda"):
            self.frame_leyenda.destroy()   

        if not hasattr(self, 'n'):
            metros = 500
            lon_objetivo = metros/(111320*math.cos(40.4))
            lat_objetivo = metros/111320 
            n_lon = abs(self.maxLon - self.minLon) / lon_objetivo
            n_lat = abs(self.maxLat - self.minLat) / lat_objetivo
            self.n = math.ceil(max(n_lon, n_lat))
        
        self.lon_celda = (self.maxLon - self.minLon) / self.n
        self.lat_celda = (self.maxLat - self.minLat) / self.n
        self.idMap = np.repeat(0, repeats=self.n**2).reshape((self.n,self.n))
        self.diccionario = utilEstaciones.crear_diccionario_zonas(self.estaciones, self.n, self.minLon, self.maxLat, self.lon_celda, self.lat_celda, self.idMap)
        #self.maxLon, self.minLon, self.maxLat, self.minLat = -3.4214, -3.93884035, 40.62442815, 40.22383835
        #self.maxLon, self.minLon, self.maxLat, self.minLat = -3.521772, -3.784628, 40.5157613, 40.330671
        
        if self.clasificacion == "General":
            min_val = min(self.diccionario['cantidades'])
            max_val = max(self.diccionario['cantidades'])
            self.diccionario['cantidad_maxima'] = max_val
            rangos_flotantes = min_val + (np.linspace(0, 1, 9)**2) * (max_val - min_val)
            rangos = sorted(set(np.round(rangos_flotantes).astype(int)))

            rangos = min_val + ((np.arange(9) ** 2) * (max_val - min_val) // 8 ** 2)

            colores = ["#FF3300", "#FF6600", "#FFCC33", "#FFDD33", "#FFFF00", "#CCFF66", "#99FF66", "#00FF00"]
            ############################       Leyenda     ##############################
            self.frame_leyenda = Frame(self.panel_principal, width=20, height=100, bg=None)
            self.frame_leyenda.place(relx=0.9, rely=0.3, width=50, height=168)
            i=8
            for color in colores[::-1]:
                color_label = Label(self.frame_leyenda, width=60, height=1, bg=color, text=f"{rangos[i-1]}-{rangos[i]}")
                color_label.pack()
                i=i-1
            ###############################################################################

        elif self.clasificacion == "LLenado":
            rangos = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            colores = ["#FF3300", "#FF6600", "#FF9933", "#FFCC33", "#FFDD33", "#FFFF00", "#CCFF66", "#99FF66", "#66FF33", "#00FF00"]
            i=10
            ############################       Leyenda     ##############################
            self.frame_leyenda = Frame(self.panel_principal, width=20, height=100, bg=None)
            self.frame_leyenda.place(relx=0.9, rely=0.3, width=50, height=210) 

            for color in colores[::-1]:
                color_label = Label(self.frame_leyenda, width=50, height=1, bg=color, text=f"{rangos[i-1]}-{rangos[i]}")
                color_label.pack()
                i=i-1
            ###############################################################################
        
        
        for i in range(pow(self.n, 2)):
            #if(self.diccionario['num_estaciones'][i]) != 0: #los que son 0 no pintarlos
            if self.clasificacion == "General":
                color = utilEstaciones.get_color(self.diccionario['cantidades'][i], rangos, colores)
            elif self.clasificacion == "LLenado":
                if self.diccionario['capacidades'][i] != 0:
                    porcentaje = (self.diccionario['cantidades'][i]/self.diccionario['capacidades'][i])*100
                else: porcentaje = 0
                color = utilEstaciones.get_color(porcentaje, rangos, colores)
            poligono = self.labelMap.set_polygon(self.diccionario['coordenadas'][i],
                                    fill_color=color,
                                    outline_color="grey",
                                    border_width=1,
                                    name=f'Zona {self.diccionario['ids'][i]}')
            if self.n in self.poligonos_zonas:
                self.poligonos_zonas[self.n].append(poligono)
            else:
                self.poligonos_zonas[self.n] = [poligono]

        self.labelMap.add_right_click_menu_command(label=f"Info zona con n={self.n}",
                                        command=self.show_info_zona,
                                        pass_coords=True)
    

    def mostrar_mapapordefecto(self):
        self.borrar_mapacalor()
        self.clasificacion = "General"
        self.pintar_mapa_calor()

    def borrar_mapacalor(self):
        if hasattr(self, "n"):
            poligonos = self.poligonos_zonas[self.n]
            if len(poligonos) != 0:
                for poligono in poligonos:
                    poligono.delete()
            self.frame_leyenda.destroy()

    def modificar_cuadricula(self):
        self.ventana_mod = Toplevel(self.frame_mapa)
        self.ventana_mod.title("Entrada de Mapa de Calor")

        ancho_pantalla = self.ventana_mod.winfo_screenwidth()
        alto_pantalla = self.ventana_mod.winfo_screenheight()

        ancho_ventana = 300
        alto_ventana = 150

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_mod.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        if self.n == 41: self.seleccionado.set(500)
        elif self.n == 51: self.seleccionado.set(400)
        elif self.n == 68: self.seleccionado.set(300)
        elif self.n == 102: self.seleccionado.set(200)

        # Crear RadioButtons
        radio500 = Radiobutton(self.ventana_mod, text="500 metros", variable=self.seleccionado, value=500)
        radio500.pack(anchor=W)

        radio400 = Radiobutton(self.ventana_mod, text="400 metros", variable=self.seleccionado, value=400)
        radio400.pack(anchor=W)

        radio300 = Radiobutton(self.ventana_mod, text="300 metros", variable=self.seleccionado, value=300)
        radio300.pack(anchor=W)

        radio200 = Radiobutton(self.ventana_mod, text="200 metros", variable=self.seleccionado, value=200)
        radio200.pack(anchor=W)

        submit_button = Button(self.ventana_mod, text="Mostrar", command=self.enviar)
        submit_button.pack(pady=5)

        self.ventana_mod.protocol("WM_DELETE_WINDOW", self.ventana_mod.destroy)


    def enviar(self):        
        self.borrar_mapacalor()
        self.ventana_mod.destroy()

        
        metros = float(self.seleccionado.get())
        lon_objetivo = metros/(111320*math.cos(40.4))
        lat_objetivo = metros/111320 
        n_lon = abs(self.maxLon - self.minLon) / lon_objetivo
        n_lat = abs(self.maxLat - self.minLat) / lat_objetivo
        self.n = math.ceil(max(n_lon, n_lat))

        if not hasattr(self, 'clasificacion'):
            self.clasificacion = "General"

        self.pintar_mapa_calor()

    def porcentaje_llenado(self):
        self.borrar_mapacalor()
        self.clasificacion = "LLenado"
        self.pintar_mapa_calor()


    def close_infoest(self):
        if self.est_seleccion is not None:
            self.est_seleccion.delete()
        if hasattr(self, 'infoest_frame'):
            self.infoest_frame.destroy()

    def show_info_estacion(self, polygon):
        self.close_infoest()

        self.infoest_frame = Frame(self.panel_principal, bg="white", borderwidth=1, relief="solid")
        self.infoest_frame.place(relx=0.6, rely=0.9)
        
        id, coord_estacion = polygon.name
        info_label = Label(self.infoest_frame, text=f"Estación seleccionada: {self.estaciones[id]['name']} \n Cantidad de bicis: {self.estaciones[id]['bike_bases']}", bg="white")
        info_label.pack(side="left", padx=5, pady=5)

        #Añadir marcador en la estacion seleccionada
        self.est_seleccion = self.labelMap.set_marker(coord_estacion[0], coord_estacion[1])
        close_button = Button(self.infoest_frame, text="x", command=self.close_infoest, bg="white", fg="red", borderwidth=0)
        close_button.pack(side="right", padx=5, pady=5)
    
    def pintar_estaciones(self):
        for id in self.estaciones:
            coord_estacion = tuple(self.estaciones[id]['coordinates'][::-1])
            d = 0.00000001
            coordinates = [(coord_estacion[0], coord_estacion[1]),
                           (coord_estacion[0], coord_estacion[1]+ d),
                           (coord_estacion[0] + d, coord_estacion[1] + d),
                           (coord_estacion[0] + d, coord_estacion[1])]
            poligono = self.labelMap.set_polygon(coordinates,
                                    outline_color="blue",
                                    border_width=5,
                                    name=(id, coord_estacion),
                                    command=self.show_info_estacion,
                                    )
            self.poligonos_estaciones.append(poligono)
           
    def boton_fijas(self, checkbox_fijas):
        if checkbox_fijas.get() == True:
            self.pintar_estaciones()
        elif checkbox_fijas.get() == False:
            for poligono in self.poligonos_estaciones:
                poligono.delete()

      
    def pintar_flotantes(self):
        radio = 0.005
        df_flotantes = utilEstaciones.generar_flotantes_v2(self.estaciones, radio)        

        for i in range(len(df_flotantes['id'])):

            coord_estacion = df_flotantes['coord'][i]
            d = 0.00000001
            #coordinates = [(coord_estacion[0], coord_estacion[1]),
            #                (coord_estacion[0], coord_estacion[1]+ d),
            #                (coord_estacion[0] + d, coord_estacion[1] + d),
            #                (coord_estacion[0] + d, coord_estacion[1])]

            poligono = self.labelMap.set_polygon([coord_estacion],
                                    outline_color="red",
                                    border_width=1,
                                    name=df_flotantes['info'][i])
            self.poligonos_flotantes.append(poligono)        
    
    def boton_flotantes(self, checkbox_flotantes):
        if checkbox_flotantes.get() == True:
            self.pintar_flotantes()
        elif checkbox_flotantes.get() == False:
            for poligono in self.poligonos_flotantes:
                poligono.delete()


def anadir_mapa(self):
    self.labelMap=tkintermapview.TkinterMapView(self.frame_mapa, width=900, height=700, corner_radius=0)
    self.labelMap.pack(fill="both")
    self.labelMap.config(bg=COLOR_CUERPO_PRINCIPAL)
    
    #self.labelMap.set_marker(40.4454477, -3.6853377000000003)
    self.labelMap.set_position(40.4168, -3.7038)
    self.labelMap.set_zoom(12)

    self.labelMap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
    #self.labelMap.set_tile_server("https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png", max_zoom=22)  # black and white

        
def pintar_estaciones_v2(self):
    self.imagenEstacionesFijas = utilImagenes.leer_imagen("./imagenes/green_marker.ico", (15,20))
    for id in self.estaciones:
        self.labelMap.set_marker(self.estaciones[id]['coordinates'][1], self.estaciones[id]['coordinates'][0], 
                                 icon=self.imagenEstacionesFijas)



