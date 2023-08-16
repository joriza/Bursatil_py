import sqlite3
import talib
import numpy as np
from tqdm import tqdm
import datetime

DB_NAME = "bursatil.db"

def convertir_temporalidad_semanal(cursor):
    # Crear tabla "semanal" si no existe
    cursor.execute("CREATE TABLE IF NOT EXISTS semanal (ticker TEXT, date TEXT, rsi REAL, wma_20 REAL, sma_30 REAL, max_52w REAL)")

    # Obtener los datos de la tabla cotizaciones
    cursor.execute("SELECT DISTINCT ticker, date, close FROM cotizaciones")
    data = cursor.fetchall()

    # Procesar los datos por ticker
    for ticker in tqdm(set([row[0] for row in data]), desc="Procesando tickers"):
        ticker_data = [(row[1], row[2]) for row in data if row[0] == ticker]

        # Convertir a temporalidad semanal
        weekly_dates = []
        weekly_close_prices = []
        prev_week_number = -1

        for i in range(len(ticker_data)):
            date = datetime.datetime.strptime(ticker_data[i][0], "%Y-%m-%d")
            week_number = date.isocalendar()[1]

            if week_number != prev_week_number:
                weekly_dates.append(date)
                weekly_close_prices.append(ticker_data[i][1])
                prev_week_number = week_number
            else:
                weekly_close_prices[-1] = ticker_data[i][1]

        weekly_dates = [date.strftime("%Y-%m-%d") for date in weekly_dates]

        # Calcular indicadores para los datos semanales
        rsi = talib.RSI(np.array(weekly_close_prices, dtype=float))
        wma_20 = talib.WMA(np.array(weekly_close_prices, dtype=float), timeperiod=20)
        sma_30 = talib.SMA(np.array(weekly_close_prices, dtype=float), timeperiod=30)
        max_52w = np.max(np.array([row[1] for row in ticker_data], dtype=float)[-252:])

        # Guardar los indicadores en la tabla "semanal"
        for i in range(len(weekly_dates)):
            cursor.execute("INSERT INTO semanal (ticker, date, rsi, wma_20, sma_30, max_52w) VALUES (?, ?, ?, ?, ?, ?)",
                           (ticker, weekly_dates[i], rsi[i], wma_20[i], sma_30[i], max_52w))

def calcular_indicadores():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Convertir la temporalidad de la tabla cotizaciones a semanal
    convertir_temporalidad_semanal(cursor)

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

    print("Indicadores calculados y guardados con éxito.")

# Llamada a la función para calcular y guardar los indicadores
calcular_indicadores()
