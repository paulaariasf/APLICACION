import requests
import json
import pandas as pd
import numpy as np

def devolver_estaciones():
    """#Hago login y guardo el token de acceso
    url_login = "https://openapi.emtmadrid.es/v1/mobilitylabs/user/login/"
    headers_login = {'email':'paulariasfer01@gmail.com', 'password':'Poseido58'}

    response_login = requests.get(url_login, headers=headers_login)
    datos_login = json.loads(response_login.content)
    token = datos_login['data'][0]['accessToken']

    #Tomo información sobre las estaciones

    url_stations = "http://openapi.emtmadrid.es/v1/transport/bicimad/stations/"
    headers_stations = {'accessToken': token}

    response_stations = requests.get(url_stations, headers=headers_stations)
    datos_stations = json.loads(response_stations.content)"""

    with open('estaciones_api.json', "r") as archivo:
        datos_stations = json.load(archivo)

    stations = {}
    for station in datos_stations['data']:
        if station['no_available'] == 0:
            stations[station['id']] = {
                "name": station['name'],
                "free_bases": station['free_bases'],
                "bike_bases": station['dock_bikes'],
                "coordinates": station['geometry']['coordinates'],
                "zona": -1
            }
    return stations

# Calcular los límites de la cuadrícula

def limites(estaciones):
    coordenadasLon = []
    coordenadasLat = []

    for id in estaciones:
        coordEstacion = estaciones[id]["coordinates"]
        coordenadasLon.append(coordEstacion[0])
        coordenadasLat.append(coordEstacion[1])
        
    maxLon = max(coordenadasLon) + 0.00500001
    minLon = min(coordenadasLon) - 0.00500001
    maxLat = max(coordenadasLat) + 0.00500001
    minLat = min(coordenadasLat) - 0.00500001

    return maxLon, minLon, maxLat, minLat


def crear_diccionario_zonas_nuevo(estaciones, n, minLon, maxLat, lon_celda, lat_celda):
    #Coordenadas: [(40.62173325, -3.9388403499999997), (40.62173325, -3.42344035), (40.22653325, -3.9388403499999997), (40.22653325, -3.42344035)]
    #Coordenadas BUENAS: 
    # [(40.62442815, −3.93884035), (40.62442815, −3.4214), 
    # (40.22383835, −3.93884035), (40.22383835, −3.4214)]
    x=0

def crear_diccionario(estaciones, flotantes, patinetes, n, minLon, maxLat, lon_celda, lat_celda, add_fijas, add_flotantes, add_patinetes, mostrar_huecos):
    print(f'add_fijas: {add_fijas}, add_flotantes: {add_flotantes}, add_patinetes: {add_patinetes}')
    matriz = [[(maxLat, minLon) for _ in range(n+1)] for _ in range(n+1)]
    #Creo la matriz con las coordenadas para cada extremo de la cuadricula
    for i in range(n+1):
        for j in range(n+1):
            matriz[i][j] = (matriz[i][j][0] - lat_celda * i, matriz[i][j][1] + lon_celda * j)
    diccionario={
            'ids': [],
            'coordenadas': [],
            'cantidades': [],
            'cantidad_maxima': -1,
            'cantidades_suavizadas': [],
        }
    diccionario['cantidades'] = [0 for i in range(pow(n,2))]
    diccionario['cantidades_estaciones'] = [0 for _ in range(pow(n,2))]
    diccionario['cantidades_flotantes'] = [0 for _ in range(pow(n,2))]
    diccionario['cantidades_patinetes'] = [0 for _ in range(pow(n,2))]

    #Guardo en ids y coordenadas la información sobre las zonas del mapa de calor
    id = 1 
    for i in range(n):
        for j in range(n):
            diccionario['ids'].append(id)
            coord_poligono = [matriz[i][j], matriz[i][j+1], matriz[i+1][j+1], matriz[i+1][j]]
            diccionario['coordenadas'].append(coord_poligono)
            id=id+1

    if add_fijas and estaciones != None:
        diccionario['capacidades'] = [0 for i in range(pow(n,2))]
        diccionario['num_estaciones'] = [0 for i in range(pow(n,2))]
        
        #Relleno las cantidades para cada zona
        for id in estaciones:
            zona = clasificar_punto(n, estaciones[id]['coordinates'][::-1], lon_celda, lat_celda, minLon, maxLat)
            estaciones[id]['zona'] = zona
            diccionario['cantidades'][zona-1] = diccionario['cantidades'][zona-1] + estaciones[id]['bike_bases']
            diccionario['cantidades_estaciones'][zona-1] = diccionario['cantidades_estaciones'][zona-1] + estaciones[id]['bike_bases']
            diccionario['capacidades'][zona-1] = diccionario['capacidades'][zona-1] + (estaciones[id]['bike_bases']+estaciones[id]['free_bases'])
            diccionario['num_estaciones'][zona-1] = diccionario['num_estaciones'][zona-1] + 1
    
    if add_flotantes and flotantes != None:
        #Relleno las cantidades para cada zona
        for id in flotantes['id']:
            zona = clasificar_punto(n, flotantes['coord'][id-1], lon_celda, lat_celda, minLon, maxLat)
            flotantes['zona'].append(zona)
            diccionario['cantidades'][zona-1] = diccionario['cantidades'][zona-1] + 1
            diccionario['cantidades_flotantes'][zona-1] = diccionario['cantidades_flotantes'][zona-1] + 1

    if add_patinetes and patinetes != None:
        #Relleno las cantidades para cada zona
        for id in patinetes['id']:
            zona = clasificar_punto(n, patinetes['coord'][id-1], lon_celda, lat_celda, minLon, maxLat)
            patinetes['zona'].append(zona)
            diccionario['cantidades'][zona-1] = diccionario['cantidades'][zona-1] + 1
            diccionario['cantidades_patinetes'][zona-1] = diccionario['cantidades_patinetes'][zona-1] + 1

    if mostrar_huecos and estaciones != None:
        diccionario['capacidades'] = [0 for i in range(pow(n,2))]
        diccionario['num_estaciones'] = [0 for i in range(pow(n,2))]

        #Relleno los huecos para cada zona
        for id in estaciones:
            zona = clasificar_punto(n, estaciones[id]['coordinates'][::-1], lon_celda, lat_celda, minLon, maxLat)
            estaciones[id]['zona'] = zona
            diccionario['cantidades'][zona-1] = diccionario['cantidades'][zona-1] + estaciones[id]['free_bases']
            diccionario['capacidades'][zona-1] = diccionario['capacidades'][zona-1] + (estaciones[id]['bike_bases']+estaciones[id]['free_bases'])
            diccionario['num_estaciones'][zona-1] = diccionario['num_estaciones'][zona-1] + 1

    return diccionario


