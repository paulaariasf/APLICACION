from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL, COLOR_BARRA_SUPERIOR
import util.utilEstaciones as utilEstaciones
import tkintermapview


class FormEstacionesFijasDesign():

    def __init__(self, panel_principal):

        self.frame_general = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_general.pack(fill="both")

        anadir_mapa(self, self.frame_general)

        # Definir el numero de filas y columnas
        n = 10

        self.estaciones = utilEstaciones.devolver_estaciones()
        self.maxLon, self.minLon, self.maxLat, self.minLat = utilEstaciones.limites(self.estaciones)

        self.lon_celda = (self.maxLon - self.minLon) / n
        self.lat_celda = (self.maxLat - self.minLat) / n

        self.diccionario = utilEstaciones.crear_dicCoord(self.estaciones, n, self.minLon, self.minLat, self.maxLat, self.lon_celda, self.lat_celda)

        
        #creacion_paneles_info(self, panel_principal)
        pintar_estaciones(self)
        pintar_mapa_calor(self, n)

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

    self.labelMap.set_position(40.4168, -3.7038)
    self.labelMap.set_zoom(12)

    self.labelMap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal


def pintar_mapa_calor(self,n):
    for i in range(pow(n, 2)):
        self.labelMap.set_polygon(self.diccionario['coordenadas'][i],
                                fill_color=utilEstaciones.get_color(self.diccionario['cantidades'][i], 0, max(self.diccionario['cantidades'])),
                                outline_color=None,
                                name=f'Zona {self.diccionario['ids'][i]}')

    self.labelMap.add_right_click_menu_command(label="Right Click",
                                    command=click_event,
                                    pass_coords=True)

def pintar_estaciones(self):
    for id in self.estaciones:
        self.labelMap.set_polygon([tuple(self.estaciones[id]['coordinates'][::-1])],
                                outline_color="blue",
                                border_width=1,
                                name=self.estaciones[id]['name'])

def click_event(coords):
    print(f"Ha pulsado en las coordenadas: {coords}")
