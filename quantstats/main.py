import pandas as pd
import yfinance as yf
import quantstats as qs

qs.extend_pandas()

stock = qs.utils.download_returns('TSLA')

print(stock.sharpe())
stock.plot_earnings(savefig='tsla', start_balance=1000)

# Eliminar información de la zona horaria del índice
stock.index = stock.index.tz_localize(None)

qs.reports.html(stock, 'SPY', title='tsla', output='c:\\Users\\jizaguirre\\source\\repos\\PythonApplication1\\bursatil\\quantstats\\a.html')
