import pandas as pd


def extract_data(input_path: str, output_path: str):
    # root_dir = Path(__file__).resolve().parent.parent
    # input_path = root_dir / "data" / input_filename
    # output_path = root_dir / "data" / output_filename

    # Aunque estemos leyendo ya un archivo csv hacemos esta extración para ver si es necesario rectificar algun campo o se cambiara de formato a parquet etc
    df = pd.read_csv(input_path)

    amount_strs = df["amount"].astype(str)

    # Verifica un punto decimal minimo en amount
    valores_invalidos = amount_strs[amount_strs.str.count("\.") > 1]

    if not valores_invalidos.empty:
        print("⚠️ Hay valores en 'amount' con más de un punto decimal:")
        print(valores_invalidos)
        return "El amount no está correctamente formateado."

    # La eleccion de que fuera por ahora csv es por el tipo de base de datos primeramente es en excel es facil estar cambiando entre .xlsx y .csv, contiene pocas columnas y filas asi que es una base de datos pequeña y sin tantos cambios
    # Entonces como no es una base de datos de bigdata es efectivo usar csv en lugar de parquet ya que no necesita comprimir tanto la data y es de mas facil lectura el csv asi como muy versatil para Exportación simple
    # Y por ultimo dado que en este ejercicio no utilizaremos herramientas como Apache o Kafka para procesar los dataframes, y considerando que el objetivo es facilitar la lectura y manipulación de los datos de manera directa y comprensible, este formato es fácilmente legible por los humanos.
    df.to_csv(output_path, index=False)
    print(f"Extracción completa: {output_path}")


if __name__ == "__main__":
    extract_data("data/data_prueba_tecnica.csv", "data/extracted.csv")

# Ya que mas adelante hay que checar el esquema para la base de datos de lo que se sube tenia 2 opciones:
# verificar cuando se transforma o desde aqui antes de convertilo a csv separdo por comas
