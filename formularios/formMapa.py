from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL, COLOR_BARRA_SUPERIOR
import util.utilEstaciones as utilEstaciones
import util.utilImagenes as utilImagenes
import tkintermapview
from tkinter import messagebox
import numpy as np

class FormMapaDesign():

    def __init__(self, panel_principal):

        self.frame_general = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_general.pack(fill="both")

        self.estaciones = utilEstaciones.devolver_estaciones()

        anadir_mapa(self, self.frame_general)

        #creacion_paneles_info(self, panel_principal)
    
    def close_infozona(self):
        if hasattr(self, 'infozona_frame'):
            self.infozona_frame.destroy()

    def show_info_zona(self, coords):
        self.close_infozona()

        self.infozona_frame = Frame(self.frame_general, bg="white", borderwidth=1, relief="solid")
        self.infozona_frame.place(relx=0.8, rely=0.8)
        
        zona = utilEstaciones.clasificar_punto(self.n, (coords[1], coords[0]), self.lon_celda, self.lat_celda, self.minLon, self.minLat, self.idMap)
        
        info_label = Label(self.infozona_frame, text=f"Zona seleccionada: {zona} de {self.n**2}\n Cantidad de bicis: {self.diccionario['cantidades'][zona]}", bg="white")
        info_label.pack(side="left", padx=5, pady=5)

        close_button = Button(self.infozona_frame, text="x", command=self.close_infozona, bg="white", fg="red", borderwidth=0)
        close_button.pack(side="right", padx=5, pady=5)

    def pintar_mapa_calor(self):
        self.maxLon, self.minLon, self.maxLat, self.minLat = utilEstaciones.limites(self.estaciones)
        self.lon_celda = (self.maxLon - self.minLon) / self.n
        self.lat_celda = (self.maxLat - self.minLat) / self.n
        self.idMap = np.repeat(0, repeats=self.n**2).reshape((self.n,self.n))
        self.diccionario = utilEstaciones.crear_dicCoord(self.estaciones, self.n, self.minLon, self.minLat, self.maxLat, self.lon_celda, self.lat_celda, self.idMap)

        for i in range(pow(self.n, 2)):
            self.labelMap.set_polygon(self.diccionario['coordenadas'][i],
                                    fill_color=utilEstaciones.get_color(self.diccionario['cantidades'][i], 0, max(self.diccionario['cantidades'])),
                                    outline_color=None,
                                    name=f'Zona {self.diccionario['ids'][i]}')

        self.labelMap.add_right_click_menu_command(label="Show Info",
                                        command=self.show_info_zona,
                                        pass_coords=True)
    
    def introducir_n(self):
        self.ventana_n = Toplevel(self.frame_general)
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
        if hasattr(self, 'infoest_frame'):
            self.infoest_frame.destroy()

    def show_info_estacion(self, polygon):
        self.close_infoest()

        self.infoest_frame = Frame(self.frame_general, bg="white", borderwidth=1, relief="solid")
        self.infoest_frame.place(relx=0.7, rely=0.9)
        
        id = polygon.name
        info_label = Label(self.infoest_frame, text=f"Estación seleccionada: {self.estaciones[id]['name']} \n Cantidad de bicis: {self.estaciones[id]['bike_bases']}", bg="white")
        info_label.pack(side="left", padx=5, pady=5)

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
            self.labelMap.set_polygon(coordinates,
                                    outline_color="blue",
                                    border_width=3,
                                    name=id,
                                    command=self.show_info_estacion,
                                    )
            
    def pintar_flotantes(self):
        radio = 0.005 #es un valor definido, posteriormente se parametrizará
        df_flotantes = utilEstaciones.generar_flotantes_v2(self.estaciones, radio)        

        for i in range(len(df_flotantes['id'])):

            coord_estacion = df_flotantes['coord'][i]
            d = 0.00000001
            coordinates = [(coord_estacion[0], coord_estacion[1]),
                            (coord_estacion[0], coord_estacion[1]+ d),
                            (coord_estacion[0] + d, coord_estacion[1] + d),
                            (coord_estacion[0] + d, coord_estacion[1])]

            self.labelMap.set_polygon(coordinates,
                                    outline_color="red",
                                    border_width=2,
                                    name=df_flotantes['info'][i])

def creacion_paneles_info(self, panel_principal):
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

def anadir_mapa(self, frame):
    self.labelMap=tkintermapview.TkinterMapView(frame, width=900, height=700, corner_radius=0)
    self.labelMap.pack(fill="both")
    self.labelMap.config(bg=COLOR_CUERPO_PRINCIPAL)
    
    #self.labelMap.set_marker(40.4454477, -3.6853377000000003)
    self.labelMap.set_position(40.4168, -3.7038)
    self.labelMap.set_zoom(12)

    self.labelMap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
    #self.labelMap.set_tile_server("https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png", max_zoom=22)  # black and white

    #Botones
    self.buttonMapaCalor = Button(frame, text='Mostrar Mapa de Calor', font=("Roboto", 12, "bold"), 
                       bg="#1F71A9", fg="white", width=22, command=self.introducir_n)
    self.buttonMapaCalor.place(relx=0.8, rely=0.05)

    self.buttonEstaciones = Button(frame, text='Mostrar Estaciones Fijas', font=("Roboto", 12, "bold"), 
                       bg="#1F71A9", fg="white", width=22, command=self.pintar_estaciones)
    self.buttonEstaciones.place(relx=0.8, rely=0.15)

    self.buttonBicicletas = Button(frame, text='Mostrar Bicicletas Flotantes', font=("Roboto", 12, "bold"), 
                       bg="#1F71A9", fg="white", width=22, command=self.pintar_flotantes)
    self.buttonBicicletas.place(relx=0.8, rely=0.25)

        
def pintar_estaciones_v2(self):
    self.imagenEstacionesFijas = utilImagenes.leer_imagen("./imagenes/green_marker.ico", (15,20))
    for id in self.estaciones:
        self.labelMap.set_marker(self.estaciones[id]['coordinates'][1], self.estaciones[id]['coordinates'][0], 
                                 icon=self.imagenEstacionesFijas)




