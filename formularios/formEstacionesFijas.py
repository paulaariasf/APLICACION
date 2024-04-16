from tkinter import *
from tkinter import ttk
from config import COLOR_CUERPO_PRINCIPAL, COLOR_BARRA_SUPERIOR
import util.utilEstaciones as utilEstaciones
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import geojson
import plotly.express as px
import numpy as np


class FormEstacionesFijasDesign():

    def __init__(self, panel_principal, imagen):
        self.barra_superior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_superior.pack(side=TOP, fill=X, expand=False)

        self.barra_inferior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_inferior.pack(side=TOP, fill="both", expand=True)

        self.barra_boton = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_boton.pack(side=TOP, fill="both", expand=True)

        self.labelTitulo=Label(self.barra_superior, text="Estaciones fijas")
        self.labelTitulo.config(fg="#1F71A9", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=20)
        self.labelTitulo.pack(side=TOP, fill = "both", expand=True)

        self.labelImage=Label(self.barra_inferior, image=imagen)
        self.labelImage.pack(pady=50)
        self.labelImage.config(bg=COLOR_CUERPO_PRINCIPAL)
        
        estaciones = utilEstaciones.devolver_estaciones()
        maxLon, minLon, maxLat, minLat = utilEstaciones.limites(estaciones)

        # Definir el numero de filas y columnas
        n = 50

        # Calcular el ancho y alto de cada celda de la cuadrícula
        lon_celda = (maxLon - minLon) / n
        lat_celda = (maxLat - minLat) / n

        geo_json, df_cuad = utilEstaciones.crear_geojson_df(estaciones, n, minLon, minLat, lon_celda, lat_celda)
        df_points = utilEstaciones.crear_df_estaciones(estaciones)
        
        """cantidadMin = min(estaciones[id]['bike_bases'] for id in estaciones)
        cantidadMax = max(estaciones[id]['bike_bases'] for id in estaciones)

        minZona = min(df.values.flatten())
        maxZona = max(df.values.flatten())

        print("maxLon: " + str(maxLon) + "; minLon: " + str(minLon) + "; maxLat: " + str(maxLat) + "; minLat: " + str(minLat))
        print("Numero de celdas: " + str(n) + " lon_celda: " + str(lon_celda) + "; lat_celda: " + str(lat_celda))
        print(df)
        print("cantidadMin: " + str(cantidadMin), " cantidadMax: " + str(cantidadMax))
        print("minZona: " + str(minZona), " maxZona: " + str(maxZona))"""

        self.boton = Button(self.barra_boton, text="Cargar  mapa de calor", 
                            font=("Roboto", 10, "bold"), command= lambda: self.cargar_mapa(geo_json, df_cuad, df_points))
        self.boton.config(padx=10, pady=10, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.boton.pack()



        
    def cargar_mapa(self, geo_json, df_cuad, df_points):
        ruta_archivo = "cuadricula.geojson"
        with open(ruta_archivo, "w") as archivo:
            geojson.dump(geo_json, archivo)

        with open(ruta_archivo, "r") as archivo:
            geojson_objeto = geojson.load(archivo)

        """fig = px.choropleth(df, 
                            locations='id', 
                            geojson=geojson_objeto, 
                            color='cantidad', 
                            hover_name='name',
                            color_continuous_scale='rdylgn')
        fig.update_geos(fitbounds="locations", visible=False)"""

        colorscale = [
            (0, 'rgba(0, 0, 0, 0)'),  # Transparente para el valor 0
            (0.01, 'rgb(255, 0, 0)'),  # Rojo
            (0.2, 'rgb(255, 85, 0)'),
            (0.3, 'rgb(255, 170, 0)'),
            (0.4, 'rgb(255, 255, 0)'),  # Amarillo
            (0.5, 'rgb(170, 255, 0)'),
            (0.6, 'rgb(85, 255, 0)'),
            (0.7, 'rgb(0, 255, 0)'),  # Verde claro
            (0.8, 'rgb(0, 170, 0)'),
            (0.9, 'rgb(0, 85, 0)'),
            (1, 'rgb(0, 50, 0)')  # Verde
        ]

        mapbox_token = "pk.eyJ1IjoicGF1bGFhcmlhc2YiLCJhIjoiY2x2MWViNTZpMDUzNDJpcnl5YTQ0ZnlhMSJ9.VCTWeNlVpK5UcVMpxeAhkQ"
        
        fig = px.choropleth_mapbox(df_cuad, 
                           geojson=geo_json, 
                           locations='id', 
                           color='cantidad',
                           color_continuous_scale=colorscale,
                           hover_name='name',
                           mapbox_style="carto-positron",
                           zoom=11, 
                           center={"lat": 40.4168, "lon": -3.7038},
                           opacity=0.5
                          )
        fig.update_traces(marker_line_width = 0)
        fig.update_layout(mapbox_accesstoken=mapbox_token)

        fig.add_scattermapbox(
            lat=df_points['lat'],
            lon=df_points['lon'],
            mode='markers',
            marker=dict(
                size=6,
                color='grey',
                opacity=1
            ),
            hovertext=df_points['info'],
            hoverinfo='text'
        )

        fig.show()
        