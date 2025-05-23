from tkinter import *
from tkinter import font
import util.utilVentana as utilVentana
import util.utilImagenes as utilImagenes
from PIL import ImageTk, Image
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_LATERAL
from formularios.formConstruccion import FormConstruccionDesign
from formularios.formInicio import FormInicioDesign
from formularios.formMapa import FormMapaDesign
from formularios.formBicicletasFlotantes import FormBicicletasFlotantesDesign


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
        buttonTitulo = Button(self.barraSuperior, text="Aplicación de Transporte", command=self.abrir_panel_inicio)
        buttonTitulo.config(fg = "#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, width=25, borderwidth=0)
        buttonTitulo.pack(side=LEFT)

        #Logo URJC
        labelLogoURJC = Label(self.barraSuperior, image=self.logo, bg=COLOR_BARRA_SUPERIOR)
        labelLogoURJC.pack(side=RIGHT)

        #Etiqueta de informacion
        labeltexto = Label(self.barraSuperior, image=self.link_my_city, bg=COLOR_BARRA_SUPERIOR)
        labeltexto.pack(side=RIGHT)
        """
        labelInfo = Label(self.barraSuperior, text="Link My City")
        labelInfo.config(fg="#fff", font=("Roboto", 15, "bold"), bg=COLOR_BARRA_SUPERIOR, padx=10)
        labelInfo.pack(side=RIGHT)labelLogoURJC = Label(self.barraSuperior, image=self.logo, bg=COLOR_BARRA_SUPERIOR)
        labelLogoURJC.pack(side=RIGHT)"""
        

    
    def togglePanel(self):
        #Alternar la visibilidad del panel lateral
        if self.menuLateral.winfo_ismapped():
            self.menuLateral.pack_forget()
        else:
            self.menuLateral.pack(side=LEFT, fill="y")

    """def controlesMenuLateral(self):
        fontAwesome=font.Font(family="FontAwesome", size=15)

        #Botones del menu lateral

        self.buttonTipoTransporte = Button(self.menuLateral, text="\uf3c5    Tipo de transporte", font=fontAwesome, command=self.abrir_panel_mapa)
        self.buttonTipoTransporte.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonTipoTransporte.pack(side=TOP)
        self.bindHoverEvents(self.buttonTipoTransporte)

        checkbox_fijas = BooleanVar()
        self.buttonEstacionesFijas = Checkbutton(self.menuLateral, text="\uf3c5    Estaciones fijas", font=font.Font(family="FontAwesome", size=10), 
                                                 variable=checkbox_fijas, anchor="e", command= lambda : self.boton_estacionesfijas(checkbox_fijas))
        self.buttonEstacionesFijas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonEstacionesFijas.pack(side=TOP)
        self.bindHoverEvents(self.buttonEstacionesFijas)

        checkbox_flotantes = BooleanVar()
        self.buttonBicicletasFlotantes = Checkbutton(self.menuLateral, text="\uf206    Bicicletas flotantes", font=font.Font(family="FontAwesome", size=10),
                                                     variable=checkbox_flotantes, anchor="e")
        self.buttonBicicletasFlotantes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonBicicletasFlotantes.pack(side=TOP)
        self.bindHoverEvents(self.buttonBicicletasFlotantes)

        self.buttonIntegracion = Button(self.menuLateral, text="\ue4bd    Integración", font=fontAwesome, command=self.abrir_panel_construccion)
        self.buttonIntegracion.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonIntegracion.pack(side=TOP)
        self.bindHoverEvents(self.buttonIntegracion)

        self.buttonDemanda = Button(self.menuLateral, text="\ue4b7    Demanda", font=fontAwesome, command=self.abrir_panel_construccion)
        self.buttonDemanda.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonDemanda.pack(side=TOP)
        self.bindHoverEvents(self.buttonDemanda)"""

    """def botones_desplegados(self):
        fontAwesome=font.Font(family="FontAwesome", size=15)

        self.buttonTipoTransporte = Button(self.menuLateral, text="   \uf3c5    Tipo de transporte", font=fontAwesome, command=self.abrir_panel_estaciones_fijas)
        self.buttonTipoTransporte.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonTipoTransporte.pack(side=TOP)
        self.bindHoverEvents(self.buttonTipoTransporte)

        self.buttonEstacionesFijas = Checkbutton(self.menuLateral, text="\uf3c5    Estaciones fijas", font=fontAwesome, command=self.abrir_panel_mapa)
        self.buttonEstacionesFijas.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonEstacionesFijas.pack(side=TOP)
        self.bindHoverEvents(self.buttonEstacionesFijas)

        self.buttonBicicletasFlotantes = Checkbutton(self.menuLateral, text="\uf206    Bicicletas flotantes", font=fontAwesome, command=self.abrir_panel_bicicletas_flotantes)
        self.buttonBicicletasFlotantes.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonBicicletasFlotantes.pack(side=TOP)
        self.bindHoverEvents(self.buttonBicicletasFlotantes)

        self.buttonIntegracion = Button(self.menuLateral, text="   \ue4bd    Integración", font=fontAwesome, command=self.abrir_panel_construccion)
        self.buttonIntegracion.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonIntegracion.pack(side=TOP)
        self.bindHoverEvents(self.buttonIntegracion)

        self.buttonDemanda = Button(self.menuLateral, text="   \ue4b7    Demanda", font=fontAwesome, command=self.abrir_panel_construccion)
        self.buttonDemanda.config(bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=20, height=2)
        self.buttonDemanda.pack(side=TOP)
        self.bindHoverEvents(self.buttonDemanda)
        """
        
    """def bindHoverEvents(self, button):
        #Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        #Cambiar el estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg="white")
        
    def on_leave(self, event, button):
        #Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg="white")"""

    
    def controlesCuerpo(self):
        self.abrir_panel_inicio()


    """def abrir_panel_construccion(self):
        self.limpiar_panel(self.cuerpoPrincipal)
        FormConstruccionDesign(self.cuerpoPrincipal, self.imagenConstruccion)"""


    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def abrir_panel_inicio(self):
        self.limpiar_panel(self.cuerpoPrincipal)
        self.inicio = FormInicioDesign(self.cuerpoPrincipal, self.imagenPortada, self.aplicacion_ancho, self.buttonMenuLateral, self.menuLateral)
        self.mapa = self.inicio.get_mapa()

    """def abrir_panel_mapa(self):
        self.limpiar_panel(self.cuerpoPrincipal)
        self.mapa = FormMapaDesign(self.cuerpoPrincipal, self.menuLateral)

    def abrir_panel_bicicletas_flotantes(self):
        self.limpiar_panel(self.cuerpoPrincipal)
        FormBicicletasFlotantesDesign(self.cuerpoPrincipal)

    def boton_estacionesfijas(self,checkbox_fijas):
        if checkbox_fijas.get() == True:
            self.mapa.pintar_estaciones()
        elif checkbox_fijas.get() == False:
            self.mapa.borrar_estaciones()"""