import mimetypes
import os

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

def trim_text(text: str) -> str:
    """
    Remove extra space characters from text (blank, newline, tab, etc.)
    """
    return text.strip().replace("\n", " ")
