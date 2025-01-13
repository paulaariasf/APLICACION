
import util.utilEstaciones as utilEstaciones 
from tkinter import *
import numpy as np

def close_infozona(form_mapa):
    if form_mapa.pol_seleccion is not None:
        form_mapa.pol_seleccion.delete()
    if hasattr(form_mapa, 'infozona_frame'):
        form_mapa.infozona_frame.destroy()

def show_info_zona(form_mapa, coords):
    close_infozona(form_mapa)

    form_mapa.infozona_frame = Frame(form_mapa.panel_principal, bg="white", borderwidth=1, relief="solid")
    form_mapa.infozona_frame.place(x=825, y=475)
    
    zona = utilEstaciones.clasificar_punto(form_mapa.n, (coords[0], coords[1]), form_mapa.lon_celda, form_mapa.lat_celda, form_mapa.minLon, form_mapa.maxLat)

    if form_mapa.clasificacion == "General" and form_mapa.influencia =='con':
        texto=f"Zona seleccionada: {zona} de {form_mapa.n**2}\n"
        if form_mapa.checkbox_mapa_estaciones.get():
            texto+=f"Número de estaciones:{form_mapa.dic_mapa_calor['num_estaciones'][zona-1]}\n"
            texto+=f"Cantidad bicicletas estaciones: {form_mapa.dic_mapa_calor['cantidades_estaciones'][zona-1]}\n"
        if form_mapa.checkbox_mapa_flotantes.get():
            texto+=f"Número de bicicletas flotantes:{form_mapa.dic_mapa_calor['cantidades_flotantes'][zona-1]}\n"
        if form_mapa.checkbox_mapa_patinetes.get():
            texto+=f"Número de patinetes:{form_mapa.dic_mapa_calor['cantidades_patinetes'][zona-1]}\n"
        texto+=f"Cobertura Relativa: {form_mapa.dic_mapa_calor['cantidades_suavizadas'][zona-1]*100/np.max(form_mapa.dic_mapa_calor['cantidades_suavizadas']):.2f}%\n"
        texto+=f"Valor de mapa de calor: {form_mapa.dic_mapa_calor['cantidades_suavizadas'][zona-1]:.2f}"

    elif form_mapa.clasificacion == "General" and form_mapa.influencia =='sin':
        texto=f"Zona seleccionada: {zona} de {form_mapa.n**2}\n"
        if form_mapa.checkbox_mapa_estaciones.get():
            texto+=f"Número de estaciones:{form_mapa.dic_mapa_calor['num_estaciones'][zona-1]}\n"
            texto+=f"Cantidad bicicletas estaciones: {form_mapa.dic_mapa_calor['cantidades_estaciones'][zona-1]}\n"
        if form_mapa.checkbox_mapa_flotantes.get():
            texto+=f"Número de bicicletas flotantes:{form_mapa.dic_mapa_calor['cantidades_flotantes'][zona-1]}\n"
        if form_mapa.checkbox_mapa_patinetes.get():
            texto+=f"Número de patinetes:{form_mapa.dic_mapa_calor['cantidades_patinetes'][zona-1]}\n"
        texto+=f"Cobertura Relativa: {form_mapa.dic_mapa_calor['cantidades'][zona-1]*100/np.max(form_mapa.dic_mapa_calor['cantidades']):.2f}%\n"
        texto+=f"Valor de mapa de calor: {form_mapa.dic_mapa_calor['cantidades'][zona-1]:.2f}"

    elif form_mapa.clasificacion == "Llenado":
        if form_mapa.dic_mapa_calor['capacidades'] != 0:
            texto=f"Zona seleccionada: {zona} de {form_mapa.n**2}\nNúmero de estaciones:{form_mapa.dic_mapa_calor['num_estaciones'][zona-1]}\nCantidad de bicicletas: {form_mapa.dic_mapa_calor['cantidades'][zona-1]} de {form_mapa.dic_mapa_calor['capacidades'][zona-1]}: {(100*(form_mapa.dic_mapa_calor['cantidades'][zona-1]/form_mapa.dic_mapa_calor['capacidades'][zona-1])):.2f}%"
    
    elif form_mapa.clasificacion == "Huecos":
        texto=f"Zona seleccionada: {zona} de {form_mapa.n**2}\nNúmero de huecos libres:{form_mapa.dic_mapa_calor['cantidades'][zona-1]} de {form_mapa.dic_mapa_calor['capacidades'][zona-1]}"
    
    info_label = Label(form_mapa.infozona_frame, text=texto, bg="white")
    info_label.pack(side="left", padx=5, pady=5)

    #Resaltar zona seleccionada
    form_mapa.pol_seleccion =form_mapa.labelMap.set_polygon(form_mapa.dic_mapa_calor['coordenadas'][zona-1],
                                fill_color="#1F71A9",
                                outline_color="#1F71A9",
                                border_width=3)

    close_button = Button(form_mapa.infozona_frame, text="x", command=lambda: close_infozona(form_mapa), bg="white", fg="red", borderwidth=0)
    close_button.pack(side="right", padx=5, pady=5)


