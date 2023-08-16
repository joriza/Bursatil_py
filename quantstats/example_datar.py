import pandas as pd
import pandas_datareader as pdr
from datetime import datetime

# Definir la fecha de hoy
today = datetime.today().strftime('%Y-%m-%d')

# Obtener datos históricos de precios de acciones
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']  # Agrega aquí los tickers de las acciones que deseas analizar
data = pdr.get_data_yahoo(tickers, start='2010-01-01', end=today)

# Calcular el RSI para cada ticker
for ticker in tickers:
    df = data['Close'][ticker].to_frame()
    df['delta'] = df['Close'].diff()
    df['gain'] = df['delta'].where(df['delta'] > 0, 0)
    df['loss'] = -df['delta'].where(df['delta'] < 0, 0)
    df['avg_gain'] = df['gain'].rolling(window=14).mean()
    df['avg_loss'] = df['loss'].rolling(window=14).mean()
    df['rs'] = df['avg_gain'] / df['avg_loss']
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    
    # Filtrar los tickers con RSI menor que 40
    if df['rsi'].iloc[-1] < 40:
        print(f"Ticker: {ticker}, RSI: {df['rsi'].iloc[-1]}")
