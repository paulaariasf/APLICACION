from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL, COLOR_BARRA_SUPERIOR
import util.utilEstaciones as utilEstaciones
import tkintermapview
import tkinter as tk

class FormBicicletasFlotantesDesign():

    def __init__(self, panel_principal):
        self.barra_superior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_superior.pack(side=TOP, fill=X, expand=False)

        self.barra_inferior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_inferior.pack(side=TOP, fill="both", expand=True)

        self.labelTitulo=Label(self.barra_superior, text="Bicicletas flotantes")
        self.labelTitulo.config(fg="#1F71A9", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=20)
        self.labelTitulo.pack(side=TOP, fill = "both", expand=True)

        """self.labelInfo = tk.Label(self.barra_superior, text="", font=("Arial", 14))
        self.labelInfo.config(fg="#1F71A9", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=20)
        self.labelInfo.pack(padx=200, fill=Y, expand=True)"""

        self.labelMap=tkintermapview.TkinterMapView(self.barra_inferior, width=900, height=700, corner_radius=0)
        self.labelMap.pack(fill="both")
        self.labelMap.config(bg=COLOR_CUERPO_PRINCIPAL)

        self.labelMap.set_position(40.4168, -3.7038)
        self.labelMap.set_zoom(12)

        self.labelMap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal

        estaciones = utilEstaciones.devolver_estaciones()
        radio = 0.005 #es un valor definido, posteriormente se parametrizará
        df_flotantes = utilEstaciones.generar_flotantes_v2(estaciones, radio)


        for i in range(len(df_flotantes['id'])):
            self.labelMap.set_polygon(df_flotantes['coord'][i],
                                    outline_color="blue",
                                    border_width=0,
                                    name=df_flotantes['info'][i])
            
        self.labelMap.add_right_click_menu_command(label="Right Click",
                                                command=None,
                                                pass_coords=True)
            
"""def click_event(coords):
     self.labelMap.config(text=f"Has hecho clic en el polígono: {polygon_name}")"""