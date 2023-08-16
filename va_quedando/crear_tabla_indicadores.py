"""
crear una archivo aparte que me permita agregar la tabla indicadores, 
sebun las indicaciones anteriores.
"""

import sqlite3

DB_NAME = "bursatil.db"

def crear_tabla_indicadores():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Crear la tabla indicadores si no existe
    cursor.execute("CREATE TABLE IF NOT EXISTS indicadores (ticker TEXT, date TEXT, rsi REAL, wma_20 REAL, sma_30 REAL, max_52w REAL)")

    conn.commit()
    conn.close()

    print("Tabla 'indicadores' creada con éxito.")

if __name__ == "__main__":
    crear_tabla_indicadores()

