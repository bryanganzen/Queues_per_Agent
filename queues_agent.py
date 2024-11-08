import requests
import pandas as pd
import time


def obtener_token_de_acceso(token_url):
    """
    Función para obtener el token de acceso desde una URL especificada.

    Args:
        token_url (str): URL del servicio para obtener el token.

    Returns:
        str: Token de acceso si se obtiene correctamente.
        None: Si ocurre algún error al obtener el token.
    """
    response = requests.get(token_url)
    if response.status_code == 200:
        access_token = response.json().get('token')
        return access_token
    else:
        print(f"Error al obtener el token de acceso: {response.status_code}")
        return None

def listar_usuarios(token, host):
    """
    Función para listar todos los usuarios de una organización usando la API de Genesys Cloud.

    Args:
        token (str): Token de acceso válido.
        host (str): URL del host de la API de Genesys Cloud.

    Returns:
        list: Lista de usuarios obtenidos desde la API.
    """
    url = f"{host}/api/v2/users"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    page_number = 1
    page_size = 25
    usuarios = []

    while True:
        params = {
            'pageNumber': page_number,
            'pageSize': page_size
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            usuarios.extend(data.get('entities', []))  # Agregar los usuarios obtenidos a la lista

            if page_number >= data.get('pageCount', 1):  # Verifica si hay más páginas de resultados
                break
            else:
                page_number += 1  # Incrementar el número de página para la siguiente solicitud
        else:
            print(f"Error al obtener usuarios: {response.status_code}, {response.text}")
            break

    return usuarios

def obtener_queues_usuario(token, user_id, host):
    """
    Función para obtener las colas (queues) de un usuario específico.

    Args:
        token (str): Token de acceso válido.
        user_id (str): ID del usuario.
        host (str): URL del host de la API de Genesys Cloud.

    Returns:
        list: Lista de colas asociadas al usuario.
        []: Lista vacía si ocurre un error o si el usuario no tiene colas asociadas.
    """
    url = f"{host}/api/v2/users/{user_id}/queues"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('entities', [])
    else:
        print(f"Error al obtener queues para el usuario {user_id}: {response.status_code}, {response.text}")
        return []

# Solicitar el nombre de la organización
nombre_entidad = input("Ingresa el nombre de la organización (1 o 2): ").strip().upper()

# Configurar la URL del token y el host de acuerdo a la organización
if nombre_entidad == "1":
    token_url = 'url para obtener el token de la organización 1'
    host = 'host de la región de la organización 1'
    nombre_archivo = "usuarios_queues_organización_{nombre_entidad}.xlsx"
elif nombre_entidad == "2":
    token_url = 'url para obtener el token de la organización 2'
    host = 'host de la región de la organización 2'
    nombre_archivo = "suarios_queues_organización_{nombre_entidad}.xlsx"
else:
    print("Organización no válida. Debe ser 'UNITEC' o 'UVM'.")
    exit()

print("Cargando el informe, esto puede tardar un momento...")

# Marcar el tiempo inicial del proceso total
start_time_total = time.time()

# Obtener el token de acceso
token = obtener_token_de_acceso(token_url)

# Lista para almacenar los resultados
resultados = []

if token:
    # Obtener los usuarios
    start_time_users = time.time()
    usuarios = listar_usuarios(token, host)
    end_time_users = time.time()
    print(f"Tiempo en obtener usuarios: {end_time_users - start_time_users:.2f} segundos")

    # Obtener las queues asociadas a los usuarios
    start_time_queues = time.time()
    for usuario in usuarios:
        user_id = usuario['id']
        user_name = usuario['name']

        # Obtener las queues para cada usuario
        queues = obtener_queues_usuario(token, user_id, host)

        if not queues:  # Si el usuario no tiene colas asociadas
            resultados.append({"Usuario": user_name, "Queue": "N/A", "Estado": "N/A"})
        else:
            for queue in queues:  # Para cada cola obtenida del usuario
                queue_name = queue['name']
                queue_joined = "Activada" if queue['joined'] else "Desactivada"
                resultados.append({"Usuario": user_name, "Queue": queue_name, "Estado": queue_joined})

    end_time_queues = time.time()
    print(f"Tiempo en obtener las queues: {end_time_queues - start_time_queues:.2f} segundos")

# Crear un DataFrame con los resultados y guardarlo en un archivo Excel
df = pd.DataFrame(resultados)
df.to_excel(nombre_archivo, index=False)

# Marcar el tiempo final del proceso total
end_time_total = time.time()

print(f"Proceso finalizado. Los datos se han guardado en '{nombre_archivo}'.")
print(f"Tiempo total del proceso: {end_time_total - start_time_total:.2f} segundos")
