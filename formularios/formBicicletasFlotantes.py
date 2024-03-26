from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL, COLOR_BARRA_SUPERIOR
from tkhtmlview import HTMLLabel
import folium

import json
import pandas as pd
import plotly.express as px

from PIL import ImageTk
import io


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
        
        self.boton = Button(self.barra_boton, text="Cargar  mapa de calor", font=("Roboto", 10, "bold"), command=self.cargar_mapa)
        self.boton.config(padx=10, pady=10, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.boton.pack()


    def cargar_mapa(self):
            madrid = json.load(open("C:/Users/paula/OneDrive/Escritorio/5CARRERA/TFG/PRUEBAS/madrid-districts.geojson", 'r'))

            id_map = {}
            for feature in madrid['features']:
                feature['id'] = feature['properties']['cartodb_id']
                id_map[feature['properties']['name']] = feature['id']

            df = pd.read_excel("C:/Users/paula/OneDrive/Escritorio/5CARRERA/TFG/PRUEBAS/bicis_barrios.xlsx")


            fig = px.choropleth(df, 
                                locations='id', 
                                geojson=madrid, 
                                color='cantidad', 
                                hover_name='name')
            fig.update_geos(fitbounds="locations", visible=False)

            fig.show()