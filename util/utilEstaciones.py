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
        
    maxLon = max(coordenadasLon) + 0.000001
    minLon = min(coordenadasLon) - 0.000001
    maxLat = max(coordenadasLat) + 0.000001
    minLat = min(coordenadasLat) - 0.000001

    return maxLon, minLon, maxLat, minLat


def crear_diccionario_zonas(estaciones, n, minLon, maxLat, lon_celda, lat_celda, idMap):
    #Creo matriz para guardar las coordenadas de todos los puntos
    matriz = [[(maxLat, minLon) for _ in range(n+1)] for _ in range(n+1)]

    for i in range(n+1):
        for j in range(n+1):
            matriz[i][j] = (matriz[i][j][0] - lat_celda * i, matriz[i][j][1] + lon_celda * j)
    diccionario={
        'ids': [],
        'coordenadas': [],
        'cantidades': [],
        'capacidades': [],
        'num_estaciones': [],
        'cantidad_maxima': -1,
        #'cantidades_mat': [],
        'cantidades_suavizadas': [],
    }
    id = 1
    for i in range(n):
        for j in range(n):
            diccionario['ids'].append(id)
            coord_poligono = [matriz[i][j], matriz[i][j+1], matriz[i+1][j+1], matriz[i+1][j]]
            diccionario['coordenadas'].append(coord_poligono)
            idMap[i][j] = id
            id = id + 1

    
    diccionario['cantidades'] = [0 for i in range(pow(n,2))]
    diccionario['capacidades'] = [0 for i in range(pow(n,2))]
    diccionario['num_estaciones'] = [0 for i in range(pow(n,2))]
    diccionario['cantidades_mat'] = [[0 for _ in range(n)] for _ in range(n)]

    
    #Relleno las cantidades para cada zona
    for id in estaciones:
        estaciones[id]['zona'] = clasificar_punto(n, estaciones[id]['coordinates'][::-1], lon_celda, lat_celda, minLon, maxLat, idMap)
        diccionario['cantidades'][estaciones[id]['zona']-1] = diccionario['cantidades'][estaciones[id]['zona']-1] + estaciones[id]['bike_bases']
        diccionario['capacidades'][estaciones[id]['zona']-1] = diccionario['capacidades'][estaciones[id]['zona']-1] + (estaciones[id]['bike_bases']+estaciones[id]['free_bases'])
        diccionario['num_estaciones'][estaciones[id]['zona']-1] = diccionario['num_estaciones'][estaciones[id]['zona']-1] + 1
        fila = (estaciones[id]['zona']-1)//n
        columna =((estaciones[id]['zona']-1)%n)
        #diccionario['cantidades_mat'][fila][columna] = diccionario['cantidades_mat'][fila][columna] + estaciones[id]['bike_bases']
    return diccionario

def crear_diccionario_zonas_nuevo(estaciones, n, minLon, maxLat, lon_celda, lat_celda, idMap):
    #Coordenadas: [(40.62173325, -3.9388403499999997), (40.62173325, -3.42344035), (40.22653325, -3.9388403499999997), (40.22653325, -3.42344035)]
    #Coordenadas BUENAS: 
    # [(40.62442815, −3.93884035), (40.62442815, −3.4214), 
    # (40.22383835, −3.93884035), (40.22383835, −3.4214)]
    x=0


def clasificar_punto(n, punto, lon_celda, lat_celda, minLon, maxLat, idMap):
    lat, lon = punto
    zona_lat = int(abs(lat - maxLat)/lat_celda)
    zona_lon = int(abs(lon - minLon)/lon_celda)
    return idMap[zona_lat][zona_lon]

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

def get_color(valor, rangos, colores):

    if valor == 0:
        return None

    for i in range(len(rangos)-1):
        if rangos[i] <= valor < rangos[i+1]:
            return colores[i]
    if valor == rangos[len(rangos)-1]:
        return "#00FF00"
    """
    escala = (valor - min_val) / (max_val - min_val)
    
    if escala <= 0.5:   # Entre rojo (255, 0, 0) y amarillo (255, 255, 0)
        r = 255
        g = int(255 * (escala / 0.5))  # Va de 0 a 255
        b = 0
    else:               # Entre amarillo (255, 255, 0) y verde (0, 255, 0)
        r = int(255 * (1 - (escala - 0.5) / 0.5))  # Va de 255 a 0
        g = 255
        b = 0
    
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    return f'#{r:02x}{g:02x}{b:02x}'
    """

"""
def crear_geojson_df(estaciones, n, minLon, minLat, maxLat, lon_celda, lat_celda):
    #Creo matriz para guardar las coordenadas de todos los puntos
    matriz = [[[minLon, maxLat] for _ in range(n+1)] for _ in range(n+1)]
    #idMap = [[0 for _ in range(n)] for _ in range(n)]
    idMap = np.repeat(0, repeats=n**2).reshape((n,n))

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
    """