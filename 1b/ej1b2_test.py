"""
Tests para el ejercicio ej1b2.py
Este archivo contiene pruebas para verificar la correcta implementación
de la función request_with_error_handling para gestionar diferentes tipos de errores HTTP.
"""

import pytest
import requests
import responses
from unittest.mock import patch, Mock

from ej1b2 import request_with_error_handling

@pytest.fixture
def mock_responses():
    """
    Fixture para configurar respuestas simuladas para las peticiones HTTP
    """
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        # Configurar respuesta 404 - Not Found
        rsps.add(
            responses.GET,
            "https://httpstatuses.maor.io/404",
            json={"code": 404, "description": "Not Found"},
            status=404,
            content_type="application/json"
        )

        # Configurar respuesta 500 - Server Error
        rsps.add(
            responses.GET,
            "https://httpstatuses.maor.io/500",
            json={"code": 500, "description": "Internal Server Error"},
            status=500,
            content_type="application/json"
        )

        # Configurar respuesta 301 - Redirección
        rsps.add(
            responses.GET,
            "https://httpstatuses.maor.io/301",
            json={"code": 301, "description": "Moved Permanently"},
            status=301,
            headers={"Location1": "https://httpstatuses.maor.io/"},
            content_type="application/json"
        )

        # Configurar respuesta 200 - OK
        rsps.add(
            responses.GET,
            "https://httpstatuses.maor.io/200",
            json={"code": 200, "description": "OK"},
            status=200,
            content_type="application/json"
        )

        yield rsps

def test_404_client_error(mock_responses):
    """
    Prueba la función request_with_error_handling cuando se produce un error 404 (client error).
    """
    url = "https://httpstatuses.maor.io/404"
    result = request_with_error_handling(url)

    # Verificaciones básicas
    assert isinstance(result, dict), "La función debe devolver un diccionario"

    # Verificación de campos obligatorios
    assert 'success' in result, "El resultado debe contener el campo 'success'"
    assert 'status_code' in result, "El resultado debe contener el campo 'status_code'"
    assert 'is_redirect' in result, "El resultado debe contener el campo 'is_redirect'"
    assert 'message' in result, "El resultado debe contener el campo 'message'"

    # Verificación de valores para el caso específico
    assert result['success'] is False, "Para un 404, 'success' debe ser False"
    assert result['status_code'] == 404, "El código de estado debe ser 404"
    assert result['is_redirect'] is False, "Para un 404, 'is_redirect' debe ser False"
    assert 'error_type' in result, "El resultado debe contener el campo 'error_type' para errores"
    assert result['error_type'] == 'client_error', "Para un 404, 'error_type' debe ser 'client_error'"

def test_500_server_error(mock_responses):
    """
    Prueba la función request_with_error_handling cuando se produce un error 500 (server error).
    """
    url = "https://httpstatuses.maor.io/500"
    result = request_with_error_handling(url)

    # Verificaciones básicas
    assert isinstance(result, dict), "La función debe devolver un diccionario"

    # Verificación de campos obligatorios
    assert 'success' in result, "El resultado debe contener el campo 'success'"
    assert 'status_code' in result, "El resultado debe contener el campo 'status_code'"
    assert 'is_redirect' in result, "El resultado debe contener el campo 'is_redirect'"
    assert 'message' in result, "El resultado debe contener el campo 'message'"

    # Verificación de valores para el caso específico
    assert result['success'] is False, "Para un 500, 'success' debe ser False"
    assert result['status_code'] == 500, "El código de estado debe ser 500"
    assert result['is_redirect'] is False, "Para un 500, 'is_redirect' debe ser False"
    assert 'error_type' in result, "El resultado debe contener el campo 'error_type' para errores"
    assert result['error_type'] == 'server_error', "Para un 500, 'error_type' debe ser 'server_error'"

def test_301_redirect(mock_responses):
    """
    Prueba la función request_with_error_handling cuando se produce una redirección 301.
    """
    url = "https://httpstatuses.maor.io/301"
    result = request_with_error_handling(url)

    # Verificaciones básicas
    assert isinstance(result, dict), "La función debe devolver un diccionario"

    # Verificación de campos obligatorios
    assert 'success' in result, "El resultado debe contener el campo 'success'"
    assert 'status_code' in result, "El resultado debe contener el campo 'status_code'"
    assert 'is_redirect' in result, "El resultado debe contener el campo 'is_redirect'"
    assert 'message' in result, "El resultado debe contener el campo 'message'"

    # Verificación de valores para el caso específico
    assert result['success'] is False, "Para un 301, 'success' debe ser False (es una redirección)"
    assert result['status_code'] == 301, "El código de estado debe ser 301"
    assert result['is_redirect'] is True, "Para un 301, 'is_redirect' debe ser True"
    assert 'redirect_url' in result, "El resultado debe contener el campo 'redirect_url' para redirecciones"
    assert result['redirect_url'] == "https://httpstatuses.maor.io/", "La URL de redirección debe ser correcta"

def test_200_success(mock_responses):
    """
    Prueba la función request_with_error_handling cuando se produce una respuesta exitosa 200.
    """
    url = "https://httpstatuses.maor.io/200"
    result = request_with_error_handling(url)

    # Verificaciones básicas
    assert isinstance(result, dict), "La función debe devolver un diccionario"

    # Verificación de campos obligatorios
    assert 'success' in result, "El resultado debe contener el campo 'success'"
    assert 'status_code' in result, "El resultado debe contener el campo 'status_code'"
    assert 'is_redirect' in result, "El resultado debe contener el campo 'is_redirect'"
    assert 'message' in result, "El resultado debe contener el campo 'message'"

    # Verificación de valores para el caso específico
    assert result['success'] is True, "Para un 200, 'success' debe ser True"
    assert result['status_code'] == 200, "El código de estado debe ser 200"
    assert result['is_redirect'] is False, "Para un 200, 'is_redirect' debe ser False"
    assert 'error_type' not in result, "No debe haber campo 'error_type' para respuestas exitosas"

def test_connection_error():
    """
    Prueba la función request_with_error_handling cuando se produce un error de conexión.
    """
    with patch('requests.get') as mock_get:
        # Configurar el mock para simular un error de conexión
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        url = "https://nonexistentserver.error"
        result = request_with_error_handling(url)

        # Verificaciones básicas
        assert isinstance(result, dict), "La función debe devolver un diccionario incluso en caso de error de conexión"

        # Verificación de campos obligatorios
        assert 'success' in result, "El resultado debe contener el campo 'success'"
        assert 'message' in result, "El resultado debe contener el campo 'message'"

        # Verificación de valores para el caso específico
        assert result['success'] is False, "Para un error de conexión, 'success' debe ser False"
        assert 'connection_error' in str(result['message']).lower(), "El mensaje debe indicar que hubo un error de conexión"
