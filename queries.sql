queries

-- POR TICKER
SELECT
    c.ticker,
    MAX(CASE WHEN i.rsi < 40 THEN i.date ELSE NULL END) AS fecha_rsi_menor_40,
    MIN(CASE WHEN i.date > (SELECT MAX(date) FROM indicadores WHERE ticker = c.ticker AND rsi < 40) AND c.close > i.wma_20 THEN i.date ELSE NULL END) AS fecha_close_mayor_wma20,
    MAX(CASE WHEN i.rsi < 40 THEN i.rsi ELSE NULL END) AS rsi,
    MAX(CASE WHEN i.rsi < 40 THEN i.wma_20 ELSE NULL END) AS wma_20
FROM
    cotizaciones AS c
JOIN
    indicadores AS i ON c.ticker = i.ticker AND c.date = i.date
WHERE
    c.ticker IN ('ARES', 'CRWD', 'VIST')
GROUP BY
    c.ticker;

-- odenado por fechade RSI
SELECT * FROM (
    SELECT
        c.ticker,
        MAX(CASE WHEN i.rsi < 40 THEN i.date ELSE NULL END) AS fecha_rsi_menor_40,
        MIN(CASE WHEN i.date > (SELECT MAX(date) FROM indicadores WHERE ticker = c.ticker AND rsi < 40) AND c.close > i.wma_20 THEN i.date ELSE NULL END) AS fecha_close_mayor_wma20,
        MAX(CASE WHEN i.rsi < 40 THEN i.rsi ELSE NULL END) AS rsi,
        MAX(CASE WHEN i.rsi < 40 THEN i.wma_20 ELSE NULL END) AS wma_20
    FROM
        cotizaciones AS c
    JOIN
        indicadores AS i ON c.ticker = i.ticker AND c.date = i.date
    WHERE
        c.ticker IN ('CRWD', 'VIST', 'IBM', 'TEAM', 'NET')
    GROUP BY
        c.ticker
) AS subquery
ORDER BY fecha_rsi_menor_40;


SELECT * FROM (
    SELECT
        c.ticker,
        MAX(CASE WHEN i.rsi < 30 THEN i.date ELSE NULL END) AS fecha_rsi_bajo,
        MIN(CASE WHEN i.date > (SELECT MAX(date) FROM indicadores WHERE ticker = c.ticker AND rsi < 30) AND c.close > i.wma_20 THEN i.date ELSE NULL END) AS fecha_close_mayor_ema,
        MAX(CASE WHEN i.rsi < 30 THEN i.rsi ELSE NULL END) AS rsi,
        MAX(CASE WHEN i.rsi < 30 THEN i.wma_20 ELSE NULL END) AS wma_20
    FROM
        cotizaciones AS c
    JOIN
        indicadores AS i ON c.ticker = i.ticker AND c.date = i.date
    GROUP BY
        c.ticker
) AS subquery
ORDER BY fecha_close_mayor_ema desc, fecha_rsi_bajo desc;


