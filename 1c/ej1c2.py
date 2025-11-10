"""
Enunciado:
Desarrolla un cliente para consultar la información de estaciones del sistema de bicicletas 
compartidas de Barcelona utilizando la API GBFS (General Bikeshare Feed Specification).

Tareas:
1. Consultar el endpoint de información de estaciones
2. Extraer datos específicos de cada estación
3. Convertir coordenadas de estaciones a un DataFrame de pandas
4. Procesar y estructurar la información recibida

Esta práctica te ayudará a entender cómo trabajar con APIs reales y procesar datos
en diferentes formatos utilizando pandas.

Tu tarea es completar la implementación de las funciones indicadas.
"""

import requests
import pandas as pd
import json

def get_stations_data():
    """
    Realiza una petición a la API para obtener información de las estaciones
    y extrae el objeto 'data' de la respuesta.
    
    Returns:
        dict: El objeto 'data' que contiene la lista de estaciones
        None: Si ocurre un error en la petición o el objeto 'data' no existe
    """
    # URL del endpoint de información de estaciones
    url = "https://barcelona.publicbikesystem.net/customer/gbfs/v2/en/station_information"
    
    # Implementa aquí la lógica para:
    # 1. Realizar una petición GET a la URL
    # 2. Verificar que la respuesta sea correcta (código 200)
    # 3. Extraer y devolver el objeto 'data' del JSON recibido
    # 4. Manejar posibles errores (conexión, formato, etc.)
    
    data_return = None
    try:
        # crido la funció per obtenir informació sobre les estacións
        r = requests.get(url)
        r.raise_for_status()

        if r.status_code == 200:
            #extrec objecte data de la resposta i agafo el camp "data" i el torno 
            # en format diccionari
            data_return = r.json().get('data', None)
        
    
    except requests.exceptions.RequestException as err:
        data_return=None

    return data_return


def get_station_info(stations_data, station_id):
    """
    Busca y devuelve la información de una estación específica según su ID.
    
    Args:
        stations_data (dict): Datos de estaciones obtenidos con get_stations_data()
        station_id (str): ID de la estación a buscar
        
    Returns:
        dict: Información de la estación solicitada
        None: Si no se encuentra la estación o los datos de entrada son inválidos
    """
    # Implementa aquí la lógica para:
    # 1. Verificar que stations_data no es None y tiene la estructura esperada
    
    # 2. Buscar la estación con el ID proporcionado en la lista de estaciones
    # 3. Devolver la información completa de esa estación
    # 4. Si no existe, devolver None
    
    # inicialitzo data_return
    data_return = None
    # Verifico que no es none
    if stations_data == None:
        data_return= None
    # is no esta buida, cobprobo que es un diccionari
    elif not isinstance(stations_data,dict):
        data_return = None
    # arribo aqui quan stations_data te informació i és un diccionari.
    else:
        try:
            list_stations = stations_data.get('stations')
            # rtorna primera "station" trobada amb id=station_id
            data_return = next((info for info in list_stations if info['station_id'] == station_id),None)
            
        # capturo error --> Key Error, or Value Error
        except KeyError as err:
            print(f'Station ID: {station_id} --> No Trobat o impossible recuperar informació')
            data_return = None
        except Exception as err:
            print(f'Station ID: {station_id} --> Error Desconegut {err}')
            data_return = None


    # retorno el valor de l'estació sel·leccionada o None si hi ha error
    return data_return

def get_station_coordinates(station_info):
    """
    Extrae las coordenadas (latitud y longitud) de una estación.
    
    Args:
        station_info (dict): Información de una estación específica
        
    Returns:
        tuple: Par (latitud, longitud) de la estación
        None: Si station_info es None o no contiene las coordenadas
    """
    # Implementa aquí la lógica para:
    # 1. Verificar que station_info no es None
    # 2. Extraer los valores de latitud y longitud del diccionario
    # 3. Devolver ambos valores como una tupla (lat, lon)
    # 4. Manejar casos donde los campos no existan
    
    # inicialitzo data_return com a diccionari
    data_return = None
    
    # comprobo que no esta buit
    if station_info == None:
        data_return = None

    # processo station_info, extreure coordenades
    else:
        # try except: per capturar excepcions de keys no existents
        try:
            lat = station_info['lat']
            long = station_info['lon']
            data_return = (lat,long)
        except (KeyError) as err:
            print(f'Keys Lat or Lon no existeixen')
            data_return = None
    
    # retorno el valor
    return data_return



def create_stations_dataframe(stations_data:list):
    """
    Crea un DataFrame de pandas con información básica de todas las estaciones.
    
    Args:
        stations_data (dict): Datos de estaciones obtenidos con get_stations_data()
        
    Returns:
        pandas.DataFrame: DataFrame con columnas 'station_id', 'latitude', 'longitude', 'name'
        None: Si stations_data es None o no tiene la estructura esperada
    """
    # Implementa aquí la lógica para:
    # 1. Verificar que stations_data no es None y tiene la estructura esperada
    # 2. Crear una lista de diccionarios con la información básica de cada estación
    # 3. Convertir esa lista en un DataFrame de pandas
    # 4. El DataFrame debe tener las columnas: 'station_id', 'latitude', 'longitude', 'name'
    
    df_stations = None

    if stations_data == None:
        df_stations = None

    else:
        # miro si stations data conte el camp "stations", si no genero excepció "key Error"
        stations = stations_data.get('stations')

        
        # en cas afirmatiu, processo, stations. 
        # Retorno: 'None' si la info esta mal "formatejada", "Empty DF" si llista estacions esta buida,
        # o un DF amb la llista.
        
        if stations:
            # creo dataframe and station_id, name, latitude, longitude i retorno el valor
            df_stations = pd.DataFrame(stations,columns=['station_id','name','lat','lon'])

            # si no existeixen camps, el dataframe torna buit
            if df_stations.empty:
                df_stations = None
        else:
            if isinstance(stations,list):
                df_stations = pd.DataFrame() # create an empty dataframe
            else:
                df_stations = None

    return df_stations


if __name__ == '__main__':
    # Obtener los datos de todas las estaciones
    stations_data = get_stations_data()
    
    if stations_data:
        # Ejemplo: Obtener información de la estación con ID "1"
        station_1 = get_station_info(stations_data, "1")
        if station_1:
            print(f"Estación encontrada: {station_1['name']}")
            
            # Obtener coordenadas
            coordinates = get_station_coordinates(station_1)
            if coordinates:
                lat, lon = coordinates
                print(f"Coordenadas: ({lat}, {lon})")
        
        # Crear DataFrame con todas las estaciones
        df = create_stations_dataframe(stations_data)
        if df is not None:
            print("\nPrimeras 5 estaciones:")
            print(df.head())
            print(f"\nTotal de estaciones: {len(df)}")
    else:
        print("No se pudieron obtener los datos de las estaciones.")
