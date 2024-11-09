import os
from datetime import datetime
from rembg import remove


# Función principal que procesa las imágenes, elimina el fondo y mueve las imágenes procesadas
def process_images(input_folder, output_folder):
    # Obtener la fecha y hora actuales para crear una carpeta única para las imágenes procesadas
    current_date = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    # Crear la carpeta donde se guardarán las imágenes procesadas (sin fondo)
    no_background_folder = os.path.join(output_folder, current_date)
    os.makedirs(no_background_folder, exist_ok=True)

    # Iterar sobre todos los archivos de la carpeta de entrada
    for file_name in os.listdir(input_folder):
        if file_name.endswith((".png", ".jpg", ".jpeg")):
            source_folder = os.path.join(input_folder, file_name)
            final_folder = os.path.join(output_folder, file_name)
            remove_background(source_folder, final_folder)
            move_image(source_folder, no_background_folder)


# Función que elimina el fondo de la imagen usando la librería rembg
def remove_background(source_folder, final_folder):
    with open(source_folder, "rb") as inp, open(final_folder, "wb") as outp:
        background_output = remove(inp.read())
        outp.write(background_output)


# Función que mueve la imagen original a una carpeta específica dentro del directorio de salida
def move_image(source_folder, destination_folder):
    original_folder = os.path.join(destination_folder, "originals")
    os.makedirs(original_folder, exist_ok=True)

    # Obtener solo el nombre del archivo desde la ruta completa
    file_name = os.path.basename(source_folder)
    new_folder = os.path.join(original_folder, file_name)
    os.rename(source_folder, new_folder)
