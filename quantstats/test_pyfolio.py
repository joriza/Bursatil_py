## cruce dorado

from zipline.api import order_target_percent, record, symbol
import pandas as pd
from datetime import datetime

def initialize(context):
    context.asset = symbol('AAPL')
    context.short_ma_window = 50
    context.long_ma_window = 200
    context.start_date = datetime(2022, 1, 1)  # Fecha de inicio del testing

def handle_data(context, data):
    # Verificar si la fecha actual es posterior a la fecha de inicio
    if data.current_dt >= context.start_date:
        # Obtener los precios históricos de cierre
        prices = data.history(context.asset, 'close', context.long_ma_window + 1, '1d')

        # Calcular los promedios móviles
        short_ma = prices[-context.short_ma_window:].mean()
        long_ma = prices.mean()

        # Generar señales de compra y venta
        if short_ma > long_ma:
            order_target_percent(context.asset, 1.0)  # Comprar todo el capital disponible
        elif short_ma < long_ma:
            order_target_percent(context.asset, 0.0)  # Vender todo el capital disponible

        # Registrar el valor del promedio móvil más corto para su visualización posterior
        record(short_ma=short_ma)
