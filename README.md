# Notificador de Renovaciones - Grupo Indesco

Este proceso automatizado se encarga de enviar mensajes automáticos por WhatsApp para recordar a las personas interesadas sobre la renovación de licencias de software dentro del Grupo Indesco.

## 📦 Requisitos

- Python 3.x
- Cronjob programado en SO Linux o Automatizador de tareas de Windows
- Base de datos PostgreSQL
- Una cuenta con acceso a la API de WhatsApp (Meta)
- Archivo `.env` (importante que se llame tal cual) con las siguientes variables de entorno configuradas:

```
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=
TOKEN=
NUM_ID=
```

- En caso de ejecutar el script en un SO Ubuntu, se debe crear un ambiente virtual (solo se debe crear una vez en la misma ruta donde se aloja el script).

Nos dirigimos a la ruta donde se aloja el script

/home/soporte/ProyectosInnovacion/ChatBotNRP
├── .env
├── .git/
├── .gitignore
├── notificar_renovaciones.py

Se instala la librería de entornos virtuales de Python para Ubuntu

```bash
sudo apt-get install python3-venv
```

Creamos el entorno virtual mediante

```bash
python3 -m venv venv
```

De esta manera, debe quedar una nueva carpeta en el directorio que contiene al script de esta manera
/home/soporte/ProyectosInnovacion/ChatBotNRP
├── .env
├── .git/
├── .gitignore
├── notificar_renovaciones.py
├── venv/

Para activar el entorno virtual, se ejecuta:

```bash
source venv/bin/activate
```
O también se puede ejecutar (solo cuando hay un alias creado):

```bash
avenv
```

### 🧪 Librerías necesarias

Se instalan con:

```bash
pip install psycopg2-binary requests python-dotenv
```

## 🚀 Ejecución

Se debe ejecutar el script con:

```bash
python3 notificar_renovaciones.py
```

Se debe asegurar que:
- El entorno virtual esté activado
- El archivo `.env` esté en el mismo directorio
- La base de datos tenga las tablas `telefonos` y `listado_programas` correctamente configuradas

## 🗃️ Tablas esperadas

**Tabla `telefonos`**
| Columna       | Tipo     |
|---------------|----------|
| num_telefono  | TEXT     |

**Tabla `listado_programas`**
| Columna         | Tipo     |
|------------------|----------|
| producto         | TEXT     |
| total            | NUMERIC  |
| divisa           | TEXT     |
| proveedor        | TEXT     |
| fecha_renovacion | DATE     |

## 🔁 Flujo del proceso

El flujo general del script es el siguiente:

1. Carga las variables de entorno.
2. Se conecta a la base de datos.
3. Consulta los números de teléfono.
4. Si no hay teléfonos, finaliza el script.
5. Calcula las fechas objetivo de renovación (15 y 30 días antes).
6. Consulta productos con renovación en esas fechas.
7. Si no hay productos para renovar, finaliza el script.
8. Por cada producto, formatea el mensaje y lo envía vía API de WhatsApp.
9. Imprime si el mensaje fue enviado correctamente o si hubo errores.
10. Cierra la conexión a la base de datos.


## 📝 Notas

- El script está diseñado para ser ejecutado automáticamente mediante un cronjob diario.
- Los mensajes usan una plantilla de WhatsApp llamada `suscrip_venci`.
- Se imprime en consola el resultado de cada envío para seguimiento.
