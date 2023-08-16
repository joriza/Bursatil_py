import pandas as pd
import pyfolio as pf

# Crear un DataFrame simulado de rendimientos diarios
returns = pd.DataFrame({'Date': pd.date_range(start='2020-01-01', periods=100),
                        'Return': [0.01, -0.02, 0.015, 0.03, -0.01] * 20})

# Calcular métricas de rendimiento y generar el informe
pf.create_full_tear_sheet(returns)

