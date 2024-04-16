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
        maxLon, minLon, maxLat, minLat = utilEstaciones.limites(estaciones)

        # Definir el numero de filas y columnas
        n = 10

        # Calcular el ancho y alto de cada celda de la cuadrícula
        lon_celda = (maxLon - minLon) / n
        lat_celda = (maxLat - minLat) / n

        geo_json, df = utilEstaciones.crear_geojson_df(estaciones, n, minLon, minLat, lon_celda, lat_celda)

        df = utilEstaciones.crear_df_estaciones(estaciones)
        
        self.boton = Button(self.barra_boton, text="Cargar  mapa de calor", 
                            font=("Roboto", 10, "bold"), command= lambda: self.cargar_mapa(geo_json, df))
        self.boton.config(padx=10, pady=10, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.boton.pack()


    def cargar_mapa(self, geo_json, df):
        ruta_archivo = "cuadricula.geojson"
        with open(ruta_archivo, "w") as archivo:
            geojson.dump(geo_json, archivo)

        with open(ruta_archivo, "r") as archivo:
            geojson_objeto = geojson.load(archivo)


        fig = px.scatter_mapbox(df,
                                lat='lat',
                                lon='lon',
                                mapbox_style='carto-positron',
                                color='bike_bases',
                                size='bike_bases')
        fig.update_geos(fitbounds="locations", visible=False)

        # Guardar el gráfico como archivo HTML
        html_file = "scatter_mapbox.html"
        fig.write_html(html_file)

        fig.show()