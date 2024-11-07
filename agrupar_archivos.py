import os
import shutil

def organize_folder(folder):
    file_types = {
        "Imagenes": [".jpeg", ".jpg", ".png", ".gif", ".bmp", ".tiff",".webp"],
        "Videos": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"],
        "Documentos": [".pdf", ".docx", ".pptx", ".txt", ".rtf"],
        "Datasets": [".csv", ".json", ".xlsx", ".tsv", ".xml", ".hdf5", ".sav"],
        "Comprimidos": [".zip", ".rar", ".tar", ".gz", ".7z", ".bz2"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
        "Imágenes Vectoriales": [".svg", ".ai", ".eps", ".cdr"]
    }

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            for folder_name, extensions in file_types.items():
                if ext in extensions:
                    target_folder = os.path.join(folder, folder_name)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_folder, filename))
                    #print(f"Archivo {filename} movido a {folder_name}")

