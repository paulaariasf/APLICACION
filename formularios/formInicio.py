from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL
import util.utilImagenes as utilImagenes
from formularios.formMapa import FormMapaDesign

class FormInicioDesign():

    def __init__(self, panel_principal, logo, aplicacion_ancho):

        #Frames
        barraSuperior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL, height=50)
        barraSuperior.pack(side=TOP, fill=X, expand=True, pady=0)

        frame_central = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        frame_central.pack(side=TOP, fill="both", expand=True, pady=0)

        frame_izq = Frame(frame_central, bg=COLOR_CUERPO_PRINCIPAL)
        frame_izq.pack(side="left", fill="both", expand=True, padx=10, pady=0)

        frame_dch = Frame(frame_central, bg=COLOR_CUERPO_PRINCIPAL)
        frame_dch.pack(side="right", fill="both", expand=True, padx=10, pady=0)

        frame_boton = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        frame_boton.pack(side=TOP, fill=X)

        #Titulo
        labelTitulo = Label(barraSuperior, text="Visualización de datos de sistemas de transporte compartidos")
        labelTitulo.config(fg="#1F71A9", font=("Roboto", 24, "bold"), bg=COLOR_CUERPO_PRINCIPAL, padx=10)
        x_titulo=(aplicacion_ancho - labelTitulo.winfo_reqwidth())/2
        labelTitulo.place(x=x_titulo, y=0)

        #Texto principal
        labelTexto=Label(frame_izq, anchor="w", text="Bienvenido a la aplicación de transporte \n compartido. En esta aplicación podrá apreciar \n mediante distintos mapas de calor el exceso o \n falta   de   diferentes   medios   de   transporte:\n ● Estaciones fijas\n ● Bicicletas flotantes\n ● Combinación de ambas\n ● Demanda de estos recursos\n En el botón de abajo podrá abrir el mapa donde \nse podrán visualizar los diferentes medios de transporte")
        labelTexto.config(fg="#1F71A9", font=("Roboto", 18), bg=COLOR_CUERPO_PRINCIPAL, padx=10, anchor="w")
        labelTexto.pack(side="left", fill="y", expand=False)

        #Imagen portada
        labelPortada = Label(frame_dch, image=logo, bg=COLOR_CUERPO_PRINCIPAL)
        labelPortada.place(x=0, y=0, relwidth=1, relheight=1)

        def abrir_pagina_principal():
            for widget in panel_principal.winfo_children():
                widget.destroy()
            FormMapaDesign(panel_principal)

        # Creación del botón
        boton = Button(frame_boton, text="Pulse para iniciar", font=("Roboto", 16), 
                       bg="#1F71A9", fg="white", width=20, command=abrir_pagina_principal)
        boton.pack(pady=10)
