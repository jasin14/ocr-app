from google.cloud import storage
from dotenv import load_dotenv
import os

# Wczytanie zmiennych środowiskowych z .env
load_dotenv()

# Pobieranie zmiennych z .env
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
GCS_DEFALUT_DESTINATION_FOLDER = os.getenv("GCS_DEFALUT_DESTINATION_FOLDER")

def upload_to_cloud_storage(source_file_path, folder_storage):
    """
    Przesyła plik do Cloud Storage na podstawie zmiennych środowiskowych.
    Nazwa pliku w Cloud Storage będzie generowana na podstawie nazwy pliku źródłowego.
    """
    try:
        # Inicjalizacja klienta Google Cloud Storage
        storage_client = storage.Client()
        
        # Pobierz bucket
        bucket = storage_client.bucket(GCS_BUCKET_NAME)

        if folder_storage:
            destination_folder = folder_storage
        else:
            destination_folder = GCS_DEFALUT_DESTINATION_FOLDER
        
        # Nazwa pliku w Cloud Storage (dodajemy folder destynacji oraz nazwę pliku)
        file_name = os.path.basename(source_file_path)  # Wyciągnięcie nazwy pliku
        destination_blob_name = f"{destination_folder}/{file_name}"
        
        # Zdefiniowanie blobu
        blob = bucket.blob(destination_blob_name)
        
        # Przesyłanie pliku
        blob.upload_from_filename(source_file_path)
        
        print(f"File {source_file_path} uploaded to {destination_blob_name} in bucket {GCS_BUCKET_NAME}.")
    
    except Exception as e:
        print(f"Error during file upload: {e}")