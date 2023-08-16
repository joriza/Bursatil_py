'''
Aquí tienes el código completo en un solo archivo .py que utiliza pandas-datareader y pyti 
para obtener datos de los últimos 6 meses y calcular los indicadores 
RSI, media móvil simple de 20 períodos, MACD y estocástico para una lista de tickers:
'''

import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, timedelta
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.simple_moving_average import simple_moving_average as sma
from pyti.macd import macd
from pyti.stochastic import percent_k, percent_d

tickers = ['AAPL', 'MSFT', 'GOOGL']  # Lista de tickers a analizar

end_date = datetime.now()
start_date = end_date - timedelta(days=6*30)  # Retrocede 6 meses

data = pdr.get_data_yahoo(tickers, start_date, end_date)

for ticker in tickers:
    # RSI
    data['RSI'] = rsi(data['Close'][ticker], 14)

    # Media móvil simple de 20 períodos
    data['SMA'] = sma(data['Close'][ticker], 20)

    # MACD
    macd_line, macd_signal, _ = macd(data['Close'][ticker])

    # Estocástico
    data['%K'] = percent_k(data['Close'][ticker])
    data['%D'] = percent_d(data['Close'][ticker])

for ticker in tickers:
    print(f"Ticker: {ticker}")
    print(data[ticker])
    print("\n")

