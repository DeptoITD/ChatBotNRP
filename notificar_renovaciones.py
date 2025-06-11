import psycopg2
import requests
from datetime import datetime, timedelta

# Leer números de teléfono desde la tabla telefonos en la base de datos eventos_chatbot
# with open("numeros.txt", "r") as archivo:
#     numeros_destino = [line.strip() for line in archivo if line.strip()]
try:
    conexion = psycopg2.connect(
        host = "localhost",
        database = "eventos_chatbot",
        user = "chatbot",
        password = "IND_chatbot2025",
        port = 5432
    )

    cursor = conexion.cursor()

    # Ejecutar consulta para obtener los números de teléfono
    cursor.execute("SELECT num_telefono FROM telefonos") 

    #Recuperamos los datos de la consulta
    resultados = cursor.fetchall()
    telefonos = [fila[0] for fila in resultados]
    print (telefonos)     

except Exception as e:
    print("No se puede conectar a la base de datos: ", e)


# Conectar a la base de datos
try:
    conexion = psycopg2.connect(
        host="localhost",
        database="eventos_chatbot",
        user="chatbot",
        password="IND_chatbot2025",
        port=5432
    )
    cursor = conexion.cursor()

    # Calcular fechas objetivo (30 y 15 días desde hoy)
    hoy = datetime.now().date()
    fechas_objetivo = [hoy + timedelta(days=30), hoy + timedelta(days=15)]

    # Consultar productos que vencen en esas fechas
    cursor.execute("""
        SELECT producto, valor_total, fecha_renovacion
        FROM listado_programas
        WHERE fecha_renovacion = %s OR fecha_renovacion = %s
    """, (fechas_objetivo[0], fechas_objetivo[1]))

    resultados = cursor.fetchall()

    if not resultados:
        print("No hay renovaciones para notificar hoy.")
    else:
        for producto, total, fecha in resultados:
            fecha_str = fecha.strftime('%d/%m/%Y')  # Formato requerido en la plantilla

            for numero in telefonos:
                payload = {
                    "messaging_product": "whatsapp",
                    "to": numero,
                    "type": "template",
                    "template": {
                        "name": "suscrip_venci",
                        "language": { "code": "en_US" },
                        "components": [
                            {
                                "type": "body",
                                "parameters": [
                                    { "type": "text", "text": producto },
                                    { "type": "text", "text": fecha_str },
                                    { "type": "text", "text": f"${total:,.0f}" }
                                ]
                            }
                        ]
                    }
                }

                headers = {
                    "Authorization": "Bearer EAAI5ZBpi6QCUBOz94ScqRczRf3v0VXZAwKK2ZAwTS817OYaZAOkYHw4cu54L1SG51lgHDZAeLM3mtTAo5cPfHvVuVXvWFBDUDKtx2Yfv2K4ZBNH1tzFRKAaQnh4RbfST0AV3QrqTaV84JO1XhIpTyXEBaOaWcU3voom1o4TS5FzKYbvr1NR2ftvdPNjNeZAovZBQh3nMTP1y50zszLoX",  # <-- Reemplaza
                    "Content-Type": "application/json"
                }

                url = "https://graph.facebook.com/v18.0/641965869002719/messages"  # <-- Reemplaza también
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    print(f" Mensaje enviado a {numero}")
                else:
                    print(f" Error al enviar a {numero}: {response.text}")

except Exception as e:
    print(" Error general:", e)

finally:
    if 'conexion' in locals():
        cursor.close()
        conexion.close()
        print("Conexión cerrada.")
