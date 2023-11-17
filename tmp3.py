# Prueba cotizacion del momento
import yfinance as yf
import datetime

# Símbolo del ticker de la acción que deseas consultar (por ejemplo, AAPL para Apple Inc.)
ticker_symbol = "AAPL"

# Crear un objeto Ticker para el símbolo
stock = yf.Ticker(ticker_symbol)

# Obtener los datos del día actual
current_date = datetime.date.today()
data = stock.history(period="1d", start=current_date, end=current_date)

# Mostrar los datos
print(data)
