import psycopg2
import pandas as pd

# Leer el CSV con codificación correcta
df = pd.read_csv("programasLISTADOS.csv", encoding="latin1")

# Renombrar columnas para evitar errores por tildes o espacios
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("á", "a")
    .str.replace("é", "e")
    .str.replace("í", "i")
    .str.replace("ó", "o")
    .str.replace("ú", "u")
)

print("Columnas detectadas:", df.columns.tolist())

# Limpiar columna total para convertirla a número
df['total'] = (
    df['total']
    .replace(r'[$,]', '', regex=True)
    .astype(float)
)


try:
    conexion = psycopg2.connect(
        host="localhost",
        database="renovaciones",
        user="postgres",
        password="1234",
        port=5432
    )
    cursor = conexion.cursor()

    for index, fila in df.iterrows():
        fecha = pd.to_datetime(fila['fecha_de_renovacion'], errors='coerce')
        fecha_final = fecha.date() if pd.notnull(fecha) else None

        sql = """
        INSERT INTO renovaciones (producto, total, fecha_renovacion)
        VALUES (%s, %s, %s)
        """
        valores = (
            fila['producto'],
            fila['total'],
            fecha_final
        )
        cursor.execute(sql, valores)

    conexion.commit()
    print("Datos del CSV insertados correctamente.")

except Exception as e:
    print("Error:", e)

finally:
    if conexion:
        cursor.close()
        conexion.close()
        print("Conexión cerrada.")
