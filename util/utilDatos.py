import random
import pandas as pd
import re
import json
import numpy as np
import requests
from tkinter import *
from tkinter import messagebox

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

def generar_aleatorios_estaciones_num_bicicletas(estaciones):
    datos_generados = {}
    for id in estaciones:
        puestos = estaciones[id]['bike_bases'] + estaciones[id]['free_bases']
        num = random.randint(0, puestos)
        datos_generados[id] = {
            "name": estaciones[id]['name'],
            "coordinates": estaciones[id]['coordinates'],
            "bike_bases": num,
            "free_bases": puestos - num
        }
    return datos_generados

def generar_aleatorios_estaciones_uniformes(n, max_lon, min_lon, max_lat, min_lat):
    datos_generados = {}
    for i in range(n):
        max = 28
        num = random.randint(0, max)
        datos_generados[i] = {
            "name": f'Estacion {i}',
            "coordinates": [random.uniform(min_lon, max_lon),
                            random.uniform(min_lat, max_lat)],
            "bike_bases": num,
            "free_bases": max - num
        }
    return datos_generados

def generar_aleatorios_estaciones_centrados(n, max_lon, min_lon, max_lat, min_lat):
    datos_generados = {}

    #coordenadas de la plaza del sol (centro de Madrid)
    center_lon = -3.703339
    center_lat = 40.416729
    
    std_dev_lon = (max_lon - min_lon) / 10
    std_dev_lat = (max_lat - min_lat) / 10

    max = 28

    for i in range(n):
        while True:
            lon = random.gauss(center_lon, std_dev_lon)
            lat = random.gauss(center_lat, std_dev_lat)
            if min_lon <= lon <= max_lon and min_lat <= lat <= max_lat:
                num = random.randint(0, max)
                datos_generados[i] = {
                    "name": f'Estacion {i}',
                    "coordinates": [lon, lat],
                    "bike_bases": num,
                    "free_bases": max - num
                }
                break
    return datos_generados

def generar_aleatorios_flotantes_estaciones(estaciones, radio=0.005):
    data = {'id': [], 'coord': [], 'info':[], 'zona': []}
    id_flot = 1
    for id in estaciones:
        puntos_flotantes = generar_puntos(estaciones[id]['coordinates'], 
                                            radio, 
                                            estaciones[id]['bike_bases'])
        for p in puntos_flotantes:
            data['id'].append(id_flot)
            data['coord'].append(p)
            data['info'].append('Flotante nº '+ str(id_flot))
            id_flot+=1
    return data

def generar_puntos(centro, radio, nPuntos):
    #Polares
    random_rad = np.random.uniform(0, radio, nPuntos)
    random_ang = np.random.uniform(0, 2*np.pi, nPuntos)
    
    #Cartesianas
    lon = centro[0] + random_rad * np.cos(random_ang)
    lat = centro[1] + random_rad * np.sin(random_ang)
    
    #puntos = np.column_stack((lon, lat))
    puntos = [pair for pair in zip(lat, lon)]
    return puntos

def generar_aleatorios_flotantes_uniforme(n, max_lon, min_lon, max_lat, min_lat):
    data = {'id': [], 'coord': [], 'info':[], 'zona': []}
    for i in range(n):
        data['id'].append(i+1)
        data['coord'].append([random.uniform(min_lat, max_lat),
                              random.uniform(min_lon, max_lon)])
    return data

def generar_aleatorios_flotantes_centrado(n, max_lon, min_lon, max_lat, min_lat):
    #coordenadas de la plaza del sol
    center_lon = -3.703339
    center_lat = 40.416729
    
    std_dev_lon = (max_lon - min_lon) / 10
    std_dev_lat = (max_lat - min_lat) / 10
    
    data = {'id': [], 'coord': [], 'info':[], 'zona': []}
    id = 1
    
    for _ in range(n):
        while True:
            lon = random.gauss(center_lon, std_dev_lon)
            lat = random.gauss(center_lat, std_dev_lat)
            if min_lon <= lon <= max_lon and min_lat <= lat <= max_lat:
                data['id'].append(id)
                id+=1
                data['coord'].append([lat, lon])
                break
    return data
