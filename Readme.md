

## la librería talib tiene calculo para varios indicadores

 "Ta-Lib" (Technical Analysis Library)
 Es complicada de instalar, solo con anaconda no tuve problemas.
ES necesario que sea python 3.10.x pero menor de pythjon 3.11

## Para vaciar los datos de las tablas

~~~ sql
delete from cotizaciones
delete from indicadores
vacuum
~~~

## Listar ticker posibles
~~~ sql
-- primero rsi bajo y luego precio > WMA20. t.prox 70seg / 30k de egistros
@num=35;
    SELECT *
      FROM (
               SELECT c.ticker,
                      MAX(CASE WHEN i.rsi < @num THEN i.date ELSE NULL END) AS fecha_rsi_bajo,
                      MIN(CASE WHEN i.date > (
                                                 SELECT MAX(date) 
                                                   FROM indicadores
                                                  WHERE ticker = c.ticker AND 
                                                        rsi < @num
                                             )
    AND 
                                    c.close > i.wma_20 THEN i.date ELSE NULL END) AS fch_close_may_ema,
                      MAX(round(CASE WHEN i.rsi < @num THEN i.rsi ELSE NULL END,2)) AS rsi,
                      MAX(round(CASE WHEN i.rsi < @num THEN i.wma_20 ELSE NULL END,2)) AS wma_20
                 FROM cotizaciones AS c
                      JOIN
                      indicadores AS i ON c.ticker = i.ticker AND 
                                          c.date = i.date
                GROUP BY c.ticker
           )
           AS subquery
     ORDER BY fch_close_may_ema DESC,
              fecha_rsi_bajo DESC
~~~

