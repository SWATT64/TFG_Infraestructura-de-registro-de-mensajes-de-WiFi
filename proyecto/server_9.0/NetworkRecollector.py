import pandas as pd
import json
import sys

def extract_first_table(input_file):
    # Leer el archivo completo como una lista de líneas
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Eliminar la primera línea si está en blanco
    if lines[0].strip() == '':
        lines = lines[1:]

    # Encontrar el índice donde termina la primera tabla
    table_end_index = None
    for index, line in enumerate(lines):
        if line.strip() == '':  # Buscar la primera línea vacía después de la línea inicial
            table_end_index = index
            break

    # Ajustar para manejar casos donde no haya líneas vacías adicionales
    if table_end_index is None:
        table_end_index = len(lines)

    # Extraer las líneas de la primera tabla
    first_table_lines = lines[:table_end_index]

    # Preparar los datos para el DataFrame
    if not first_table_lines or len(first_table_lines) < 2:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no hay suficientes líneas
    
    # Asegurar que todas las filas tengan el mismo número de elementos
    header = first_table_lines[0].strip().split(',')
    data = [line.strip().split(',') for line in first_table_lines[1:] if line.strip()]
    # Corregir filas que no tengan el mismo número de columnas que los encabezados
    data = [row if len(row) == len(header) else row[:len(header)] for row in data]

    # Crear el DataFrame
    df_first_table = pd.DataFrame(data, columns=header)

    # Renombrar columnas según especificado
    rename_columns = {'BSSID': 'bssid', ' channel': 'channel', ' Privacy': 'security', ' ESSID': 'essid'}
    df_first_table.rename(columns=rename_columns, inplace=True)

    # Seleccionar solo las columnas de interés
    columns_of_interest = ['bssid', 'channel', 'security', 'essid']
    return df_first_table[columns_of_interest]

def convert_to_json(df):
    # Convertir el DataFrame a un diccionario
    networks = df.to_dict(orient='records')

    # Crear la estructura JSON deseada
    data = {'networks': networks}

    # Imprimir el JSON formateado con indentación de 4 espacios
    print(json.dumps(data, indent=4))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <input_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]  # Tomar la ruta del archivo desde el primer argumento de línea de comando

    # Ejecutar la función para extraer la primera tabla
    df_first_table = extract_first_table(input_file_path)

    # Verificar si el DataFrame está vacío y actuar en consecuencia
    if df_first_table.empty:
        print("No data found in the input file.")
    else:
        # Convertir a JSON y imprimir
        convert_to_json(df_first_table)