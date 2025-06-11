import psycopg2
import requests
from datetime import datetime, timedelta

# Leer números de teléfono desde el archivo
with open("numeros.txt", "r") as archivo:
    numeros_destino = [line.strip() for line in archivo if line.strip()]

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
        SELECT producto, total, fecha_renovacion
        FROM listado_programas
        WHERE fecha_renovacion = %s OR fecha_renovacion = %s
    """, (fechas_objetivo[0], fechas_objetivo[1]))

    resultados = cursor.fetchall()

    if not resultados:
        print("No hay renovaciones para notificar hoy.")
    else:
        for producto, total, fecha in resultados:
            fecha_str = fecha.strftime('%d/%m/%Y')  # Formato requerido en la plantilla

            for numero in numeros_destino:
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
                    "Authorization": "Bearer EAAI5ZBpi6QCUBO9ZBUGqTexSs8DtZAAKpSyWmTqnMjpT0EJMrbKZC83ZBn8w6FZB19WlNY5URaGt8dy9MZC2BYEOO8sHZB9qtpdsDeuN5FuLaIg2jSDl3EA2vhzVaUeww6cwooffy3ZBaL8bjYbujH9jC87rHY3XtYLpleZAfFZAZCPZCZBUFZAImyl1IYaqaDxYK9TvT2zJfGXQqcZD",  # <-- Reemplaza
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
