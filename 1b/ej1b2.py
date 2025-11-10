"""
Enunciado:
Manejo avanzado de errores HTTP con la biblioteca requests de Python.

En este ejercicio, aprenderás a:
1. Realizar peticiones a diferentes URLs que generarán distintos códigos de estado HTTP
2. Diferenciar entre varios tipos de errores HTTP (4xx, 5xx)
3. Manejar redirecciones (códigos 3xx)
4. Extraer información detallada de las respuestas de error
5. Procesar respuestas JSON con información específica sobre el estado

Tu tarea es completar la función request_with_error_handling para manejar adecuadamente
diferentes tipos de respuestas HTTP, incluyendo errores cliente (4xx), errores servidor (5xx)
y redirecciones (3xx).

Nota: El servidor httpstatuses.maor.io devuelve respuestas JSON con la siguiente estructura:

{
    "code": 404,
    "description": "Not Found"
}

Deberás comprobar que el código en el encabezado HTTP coincide con el campo "code"
en el cuerpo JSON y usar el campo "description" para proporcionar información detallada.
"""

import requests

def request_with_error_handling(url):
    """
    Realiza una petición GET a la URL proporcionada y maneja los diferentes tipos de
    respuestas HTTP que puedan ocurrir.

    Args:
        url (str): La URL a la que se realizará la petición

    Returns:
        dict: Un diccionario con la siguiente información:
            - success (bool): True si la petición fue exitosa (código 2xx), False en otro caso
            - status_code (int): El código de estado HTTP
            - is_redirect (bool): True si la respuesta es una redirección (código 3xx)
            - redirect_url (str, opcional): URL de redirección si is_redirect es True
            - error_type (str, opcional): "client_error" para 4xx, "server_error" para 5xx
            - message (str): Un mensaje descriptivo sobre el resultado de la petición
    """
    # Completa esta función para manejar diferentes tipos de respuestas HTTP
    # Debes gestionar al menos:
    # - Respuestas exitosas (códigos 2xx)
    # - Redirecciones (códigos 3xx)
    # - Errores del cliente (códigos 4xx)
    # - Errores del servidor (códigos 5xx)

    # Inicialitzo dictionari per retorn d'informació amb valors per defecte
    data = {
        'success': False,
        'status_code': int(0),
        'message': '',
        'is_redirect': False,
        'redirect_url': ''
    }

    try:
        print(f'------> (1) URL: {url}')
        response = requests.get(url)
        print('-----> (2) SERVER REPLIED')

        response_body = response.json()

        # processo els status code
        sc = int(response.status_code/100)
        print(f'------> (3) **** SC: {sc}')
        print(f'------> (4) ***** BODY: {response_body}')
        
        # comprovo que el codi al "header" és el mateix que en el message body --> si no genero una excepció
        if int(response_body['code']) != int(response.status_code):
            print("--- (5) ERROR DIFFERENTS CODES")
            raise ValueError("code in body and header do not match")

        # modifico diccionari amb els valors independents del resultat
        data['status_code']=response_body['code']  # alternatively: response.status_code
        data['message'] = response_body['description'] # alternatively: response.reason
        print(f'---------------->\n{data}\n<--------------------')
        if sc == 1 or sc == 2:
            # response 1XX o 2XX o 3XX
            data['success']=True  
            
        elif sc == 3:
        # response to 3XX
            data['success']=False
            # info sobre redireccó
            data['is_redirect'] = True
            # servidor ha de respondre amb la redirecció en un camp 'location' al header
            # no obstant, no és obligatori
            data['redirect_url'] = response.headers.get('location1',"")

        # error de client o servidor 4XX, 5XX
        elif sc == 4 or sc == 5:
            data['success']=False
            data['error_type'] = 'client_error' if sc == 4 else 'server_error'
    
    except requests.exceptions.ConnectionError as err:
        data['message']= 'connection_error'
        print(f'Connection Error:\n{err}')
            
    return data

    


if __name__ == "__main__":
    # Puedes probar tu función con estas URLs:

    # Para probar un error 404 (Not Found)
    print("Probando URL con error 404:")
    result = request_with_error_handling("https://httpstatuses.maor.io/404")
    print(f"Resultado: {result}")

    # Para probar un error 500 (Server Error)
    print("\nProbando URL con error 500:")
    result = request_with_error_handling("https://httpstatuses.maor.io/500")
    print(f"Resultado: {result}")

    # Para probar una redirección 301 (Moved Permanently)
    print("\nProbando URL con redirección 301:")
    result = request_with_error_handling("https://httpstatuses.maor.io/301")
    print(f"Resultado: {result}")

    # Para probar una respuesta exitosa
    print("\nProbando URL con respuesta exitosa:")
    result = request_with_error_handling("https://httpstatuses.maor.io/200")
    print(f"Resultado: {result}")
