import os
from datetime import datetime
from rembg import remove


# Función principal que procesa las imágenes, elimina el fondo y mueve las imágenes procesadas
def process_images(input_folder):
    output_folder = os.path.join(os.getcwd(), 'Imagenes sin fondo')
    os.makedirs(output_folder, exist_ok=True)
    current_date = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    no_background_folder = os.path.join(output_folder, current_date)
    os.makedirs(no_background_folder, exist_ok=True)

    # Crear la carpeta para las imágenes originales
    originals_folder = os.path.join(no_background_folder, "originals")
    os.makedirs(originals_folder, exist_ok=True)
    for file_name in os.listdir(input_folder):
        if file_name.endswith((".png", ".jpg", ".jpeg")):
            source_path = os.path.join(input_folder, file_name)
            final_path = os.path.join(no_background_folder, file_name)
            remove_background(source_path, final_path)
            move_image(source_path, originals_folder)


# Función que elimina el fondo de la imagen usando la librería rembg
def remove_background(image_path, output_path):
    try:
        with open(image_path, "rb") as inp, open(output_path, "wb") as outp:
            background_output = remove(inp.read())
            outp.write(background_output)

    except Exception as e:
        a = f"Error al eliminar fondo de la imagen {image_path}: {e}"


# Función que mueve la imagen original a una carpeta específica dentro del directorio de salida
def move_image(image_path, destination_folder):
    try:
        # Obtener solo el nombre del archivo desde la ruta completa
        file_name = os.path.basename(image_path)
        new_folder = os.path.join(destination_folder, file_name)
        os.rename(image_path, new_folder)
    except Exception as e:
        a = f"Error al mover la imagen {image_path}: {e}"


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

