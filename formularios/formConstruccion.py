from tkinter import *
from config import COLOR_CUERPO_PRINCIPAL
import util.utilImagenes as utilImagenes

class FormConstruccionDesign():

    def __init__(self, panel_principal, logo):

        self.barra_superior = Frame(panel_principal)
        self.barra_superior.pack(side=TOP, fill=X, expand=False)

        self.barra_inferior = Frame(panel_principal)
        self.barra_inferior.pack(side=TOP, fill="both", expand=True)

        self.labelTitulo=Label(self.barra_superior, text="Página en construcción")
        self.labelTitulo.config(fg="#1F71A9", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL, pady=20)
        self.labelTitulo.pack(side=TOP, fill = "both", expand=True)

        self.labelImage=Label(self.barra_inferior, image=logo)
        self.labelImage.place(x=0, y=0, relwidth=1, relheight=1)
        self.labelImage.config(fg="#fff", font=("Roboto", 10), bg=COLOR_CUERPO_PRINCIPAL)