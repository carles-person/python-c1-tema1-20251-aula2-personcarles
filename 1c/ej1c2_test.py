"""
Tests para el ejercicio ej1c2.py
Este archivo contiene pruebas para verificar la correcta implementación
de las funciones para consultar información de estaciones del sistema de bicicletas
compartidas de Barcelona mediante la API GBFS.
"""

import pytest
import pandas as pd
import requests
from unittest.mock import patch, MagicMock

from ej1c2 import get_stations_data, get_station_info, get_station_coordinates, create_stations_dataframe

@pytest.fixture
def sample_stations_response():
    """
    Fixture que proporciona una respuesta de ejemplo del endpoint de station_information
    """
    return {
        "last_updated": 1759834680,
        "ttl": 0,
        "data": {
            "stations": [
                {
                    "station_id": "1",
                    "name": "GRAN VIA CORTS CATALANES, 760",
                    "physical_configuration": "ELECTRICBIKESTATION",
                    "lat": 41.3979779,
                    "lon": 2.1801069,
                    "altitude": 16,
                    "address": "GRAN VIA CORTS CATALANES, 760",
                    "cross_street": "02-Eixample/05-el Fort Pienc",
                    "post_code": "08013",
                    "capacity": 46,
                    "is_charging_station": True,
                    "geofenced_capacity": 0,
                    "rental_methods": [
                        "KEY",
                        "TRANSITCARD",
                        "CREDITCARD",
                        "PHONE"
                    ],
                    "is_virtual_station": False,
                    "groups": [
                        "40.03"
                    ],
                    "obcn": "1",
                    "short_name": "1",
                    "nearby_distance": 1000,
                    "_bluetooth_id": "a7a8",
                    "_ride_code_support": True,
                    "rental_uris": {}
                },
                {
                    "station_id": "2",
                    "name": "C/ ROGER DE FLOR, 126",
                    "physical_configuration": "ELECTRICBIKESTATION",
                    "lat": 41.3954877,
                    "lon": 2.1771985,
                    "altitude": 17,
                    "address": "C/ ROGER DE FLOR, 126",
                    "cross_street": "02-Eixample/05-el Fort Pienc",
                    "post_code": "08013",
                    "capacity": 28,
                    "is_charging_station": True,
                    "geofenced_capacity": 0,
                    "rental_methods": [
                        "KEY",
                        "TRANSITCARD",
                        "CREDITCARD",
                        "PHONE"
                    ],
                    "is_virtual_station": False,
                    "groups": [
                        "40.05"
                    ],
                    "obcn": "2",
                    "short_name": "2",
                    "nearby_distance": 1000,
                    "_bluetooth_id": "32c5",
                    "_ride_code_support": True,
                    "rental_uris": {}
                },
                {
                    "station_id": "3",
                    "name": "C/ NÀPOLS, 82",
                    "physical_configuration": "ELECTRICBIKESTATION",
                    "lat": 41.3941557,
                    "lon": 2.1813305,
                    "altitude": 11,
                    "address": "C/ NÀPOLS, 82",
                    "cross_street": "02-Eixample/05-el Fort Pienc",
                    "post_code": "08013",
                    "capacity": 27,
                    "is_charging_station": True,
                    "geofenced_capacity": 0,
                    "rental_methods": [
                        "KEY",
                        "TRANSITCARD",
                        "CREDITCARD",
                        "PHONE"
                    ],
                    "is_virtual_station": False,
                    "groups": [
                        "40.06"
                    ],
                    "obcn": "3",
                    "short_name": "3",
                    "nearby_distance": 1000,
                    "_bluetooth_id": "5547",
                    "_ride_code_support": True,
                    "rental_uris": {}
                },
                {
                    "station_id": "4",
                    "name": "C/ RIBES, 13",
                    "physical_configuration": "ELECTRICBIKESTATION",
                    "lat": 41.3933173,
                    "lon": 2.1812483,
                    "altitude": 8,
                    "address": "C/ RIBES, 13",
                    "cross_street": "02-Eixample/05-el Fort Pienc",
                    "post_code": "08013",
                    "capacity": 21,
                    "is_charging_station": True,
                    "geofenced_capacity": 0,
                    "rental_methods": [
                        "KEY",
                        "TRANSITCARD",
                        "CREDITCARD",
                        "PHONE"
                    ],
                    "is_virtual_station": False,
                    "groups": [
                        "40.06"
                    ],
                    "obcn": "4",
                    "short_name": "4",
                    "nearby_distance": 1000,
                    "_bluetooth_id": "fc1b",
                    "_ride_code_support": True,
                    "rental_uris": {}
                },
                {
                    "station_id": "5",
                    "name": "PG. LLUIS COMPANYS, 11 (ARC TRIOMF)",
                    "physical_configuration": "ELECTRICBIKESTATION",
                    "lat": 41.3911035,
                    "lon": 2.1801763,
                    "altitude": 7,
                    "address": "PG. LLUIS COMPANYS, 11 (ARC TRIOMF)",
                    "cross_street": "01-CiutatVella/04-Sant Pere, Santa Caterina i la Ribera",
                    "post_code": "08018",
                    "capacity": 39,
                    "is_charging_station": True,
                    "geofenced_capacity": 0,
                    "rental_methods": [
                        "KEY",
                        "TRANSITCARD",
                        "CREDITCARD",
                        "PHONE"
                    ],
                    "is_virtual_station": False,
                    "groups": [
                        "35.01"
                    ],
                    "obcn": "5",
                    "short_name": "5",
                    "nearby_distance": 1000,
                    "_bluetooth_id": "abbc",
                    "_ride_code_support": True,
                    "rental_uris": {}
                }
            ]
        },
        "version": "2.3"
    }

