# Este script se encarga de enviar mensajes automatizados para
# recordar a personas interesadas sobre la renovación de licencias de software dentro
# del Grupo Indesco

# Librerías utilizadas
import psycopg2
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

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
    
    if not telefonos:
        print("No hay teléfonos para enviar mensajes")
        exit()
    else:
        print(f'Se han cargado {len(telefonos)} números para enviar mensajes')

    # Calcular fechas objetivo (30 días y 15 días)
    hoy = datetime.now().date()
    fechas_objetivo = [hoy + timedelta(days=30), hoy + timedelta(days=15)]

    # Consultar productos con renovación próxima
    cursor.execute("""
        SELECT producto, total, divisa, proveedor, fecha_renovacion
        FROM renovaciones
        WHERE fecha_renovacion = %s OR fecha_renovacion = %s
    """, (fechas_objetivo[0], fechas_objetivo[1]))

    resultados = cursor.fetchall()

    if not resultados:
        print("No hay renovaciones para notificar hoy.")
    else:
        for producto, total, divisa, proveedor, fecha in resultados:
            fecha_str = fecha.strftime('%d/%m/%Y')
            precio = f"{divisa} ${total:,.0f}"

            for numero in telefonos:
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
                                    {"type": "text", "text": producto},
                                    {"type": "text", "text": fecha_str},
                                    {"type": "text", "text": precio},
                                    {"type": "text", "text": proveedor}
                                ]
                            }
                        ]
                    }
                }

                headers = {
                    "Authorization": f"Bearer {os.getenv('TOKEN')}",
                    "Content-Type": "application/json"
                }

                url = f"https://graph.facebook.com/v18.0/{os.getenv('NUM_ID')}/messages"
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    print(f"Mensaje enviado a {numero}")
                else:
                    print(f"Error al enviar a {numero}: {response.text}")

except Exception as e:
    print("Error general:", e)

finally:
    if 'conexion' in locals():
        cursor.close()
        conexion.close()
        print("Conexión cerrada.")
