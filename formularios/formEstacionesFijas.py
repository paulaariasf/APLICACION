from tkinter import *
from tkinter import ttk
from config import COLOR_CUERPO_PRINCIPAL, COLOR_BARRA_SUPERIOR
import util.utilEstaciones as utilEstaciones
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image, ImageTk



class FormEstacionesFijasDesign():

    def __init__(self, panel_principal, imagen):
        self.barra_superior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_superior.pack(side=TOP, fill=X, expand=False)

        self.barra_inferior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.barra_inferior.pack(side=TOP, fill="both", expand=True)

        self.labelTitulo=Label(self.barra_superior, text="Estaciones fijas")
        self.labelTitulo.config(fg="#1F71A9", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=20)
        self.labelTitulo.pack(side=TOP, fill = "both", expand=True)

        #self.labelImage=Label(self.barra_inferior, image=imagen)
        #self.labelImage.pack(pady=50)
        #self.labelImage.config(bg=COLOR_CUERPO_PRINCIPAL)

        
        estaciones = utilEstaciones.devolver_estaciones()
        maxLon, minLon, maxLat, minLat = utilEstaciones.limites(estaciones)

        # Definir el numero de filas y columnas
        n = 25

        # Calcular el ancho y alto de cada celda de la cuadrícula
        lon_celda = (maxLon - minLon) / n
        lat_celda = (maxLat - minLat) / n

        df = utilEstaciones.crear_dataframe(estaciones, n, minLon, minLat, lon_celda, lat_celda)

        cantidadMin = min(estaciones[id]['bike_bases'] for id in estaciones)
        cantidadMax = max(estaciones[id]['bike_bases'] for id in estaciones)

        minZona = min(df.values.flatten())
        maxZona = max(df.values.flatten())

        print("maxLon: " + str(maxLon) + "; minLon: " + str(minLon) + "; maxLat: " + str(maxLat) + "; minLat: " + str(minLat))
        print("Numero de celdas: " + str(n) + " lon_celda: " + str(lon_celda) + "; lat_celda: " + str(lat_celda))
        print(df)
        print("cantidadMin: " + str(cantidadMin), " cantidadMax: " + str(cantidadMax))
        print("minZona: " + str(minZona), " maxZona: " + str(maxZona))


        # Crear un mapa de calor con Seaborn

        cmap_custom = sns.color_palette("RdYlGn", as_cmap=True)
        cmap_custom.set_bad(color='white')

        plt.figure(figsize=(6, 4))
        heatmap = sns.heatmap(df, cmap=cmap_custom, vmin=minZona, vmax=maxZona, mask=(df == 0))

        # Guardar el mapa de calor como una imagen PNG
        plt.savefig("heatmap.png", bbox_inches='tight')

        # Cargar la imagen del mapa de calor
        heatmap_img = Image.open("heatmap.png")
        heatmap_img = heatmap_img.resize((800, 500), Image.ANTIALIAS)  # Ajustar tamaño de la imagen

        # Convertir la imagen a formato Tkinter
        heatmap_tk = ImageTk.PhotoImage(heatmap_img)

        # Mostrar la imagen en el frame de Tkinter
        label = ttk.Label(self.barra_inferior, image=heatmap_tk)
        label.image = heatmap_tk
        label.pack()