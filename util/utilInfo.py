
import util.utilTransportes as utilTransportes 
from tkinter import *
import numpy as np
from collections import Counter

def close_infozona(form_mapa):
    if form_mapa.pol_seleccion is not None:
        form_mapa.pol_seleccion.delete()
    if hasattr(form_mapa, 'infozona_frame'):
        form_mapa.infozona_frame.destroy()

def show_info_zona(form_mapa, coords):
    close_infozona(form_mapa)

    form_mapa.infozona_frame = Frame(form_mapa.panel_principal, bg="white", borderwidth=1, relief="solid")
    form_mapa.infozona_frame.place(x=815, y=475)
    
    zona = utilTransportes.clasificar_punto(form_mapa.n, (coords[0], coords[1]), form_mapa.lon_celda, form_mapa.lat_celda, form_mapa.minLon, form_mapa.maxLat)

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
            texto=f"Zona seleccionada: {zona} de {form_mapa.n**2}\nNúmero de estaciones:{form_mapa.dic_mapa_calor['num_estaciones'][zona-1]}\nCantidad de bicicletas: {form_mapa.dic_mapa_calor['cantidades'][zona-1]}/{form_mapa.dic_mapa_calor['capacidades'][zona-1]}: {(100*(form_mapa.dic_mapa_calor['cantidades'][zona-1]/form_mapa.dic_mapa_calor['capacidades'][zona-1])):.2f}%"
    
    elif form_mapa.clasificacion == "Huecos":
        texto=f"Zona seleccionada: {zona} de {form_mapa.n**2}\nNúmero de huecos libres:{form_mapa.dic_mapa_calor['cantidades'][zona-1]} de {form_mapa.dic_mapa_calor['capacidades'][zona-1]}"
    
    elif form_mapa.clasificacion == "Demanda Bicicletas":
        texto=f"Zona seleccionada: {zona} de {form_mapa.n**2}\n"
        texto+=f"Número de bicicletas totales:{form_mapa.dic_mapa_calor['cantidades'][zona-1]}\n"
        texto+=f"Número de solicitudes: {form_mapa.dic_mapa_calor['demanda_bicicletas'][zona-1]}\n"
        bicicletas_disponibles = form_mapa.dic_mapa_calor['cantidades'][zona-1]
        solicitudes =  form_mapa.dic_mapa_calor['demanda_bicicletas'][zona-1]
        factor_llenado=100*(bicicletas_disponibles-solicitudes)/(bicicletas_disponibles+solicitudes+1)
        texto+=f"Oferta-demanda bicicletas: {factor_llenado:.2f}"
    
    elif form_mapa.clasificacion == "Demanda Patinetes":
        texto=f"Zona seleccionada: {zona} de {form_mapa.n**2}\n"
        texto+=f"Número de patinetes totales:{form_mapa.dic_mapa_calor['cantidades'][zona-1]}\n"
        texto+=f"Número de solicitudes: {form_mapa.dic_mapa_calor['demanda_patinetes'][zona-1]}\n"
        patinetes_disponibles = form_mapa.dic_mapa_calor['cantidades'][zona-1]
        solicitudes =  form_mapa.dic_mapa_calor['demanda_patinetes'][zona-1]
        factor_llenado=100*(patinetes_disponibles-solicitudes)/(patinetes_disponibles+solicitudes+1)
        texto+=f"Oferta-demanda patinetes: {factor_llenado:.2f}"


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

def close_infocentroide(form_mapa):
    if form_mapa.centroide_seleccion is not None:
        form_mapa.centroide_seleccion.delete()
    if hasattr(form_mapa, 'infocentroide_frame'):
        form_mapa.infocentroide_frame.destroy()

def show_info_centroide(form_mapa, id, centroide):
    cluster_counts = dict(Counter(form_mapa.clustering_bicicletas[form_mapa.selected_archivo_bicicletas.get()]['clusters']))

    close_infocentroide(form_mapa)

    form_mapa.infocentroide_frame = Frame(form_mapa.panel_principal, bg="white", borderwidth=1, relief="solid")
    form_mapa.infocentroide_frame.place(x=800, y=550)
    
    info_label = Label(form_mapa.infocentroide_frame, text=f"Cantidad de bicicletas en el cluster: {cluster_counts[id]}", bg="white")
    info_label.pack(side="left", padx=5, pady=5)

    #Añadir marcador en el clúster seleccionado
    form_mapa.centroide_seleccion = form_mapa.labelMap.set_marker(centroide[0], centroide[1])
    close_button = Button(form_mapa.infocentroide_frame, text="x", command=lambda: close_infocentroide(form_mapa), bg="white", fg="red", borderwidth=0)
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

def close_info_tipo(form_mapa):
    if hasattr(form_mapa, 'infotipo_frame'):
        form_mapa.infotipo_frame.destroy()

def show_info_cambio_tipo(form_mapa):
    close_info_tipo(form_mapa)

    form_mapa.infotipo_frame = Frame(form_mapa.panel_principal, bg="white", borderwidth=1, relief="solid")
    form_mapa.infotipo_frame.place(x=850, y=25)

    info_label = Label(form_mapa.infotipo_frame, text=f"Se ha cambiado con éxito \nel tipo de mapa a {form_mapa.clasificacion}", bg="white")
    info_label.pack(side="left", padx=5, pady=5)

    close_button = Button(form_mapa.infotipo_frame, text="x", command=lambda: close_info_upload(form_mapa), bg="white", fg="red", borderwidth=0)
    close_button.pack(side="right", padx=5, pady=5)

    form_mapa.infotipo_frame.after(5000, form_mapa.infotipo_frame.destroy)

def show_leyenda(frame_leyenda, fijas=False, bicis=False, virtuales_bicis=False, pats=False, virtuales_pats=False, demanda_bicis=False, demanda_pats=False, ocupacion=False):
    colors, texts = [], []

    if ocupacion:
        texts = ['Ocupación baja', 'Ocupación media', 'Ocupación alta']
        colors = ['red', 'orange', '#68ca3d']
    else:
        if fijas:
            texts.append('Estaciones fijas')
            colors.append('blue')
        if bicis: 
            texts.append('Bicicletas')
            colors.append('#fe1a1a')
        if virtuales_bicis:
            texts.append('Estaciones virtuales bicicletas')
            colors.append('#991010')
        if pats:
            texts.append('Patinetes')
            colors.append('orange')
        if virtuales_pats:
            texts.append('Estaciones virtuales patinetes')
            colors.append('#d87900')
        if demanda_bicis:
            texts.append('Demanda bicicletas')
            colors.append('#ae4fda')
        if demanda_pats:
            texts.append('Demanda patinetes')
            colors.append('#37921c')
    

    for i in range(len(texts)):
        row_frame = Frame(frame_leyenda, bg='white')
        row_frame.pack(anchor="w", pady=0)

        symbol_label = Label(row_frame, text="•", font=("", 16, 'bold'), bg="white", fg=colors[i])
        symbol_label.pack(side="left", padx=5)

        text_label = Label(row_frame, text=texts[i], font=("", 10, 'bold'), bg="white", fg="black")
        text_label.pack(side="left")

"""form_mapa.frame_leyenda_colores = Frame(form_mapa.panel_principal, bg="white", borderwidth=1, relief="solid")
    form_mapa.frame_leyenda_colores.place(x=30, y=430)

    texts = ['Estaciones fijas', 'Bicicletas', 'Estaciones virtuales bicicletas', 'Patinetes', 'Estaciones virtuales patinetes']
    colors = ['blue', '#fe1a1a', '#991010', 'orange', '#d87900']"""
