"""
Enunciado:
Introducción básica a la biblioteca requests de Python.
La biblioteca requests permite realizar peticiones HTTP de forma sencilla.

En este ejercicio, aprenderás a:
1. Realizar una petición GET a una API pública
2. Interpretar una respuesta en formato texto plano
3. Manejar errores en peticiones HTTP

Tu tarea es completar la función indicada para realizar una consulta básica
a la API de ipify.org, un servicio estable que proporciona la IP pública.
"""

import requests

def get_user_ip():
    """
    Realiza una petición GET a api.ipify.org para obtener la dirección IP pública
    en formato texto plano.

    Returns:
        str: La dirección IP si la petición es exitosa
        None: Si ocurre un error en la petición
    """
    # Completa esta función para:
    # 1. Realizar una petición GET a la URL https://api.ipify.org (sin parámetros)
    # 2. Verificar si la petición fue exitosa (código 200)
    # 3. Devolver el texto de la respuesta directamente (contiene la IP)
    # 4. Devolver None si hay algún error
    
    # Encara que no molt "ELEGANT", posarem el la direcció URL com a parametre de la funció 
    # (es per no fallar el els tests)
    url_addr='https://api.ipify.org/'

    # crido a la funció GET 
    try:
        response = requests.get(url_addr)

        # as raise_for_status is not working with "pytests, Mock" modules, we need to process errors by hand
        # print(response.raise_for_status())
        
        # comprobo que el codi és 2XX
        if response.status_code>=200 and response.status_code<299:
            # retorno el content que en aquest cas esta codificat com 'ascii'
            return response.text
        else:
            # Si el codi es diferent, retorno None: errors o redireccions (codis 1XX, 3XX, 4XX o 5XX)
            return None
    

    # s'ha produït un error, i retorno "none"
    except:
        # si hi ha algun altre problema en connectar, torna un None
        return None

if __name__ == "__main__":
    # Ejemplo de uso de la función
    ip = get_user_ip()
    if ip:
        print(f"Tu dirección IP pública es: {ip}")
    else:
        print("No se pudo obtener la dirección IP")