def clasificar_punto(n, punto, lon_celda, lat_celda, minLon, maxLat):
    lat, lon = punto
    zona_lat = int(abs(lat - maxLat)/lat_celda)
    zona_lon = int(abs(lon - minLon)/lon_celda)
    return zona_lat*n+zona_lon + 1




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

def generar_flotantes(estaciones, radio):
    data = {'id': [], 'lat': [], 'lon': [], 'info':[]}
    id_bici = 1
    for id in estaciones:
        puntos_flotantes = generar_puntos(estaciones[id]['coordinates'], 
                                            radio, 
                                            estaciones[id]['bike_bases'])
        for p in puntos_flotantes:
            data['id'].append(id_bici)
            data['lat'].append(p[1])
            data['lon'].append(p[0])
            data['info'].append('Bicicleta nº '+ str(id_bici))
            id_bici = id_bici + 1
    
    df_flotantes = pd.DataFrame(data)
    return df_flotantes

def generar_flotantes_v2(estaciones, radio):
    """data = {'id': [], 'coord': [], 'info':[]}
    id_bici = 1
    for id in estaciones:
        puntos_flotantes = generar_puntos(estaciones[id]['coordinates'], 
                                            radio, 
                                            estaciones[id]['bike_bases'])
        for p in puntos_flotantes:
            data['id'].append(id_bici)
            data['coord'].append(p)
            data['info'].append('Bicicleta nº '+ str(id_bici))
            id_bici = id_bici + 1"""
    with open("bicicletas_flotantes.json", "r") as archivo:
        data = json.load(archivo)
    #df_flotantes = pd.DataFrame(data)
    #return df_flotantes
    return data

def generar_patinetes(estaciones, radio):
    """data = {'id': [], 'coord': [], 'info':[]}
    id_patinete = 1
    for id in estaciones:
        puntos_patinetes = generar_puntos(estaciones[id]['coordinates'], 
                                            radio, 
                                            estaciones[id]['bike_bases'])
        for p in puntos_patinetes:
            data['id'].append(id_patinete)
            data['coord'].append(p)
            data['info'].append('Patinete nº '+ str(id_patinete))
            id_patinete = id_patinete + 1"""
    #with open('patinetes.json', "w", encoding="utf-8") as file:
    #    json.dump(data, file, indent=4)
    
    with open("bicicletas_flotantes.json", "r") as archivo:
        data = json.load(archivo)
    
    return data

def get_color(valor, rangos, colores):

    if valor == 0:
        return None

    for i in range(len(rangos)-1):
        if rangos[i] <= valor < rangos[i+1]:
            return colores[i]
    if valor == rangos[len(rangos)-1]:
        return "#00FF00"
