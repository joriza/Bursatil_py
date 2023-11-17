import sqlite3
import time
import yfinance as yf
from tqdm import tqdm
import datetime

DATABASE_NAME = "bursatil.db"

def actualizar_cotizaciones():

    # global DATABASE_NAME

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
            # start_date = "2023-02-01" # Fecha mas antigua de carga inicial de informacion
            start_date = datetime.date.today() - datetime.timedelta(days=60)

        end_date = time.strftime("%Y-%m-%d")
        # datenow = datetime.date.today()
        # new_date = datenow - datetime.timedelta(days=0)
        # end_date = new_date.strftime("%Y-%m-%d")

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

def crear_tabla_cotizaciones():

    # global DATABASE_NAME

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

#    cursor.execute("""
#        CREATE TABLE IF NOT EXISTS cotizaciones (
#            ticker TEXT,
#            date TEXT,
#            open REAL,
#            high REAL,
#            low REAL,
#            close REAL,
#            volume INTEGER,
#            PRIMARY KEY (ticker, date)
#        )
#
#        CREATE INDEX idx_ticker ON cotizaciones (ticker);
#        CREATE INDEX idx_date ON cotizaciones (date);
#    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    pass