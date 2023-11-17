# Cotizacion de 1 ticker con yahoo finance
import yfinance as yf

# Crear un objeto Ticker para AAPL (Apple Inc.)
aapl = yf.Ticker("AAPL")

# Obtener los datos históricos de cotización
historical_data = aapl.history(period="1d")

# Mostrar los datos
print(historical_data)
