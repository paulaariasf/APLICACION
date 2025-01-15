import random
import pandas as pd
import re
import json

def generar_datos_demanda(num_points, max_lon, min_lon, max_lat, min_lat):
    diccionario = {'coordenadas': [], 'zona' : [0] * num_points}
    #coordenadas de la plaza del sol
    center_lon = -3.703339
    center_lat = 40.416729

    std_dev_lon = (max_lon - min_lon) / 10
    std_dev_lat = (max_lat - min_lat) / 10


    for _ in range(num_points):
        while True:
            lon = random.gauss(center_lon, std_dev_lon)
            lat = random.gauss(center_lat, std_dev_lat)
            if min_lon <= lon <= max_lon and min_lat <= lat <= max_lat:
                diccionario['coordenadas'].append([lat, lon])
                break
    
    return diccionario

def cargar_datos(ano, mes, dia, hora):
    ruta_archivo = f"data/anos_anteriores/{str(ano)}{str(mes).zfill(2)}.json"
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        data = json.load(archivo)
    fecha=f'{ano}-{str(mes).zfill(2)}-{str(dia).zfill(2)}T{str(hora).zfill(2)}'

    for key in data.keys():
        if key[:13] == fecha:
            estaciones = data[key]
            break

    nombre = f'estaciones_{str(dia).zfill(2)}-{str(mes).zfill(2)}-{ano}_{str(hora).zfill(2)}:00'
    return nombre, estaciones