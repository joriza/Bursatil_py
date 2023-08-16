def actualizar_tickers():
    file_name = "tickers.txt"

    # Leer el archivo de texto
    with open(file_name, "r") as file:
        tickers = file.read().splitlines()

    # Ordenar alfabéticamente y eliminar duplicados
    tickers = sorted(list(set(tickers)))

    # Guardar los tickers actualizados en el archivo
    with open(file_name, "w") as file:
        file.write("\n".join(tickers))

    # Mostrar la cantidad de registros
    num_registros = len(tickers)
    print(f"Cantidad de registros: {num_registros}")

# Llamada a la función para actualizar los tickers
actualizar_tickers()


"""
realiza un programa en python que abra el archivo de texto llamado tickers.txt
ordene alfabeticamente y elimine los items repetidos
grabar en el archivo
mostrar cantidad de registros
"""