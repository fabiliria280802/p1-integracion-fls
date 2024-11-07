import csv
import os
import shutil
from datetime import datetime

# Directorios de trabajo
data_directory = "datosDiarios"
processed_directory = "datosProcesados"
failed_directory = "datosProcesadosFallidos"

# Asegurarse de que las carpetas de datos procesados y fallidos existan
if not os.path.exists(processed_directory):
    os.makedirs(processed_directory)
if not os.path.exists(failed_directory):
    os.makedirs(failed_directory)

# Validación de datos y separación en listas
def validate_and_separate(file_path):
    valid_rows = []
    invalid_rows = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Leer encabezados
        for row in reader:
            if any(cell.strip() == "" for cell in row):  # Verificar si hay celdas vacías
                invalid_rows.append(row)
            else:
                valid_rows.append(row)
    return headers, valid_rows, invalid_rows

# Guardar los datos en un nuevo archivo CSV
def save_to_csv(headers, rows, file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

# Procesamiento del archivo CSV
def process_csv():
    # Revisar cada archivo en la carpeta datosDiarios
    for file_name in os.listdir(data_directory):
        file_path = os.path.join(data_directory, file_name)

        # Validar si el archivo es un CSV
        if file_name.endswith('.csv'):
            print(f"Validando archivo: {file_name}")

            # Validar y separar filas válidas e inválidas
            headers, valid_rows, invalid_rows = validate_and_separate(file_path)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Formato: YYYYMMDDHHMMSS sin dos puntos
            base_file_name = file_name.split('.')[0]

            # Guardar filas válidas en datosProcesados
            if valid_rows:
                processed_file_path = os.path.join(processed_directory, f"{base_file_name}_procesado_{timestamp}.csv")
                save_to_csv(headers, valid_rows, processed_file_path)
                print(f"Archivo válido procesado y guardado en: {processed_file_path}")

            # Guardar filas inválidas en datosProcesadosFallidos
            if invalid_rows:
                failed_file_path = os.path.join(failed_directory, f"{base_file_name}_fallido_{timestamp}.csv")
                save_to_csv(headers, invalid_rows, failed_file_path)
                print(f"Archivo con errores guardado en: {failed_file_path}")

            # Eliminar el archivo original de datosDiarios tras el procesamiento
            os.remove(file_path)

# Ejecutar la validación y procesamiento de archivos
process_csv()