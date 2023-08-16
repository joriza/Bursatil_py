prompt

en una consulta sql con las siguiente estructura real de tablas
para cada uno de los siguientes ticker ('ARES', 'CRWD', 'VIST')
mostrar la fecha anterior mas proxima en que el rsi estuvo menor a 40, 
y ademas cumpla con la condicion de que luego de la fecha encontrada para el rsi, la primera fecha que el campo close sea mayor a wma_20
mostrar ademas los campos los campos rsi y wma_20
y la fecha coincidente con la condicion del rsi y la fecha coincidente con condicion de close con sma20
CREATE TABLE indicadores (
    ticker  TEXT,
    date    TEXT,
    rsi     REAL,
    wma_20  REAL,
    sma_30  REAL,
    max_52w REAL
);
CREATE TABLE cotizaciones (
    ticker TEXT,
    date   TEXT,
    open   REAL,
    high   REAL,
    low    REAL,
    close  REAL,
    volume INTEGER,
    PRIMARY KEY (
        ticker,
        date
    )
);


para esta consulta, que sea ordenado por fecha_rsi_menor_40
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
    c.ticker IN ('CRWD', 'VIST','IBM','TEAM','NET')
GROUP BY
    c.ticker;


realizar una consulta sql con la siguiente estructura real de tabla
que muestre los campos ticker, date y rsi
con la fecha anterior mas proxima en que el rsi estuvo menor a 40, 
para todos los ticker
y lo guarde en una tabla llamada rsi_menor_40
CREATE TABLE indicadores (
    ticker  TEXT,
    date    TEXT,
    rsi     REAL,
    wma_20  REAL,
    sma_30  REAL,
    max_52w REAL
);

-- *******
en una consulta sql con las siguiente estructura real de tablas
para todos los ticker de la tabla cotizaciones
mostrar la fecha anterior mas proxima en que el rsi estuvo menor a 40, 
y ademas cumpla con la condicion de que luego de la fecha encontrada para el rsi, la primera fecha que el campo close sea mayor a wma_20
mostrar ademas los campos los campos rsi y wma_20
y la fecha coincidente con la condicion del rsi y la fecha coincidente con condicion de close con sma20
CREATE TABLE indicadores (
    ticker  TEXT,
    date    TEXT,
    rsi     REAL,
    wma_20  REAL,
    sma_30  REAL,
    max_52w REAL
);
CREATE TABLE cotizaciones (
    ticker TEXT,
    date   TEXT,
    open   REAL,
    high   REAL,
    low    REAL,
    close  REAL,
    volume INTEGER,
    PRIMARY KEY (
        ticker,
        date
    )
);
--
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


en una consulta sql con las siguiente estructura real de tablas
para cada uno de los ticker
mostrar la fecha anterior mas proxima en que el rsi estuvo menor a 30
mostrar tambien valor del rsi del momento que sucede
ordenar por fecha de rsi menor a 30
CREATE TABLE indicadores (
    ticker  TEXT,
    date    TEXT,
    rsi     REAL,
    wma_20  REAL,
    sma_30  REAL,
    max_52w REAL
);
--
SELECT
    ticker,
    MAX(CASE WHEN rsi < 30 THEN date ELSE NULL END) AS fecha_rsi_menor_30,
    MAX(CASE WHEN rsi < 30 THEN rsi ELSE NULL END) AS rsi
FROM
    indicadores
WHERE
    rsi < 30
GROUP BY
    ticker
ORDER BY
    fecha_rsi_menor_30;


