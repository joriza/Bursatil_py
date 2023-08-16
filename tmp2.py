import os
import time
import sqlite3
import yfinance as yf
from tqdm import tqdm
import talib

DATABASE_NAME = "bursatil_temp.db"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("Bienvenido al programa de captura y cálculo de datos bursátiles")
    print("Seleccione una opción:")
    print("1. Obtener/Actualizar cotizaciones")
    print("2. Calcular indicadores")
    print("0. Salir")

def guardar_log(mensaje):
    with open("log.txt", "a") as file:
        file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")

def crear_tabla_cotizaciones():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotizaciones (
            ticker TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (ticker, date)
        )
    """)

    conn.commit()
    conn.close()

def actualizar_cotizaciones():
    with open("tickers.txt", "r") as file:
        tickers = sorted(file.read().splitlines())

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    for ticker in tqdm(tickers, desc="Procesando tickers", unit="ticker"):
        cursor.execute(f"SELECT MAX(date) FROM cotizaciones WHERE ticker = '{ticker}'")
        result = cursor.fetchone()
        last_date = result[0]

        if last_date:
            start_date = last_date
        else:
            start_date = "2010-01-01"

        end_date = time.strftime("%Y-%m-%d")

        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        data = data.reset_index()

        if not data.empty:
            for _, row in data.iterrows():
                values = (
                    ticker,
                    row["Date"].strftime("%Y-%m-%d"),
                    row["Open"],
                    row["High"],
                    row["Low"],
                    row["Close"],
                    row["Volume"]
                )
                cursor.execute("REPLACE INTO cotizaciones VALUES (?, ?, ?, ?, ?, ?, ?)", values)

    conn.commit()
    conn.close()

def calcular_indicadores():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT ticker FROM cotizaciones")
    tickers = cursor.fetchall()

    for ticker in tqdm(tickers, desc="Procesando tickers", unit="ticker"):
        ticker = ticker[0]

        cursor.execute(f"SELECT * FROM cotizaciones WHERE ticker = '{ticker}'")
        data = cursor.fetchall()

        if len(data) >= 20:
            close_prices = [row[5] for row in data]
            sma_20 = talib.SMA(close_prices, timeperiod=20)
            ema_20 = talib.EMA(close_prices, timeperiod=20)

            for i in range(len(data)):
                date = data[i][1]
                sma_value = sma_20[i]
                ema_value = ema_20[i]

                cursor.execute("""
                    UPDATE cotizaciones
                    SET sma20 = ?, ema20 = ?
                    WHERE ticker = ? AND date = ?
                """, (sma_value, ema_value, ticker, date))

    conn.commit()
    conn.close()

def main():
    limpiar_pantalla()

    while True:
        mostrar_menu()
        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            limpiar_pantalla()
            crear_tabla_cotizaciones()
            actualizar_cotizaciones()
            guardar_log("Cotizaciones actualizadas")

        elif opcion == "2":
            limpiar_pantalla()
            calcular_indicadores()
            guardar_log("Indicadores calculados")

        elif opcion == "0":
            limpiar_pantalla()
            print("¡Hasta luego!")
            break

        else:
            limpiar_pantalla()
            print("Opción inválida. Por favor, seleccione una opción válida.")
            time.sleep(2)

if __name__ == "__main__":
    main()



User
crear una consulta sql a la table indicadores, un registro por ticker
solo la fecha mas reciente que el precio de la tabla cotizaciones sea mayor que el valor del campo sma_20 y que el rsi sea menor a 65


    crear una consulta sql que muestre 
    el precio de cierre de la tabla cotizaciones y el valor campo rsi de la tabla indicadores
    un solo registro por ticker en la fecha mas actual en la tabla cotizaciones
    tambien debe mostrar la fecha y el campo wma_20 de la tabla indicadores
    y que rsi sea menor a 65

SELECT i.date, c.ticker, round(i.rsi,2) rsi, round(c.close,2) precio, round(i.wma_20,2) wma20, round(max_52w,2) MaxY, round(close/max_52w,2) maxP
FROM cotizaciones AS c
JOIN indicadores AS i ON c.ticker = i.ticker AND c.date = i.date
WHERE c.date = (SELECT MAX(date) FROM cotizaciones WHERE ticker = c.ticker)
and rsi < 60 
and close > wma20 
and MaxP < 0.95
order by rsi
