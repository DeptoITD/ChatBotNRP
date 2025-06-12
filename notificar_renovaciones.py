#Este script se encarga de enviar mensajes automatizados para
#recordar a personas interesadas sobre la renovación de licencias de software dentro
#del Grupo Indesco

#Librerías utilizadas
import psycopg2  # Para la conexión a la base de datos
import requests  # Para las peticiones al API de Meta
import os  # Para interactuar con el sistema operativo
from datetime import datetime, timedelta  # Para poder hacer las comparaciones respectivas de fecha
from dotenv import load_dotenv  # Para leer el archivo de credenciales .env

# Cargamos variables de entorno para poder leer el archivo .env que contiene las credenciales para el funcionamiento del script
load_dotenv()  

<<<<<<< HEAD
#     #Consultar productos que vencen en esas fechas
#     cursor.execute("""
#         SELECT producto, total, fecha_renovacion
#         FROM renovaciones
#         WHERE fecha_renovacion = %s OR fecha_renovacion = %s
#     """, (fechas_objetivo[0], fechas_objetivo[1]))

#     resultados = cursor.fetchall()

#     if not resultados:
#         print("No hay renovaciones para notificar hoy.")
#     else:
#         #Agrupar por fecha
#         renovaciones_por_fecha = {}
#         for producto, total, fecha in resultados:
#             fecha_str = fecha.strftime('%Y-%m-%d')
#             if fecha_str not in renovaciones_por_fecha:
#                 renovaciones_por_fecha[fecha_str] = []
#             renovaciones_por_fecha[fecha_str].append((producto, total))

#         #Enviar mensajes por fecha
#         for fecha, productos in renovaciones_por_fecha.items():
#             mensaje = f"🔔 Recordatorio de renovaciones para el {fecha}:\n\n"
#             for producto, total in productos:
#                 mensaje += f" •Producto: {producto}\n  Total: ${total:,.2f}\n\n"

#             for numero in numeros_destino:
#                 payload = {
#                     "messaging_product": "whatsapp",
#                     "to": numero,
#                     "type": "text",
#                     "text": {
#                         "body": mensaje
#                     }
#                 }

#                 headers = {
#                     "Authorization": "Bearer EAAI5ZBpi6QCUBO8Aj2SBWZAnQFF3FRRZBZBR0TpGB9wO3OXVQOl55iEvH7hrClJhau44Jf7U4VYEKjjq1HRkZCFV239TB9L3btWKa0wrqqtGv53RKsP47clUEIPVebmsPSAHAOdI7ZCojcpmVZAgdZA7d25QuK9IPzD1fj0KjrPUEkgSKoKlmEqOql3aZBfHgIdq9PhXtodUZD",  
#                     "Content-Type": "application/json"
#                 }

#                 url = "https://graph.facebook.com/v18.0/641965869002719/messages" 
#                 response = requests.post(url, json=payload, headers=headers)

#                 if response.status_code == 200:
#                     print(f"Mensaje enviado a {numero}")
#                 else:
#                     print(f"Error al enviar a {numero}: {response.text}")

# except Exception as e:
#     print("Error:", e)

# finally:
#     if 'conexion' in locals():
#         cursor.close()
#         conexion.close()
#         print("Conexión cerrada.")

import psycopg2
import requests
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv  #se agrega para leer archivo .env

load_dotenv()


# Leer números de teléfono desde el archivo
with open("numeros.txt", "r") as archivo:
    numeros_destino = [line.strip() for line in archivo if line.strip()]

# Conectar a la base de datos
=======
>>>>>>> develop
try:
    # Conexión a la base de datos
    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cursor = conexion.cursor()

    # Leer números de teléfono desde la tabla teléfonos
    cursor.execute("SELECT num_telefono FROM telefonos")
    telefonos = [fila[0] for fila in cursor.fetchall()]
    
    #Verifico que hayan números de telefono para enviar mensajes
    if telefonos: 
        print(f'Se han cargado {len(telefonos)} para enviar los mensajes')
    else:
        print(f'No hay teléfonos para enviar mensajes')
        exit()

    # Calcular fechas objetivo (30 días y 15 días)
    hoy = datetime.now().date()
    fechas_objetivo = [hoy + timedelta(days=30), hoy + timedelta(days=15)]

    # Obtener productos a notificar mediante consulta a la base de datos.
    cursor.execute("""
<<<<<<< HEAD
        SELECT producto, total, divisa, proveedor, fecha_renovacion
        FROM renovaciones
=======
        SELECT producto, valor_total, divisa, proveedor, fecha_renovacion
        FROM listado_programas
>>>>>>> develop
        WHERE fecha_renovacion = %s OR fecha_renovacion = %s
    """, (fechas_objetivo[0], fechas_objetivo[1]))

    resultados = cursor.fetchall()

    if not resultados:
        print("No hay renovaciones para notificar hoy.")
    else:
<<<<<<< HEAD
        #573161173578
        for producto, total, divisa, proveedor, fecha in resultados:
            fecha_str = fecha.strftime('%d/%m/%Y')  # Formato requerido en la plantilla
            precio = f"{divisa} ${total:,.0f}" 
=======
        for producto, total, divisa, proveedor, fecha in resultados:
            fecha_str = fecha.strftime('%d/%m/%Y')  # Formato requerido en la plantilla
            precio = f"{divisa} ${total:,.0f}"  # Se concatena la divisa y el valor total
>>>>>>> develop

            for numero in telefonos:
                # Petición a la API de Meta
                payload = {
                    "messaging_product": "whatsapp",
                    "to": numero,
                    "type": "template",
                    "template": {
                        "name": "suscrip_venci",
                        "language": {"code": "en_US"},
                        "components": [
                            {
                                "type": "body",
                                "parameters": [
<<<<<<< HEAD
                                    { "type": "text", "text": producto },
                                    { "type": "text", "text": fecha_str },
                                    { "type": "text", "text": precio },
                                    { "type": "text", "text": proveedor }
=======
                                    {"type": "text", "text": producto},
                                    {"type": "text", "text": fecha_str},
                                    {"type": "text", "text": precio},
                                    {"type": "text", "text": proveedor}
>>>>>>> develop
                                ]
                            }
                        ]
                    }
                }
                headers = {
<<<<<<< HEAD
                    "Authorization": f"Bearer {os.getenv('TOKEN')}",  # <-- Reemplaza
=======
                    # Recordar que el token tiene una duración de 60 días.
                    "Authorization": f"Bearer {os.getenv('TOKEN')}",
>>>>>>> develop
                    "Content-Type": "application/json"
                }
                url = f"https://graph.facebook.com/v18.0/{os.getenv('NUM_ID')}/messages"

<<<<<<< HEAD
                url = f"https://graph.facebook.com/v18.0/{os.getenv('NUM_ID')}/messages"  # <-- Reemplaza también
=======
>>>>>>> develop
                response = requests.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    print(f"Mensaje enviado a {numero}")
                else:
                    print(f"Error al enviar a {numero}: {response.text}")

except Exception as e:
    print("Error general:", e)

# Cerramos la conexión a la base de datos
finally:
    if 'conexion' in locals():
        cursor.close()
        conexion.close()
        print("Conexión cerrada.")