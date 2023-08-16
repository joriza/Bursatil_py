import os
import time
import datetime

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

    datenow = datetime.date.today()
    new_date = datenow - datetime.timedelta(days=5)
    end_date = new_date.strftime("%Y-%m-%d")
    print(end_date)

def guardar_log(mensaje):
    with open("log.txt", "a") as file:
        file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")

if __name__ == "__main__":
    pass
