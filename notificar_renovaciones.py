import psycopg2        #Conecceion con la DB
import pandas as pd    #Leer y escribir archivos de datos como CSV, Excel
import requests        #para las peticiones
from datetime import datetime, timedelta
#                                                   actualizar fechas asumiendo pagoo
#Leer números cel
with open("numeros.txt", "r") as archivo:
    numeros_destino = [line.strip() for line in archivo if line.strip()]

#Conectar a la base de datos 
try:
    conexion = psycopg2.connect(
        host="localhost",
        database="renovaciones",
        user="postgres",
        password="1234",
        port=5432
    )
    cursor = conexion.cursor()

    #Calcular fechas objetivo (30 y 15 días desde hoy)
    hoy = datetime.now().date()
    fechas_objetivo = [hoy + timedelta(days=30), hoy + timedelta(days=15)]

    #Consultar productos que vencen en esas fechas
    cursor.execute("""
        SELECT producto, total, fecha_renovacion
        FROM renovaciones
        WHERE fecha_renovacion = %s OR fecha_renovacion = %s
    """, (fechas_objetivo[0], fechas_objetivo[1]))

    resultados = cursor.fetchall()

    if not resultados:
        print("No hay renovaciones para notificar hoy.")
    else:
        #Agrupar por fecha
        renovaciones_por_fecha = {}
        for producto, total, fecha in resultados:
            fecha_str = fecha.strftime('%Y-%m-%d')
            if fecha_str not in renovaciones_por_fecha:
                renovaciones_por_fecha[fecha_str] = []
            renovaciones_por_fecha[fecha_str].append((producto, total))

        #Enviar mensajes por fecha
        for fecha, productos in renovaciones_por_fecha.items():
            mensaje = f"🔔 Recordatorio de renovaciones para el {fecha}:\n\n"
            for producto, total in productos:
                mensaje += f" •Producto: {producto}\n  Total: ${total:,.2f}\n\n"

            for numero in numeros_destino:
                payload = {
                    "messaging_product": "whatsapp",
                    "to": numero,
                    "type": "text",
                    "text": {
                        "body": mensaje
                    }
                }

                headers = {
                    "Authorization": "Bearer EAAI5ZBpi6QCUBO0B65eYm7fIIAXIb3ZCMuhZBwRKCfZAiQSRJu8g41GHpGcy75XAU8jYkE3lEOYX3vbWpXysZAMx0SGeQRDRc1Yc2nZAji5ZAcZBwPgZCahJm0Yh9GDrmP1CLXgLV8RZA0MAUo43MD3ri8zZB3szGFiB9IZBOJ5c0wOaZAJdA9QCW5W46gC2e8K9FZAGwjYGgZBvZB0kE0w5OVhLichTu8ZBQxmGFKPG91Fn7RMx4ZCAZDZD",  
                    "Content-Type": "application/json"
                }

                url = "https://graph.facebook.com/v18.0/641965869002719/messages" 
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    print(f"Mensaje enviado a {numero}")
                else:
                    print(f"Error al enviar a {numero}: {response.text}")

except Exception as e:
    print("Error:", e)

finally:
    if 'conexion' in locals():
        cursor.close()
        conexion.close()
        print("Conexión cerrada.")
