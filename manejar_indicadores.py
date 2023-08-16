"""
siendo este el script de creacion de la tabla 
CREATE TABLE IF NOT EXISTS indicadores (ticker TEXT, date TEXT, rsi REAL, wma_20 REAL, sma_30 REAL, wma_30 REAL, max_52w REAL
eliminar la tabla y volverla a crear
calcular los siguientes indicadores tecnicos para cada fecha de cada ticker
guardar los indicadores calculados en la base de datos, en una tabla distinta, llamada indicadores. 
mostrar barra de progreso con tqdm
Los indicadores son_
rsi
media movil ponderada de 20 períodos, en el nombre del campo agregar la cantidad de periodos
media movil simple de 30 períodos, en el nombre del campo agregar la cantidad de periodos
precio maximo del ultimo año. el nombre del campo debe ser max_52w 
"""

import sqlite3
import talib
import numpy as np
from tqdm import tqdm

DATABASE_NAME = "bursatil.db"

def eliminar_tabla_indicadores():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS indicadores")
    
    conn.commit()   
    conn.close()

def calcular_indicadores():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    eliminar_tabla_indicadores()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicadores (
            ticker TEXT, date TEXT, rsi REAL, wma_20 REAL, sma_30 REAL, max_52w REAL);
    """)

#    cursor.execute("CREATE INDEX idx_ticker ON indicadores (ticker);")
#     cursor.execute("CREATE INDEX idx_date ON indicadores (date);")

    # Obtener la lista de tickers
    cursor.execute("SELECT DISTINCT ticker FROM cotizaciones")
    tickers = [row[0] for row in cursor.fetchall()]

    # Calcular indicadores para cada ticker y fecha
    for ticker in tqdm(tickers, desc="Calculando indicadores"):
        cursor.execute("SELECT date, close FROM cotizaciones WHERE ticker = ? ORDER BY date", (ticker,))
        data = cursor.fetchall()
        close_prices = np.array([row[1] for row in data], dtype=float)

        rsi = talib.RSI(close_prices)
        wma_20 = talib.WMA(close_prices, timeperiod=20)
        sma_30 = talib.SMA(close_prices, timeperiod=30)

        for i in range(len(data)):
            date = data[i][0]
            rsi_value = rsi[i]
            wma_20_value = wma_20[i]
            sma_30_value = sma_30[i]
            max_52w_value = np.max(close_prices[-252:])

            cursor.execute("INSERT INTO indicadores (ticker, date, rsi, wma_20, sma_30, max_52w) VALUES (?, ?, ?, ?, ?, ?)",
                           (ticker, date, rsi_value, wma_20_value, sma_30_value, max_52w_value))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == "__main__":
# Llamada a la función para calcular y guardar los indicadores
    eliminar_tabla_indicadores()
    calcular_indicadores()
    
    print("Indicadores calculados y guardados con éxito.")
    
    
    