def close_infoest(form_mapa):
    if form_mapa.est_seleccion is not None:
        form_mapa.est_seleccion.delete()
    if hasattr(form_mapa, 'infoest_frame'):
        form_mapa.infoest_frame.destroy()

def dividir_string_por_longitud(texto, longitud_max_linea=25):
    # Verificar si el string es mayor que 35
    if len(texto) > 35:
        palabras = texto.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            # Si cabe en la linea la agrego
            if len(linea_actual) + len(palabra) + 1 <= longitud_max_linea:
                if linea_actual:
                    linea_actual += " "
                linea_actual += palabra
            else:
                # Si no cabe, paso a otra linea
                lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)
        return "\n".join(lineas)
    else:
        # Si no es mayor que 35, devolver el string original
        return texto

def show_info_estacion(form_mapa, polygon):
    close_infoest(form_mapa)

    form_mapa.infoest_frame = Frame(form_mapa.panel_principal, bg="white", borderwidth=1, relief="solid")
    form_mapa.infoest_frame.place(x=850, y=400)

    id, coord_estacion = polygon.name
    texto_mostrar = dividir_string_por_longitud(form_mapa.estaciones[id]['name'], longitud_max_linea=25)
    info_label = Label(form_mapa.infoest_frame, text=f"Estación seleccionada:\n{texto_mostrar} \n Cantidad de bicicletas: {form_mapa.estaciones[id]['bike_bases']} \n Capacidad total: {form_mapa.estaciones[id]['bike_bases'] + form_mapa.estaciones[id]['free_bases']}", bg="white")
    info_label.pack(side="left", padx=5, pady=5)

    #Añadir marcador en la estacion seleccionada
    form_mapa.est_seleccion = form_mapa.labelMap.set_marker(coord_estacion[0], coord_estacion[1])
    close_button = Button(form_mapa.infoest_frame, text="x", command=lambda: close_infoest(form_mapa), bg="white", fg="red", borderwidth=0)
    close_button.pack(side="right", padx=5, pady=5)

def close_info_upload(form_mapa):
    if hasattr(form_mapa, 'infoupload_frame'):
        form_mapa.infoupload_frame.destroy()

def show_info_upload(form_mapa, ruta):
    close_info_upload(form_mapa)

    form_mapa.infoupload_frame = Frame(form_mapa.panel_principal, bg="white", borderwidth=1, relief="solid")
    form_mapa.infoupload_frame.place(x=850, y=25)

    info_label = Label(form_mapa.infoupload_frame, text=f"Se ha cargado con éxito el archivo \n{ruta}", bg="white")
    info_label.pack(side="left", padx=5, pady=5)

    close_button = Button(form_mapa.infoupload_frame, text="x", command=lambda: close_info_upload(form_mapa), bg="white", fg="red", borderwidth=0)
    close_button.pack(side="right", padx=5, pady=5)

    form_mapa.infoupload_frame.after(5000, form_mapa.infoupload_frame.destroy)


