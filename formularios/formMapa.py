from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL, COLOR_MENU_LATERAL, COLOR_MENU_CURSOR_ENCIMA
import util.utilEstaciones as utilEstaciones
import util.utilImagenes as utilImagenes
import tkintermapview
from tkinter import messagebox
import numpy as np
from tkinter import font

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
                                                 variable=checkbox_fijas, anchor="e", command= lambda : self.boton_fijas(checkbox_fijas))
        self.buttonEstacionesFijas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonEstacionesFijas.pack(side=TOP)

        checkbox_flotantes = BooleanVar()
        self.buttonBicicletasFlotantes = Checkbutton(self.menuLateral, text="    Bicicletas flotantes", font=font.Font(family="FontAwesome", size=10),
                                                     variable=checkbox_flotantes, anchor="e", command=self.boton_flotantes(checkbox_flotantes))
        self.buttonBicicletasFlotantes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonBicicletasFlotantes.pack(side=TOP)
        self.bindHoverEvents(self.buttonBicicletasFlotantes)

        self.LabelMapaCalor_menu = Label(self.menuLateral, text="Mapa de Calor", font=fontAwesome)
        self.LabelMapaCalor_menu.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.LabelMapaCalor_menu.pack(side=TOP)

        self.buttonMostrarMapa_menu = Button(self.menuLateral, text=" Mostrar mapa de calor", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="e", command= self.mostrar_mapapordefecto_enmenu)
        self.buttonMostrarMapa_menu.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonMostrarMapa_menu.pack(side=TOP)
        self.bindHoverEvents(self.buttonMostrarMapa_menu)

        self.buttonCambiarN_menu = Button(self.menuLateral, text=" Modificar cuadrícula", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="e", command= self.introducir_n)
        self.buttonCambiarN_menu.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonCambiarN_menu.pack(side=TOP)
        self.bindHoverEvents(self.buttonCambiarN_menu)

        self.buttonBorrarMapa_menu = Button(self.menuLateral, text=" Borrar mapa de calor", font=font.Font(family="FontAwesome", size=10), 
                                                 anchor="e", command= self.borrar_mapacalor_enmenu)
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

        info_label = Label(self.infozona_frame, text=f"Zona seleccionada: {zona} de {self.n**2}\nNúmero de estaciones:{self.diccionario['num_estaciones'][zona-1]}\nCantidad de bicis: {self.diccionario['cantidades'][zona-1]}", bg="white")
        info_label.pack(side="left", padx=5, pady=5)

        #Resaltar zona seleccionada
        self.pol_seleccion =self.labelMap.set_polygon(self.diccionario['coordenadas'][zona-1],
                                    fill_color="#1F71A9",
                                    outline_color="#1F71A9",
                                    border_width=3)

        close_button = Button(self.infozona_frame, text="x", command=lambda: self.close_infozona(), bg="white", fg="red", borderwidth=0)
        close_button.pack(side="right", padx=5, pady=5)

    def pintar_mapa_calor(self):
        self.maxLon, self.minLon, self.maxLat, self.minLat = utilEstaciones.limites(self.estaciones)
        self.lon_celda = (self.maxLon - self.minLon) / self.n
        self.lat_celda = (self.maxLat - self.minLat) / self.n
        self.idMap = np.repeat(0, repeats=self.n**2).reshape((self.n,self.n))
        self.diccionario = utilEstaciones.crear_dicCoord(self.estaciones, self.n, self.minLon, self.minLat, self.maxLat, self.lon_celda, self.lat_celda, self.idMap)

        min_val = min(self.diccionario['cantidades'])
        max_val = max(self.diccionario['cantidades'])
        rangos_flotantes = min_val + (np.linspace(0, 1, 11)**2) * (max_val - min_val)
        rangos = sorted(set(np.round(rangos_flotantes).astype(int)))
        colores = ["#FF3300", "#FF6600", "#FF9933", "#FFCC33", "#FFDD33", "#FFFF00", "#CCFF66", "#99FF66", "#66FF33", "#00FF00"]
        
        self.anadir_leyenda_colores(rangos, colores)

        for i in range(pow(self.n, 2)):
            poligono = self.labelMap.set_polygon(self.diccionario['coordenadas'][i],
                                    fill_color=utilEstaciones.get_color(self.diccionario['cantidades'][i], rangos, colores),
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
    
    def anadir_leyenda_colores(self, rangos, colores):
        self.frame_leyenda = Frame(self.panel_principal, width=20, height=100, bg=None)
        self.frame_leyenda.place(relx=0.9, rely=0.3, width=50, height=210) 
        rangos[0]=1

        i=10
        for color in colores[::-1]:
            color_label = Label(self.frame_leyenda, width=50, height=1, bg=color, text=f"{rangos[i-1]}-{rangos[i]}")
            color_label.pack()
            i=i-1

    def mostrar_mapapordefecto(self):
        self.borrar_mapacalor()
        self.n = 40
        self.pintar_mapa_calor()
        self.buttonCambiarN = Button(self.panel_principal, text='Modificar cuadrícula', font=("Roboto", 8, "bold"), bg="#1F71A9", fg="white", width=17, command=self.introducir_n)
        self.buttonCambiarN.place(relx=0.85, rely=0.12)

        self.buttonBorrarMapa = Button(self.panel_principal, text='Borrar Mapa de Calor', font=("Roboto", 12, "bold"), bg="#1F71A9", fg="white", width=18, command=self.borrar_mapacalor)
        self.buttonBorrarMapa.place(relx=0.8, rely=0.17)

    def borrar_mapacalor(self):
        if hasattr(self, "n"):
            for poligono in self.poligonos_zonas[self.n]:
                poligono.delete()
            self.buttonCambiarN.destroy()
            self.buttonBorrarMapa.destroy()
            self.frame_leyenda.destroy()

    def mostrar_mapapordefecto_enmenu(self):
        self.borrar_mapacalor_enmenu()
        self.n = 40
        self.pintar_mapa_calor()

    def borrar_mapacalor_enmenu(self):
        if hasattr(self, "n"):
            for poligono in self.poligonos_zonas[self.n]:
                poligono.delete()
            self.frame_leyenda.destroy()

    def introducir_n(self):
        self.ventana_n = Toplevel(self.frame_mapa)
        self.ventana_n.title("Entrada de Mapa de Calor")

        ancho_pantalla = self.ventana_n.winfo_screenwidth()
        alto_pantalla = self.ventana_n.winfo_screenheight()

        ancho_ventana = 300
        alto_ventana = 120

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.ventana_n.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        label = Label(self.ventana_n, text="Introduzca el número de filas y columnas deseado\n para crear el mapa de calor:")
        label.pack(pady=5)

        self.text_box = Entry(self.ventana_n, width=10)
        self.text_box.pack(padx=10, pady=5)

        submit_button = Button(self.ventana_n, text="Mostrar", command=self.enviar_n)
        submit_button.pack(pady=5)

        self.ventana_n.protocol("WM_DELETE_WINDOW", self.ventana_n.destroy)

    def enviar_n(self):
        input_text = self.text_box.get().strip()

        if input_text.isdigit():
            number = int(input_text)
            if 0 <= number <= 1000:
                self.ventana_n.destroy()
                self.n = number
                self.labelMap.delete_all_polygon()
                self.pintar_mapa_calor()
            else:
                messagebox.showerror("Error", "Por favor, introduce un número entre 0 y 1000.")
        else:
            messagebox.showerror("Error", "Por favor, introduce un número válido.")

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
            coordinates = [(coord_estacion[0], coord_estacion[1]),
                            (coord_estacion[0], coord_estacion[1]+ d),
                            (coord_estacion[0] + d, coord_estacion[1] + d),
                            (coord_estacion[0] + d, coord_estacion[1])]

            poligono = self.labelMap.set_polygon(coordinates,
                                    outline_color="red",
                                    border_width=3,
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

    #Botones en mapa
    self.buttonMapaCalor = Button(self.panel_principal, text='Mostrar Mapa de Calor', font=("Roboto", 12, "bold"), bg="#1F71A9", fg="white", width=18, command=self.mostrar_mapapordefecto)
    self.buttonMapaCalor.place(relx=0.8, rely=0.05)

    #self.buttonEstaciones = Button(self.frame_general, text='Mostrar Estaciones Fijas', font=("Roboto", 12, "bold"), bg="#1F71A9", fg="white", width=22, command=self.pintar_estaciones)
    #self.buttonEstaciones.place(relx=0.8, rely=0.15)

    #self.buttonBicicletas = Button(self.frame_general, text='Mostrar Bicicletas Flotantes', font=("Roboto", 12, "bold"), bg="#1F71A9", fg="white", width=22, command=self.pintar_flotantes)
    #self.buttonBicicletas.place(relx=0.8, rely=0.25)

        
def pintar_estaciones_v2(self):
    self.imagenEstacionesFijas = utilImagenes.leer_imagen("./imagenes/green_marker.ico", (15,20))
    for id in self.estaciones:
        self.labelMap.set_marker(self.estaciones[id]['coordinates'][1], self.estaciones[id]['coordinates'][0], 
                                 icon=self.imagenEstacionesFijas)



"""def creacion_paneles_info(self, panel_principal):
    self.barra_superior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
    self.barra_superior.pack(side=TOP, fill=X, expand=False)

    self.barra_central = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)  
    self.barra_central.pack(side=TOP, fill=X, expand=False)

    self.barra_superior_left = Frame(self.barra_superior, bg=COLOR_CUERPO_PRINCIPAL)
    self.barra_superior_left.pack(side=LEFT, fill=BOTH, expand=True)

    self.barra_superior_right = Frame(self.barra_superior, bg=COLOR_CUERPO_PRINCIPAL)
    self.barra_superior_right.pack(side=LEFT, fill=BOTH, expand=True)

    self.barra_central_left = Frame(self.barra_central, bg=COLOR_CUERPO_PRINCIPAL)
    self.barra_central_left.pack(side=LEFT, fill=BOTH, expand=True)

    self.barra_central_right = Frame(self.barra_central, bg=COLOR_CUERPO_PRINCIPAL)
    self.barra_central_right.pack(side=LEFT, fill=BOTH, expand=True)

    self.barra_inferior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
    self.barra_inferior.pack(side=TOP, fill="both", expand=True)

    self.labelTituloMapaCalor=Label(self.barra_superior_left, text="Información del mapa de calor")
    self.labelTituloMapaCalor.config(fg="#1F71A9", font=("Roboto", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, pady=10)
    self.labelTituloMapaCalor.pack(side=LEFT, anchor="n", fill=X, expand=True)

    self.labelInfoMapaCalor=Label(self.barra_central_left, text="Zona: \n\n Nº de bicicletas:")
    self.labelInfoMapaCalor.config(fg="#1F71A9", font=("Roboto", 14), bg=COLOR_CUERPO_PRINCIPAL, pady=10)
    self.labelInfoMapaCalor.pack(side=LEFT, anchor="n", fill=X, expand=False)

    self.labelTituloEstacion=Label(self.barra_superior_right, text="Información de la estación")
    self.labelTituloEstacion.config(fg="#1F71A9", font=("Roboto", 20, "bold"), bg=COLOR_CUERPO_PRINCIPAL, pady=10)
    self.labelTituloEstacion.pack(side=LEFT, anchor="n", fill=X, expand=True)

    self.labelInfoEstacion=Label(self.barra_central_right, text="Estación: \n\n Nº de bicicletas:")
    self.labelInfoEstacion.config(fg="#1F71A9", font=("Roboto", 14), bg=COLOR_CUERPO_PRINCIPAL, pady=10)
    self.labelInfoEstacion.pack(side=LEFT, anchor="n", fill=X, expand=False)

    anadir_mapa(self, self.barra_inferior)
"""
