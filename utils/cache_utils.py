import hashlib
import os
import pickle
from google.cloud import documentai_v1 as documentai
from config.config import CACHE_DIR

# Tworzenie folderu cache, jeśli nie istnieje
os.makedirs(CACHE_DIR, exist_ok=True)

def _generate_cache_key(folder_name, file_name):
    """
    Generuje klucz cache na podstawie folderu i nazwy pliku.
    """
    key = f"{folder_name}_{file_name}"
    cache_key = hashlib.md5(key.encode('utf-8')).hexdigest()
    print(f"Generated cache_key: {cache_key}")

    return cache_key

def save_result_to_cache(result, folder_name, file_name):
    """
    Zapisuje wynik przetwarzania do pliku pickle w cache.
    """
    cache_key = _generate_cache_key(folder_name, file_name)
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.pkl")

    with open(cache_path, 'wb') as cache_file:
        pickle.dump(result, cache_file)
    
    print(f"Saved result as cache_key {cache_key} to cache_path: {cache_path}")

def load_result_from_cache(folder_name, file_name):
    """
    Ładuje wynik przetwarzania z pliku pickle w cache, jeśli istnieje.
    """
    cache_key = _generate_cache_key(folder_name, file_name)
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.pkl")

    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as cache_file:
            result = pickle.load(cache_file)
            
            # Upewnijmy się, że zwracamy `document`, a nie cały `ProcessResponse`
            if isinstance(result, documentai.ProcessResponse):
                return result.document  # Zwracamy tylko obiekt `Document`
            else:
                return result  # Zwracamy, co jest w cache, jeśli nie `ProcessResponse`

    return None
