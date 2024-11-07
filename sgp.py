import csv
import ftplib
import os
import time
from datetime import datetime

# Carpetas de trabajo
data_directory = "datosDiarios"
backup_directory = "respaldoDatos"

# Asegurarse de que las carpetas existan
if not os.path.exists(data_directory):
    os.makedirs(data_directory)
if not os.path.exists(backup_directory):
    os.makedirs(backup_directory)

# Generación del archivo CSV
def generate_csv(file_path):
    headers = ['Proveedor', 'Producto', 'Cantidad', 'Precio', 'Fecha']
    data = [
        ['Empanadas Doña Fabi', 'Empanadas', 10, 2.00, datetime.now().strftime("%Y-%m-%d")],
        ['Zapatos Doña Fabi', 'Zapatos', 12, 20.00, datetime.now().strftime("%Y-%m-%d")],
        ['La tiendita de Liria', 'Cholo', 5, 3.00, datetime.now().strftime("%Y-%m-%d")],
        ['', 'Atun', 5, 1.00, datetime.now().strftime("%Y-%m-%d")],
        ['La tiendita de Soto', '', 5, 3.00, datetime.now().strftime("%Y-%m-%d")]
    ]
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"Archivo CSV generado en {file_path}")

# Transferencia del archivo CSV al servidor FTP
def transfer_file_to_ftp(file_path, ftp_address, ftp_user, ftp_password):
    with ftplib.FTP(ftp_address) as ftp:
        ftp.login(ftp_user, ftp_password)
        with open(file_path, 'rb') as file:
            ftp.storbinary(f'STOR {os.path.basename(file_path)}', file)
    print("Archivo transferido exitosamente al servidor FTP.")

# Creación de un respaldo con nombre de archivo + hora
def create_backup(file_path):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Formato: YYYYMMDDHHMMSS sin dos puntos
    backup_file_path = os.path.join(backup_directory, f"facturas_diarias_{timestamp}.csv")
    with open(file_path, 'rb') as original_file:
        with open(backup_file_path, 'wb') as backup_file:
            backup_file.write(original_file.read())
    print(f"Respaldo creado en {backup_file_path}")

# Variables de configuración
ftp_server = "172.31.83.27"
ftp_user = "fabiliria"
ftp_password = "773H"

while True:
    # Ruta completa del archivo CSV en la carpeta de datosDiarios
    csv_file_path = os.path.join(data_directory, "facturas_diarias.csv")

    # Generar el archivo CSV en datosDiarios
    generate_csv(csv_file_path)

    # Transferir el archivo CSV al servidor FTP
    transfer_file_to_ftp(csv_file_path, ftp_server, ftp_user, ftp_password)

    # Crear un respaldo del archivo CSV
    create_backup(csv_file_path)

    # Esperar 1 minuto antes de volver a generar el archivo
    time.sleep(60)
