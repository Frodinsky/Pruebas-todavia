import os
import hashlib

def hash_file(filename):
    try:
        h = hashlib.md5()
        with open(filename, "rb") as file:
            while chunk := file.read(8192): #para que los archivos se dividan en 8kb aprox
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return None

def find_duplicates(folder):
    hashes = {}
    duplicates = []
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            full_path = os.path.join(dirpath, f )
            file_hash = hash_file(full_path)
            if file_hash is not None:
                if file_hash in hashes:
                    duplicates.append((full_path, hashes[file_hash]))
                else:
                    hashes[file_hash] = full_path
    return  duplicates

def delete_file(filepath):
    try:
        os.remove(filepath)
        return  True
    except Exception as e:
        return False