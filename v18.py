# main.py
import time
import sqlite3
import yfinance as yf
from tqdm import tqdm
from manejar_indicadores import *
from manejar_indicadores import *
from manejar_tickers import *
from common import *
from reporte_diario import *

DATABASE_NAME = "bursatil.db"

def mostrar_menu():
    print("Bienvenido al programa de captura y cálculo de datos bursátiles")
    print("Seleccione una opción:")
    print("1. Obtener/Actualizar cotizaciones")
    print("2. Calcular indicadores")
    print("3. Actualizar Tickers")
    print("4. Reporte Diario")
    print("0. Salir")

def guardar_log(mensaje):
    with open("log.txt", "a") as file:
        file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")

def crear_tabla_cotizaciones():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotizaciones (
            ticker TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (ticker, date)
        )
    """)

    conn.commit()
    conn.close()

def main():
    limpiar_pantalla()

    while True:
        mostrar_menu()
        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            limpiar_pantalla()
            crear_tabla_cotizaciones()
            actualizar_cotizaciones()
            guardar_log("Cotizaciones actualizadas")

        elif opcion == "2":
            limpiar_pantalla()
            calcular_indicadores()
            guardar_log("Indicadores calculados")

        elif opcion == "3":
            limpiar_pantalla()
            actualizar_tickers()
            guardar_log("Tickers Actualizados")

        elif opcion == "4":
            limpiar_pantalla()
            reporte_diario()
            guardar_log("Reporte Diario")

        elif opcion == "0":
            limpiar_pantalla()
            print("¡Hasta luego!")
            break

        else:
            limpiar_pantalla()
            print("Opción inválida. Por favor, seleccione una opción válida.")
            time.sleep(2)

if __name__ == "__main__":
    main()
