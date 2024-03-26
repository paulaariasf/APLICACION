from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL
import util.utilImagenes as utilImagenes

class FormInicioDesign():

    def __init__(self, panel_principal, logo, aplicacion_ancho):

        #Frames
        barraSuperior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL, height=60)
        barraSuperior.pack(side=TOP, fill=X, expand=False)

        frame_izq = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL, height=800, width=400)
        frame_izq.pack(side="left", fill="y", expand=True)

        frame_dch = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL, height=800, width=400)
        frame_dch.pack(side="right", fill="y", expand=True)

        #Titulo
        labelTitulo = Label(barraSuperior, text="Visualización de datos de sistemas de transporte compartidos")
        labelTitulo.config(fg="#1F71A9", font=("Roboto", 24, "bold"), bg=COLOR_CUERPO_PRINCIPAL, padx=10)
        x_titulo=(aplicacion_ancho - labelTitulo.winfo_reqwidth())/2
        labelTitulo.place(x=x_titulo, y=20)

        #Texto principal
        labelTexto=Label(frame_izq, anchor="w", text="Bienvenido a la aplicación de transporte \n compartido. En esta aplicación podrá apreciar \n mediante distintos mapas de calor el exceso o \n falta   de   diferentes   medios   de   transporte:\n ● Estaciones fijas\n ● Bicicletas flotantes\n ● Combinación de ambas\n ● Demanda de estos recursos")
        labelTexto.config(fg="#1F71A9", font=("Roboto", 18), bg=COLOR_CUERPO_PRINCIPAL, padx=10, anchor="w")
        labelTexto.pack(side="left", fill="y", expand=True)

        #Imagen portada
        labelPortada = Label(frame_dch, image=logo, bg=COLOR_CUERPO_PRINCIPAL)
        labelPortada.place(x=0, y=0, relwidth=1, relheight=1)