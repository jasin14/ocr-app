import mimetypes
import os
import json
from os.path import splitext, join
from google.cloud import documentai_v1 as documentai
from config.config import OUTPUT_JSON_DIR

def get_mime_type(file_path: str) -> str:
    """
    Returns the MIME type based on the file extension.
    Jeśli MIME type nie jest rozpoznany, zwraca domyślnie 'application/octet-stream'.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    print(f"mime_type {mime_type}")
    
    # Jeśli nie uda się rozpoznać typu MIME, zwróć 'application/octet-stream'
    if mime_type is None:
        return 'application/octet-stream'
    
    return mime_type

def is_supported_file_type(file_path: str) -> bool:
    """
    Sprawdza, czy plik jest obsługiwanym typem dla analizy. 
    Obsługiwane typy to: PDF, JPEG, PNG.
    """
    supported_mime_types = ['application/pdf', 'image/jpeg', 'image/png']
    mime_type = get_mime_type(file_path)
    return mime_type in supported_mime_types

def get_validated_mime_type(file_path: str, mime_type: str = None) -> str:
    """
    Zwraca MIME type po sprawdzeniu, czy jest obsługiwany. Jeśli MIME type nie jest podany, wykrywa go na podstawie pliku.
    """
    # Jeśli nie ma MIME type, automatycznie go ustal
    if mime_type is None:
        mime_type = get_mime_type(file_path)
        print(f"Autodetected MIME type: {mime_type}")
    
    # Sprawdzenie, czy typ pliku jest obsługiwany
    if not is_supported_file_type(file_path):
        raise ValueError(f"Unsupported file type for analysis: {file_path}")
    
    return mime_type

def trim_text(text: str) -> str:
    """
    Remove extra space characters from text (blank, newline, tab, etc.)
    """
    return text.strip().replace("\n", " ")

def ensure_folder_exists(folder_path: str):
    """
    Tworzy folder, jeśli nie istnieje.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")

def save_document_to_json(document, file_type, process_type, file_name):
    """
    Zapisuje przetworzony dokument do pliku JSON w odpowiedniej ścieżce OUTPUT_JSON_DIR/file_type/process_type.
    
    :param document: Obiekt dokumentu do zapisania.
    :param file_type: Typ pliku (np. PDF, IMAGE).
    :param process_type: Typ przetwarzania (np. FORM_PARSER, INVOICE_PARSER).
    :param file_name: Nazwa pliku (bez rozszerzenia) używana do wygenerowania pliku wyjściowego.
    """
    try:

        output_folder = join(OUTPUT_JSON_DIR, file_type, process_type)
        
        ensure_folder_exists(output_folder)

        # Ścieżka do pliku wyjściowego
        output_filename = join(output_folder, f"{file_name}_output.json")

        if isinstance(document, documentai.Document):
            document_json = documentai.Document.to_json(document)
            
            with open(output_filename, "w", encoding='utf-8') as json_file:
                json_file.write(document_json)

        else:
            document_json = document

            with open(output_filename, "w", encoding='utf-8') as json_file:
                json.dump(document_json, json_file, ensure_ascii=False, indent=4)

        print(f"Document saved to {output_filename}")
        
    except Exception as e:
        print(f"Error while saving document to JSON: {e}")
