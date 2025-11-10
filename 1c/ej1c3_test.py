"""
Tests para el ejercicio ej1c3.py
Este archivo contiene pruebas para verificar la correcta implementación
de las clases y métodos que modelan el estado de las estaciones del sistema
de bicicletas compartidas de Barcelona mediante la API GBFS.
"""

import pytest
from datetime import datetime
import requests
from unittest.mock import patch, MagicMock

from ej1c3 import StationStatus, VehicleType, StationStatusInfo, BarcelonaBikingClient

@pytest.fixture
def sample_station_status_response():
    """
    Fixture que proporciona una respuesta de ejemplo del endpoint station_status
    """
    return {
        "last_updated": 1759835019,
        "ttl": 0,
        "data": {
            "stations": [
                {
                    "station_id": "1",
                    "num_bikes_available": 12,
                    "num_bikes_disabled": 1,
                    "num_docks_available": 33,
                    "num_docks_disabled": 0,
                    "last_reported": 1759834959,
                    "is_charging_station": True,
                    "status": "IN_SERVICE",
                    "is_installed": True,
                    "is_renting": True,
                    "is_returning": True,
                    "traffic": None,
                    "vehicle_docks_available": [
                        {
                            "vehicle_type_ids": [
                                "ICONIC",
                                "BOOST"
                            ],
                            "count": 33
                        }
                    ],
                    "vehicle_types_available": [
                        {
                            "vehicle_type_id": "BOOST",
                            "count": 3
                        },
                        {
                            "vehicle_type_id": "ICONIC",
                            "count": 9
                        }
                    ]
                },
                {
                    "station_id": "2",
                    "num_bikes_available": 2,
                    "num_bikes_disabled": 3,
                    "num_docks_available": 23,
                    "num_docks_disabled": 0,
                    "last_reported": 1759834840,
                    "is_charging_station": True,
                    "status": "IN_SERVICE",
                    "is_installed": True,
                    "is_renting": True,
                    "is_returning": True,
                    "traffic": None,
                    "vehicle_docks_available": [
                        {
                            "vehicle_type_ids": [
                                "ICONIC",
                                "BOOST"
                            ],
                            "count": 23
                        }
                    ],
                    "vehicle_types_available": [
                        {
                            "vehicle_type_id": "BOOST",
                            "count": 2
                        },
                        {
                            "vehicle_type_id": "ICONIC",
                            "count": 0
                        }
                    ]
                },
                {
                    "station_id": "9",
                    "num_bikes_available": 0,
                    "num_bikes_disabled": 1,
                    "num_docks_available": 15,
                    "num_docks_disabled": 15,
                    "last_reported": 1759834472,
                    "is_charging_station": True,
                    "status": "MAINTENANCE",
                    "is_installed": True,
                    "is_renting": False,
                    "is_returning": False,
                    "traffic": None,
                    "vehicle_docks_available": [
                        {
                            "vehicle_type_ids": [
                                "ICONIC",
                                "BOOST"
                            ],
                            "count": 15
                        }
                    ],
                    "vehicle_types_available": [
                        {
                            "vehicle_type_id": "BOOST",
                            "count": 0
                        },
                        {
                            "vehicle_type_id": "ICONIC",
                            "count": 0
                        }
                    ]
                }
            ]
        },
        "version": "2.3"
    }

@pytest.fixture
def station_data_operational():
    """
    Fixture que proporciona datos de una estación operativa
    """
    return {
        "station_id": "1",
        "num_bikes_available": 12,
        "num_bikes_disabled": 1,
        "num_docks_available": 33,
        "num_docks_disabled": 0,
        "last_reported": 1759834959,
        "is_charging_station": True,
        "status": "IN_SERVICE",
        "is_installed": True,
        "is_renting": True,
        "is_returning": True,
        "traffic": None,
        "vehicle_docks_available": [
            {
                "vehicle_type_ids": ["ICONIC", "BOOST"],
                "count": 33
            }
        ],
        "vehicle_types_available": [
            {
                "vehicle_type_id": "BOOST",
                "count": 3
            },
            {
                "vehicle_type_id": "ICONIC",
                "count": 9
            }
        ]
    }

@pytest.fixture
def station_data_maintenance():
    """
    Fixture que proporciona datos de una estación en mantenimiento
    """
    return {
        "station_id": "9",
        "num_bikes_available": 0,
        "num_bikes_disabled": 1,
        "num_docks_available": 15,
        "num_docks_disabled": 15,
        "last_reported": 1759834472,
        "is_charging_station": True,
        "status": "MAINTENANCE",
        "is_installed": True,
        "is_renting": False,
        "is_returning": False,
        "traffic": None,
        "vehicle_docks_available": [
            {
                "vehicle_type_ids": ["ICONIC", "BOOST"],
                "count": 15
            }
        ],
        "vehicle_types_available": [
            {
                "vehicle_type_id": "BOOST",
                "count": 0
            },
            {
                "vehicle_type_id": "ICONIC",
                "count": 0
            }
        ]
    }