@pytest.fixture
def sample_stations_data(sample_stations_response):
    """
    Fixture que proporciona solo el objeto 'data' de la respuesta
    """
    return sample_stations_response["data"]

@patch('ej1c2.requests.get')
def test_get_stations_data_success(mock_get, sample_stations_response):
    """
    Prueba la función get_stations_data cuando la petición es exitosa
    """
    # Configurar el mock para retornar una respuesta exitosa
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_stations_response
    mock_get.return_value = mock_response

    # Ejecutar la función
    result = get_stations_data()

    # Verificar que se llamó a requests.get con la URL correcta
    mock_get.assert_called_once_with("https://barcelona.publicbikesystem.net/customer/gbfs/v2/en/station_information")

    # Verificar que el resultado es el objeto 'data' del JSON
    assert result == sample_stations_response["data"], "La función debe devolver el objeto 'data' de la respuesta JSON"

@patch('ej1c2.requests.get')
def test_get_stations_data_error_status(mock_get):
    """
    Prueba la función get_stations_data cuando la petición devuelve un código de error
    """
    # Configurar el mock para retornar un código de error
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    # Ejecutar la función
    result = get_stations_data()

    # Verificar que el resultado es None cuando hay un error
    assert result is None, "La función debe devolver None cuando hay un error de estado HTTP"

@patch('ej1c2.requests.get')
def test_get_stations_data_connection_error(mock_get):
    """
    Prueba la función get_stations_data cuando ocurre un error de conexión
    """
    # Configurar el mock para simular un error de conexión
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

    # Ejecutar la función
    result = get_stations_data()

    # Verificar que el resultado es None cuando hay un error de conexión
    assert result is None, "La función debe devolver None cuando hay un error de conexión"

def test_get_station_info_success(sample_stations_data):
    """
    Prueba la función get_station_info cuando se busca una estación que existe
    """
    # Buscar la estación con ID "1"
    result = get_station_info(sample_stations_data, "1")

    # Verificar que se encontró la estación correcta
    assert result is not None, "La función debe encontrar la estación solicitada"
    assert result["station_id"] == "1", "La estación encontrada debe tener el ID correcto"
    assert result["name"] == "GRAN VIA CORTS CATALANES, 760", "La estación debe tener el nombre correcto"

def test_get_station_info_not_found(sample_stations_data):
    """
    Prueba la función get_station_info cuando se busca una estación que no existe
    """
    # Buscar una estación que no existe
    result = get_station_info(sample_stations_data, "999")

    # Verificar que el resultado es None
    assert result is None, "La función debe devolver None cuando la estación no existe"

