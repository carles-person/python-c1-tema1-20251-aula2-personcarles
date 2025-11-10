"""
Enunciado:
Este ejercicio introduce el uso de bibliotecas especializadas para acceder a APIs de forma
sencilla y estructurada. En concreto, utilizaremos la biblioteca pybikes que proporciona
wrappers para múltiples sistemas de bicicletas compartidas en todo el mundo.

En lugar de construir nuestro propio cliente HTTP y procesar manualmente los datos JSON,
aprenderemos a utilizar herramientas existentes que hacen este trabajo por nosotros.

Tareas:
1. Explorar los sistemas de bicicletas disponibles
2. Obtener información sobre el sistema de Barcelona (Bicing)
3. Analizar los datos de las estaciones

Esta práctica ilustra cómo las bibliotecas especializadas simplifican el acceso a APIs
y permiten concentrarse en el análisis de datos en lugar de en los detalles técnicos
de la comunicación con la API.
"""

import pybikes as pb
import pybikes.data as pbd
import pandas as pd
import time
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import sys
# from models.BikeSystem import BikeSysInfo
   


def listar_sistemas_disponibles() -> List[str]:
    """
    Obtiene una lista de todos los sistemas de bicicletas disponibles en pybikes.

    Returns:
        List[str]: Lista de identificadores de sistemas disponibles
    """
    # Implementa aquí la lógica para obtener y devolver la lista
    # de sistemas disponibles en pybikes
    
    # inicialitso la llista de systemes --> instancies buida
    instance_tag_list:List[str] = []
    
    #obting llista de sistemes o schemas
    available_instances = pb.get_instances() # retorna una llista de tuples {classe:str, instancia:dict}
    
    #escanejo totes les classes i instances, i genero una llista de tots els tags
    for cls, instance in available_instances:
        instance_tag_list.append(instance.get('tag','--'))

    # retorno la llista
    return instance_tag_list

def buscar_sistema_por_ciudad(ciudad: str) -> List[str]:
    """
    Busca sistemas de bicicletas que contengan el nombre de la ciudad especificada.

    Args:
        ciudad (str): Nombre de la ciudad a buscar

    Returns:
        List[str]: Lista de sistemas que coinciden con la búsqueda
    """
    # Implementa aquí la lógica para buscar y devolver sistemas
    # que coincidan con la ciudad especificada
    
    # inicialitzo el valor a tornar
    list_of_instances_in_city:List[str] = []

    # inicialitzo la llista amb totes les instal·lacions possibles (intances)  
    instances_list = listar_sistemas_disponibles()

    # per cada instancia comprobo si existeix la ciutat, esta en el camp "meta"->"city" del diccionari anidat
    for item in instances_list:
        try:
            cls,inst=pb.find_system(item)
            _city = inst.get('meta').get('city',"--")
            if ciudad.lower() == _city.lower():
                list_of_instances_in_city.append(item)
        except Exception as err:
            print(f'Error on {item}\n{err}')
        
    return list_of_instances_in_city
        

def obtener_info_sistema(tag: str) -> Dict[str, Any]:
    """
    Obtiene la información del sistema especificado.

    Args:
        tag (str): Identificador del sistema (por ejemplo, 'bicing')

    Returns:
        Dict[str, Any]: Metadatos del sistema o None si no existe
    """
    # Implementa aquí la lógica para obtener y devolver
    # los metadatos del sistema especificado
    
    # inicialitzo la llista amb totes les instal·lacions possibles   
    
    try:
        tag_info = pb.get(tag)
        return tag_info.meta
    except:
        return None
    
    

def obtener_estaciones(tag: str) -> Optional[List]:
    """
    Obtiene la lista de estaciones del sistema especificado.

    Args:
        tag (str): Identificador del sistema (por ejemplo, 'bicing')

    Returns:
        Optional[List]: Lista de objetos estación o None si hay error
    """
    # Implementa aquí la lógica para obtener y devolver
    # la lista de estaciones del sistema especificado


    # obtinc objecte amb la informació del tag/instance
    # eb cas de qualsevol tipus error, retorno "None"
    result:List

    try:
        instance_info = pb.get(tag)
    
        # actualitzo info sobre les estacions
        instance_info.update()
        # copio a result
        result = instance_info.stations
    except:
        result = None
    
    return result
    

def crear_dataframe_estaciones(estaciones: List) -> pd.DataFrame:
    """
    Convierte la lista de estaciones en un DataFrame de pandas.

    Args:
        estaciones (List): Lista de objetos estación

    Returns:
        pd.DataFrame: DataFrame con la información de las estaciones
    """
    # Implementa aquí la lógica para convertir la lista de estaciones
    # en un DataFrame de pandas con al menos las columnas:
    # nombre, latitud, longitud, bicicletas disponibles, espacios libres
    
    """
    # per passar els unit test, he de canviar la funció a  per la sequent
    _ = [station.to_dict() for station in estaciones]
    """

    #funcio replacement per passar unit tests :( 
    _ =[ {"name": station.name,
          "latitude": station.latitude,
          "longitude": station.longitude,
          "bikes": station.bikes,
          "free": station.free } for station in estaciones]
    
    return pd.DataFrame(_)

    


def visualizar_estaciones(df: pd.DataFrame) -> None:
    """
    Genera una visualización simple de la disponibilidad de bicicletas.

    Args:
        df (pd.DataFrame): DataFrame con la información de las estaciones
    """
    # Implementa aquí la lógica para crear un gráfico de barras que muestre
    # las 10 estaciones con más bicicletas disponibles
    
    # genero un dataframe amb les 10 estacions amb mes bicicletes disponibles
    top_10 = df.nlargest(10, columns='bikes')
    top_10.plot(x='name',y='bikes', kind='bar', title="TOP 10 Estacions amb mes bicis")
    plt.show()



if __name__ == "__main__":
    # Listar sistemas disponibles
    print("\nSistemas de bicicletas disponibles:")
    sistemas = listar_sistemas_disponibles()
    print(f"Total: {len(sistemas)} sistemas")
    print(f"Algunos ejemplos: {sistemas[:5]}")

    # Buscar sistemas en Barcelona
    print("\nBuscando sistemas en Barcelona:")
    sistemas_barcelona = buscar_sistema_por_ciudad("Barcelona")
    print(f"Encontrados: {len(sistemas_barcelona)}")
    for sistema in sistemas_barcelona:
        print(f"- {sistema}")

    # Si se encuentra el sistema de Barcelona (Bicing), obtener información
    if "bicing" in sistemas:
        print("\nInformación del sistema Bicing de Barcelona:")
        info = obtener_info_sistema("bicing")
        for key, value in info.items():
            print(f"{key}: {value}")

        # Obtener estaciones
        print("\nObteniendo estaciones...")
        estaciones = obtener_estaciones("bicing")
        if estaciones:
            print(f"Obtenidas {len(estaciones)} estaciones")

            # Convertir a DataFrame
            print("\nConvirtiendo a DataFrame...")
            df = crear_dataframe_estaciones(estaciones)
            print(df.head())

            # Estadísticas básicas
            print("\nEstadísticas de bicicletas disponibles:")
            print(df['bikes'].describe())

            # Visualización
            print("\nVisualizando estaciones con más bicicletas disponibles...")
            visualizar_estaciones(df)
        else:
            print("No se pudieron obtener las estaciones.")
    else:
        print("El sistema 'bicing' no está disponible en pybikes.")

