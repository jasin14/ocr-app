import os
from PyPDF2 import PdfReader, PdfWriter

def ensure_folder_exists(folder_path):
    """
    Tworzy folder, jeśli nie istnieje.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")

def get_pdf_files(input_folder):
    """
    Zwraca listę plików PDF w folderze.
    """
    return [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.pdf')]

def rename_file_with_classification(file_path, classification_type):
    """
    Zmienia nazwę pliku na podstawie wzorca: classname_previousfilename.pdf
    """
    # Wyciągnij poprzednią nazwę pliku bez rozszerzenia
    base_name = os.path.basename(file_path)
    base_name_without_ext = os.path.splitext(base_name)[0]
    new_filename = f"{classification_type}_{base_name_without_ext}.pdf"

    # Zmień nazwę pliku
    new_file_path = os.path.join(os.path.dirname(file_path), new_filename)

    # Sprawdź, czy plik docelowy już istnieje
    if os.path.exists(new_file_path):
        os.remove(new_file_path)  # Usuń plik, aby można było go nadpisać

    os.rename(file_path, new_file_path)
    
    print(f"Renamed file {file_path} to {new_file_path}")
    return new_file_path

def split_pdf(input_file, output_folder):
    """
    Dzieli plik PDF na poszczególne strony i zapisuje je w output_folder.
    Nazwy plików wynikowych są tworzone na podstawie wzorca page_pageno_previousfilename.pdf.
    """
    ensure_folder_exists(output_folder)  # Tworzymy folder, jeśli go nie ma

    base_name = os.path.splitext(os.path.basename(input_file))[0]  # Nazwa bez rozszerzenia
    with open(input_file, "rb") as file:
        reader = PdfReader(file)
        for page_num, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)

            # Zapisujemy każdą stronę z numerem strony w nazwie
            output_filename = os.path.join(output_folder, f"page_{page_num + 1}_{base_name}.pdf")
            with open(output_filename, "wb") as output_file:
                writer.write(output_file)

            print(f"Saved: {output_filename}")

def move_file_to_folder(file_path, destination_folder, new_name=None):
    """
    Przenosi plik do docelowego folderu. Można opcjonalnie zmienić nazwę pliku.
    """
    ensure_folder_exists(destination_folder)  # Tworzymy folder, jeśli go nie ma
    
    base_name = os.path.basename(file_path)
    new_file_path = os.path.join(destination_folder, new_name or base_name)
    
    # Sprawdź, czy plik docelowy już istnieje
    if os.path.exists(new_file_path):
        os.remove(new_file_path)  # Usuń plik docelowy, jeśli istnieje, aby nadpisać go nowym

    os.rename(file_path, new_file_path)
    print(f"Moved file {file_path} to {new_file_path}")
    return new_file_path