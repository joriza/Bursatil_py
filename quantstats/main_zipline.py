'''

conda create -n zipline_env python=3.8


conda install -c anaconda cython
conda install -c conda-forge numpy
conda install -c anaconda pandas
conda install -c anaconda scipy
conda install -c conda-forge patsy
conda install -c conda-forge bottleneck
conda install -c anaconda sqlalchemy
conda install -c anaconda pytz
conda install -c anaconda statsmodels

pip install zipline

'''
from zipline.api import order_target_percent, record, symbol
from zipline import run_algorithm
from zipline.pipeline import Pipeline
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.factors import SimpleMovingAverage

def initialize(context):
    # Definir el activo objetivo
    context.asset = symbol('AAPL')

def handle_data(context, data):
    # Calcular la media móvil de 50 días
    sma = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=50)
    sma_value = data.current(context.asset, sma)

    # Tomar decisiones comerciales en función de la media móvil
    if data.current(context.asset, 'price') > sma_value:
        order_target_percent(context.asset, 0.5)
    else:
        order_target_percent(context.asset, 0)

    # Registrar el valor de la media móvil
    record(sma=sma_value)

# Configurar y ejecutar el algoritmo
start_date = pd.Timestamp('2020-01-01', tz='UTC')
end_date = pd.Timestamp('2020-12-31', tz='UTC')
result = run_algorithm(start=start_date, end=end_date, initialize=initialize, handle_data=handle_data)
