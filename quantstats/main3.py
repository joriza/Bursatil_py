import pandas_datareader.data as web

# Obtener datos históricos de un símbolo de acciones
symbol = 'AAPL'
start_date = '2010-01-01'
end_date = '2020-12-31'
data = web.DataReader(symbol, 'yahoo', start_date, end_date)

# Calcular el rendimiento diario
data['Returns'] = data['Adj Close'].pct_change()

# Imprimir los primeros registros
print(data.head())
