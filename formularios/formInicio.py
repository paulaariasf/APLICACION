from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL
import util.utilImagenes as utilImagenes
from formularios.formMapa import FormMapaDesign

class FormInicioDesign():

    def __init__(self, panel_principal, imagen, aplicacion_ancho, buttonMenuLateral, menuLateral):
        self.mapa = None
        # Cargar imágenes
        self.logo = utilImagenes.leer_imagen("./imagenes/logo.PNG", (400, 400))

        # Frames
        barraSuperior = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL, height=60)
        barraSuperior.pack(side=TOP, fill=X)

        frame_central = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        frame_central.pack(side=TOP, fill=X, pady=0)

        frame_izq = Frame(frame_central, bg=COLOR_CUERPO_PRINCIPAL)
        frame_izq.pack(side="left", fill="both",  padx=20)

        frame_dch = Frame(frame_central, bg=COLOR_CUERPO_PRINCIPAL)
        frame_dch.pack(side="right", fill="both", expand=True, padx=5)

        frame_boton = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        frame_boton.pack(side=TOP, fill=X)

        # Título
        labelTitulo = Label(barraSuperior, text="Bienvenido a LinkMyCity", 
                            fg="#0057A0", font=("Segoe UI", 30, "bold"), bg=COLOR_CUERPO_PRINCIPAL)
        labelTitulo.pack(side="top", pady=10)

        # Texto principal
        texto_bienvenida = (
            "Bienvenido a la aplicación de transporte compartido.\n\n"
            "En esta aplicación podrá realizar un análisis visual\n"
            "de transportes compartidos en la ciudad de Madrid:\n\n"
            "   • Estaciones fijas\n"
            "   • Bicicletas flotantes\n"
            "   • Patinetes flotantes\n"
            "Podrá visualizar los transportes sobre el mapa de la ciudad,\n"
            "generar mapas de calor interactivos y configurables e incluso\n"
            "observar la relación entre oferta y demanda en la ciudad.\n\n"
            "Pulse el botón de abajo para acceder al mapa interactivo."
        )

        labelTexto = Label(frame_izq, text=texto_bienvenida, anchor="w", justify="left",
                        fg="#1F71A9", font=("Segoe UI", 16), bg=COLOR_CUERPO_PRINCIPAL)
        labelTexto.pack(fill="both", expand=True)

        # Imagen principal en el frame derecho
        labelPortada = Label(frame_dch, image=self.logo, bg=COLOR_CUERPO_PRINCIPAL)
        labelPortada.pack(expand=True)

        # Función botón
        def abrir_pagina_principal():
            for widget in panel_principal.winfo_children():
                widget.destroy()
            buttonMenuLateral.invoke()
            self.mapa = FormMapaDesign(panel_principal, menuLateral)

        # Botón de inicio
        boton = Button(frame_boton, text="Pulse para iniciar", font=("Roboto", 16), 
                    bg="#1F71A9", fg="white", width=20, command=abrir_pagina_principal)
        boton.pack(pady=10)

    def get_mapa(self):
        return self.mapa
