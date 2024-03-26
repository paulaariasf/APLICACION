import requests
import json
import pandas as pd

def devolver_estaciones():
    #Hago login y guardo el token de acceso
    url_login = "https://openapi.emtmadrid.es/v1/mobilitylabs/user/login/"
    headers_login = {'email':'paulariasfer01@gmail.com', 'password':'Poseido58'}

    response_login = requests.get(url_login, headers=headers_login)
    datos_login = json.loads(response_login.content)
    token = datos_login['data'][0]['accessToken']

    #Tomo información sobre las estaciones

    url_stations = "http://openapi.emtmadrid.es/v1/transport/bicimad/stations/"
    headers_stations = {'accessToken': token}

    response_stations = requests.get(url_stations, headers=headers_stations)
    datos_stations = json.loads(response_stations.content)


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

def crear_dataframe(estaciones, n, minLon, minLat, lon_celda, lat_celda):
    # Crear DataFrame 
    df = pd.DataFrame(0, index=range(n), columns=range(n), dtype=int)  

    # Asignar las coordenadas a las celdas de la cuadrícula y sumar las cantidades asociadas
    for id in estaciones:
        asignar_celda(estaciones[id]['coordinates'], estaciones[id]['bike_bases'], df,
                      n, minLon, minLat, lon_celda, lat_celda)

    return df

def asignar_celda(coor, cantidad, df, n, minLon, minLat, lon_celda, lat_celda):
        x, y = coor
        columna = min(int((x - minLon) / lon_celda), n-1) 
        fila = min(int((y - minLat) / lat_celda), n-1)
        df.at[n-1 - fila, columna] += cantidad