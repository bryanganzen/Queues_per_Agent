# Queues_per_Agent
Este desarrollo otorga un excel con los id, nombre y estado de las queues por usuario de genesys cloud por organización

## Funcionalidades

1. **Obtención del Token de Acceso**:
   - A través de una función, se realiza una solicitud HTTP `GET` a una URL configurada para obtener el token de acceso de la API.
   
2. **Listar Usuarios**:
   - Recupera todos los usuarios de la organización seleccionada, paginando los resultados si es necesario.
   
3. **Obtener Colas de Usuario**:
   - Recupera las colas asociadas a cada usuario y el estado de participación en cada cola (`Activada` o `Desactivada`).

4. **Generación de Archivo Excel**:
   - Los resultados obtenidos se almacenan en un archivo Excel para un análisis y revisión más fácil. El archivo es nombrado según la organización seleccionada.

## Estructura del Código

- `obtener_token_de_acceso(token_url)`: Obtiene el token de acceso a partir de una URL específica.
- `listar_usuarios(token, host)`: Lista todos los usuarios de la organización especificada mediante llamadas a la API.
- `obtener_queues_usuario(token, user_id, host)`: Obtiene las colas asociadas a un usuario en particular.

## Configuración y Uso

### Prerrequisitos

- Python 3.x
- Librerías: `requests`, `pandas`, `time`

Instala las librerías necesarias ejecutando:
```bash
pip install requests pandas
```

## Ejecución

- Al ejecutar el código, se solicita al usuario ingresar el nombre de la organización (1 o 2).
- El programa configura la URL y el host de la API en función de la selección realizada.
- Se obtienen los usuarios y las colas asociadas, y los resultados se guardan en un archivo Excel con un nombre que incluye la organización seleccionada.

## Ejemplo de Ejecución

```bash
python queues_agent.py
```

## Output

El archivo Excel generado contiene las siguientes columnas:

- **Usuario:** Nombre del usuario.
- **Queue:** Nombre de la cola asociada.
- **Estado:** Estado de participación del usuario en la cola (Activada/Desactivada).

## Tiempo de Ejecución

El código muestra el tiempo de ejecución de cada sección principal:

- **Tiempo en obtener usuarios:** Tiempo para listar todos los usuarios de la organización.
- **Tiempo en obtener las queues:** Tiempo para obtener las colas de cada usuario.
- **Tiempo total del proceso:** Tiempo total de ejecución del programa.

## Ejemplo de Salida

- **1** Ingresa el nombre de la organización (1 o 2): 1
- **2** Cargando el informe, esto puede tardar un momento...
- **2.1** Tiempo en obtener usuarios: 3.45 segundos
- **2.2** Tiempo en obtener las queues: 2.78 segundos
- **3** Proceso finalizado. Los datos se han guardado en 'usuarios_queues_organización_1.xlsx'.
- **3.1** Tiempo total del proceso: 6.23 segundos
