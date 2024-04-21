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
                "coordinates": station['geometry']['coordinates']
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
        
    maxLon = max(coordenadasLon)
    minLon = min(coordenadasLon)
    maxLat = max(coordenadasLat)
    minLat = min(coordenadasLat)

    return maxLon, minLon, maxLat, minLat


def crear_geojson_df(estaciones, n, minLon, minLat, maxLat, lon_celda, lat_celda):
    #Creo matriz para guardar las coordenadas de todos los puntos
    matriz = [[[minLon, maxLat] for _ in range(n+1)] for _ in range(n+1)]
    idMap = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n+1):
        for j in range(n+1):
            matriz[i][j] = [matriz[i][j][0] + lon_celda * j,matriz[i][j][1] - lat_celda * i]
            
    #print(matriz)

    geojson = {
            "type": "FeatureCollection",
            "features": []
        }
    
    #Saco las coordenadas de cada casilla para guardarlas en el geojson
    #Guardo en el diccionario de datos los ids y los nombres de las zonas
    datos={
        'id': [],
        'name': [],
        'cantidad': [],
    }
    id = 1
    for i in range(n):
        for j in range(n):
            datos['id'].append(id)
            datos['name'].append(f"Zona {id}")
            feature = {
                "type": "Feature",
                "properties": {"name": f"Zona {id}"},
                "geometry": {
                    "coordinates": [[matriz[i+1][j], matriz[i+1][j+1], matriz[i][j+1], matriz[i][j], matriz[i+1][j]]],
                    "type": "Polygon"
                },
                'id': id
            }
            geojson['features'].append(feature)
            idMap[i][j] = id
            id = id + 1

    #print(idMap)
    
    datos['cantidad'] = [0 for i in range(pow(n,2))]
    
    #Relleno las cantidades para cada zona
    for id in estaciones:
        zona = clasificar_punto(n, estaciones[id]['coordinates'], lon_celda, lat_celda, minLon, minLat, idMap)
        datos['cantidad'][zona] = datos['cantidad'][zona] + estaciones[id]['bike_bases']
        #print(f"La estacion {id} pertenece a la zona {zona}")
    
    df = pd.DataFrame(datos)
    #df.to_excel('datos.xlsx')
    return geojson, df

def crear_df_estaciones(estaciones):
    data = {"id": [], "name": [], "bike_bases": [], "free_bases": [], "lat": [], "lon": [], 'info':[]}
    for id in estaciones:
        data['id'].append(id)
        data['name'].append(estaciones[id]['name'])
        data['bike_bases'].append(estaciones[id]['bike_bases'])
        data['free_bases'].append(estaciones[id]['free_bases'])
        data['lat'].append(estaciones[id]['coordinates'][1])
        data['lon'].append(estaciones[id]['coordinates'][0])
        data['info'].append(estaciones[id]['name'] + ' Bicicletas: ' + str(estaciones[id]['bike_bases']))
    
    df = pd.DataFrame(data)
    return df

def clasificar_punto(n, punto, lon_celda, lat_celda, minLon, minLat, idMap):
    lon, lat = punto
    zona_lon = int((lon - minLon)/lon_celda)
    zona_lat = int((lat - minLat)/lat_celda)
    return idMap[n-zona_lat-1][zona_lon-1]

"""def clasificar_punto2(n, punto, lon_celda, lat_celda, minLon, minLat, idMap):
    lon, lat = punto
    zona_lon = int((lon - minLon) / lon_celda)
    zona_lat = int((lat - minLat) / lat_celda)
    if zona_lon==n:
        zona_lon=n-1
    if zona_lat==n:
        zona_lat=n-1
    return int(idMap[n-zona_lat-1][zona_lon-1])"""



def generar_puntos(centro, radio, nPuntos):
    #Polares
    random_rad = np.random.uniform(0, radio, nPuntos)
    random_ang = np.random.uniform(0, 2*np.pi, nPuntos)
    
    #Cartesianas
    lon = centro[0] + random_rad * np.cos(random_ang)
    lat = centro[1] + random_rad * np.sin(random_ang)
    
    puntos = np.column_stack((lon, lat))
    
    return puntos

def generar_flotantes(estaciones, radio):
    data = {"id": [], "lat": [], "lon": [], 'info':[]}
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