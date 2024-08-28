"""
Questo programma identifica e gestisce immagini duplicate.

Come usare il programma:
- Inserisci le immagini che desideri controllare nella cartella "./images".
- Esegui il programma.
- Controlla la cartella "./tocheck" per visualizzare e gestire le immagini duplicate.

"""

import os
import hashlib
import shutil
from collections import defaultdict

def calculate_hash(image_path, chunk_size=1024):
    """Calcola l'hash di un'immagine."""
    hash_md5 = hashlib.md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_duplicate_images(directory):
    """Trova immagini duplicate all'interno di una cartella."""
    files_hash = defaultdict(list)

    # Scansiona tutti i file nella directory specificata
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Calcola l'hash del file
            file_hash = calculate_hash(file_path)
            files_hash[file_hash].append(file_path)

    # Filtra solo i gruppi di file che hanno più di un elemento (duplicate)
    duplicates = {hash_: paths for hash_, paths in files_hash.items() if len(paths) > 1}

    return duplicates

def move_duplicates_to_check(duplicates, check_directory):
    """Sposta le immagini duplicate nella cartella ./tocheck."""
    os.makedirs(check_directory, exist_ok=True)
    
    for paths in duplicates.values():
        for path in paths:
            # Estrai il nome del file
            file_name = os.path.basename(path)
            # Crea il nuovo percorso nella cartella ./tocheck
            new_path = os.path.join(check_directory, file_name)
            # Se il file esiste già nella cartella di destinazione, aggiungi un numero al nome
            counter = 1
            while os.path.exists(new_path):
                name, ext = os.path.splitext(file_name)
                new_path = os.path.join(check_directory, f"{name}_{counter}{ext}")
                counter += 1
            # Sposta il file
            shutil.move(path, new_path)
            print(f"Spostato: {path} -> {new_path}")

def main():
    # Definisci il percorso della cartella contenente le immagini
    image_directory = "./images"
    # Definisci il percorso della cartella dove spostare i duplicati
    check_directory = "./tocheck"
    
    # Trova le immagini duplicate
    duplicates = find_duplicate_images(image_directory)

    if duplicates:
        print("Immagini duplicate trovate, spostamento in corso...")
        move_duplicates_to_check(duplicates, check_directory)
        print("Spostamento completato.")
    else:
        print("Non sono state trovate immagini duplicate.")

if __name__ == "__main__":
    main()
