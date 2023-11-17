import pyodbc
import yfinance as yf
import datetime
from tqdm import tqdm

DATABASE_SERVER = 'tu_servidor_sql'
DATABASE_NAME = 'Bursatil'
DATABASE_USER = 'tu_usuario'
DATABASE_PASSWORD = 'tu_contraseña'

def conectar_sql_server():
    connection_string = f"DRIVER={{SQL Server}};SERVER=DESKTOP-VRF1S93\\SQLEXPRESS;DATABASE=Bursatil;Trusted_Connection=yes;"
    return pyodbc.connect(connection_string)

def actualizar_cotizaciones():
    with open("tickers.txt", "r") as file:
        tickers = sorted(file.read().splitlines())

    conn = conectar_sql_server()
    cursor = conn.cursor()

    for ticker in tqdm(tickers, desc="Procesando tickers", unit="ticker"):
        cursor.execute(f"SELECT MAX(fecha) FROM cotizaciones WHERE ticker = '{ticker}'")
        result = cursor.fetchone()
        last_date = result[0]

        if last_date:
            start_date = last_date
        else:
            start_date = datetime.date.today() - datetime.timedelta(days=60)

        end_date = datetime.date.today().strftime("%Y-%m-%d")

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
                cursor.execute("MERGE INTO cotizaciones AS target "
                               "USING (VALUES (?, ?, ?, ?, ?, ?, ?)) AS source (ticker, fecha, _open, _high, _low, _close, volume) "
                               "ON target.ticker = source.ticker AND target.fecha = source.fecha "
                               "WHEN MATCHED THEN UPDATE SET _open = source._open, _high = source._high, _low = source._low, _close = source._close, volume = source.volume "
                               "WHEN NOT MATCHED THEN INSERT (ticker, fecha, _open, _high, _low, _close, volume) VALUES (source.ticker, source.fecha, source._open, source._high, source._low, source._close, source.volume);", values)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    actualizar_cotizaciones()
