from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL, COLOR_BARRA_SUPERIOR
import util.utilEstaciones as utilEstaciones
import tkintermapview


class FormEstacionesFijasDesign_v2():

    def __init__(self, panel_principal):
        self.barra_superior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_superior.pack(side=TOP, fill=X, expand=False)

        self.barra_inferior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_inferior.pack(side=TOP, fill="both", expand=True)

        self.labelTitulo=Label(self.barra_superior, text="Estaciones fijas")
        self.labelTitulo.config(fg="#1F71A9", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=20)
        self.labelTitulo.pack(side=TOP, fill = "both", expand=True)

        self.labelMap=tkintermapview.TkinterMapView(self.barra_inferior, width=900, height=700, corner_radius=0)
        self.labelMap.pack(pady=5, fill=X)
        self.labelMap.config(bg=COLOR_CUERPO_PRINCIPAL)

        self.labelMap.set_position(40.4168, -3.7038)
        self.labelMap.set_zoom(12)

        #self.labelMap.set_tile_server("http://tile.stamen.com/toner-lite/{z}/{x}/{y}.png", max_zoom=22)
        
        estaciones = utilEstaciones.devolver_estaciones()
        maxLon, minLon, maxLat, minLat = utilEstaciones.limites(estaciones)

        # Definir el numero de filas y columnas
        n = 50

        lon_celda = (maxLon - minLon) / n
        lat_celda = (maxLat - minLat) / n

        diccionario = utilEstaciones.crear_dicCoord(estaciones, n, minLon, minLat, maxLat, lon_celda, lat_celda)
        
        #Pintar el mapa de calor
        for i in range(pow(n, 2)):
            self.labelMap.set_polygon(diccionario['coordenadas'][i],
                                    fill_color=utilEstaciones.get_color(diccionario['cantidades'][i], 0, max(diccionario['cantidades'])),
                                    outline_color=None,
                                    name=f'Zona {diccionario['ids'][i]}')

        self.labelMap.add_right_click_menu_command(label="Right Click",
                                        command=click_event,
                                        pass_coords=True)
        
        #Pintar las estaciones
        for id in estaciones:
            self.labelMap.set_polygon([tuple(estaciones[id]['coordinates'][::-1])],
                                    outline_color="blue",
                                    border_width=1,
                                    name=estaciones[id]['name'])
            
def click_event(coords):
    print(f"Ha pulsado en las coordenadas: {coords}")