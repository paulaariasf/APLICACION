from tkinter import *
from tkinter import font
import util.utilVentana as utilVentana
import util.utilImagenes as utilImagenes
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_LATERAL
from formularios.formInicio import FormInicioDesign


class FormularioGeneral(Tk):

    def __init__(self):
        super().__init__()
        #self.logo=utilImagenes.leer_imagen("C:/Users/paula/OneDrive/Escritorio/5CARRERA/TFG/INFORMATICA/APLICACION/imagenes/logo_bicimad.png", (560, 136))
        self.logo = utilImagenes.leer_imagen("./imagenes/logo_bici_patinete_blanco.png", (75, 50))
        self.imagenPortada = utilImagenes.leer_imagen("./imagenes/fotoPortada.png", (260, 260))
        self.link_my_city = utilImagenes.leer_imagen("./imagenes/link_my_city.png", (170, 40))
        #self.imagenConstruccion = utilImagenes.leer_imagen("./imagenes/construccion.png", (270, 270))
        #self.imagenEstacionesFijas = utilImagenes.leer_imagen("./imagenes/estacion.png", (500, 250))
        #self.imagenBicicletaFlotante = utilImagenes.leer_imagen("./imagenes/bicicletaFlotante.png", (500, 300))
        self.config_window()
        self.paneles()
        self.mapa = None
        
    def config_window(self):
        #Configuracion inicial de la ventana
        self.title("Aplicación de Visualización de Transportes Compartidos")
        self.iconbitmap("./imagenes/bycicle_icon.ico")
        self.aplicacion_ancho=1200
        self.aplicacion_largo=600
        utilVentana.centrar_ventana(self, self.aplicacion_ancho, self.aplicacion_largo)

    def paneles(self):
        self.barraSuperior = Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barraSuperior.pack(side=TOP, fill="both")
        self.controlesBarraSuperior()
        
        self.menuLateral = Frame(self, bg=COLOR_MENU_LATERAL, width=200)
        #self.menuLateral.pack(side=LEFT, fill="both", expand=False)
        #self.controlesMenuLateral()

        self.cuerpoPrincipal = Frame(self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpoPrincipal.pack(side=RIGHT, fill="both", expand=True)
        self.controlesCuerpo()


    def controlesBarraSuperior(self):
        fontAwesome=font.Font(family="FontAwesome", size=15)

        #Boton de menu lateral
        self.buttonMenuLateral = Button(self.barraSuperior, text="\uf0c9", font=fontAwesome,
                                        command = self.togglePanel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.config(padx=10, pady=10)
        self.buttonMenuLateral.pack(side=LEFT)

        #Boton inicio
        labelTitulo = Label(self.barraSuperior, text="Aplicación de Transporte")
        labelTitulo.config(fg = "#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, width=25, borderwidth=0)
        labelTitulo.pack(side=LEFT)

        #Logo URJC
        labelLogoURJC = Label(self.barraSuperior, image=self.logo, bg=COLOR_BARRA_SUPERIOR)
        labelLogoURJC.pack(side=RIGHT)

        #Etiqueta de informacion
        labeltexto = Label(self.barraSuperior, image=self.link_my_city, bg=COLOR_BARRA_SUPERIOR)
        labeltexto.pack(side=RIGHT)       

    
    def togglePanel(self):
        #Alternar la visibilidad del panel lateral
        if self.menuLateral.winfo_ismapped():
            self.menuLateral.pack_forget()
        else:
            self.menuLateral.pack(side=LEFT, fill="y")      

    def controlesCuerpo(self):
        self.abrir_panel_inicio()

    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def abrir_panel_inicio(self):
        self.limpiar_panel(self.cuerpoPrincipal)
        self.inicio = FormInicioDesign(self.cuerpoPrincipal, self.imagenPortada, self.aplicacion_ancho, self.buttonMenuLateral, self.menuLateral)
        self.mapa = self.inicio.get_mapa()