class TestStationStatus:
    """
    Pruebas para la enumeración StationStatus
    """
    
    def test_enum_values(self):
        """
        Verificar que la enumeración StationStatus contiene los valores esperados
        """
        assert hasattr(StationStatus, 'IN_SERVICE'), "StationStatus debe tener el valor IN_SERVICE"
        assert hasattr(StationStatus, 'MAINTENANCE'), "StationStatus debe tener el valor MAINTENANCE"
        assert StationStatus.IN_SERVICE.name == 'IN_SERVICE', "El nombre del enum debe ser IN_SERVICE"
        assert StationStatus.MAINTENANCE.name == 'MAINTENANCE', "El nombre del enum debe ser MAINTENANCE"

class TestVehicleType:
    """
    Pruebas para la clase VehicleType
    """
    
    def test_vehicle_type_attributes(self):
        """
        Verificar que la clase VehicleType tiene los atributos esperados
        """
        vehicle_type = VehicleType(vehicle_type_id="BOOST", count=3)
        assert vehicle_type.vehicle_type_id == "BOOST", "El tipo de vehículo debe ser BOOST"
        assert vehicle_type.count == 3, "La cantidad debe ser 3"

class TestStationStatusInfo:
    """
    Pruebas para la clase StationStatusInfo
    """
    
    def test_creation_from_api_data(self, station_data_operational):
        """
        Verificar que se puede crear una instancia de StationStatusInfo a partir de datos de la API
        """
        station = StationStatusInfo(station_data_operational)
        
        # Verificar atributos básicos
        assert station.station_id == "1", "El ID de la estación debe ser 1"
        assert station.num_bikes_available == 12, "Debe tener 12 bicicletas disponibles"
        assert station.num_bikes_disabled == 1, "Debe tener 1 bicicleta deshabilitada"
        assert station.num_docks_available == 33, "Debe tener 33 anclajes disponibles"
        
        # Verificar estado
        assert station.status == StationStatus.IN_SERVICE, "El estado debe ser IN_SERVICE"
        assert station.is_renting is True, "La estación debe permitir alquilar"
        assert station.is_returning is True, "La estación debe permitir devolver"
        
        # Verificar última actualización
        assert station.last_reported == 1759834959, "El timestamp debe ser correcto"
    
    def test_is_operational_method(self, station_data_operational, station_data_maintenance):
        """
        Verificar que el método is_operational funciona correctamente
        """
        # Estación operativa
        station1 = StationStatusInfo(station_data_operational)
        assert station1.is_operational is True, "La estación debe estar operativa"
        
        # Estación en mantenimiento
        station2 = StationStatusInfo(station_data_maintenance)
        assert station2.is_operational is False, "La estación no debe estar operativa"
    
    def test_get_available_bikes_by_type(self, station_data_operational):
        """
        Verificar que el método get_available_bikes_by_type devuelve los datos correctos
        """
        station = StationStatusInfo(station_data_operational)
        bikes_by_type = station.get_available_bikes_by_type()
        
        # Verificar el diccionario resultante
        assert len(bikes_by_type) == 2, "Debe haber 2 tipos de bicicletas"
        assert bikes_by_type["BOOST"] == 3, "Debe haber 3 bicicletas BOOST"
        assert bikes_by_type["ICONIC"] == 9, "Debe haber 9 bicicletas ICONIC"
    
    def test_str_representation(self, station_data_operational):
        """
        Verificar que el método __str__ devuelve una representación adecuada
        """
        station = StationStatusInfo(station_data_operational)
        str_rep = str(station)
        
        # Verificar que la representación en texto contiene información importante
        assert "1" in str_rep, "La representación debe incluir el ID de la estación"
        assert "12" in str_rep, "La representación debe incluir el número de bicicletas disponibles"
        assert "IN_SERVICE" in str_rep, "La representación debe incluir el estado"