def test_get_station_info_invalid_input():
    """
    Prueba la función get_station_info cuando los datos de entrada son inválidos
    """
    # Verificar con datos de entrada None
    assert get_station_info(None, "1") is None, "La función debe devolver None cuando stations_data es None"

    # Verificar con datos de entrada con formato incorrecto (sin estaciones)
    invalid_data = {"other_field": "value"}
    assert get_station_info(invalid_data, "1") is None, "La función debe devolver None cuando stations_data no tiene la estructura esperada"

def test_get_station_coordinates_success(sample_stations_data):
    """
    Prueba la función get_station_coordinates cuando la estación tiene coordenadas
    """
    # Obtener la información de una estación
    station_info = get_station_info(sample_stations_data, "1")

    # Obtener las coordenadas
    coordinates = get_station_coordinates(station_info)

    # Verificar que las coordenadas son correctas
    assert coordinates is not None, "La función debe devolver un valor no nulo"
    assert isinstance(coordinates, tuple), "La función debe devolver una tupla"
    assert len(coordinates) == 2, "La tupla debe tener dos elementos"
    assert coordinates == (41.3979779, 2.1801069), "Las coordenadas deben ser correctas"

def test_get_station_coordinates_missing_fields():
    """
    Prueba la función get_station_coordinates cuando faltan campos en la información de la estación
    """
    # Estación sin coordenadas
    station_without_coords = {"station_id": "999", "name": "Test Station"}
    assert get_station_coordinates(station_without_coords) is None, "Debe devolver None cuando faltan coordenadas"

    # Estación sin latitud
    station_without_lat = {"station_id": "999", "name": "Test Station", "lon": 2.1801069}
    assert get_station_coordinates(station_without_lat) is None, "Debe devolver None cuando falta la latitud"

    # Estación sin longitud
    station_without_lon = {"station_id": "999", "name": "Test Station", "lat": 41.3979779}
    assert get_station_coordinates(station_without_lon) is None, "Debe devolver None cuando falta la longitud"

def test_get_station_coordinates_invalid_input():
    """
    Prueba la función get_station_coordinates cuando los datos de entrada son inválidos
    """
    assert get_station_coordinates(None) is None, "Debe devolver None cuando station_info es None"

def test_create_stations_dataframe_success(sample_stations_data):
    """
    Prueba la función create_stations_dataframe con datos válidos
    """
    # Crear el DataFrame
    df = create_stations_dataframe(sample_stations_data)

    # Verificar que el resultado es un DataFrame
    assert df is not None, "La función debe devolver un DataFrame"
    assert isinstance(df, pd.DataFrame), "El resultado debe ser un DataFrame de pandas"

    # Verificar las columnas
    expected_columns = ['station_id', 'lat', 'lon', 'name']
    for col in expected_columns:
        assert col in df.columns, f"El DataFrame debe contener la columna '{col}'"

    # Verificar el número de filas
    assert len(df) == 5, "El DataFrame debe contener 5 filas (una por estación)"

    # Verificar el contenido para la primera estación
    first_station = df[df['station_id'] == "1"].iloc[0]
    assert first_station['lat'] == 41.3979779, "La latitud debe ser correcta"
    assert first_station['lon'] == 2.1801069, "La longitud debe ser correcta"
    assert first_station['name'] == "GRAN VIA CORTS CATALANES, 760", "El nombre debe ser correcto"

def test_create_stations_dataframe_invalid_input():
    """
    Prueba la función create_stations_dataframe con datos de entrada inválidos
    """
    # Con datos None
    assert create_stations_dataframe(None) is None, "Debe devolver None cuando stations_data es None"

    # Con datos sin el formato esperado
    invalid_data = {"other_field": "value"}
    assert create_stations_dataframe(invalid_data) is None, "Debe devolver None cuando los datos no tienen el formato esperado"

    # Con datos vacíos
    empty_data = {"stations": []}
    df = create_stations_dataframe(empty_data)
    assert isinstance(df, pd.DataFrame), "Debe devolver un DataFrame vacío cuando no hay estaciones"
    assert len(df) == 0, "El DataFrame debe estar vacío cuando no hay estaciones"
