# Este script se encarga de actualizar automáticamente la base de datos
# del chatbot para la notificación periódica de eventos.

import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta #Librería útil para incrementar los meses a la base de datos

# Cargar variables del entorno (.env) (mismas credenciales para la base de datos)
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

    # Obtener la fecha de hoy
    hoy = datetime.now().date()

    # Consultar productos cuya fecha_renovacion coincide con la fecha actual.
    cursor.execute("""
        SELECT id, fecha_renovacion, tiempo_renovacion
        FROM listado_programas
        WHERE fecha_renovacion = %s
    """, (hoy,))

    filas = cursor.fetchall()

    if not filas:
        print("No hay renovaciones para actualizar hoy.")
    else:
        for fila in filas:
            id_producto = fila[0]
            fecha_actual = fila[1]
            meses = fila[2]

            # Sumar los meses a la fecha actual
            nueva_fecha = fecha_actual + relativedelta(months=meses)

            # Actualizar la fecha en la base de datos
            cursor.execute("""
                UPDATE listado_programas
                SET fecha_renovacion = %s
                WHERE id = %s
            """, (nueva_fecha, id_producto))

            print(f"[✔] Producto con ID {id_producto} actualizado a {nueva_fecha}")

        # Confirmar los cambios
        conexion.commit()

except Exception as e:
    print("Error al actualizar fechas de renovación:", e)

finally:
    if 'conexion' in locals():
        cursor.close()
        conexion.close()
        print("Conexión cerrada.")