class TestBarcelonaBikingClient:
    """
    Pruebas para la clase BarcelonaBikingClient
    """
    
    @patch('ej1c3.requests.get')
    def test_get_stations_status_success(self, mock_get, sample_station_status_response):
        """
        Verificar que el método get_stations_status funciona correctamente cuando la API responde
        """
        # Configurar el mock para retornar una respuesta exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_station_status_response
        mock_get.return_value = mock_response
        
        # Crear el cliente y llamar al método
        client = BarcelonaBikingClient()
        stations, last_updated = client.get_stations_status()
        
        # Verificar que se llamó a la URL correcta
        mock_get.assert_called_once_with("https://barcelona.publicbikesystem.net/customer/gbfs/v2/en/station_status")
        
        # Verificar que se devolvieron las estaciones y el timestamp
        assert len(stations) == 3, "Deben devolverse 3 estaciones"
        assert all(isinstance(station, StationStatusInfo) for station in stations), "Todas deben ser instancias de StationStatusInfo"
        assert last_updated == 1759835019, "El timestamp de actualización debe ser correcto"
    
    @patch('ej1c3.requests.get')
    def test_get_stations_status_error(self, mock_get):
        """
        Verificar que el método get_stations_status maneja correctamente los errores
        """
        # Configurar el mock para simular un error
        mock_get.side_effect = requests.exceptions.RequestException("Error de conexión")
        
        # Crear el cliente y llamar al método
        client = BarcelonaBikingClient()
        stations, last_updated = client.get_stations_status()
        
        # Verificar que se devuelven valores nulos en caso de error
        assert stations == [], "Debe devolverse una lista vacía"
        assert last_updated is None, "El timestamp debe ser None"
    
    @patch('ej1c3.BarcelonaBikingClient.get_stations_status')
    def test_find_station_by_id(self, mock_get_stations_status, station_data_operational, station_data_maintenance):
        """
        Verificar que el método find_station_by_id encuentra correctamente una estación
        """
        # Crear instancias de estaciones para el mock
        station1 = StationStatusInfo(station_data_operational)
        station9 = StationStatusInfo(station_data_maintenance)
        
        # Configurar el mock para devolver las estaciones simuladas
        mock_get_stations_status.return_value = ([station1, station9], 1759835019)
        
        # Crear el cliente y buscar una estación
        client = BarcelonaBikingClient()
        client.station_list,last_updated = client.get_stations_status()

        found_station = client.find_station_by_id("1")
        
        # Verificar que se encontró la estación correcta
        assert found_station is not None, "La estación debe ser encontrada"
        assert found_station.station_id == "1", "Debe encontrarse la estación con ID 1"
        
        # Buscar una estación que no existe
        not_found = client.find_station_by_id("999")
        assert not_found is None, "Debe devolver None para una estación inexistente"
    
    @patch('ej1c3.BarcelonaBikingClient.get_stations_status')
    def test_get_operational_stations(self, mock_get_stations_status, station_data_operational, station_data_maintenance):
        """
        Verificar que el método get_operational_stations filtra correctamente
        """
        # Crear instancias de estaciones para el mock
        station1 = StationStatusInfo(station_data_operational)
        station9 = StationStatusInfo(station_data_maintenance)
        
        # Configurar el mock para devolver las estaciones simuladas
        mock_get_stations_status.return_value = ([station1, station9], 1759835019)
        
        # Crear el cliente y obtener estaciones operativas
        client = BarcelonaBikingClient()
        client.station_list,last_updated = client.get_stations_status()
        
        operational = client.get_operational_stations()
        
        # Verificar que solo se devuelven las estaciones operativas
        assert len(operational) == 1, "Solo debe haber 1 estación operativa"
        assert operational[0].station_id == "1", "La estación operativa debe ser la ID 1"
    
    @patch('ej1c3.BarcelonaBikingClient.get_stations_status')
    def test_get_stations_with_available_bikes(self, mock_get_stations_status, station_data_operational, station_data_maintenance):
        """
        Verificar que el método get_stations_with_available_bikes filtra correctamente
        """
        # Crear instancias de estaciones para el mock
        station1 = StationStatusInfo(station_data_operational)
        station9 = StationStatusInfo(station_data_maintenance)
        
        # Configurar el mock para devolver las estaciones simuladas
        mock_get_stations_status.return_value = ([station1, station9], 1759835019)
        
        # Crear el cliente y obtener estaciones con bicicletas disponibles
        client = BarcelonaBikingClient()
        client.station_list,last_updated = client.get_stations_status()
 
        with_bikes = client.get_stations_with_available_bikes(min_bikes=5)
        
        # Verificar que solo se devuelven estaciones con suficientes bicicletas
        assert len(with_bikes) == 1, "Solo debe haber 1 estación con más de 5 bicicletas"
        assert with_bikes[0].station_id == "1", "La estación con bicicletas debe ser la ID 1"
        
        # Probar con un umbral diferente
        with_any_bike = client.get_stations_with_available_bikes(min_bikes=1)
        assert len(with_any_bike) == 1, "Solo debe haber 1 estación con bicicletas"
