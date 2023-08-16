import sqlite3
from tabulate import tabulate
import keyboard

def reporte_diario2():

    # Conexión a la base de datos
    conn = sqlite3.connect('bursatil.db')
    cursor = conn.cursor()

    # Ejecución de la consulta SQL
    cursor.execute("""
        SELECT * FROM (
            SELECT
                c.ticker,
                MAX(CASE WHEN i.rsi < 30 THEN i.date ELSE NULL END) AS fecha_rsi_bajo,
                MIN(CASE WHEN i.date > (SELECT MAX(date) FROM indicadores WHERE ticker = c.ticker AND rsi < 30) AND c.close > i.wma_20 THEN i.date ELSE NULL END) AS fecha_close_mayor_ema,
                MAX(CASE WHEN i.rsi < 30 THEN i.rsi ELSE NULL END) AS rsi,
                MAX(CASE WHEN i.rsi < 30 THEN i.wma_20 ELSE NULL END) AS wma_20
            FROM
                cotizaciones AS c
            JOIN
                indicadores AS i ON c.ticker = i.ticker AND c.date = i.date
            GROUP BY
                c.ticker
        ) AS subquery
        ORDER BY fecha_close_mayor_ema desc, fecha_rsi_bajo desc
        LIMIT 15
    """)

    # Obtención de los resultados
    resultados = cursor.fetchall()

    # Encabezados de las columnas
    encabezados = ["Fecha", "rsi", "wma20", "RSI", "WMA20"]

    # Mostrar los resultados en forma de tabla
    tabla = tabulate(resultados, headers=encabezados, tablefmt="fancy_grid")
    print(tabla)

    # Cerrar la conexión a la base de datos
    conn.close()

    # Esperar hasta que se presione una tecla
    print("Presiona una tecla para continuar...")
    keyboard.read_key()
    
if __name__ == "__main__":
    pass