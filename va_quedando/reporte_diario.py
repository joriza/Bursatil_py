import sqlite3
from tabulate import tabulate
import keyboard

def reporte_diario():

    # Conexión a la base de datos
    conn = sqlite3.connect('bursatil.db')
    cursor = conn.cursor()

    # Ejecución de la consulta SQL
    cursor.execute("""
        SELECT i.date, c.ticker, round(i.rsi,2) rsi, 
                                round(c.close,2) precio, 
                                round(i.wma_20,2) wma20, 
                                round(i.sma_30,2) sma30, 
                                round(max_52w,2) MaxY, round(close/max_52w,2) maxP
        FROM cotizaciones AS c
        JOIN indicadores AS i ON c.ticker = i.ticker AND c.date = i.date
        WHERE c.date = (SELECT MAX(date) FROM cotizaciones WHERE ticker = c.ticker)
        and rsi < 60
        and close > wma20 
        and close > sma30 
        and MaxP < 0.90
        order by i.rsi
        LIMIT 15
    """)

    # Obtención de los resultados
    resultados = cursor.fetchall()

    # Encabezados de las columnas
    encabezados = ["Fecha", "Ticker", "RSI", "Precio", "WMA20", "SMA30", "MaxY", "MaxP"]

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