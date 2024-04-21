from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL, COLOR_BARRA_SUPERIOR
import geojson
import pandas as pd
import plotly.express as px
import util.utilEstaciones as utilEstaciones


class FormBicicletasFlotantesDesign():

    def __init__(self, panel_principal, imagen):
        self.barra_superior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_superior.pack(side=TOP, fill=X, expand=False)

        self.barra_inferior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_inferior.pack(side=TOP, fill="both", expand=True)

        self.barra_boton = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_boton.pack(side=TOP, fill="both", expand=True)

        self.labelTitulo=Label(self.barra_superior, text="Bicicletas flotantes")
        self.labelTitulo.config(fg="#1F71A9", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=20)
        self.labelTitulo.pack(side=TOP, fill = "both", expand=True)

        self.labelImage=Label(self.barra_inferior, image=imagen)
        self.labelImage.pack(pady=50)
        self.labelImage.config(bg=COLOR_CUERPO_PRINCIPAL)

        estaciones = utilEstaciones.devolver_estaciones()

        estaciones = utilEstaciones.devolver_estaciones()
        radio = 0.005 #es un valor definido, posteriormente se parametrizará

        self.boton = Button(self.barra_boton, text="Cargar  mapa de calor", 
                            font=("Roboto", 10, "bold"), command= lambda: self.cargar_mapa(estaciones, radio))
        self.boton.config(padx=10, pady=10, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.boton.pack()


    def cargar_mapa(self, estaciones, radio):
        df_flotantes = utilEstaciones.generar_flotantes(estaciones, radio)
        mapbox_token = "pk.eyJ1IjoicGF1bGFhcmlhc2YiLCJhIjoiY2x2MWViNTZpMDUzNDJpcnl5YTQ0ZnlhMSJ9.VCTWeNlVpK5UcVMpxeAhkQ"
        fig = px.scatter_mapbox(df_flotantes, 
                        lat='lat', 
                        lon='lon',
                        zoom=11,
                        mapbox_style="carto-positron")
        fig.update_layout(mapbox_accesstoken=mapbox_token)
        fig.show()