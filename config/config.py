import os
from google.cloud import documentai_v1 as documentai
from dotenv import load_dotenv

# Wczytaj zmienne środowiskowe z pliku .env
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "")
API_LOCATION = os.getenv("API_LOCATION", "")

CACHE_DIR  = os.getenv("CACHE_DIR", "")
OUTPUT_JSON_DIR  = os.getenv("OUTPUT_JSON_DIR", "")

INVOICE_PROCESSOR_ID = os.getenv("INVOICE_PROCESSOR_ID", "")
CLASSIFICATION_PROCESSOR_ID = os.getenv("CLASSIFICATION_PROCESSOR_ID", "")
FORM_PROCESSOR_ID  = os.getenv("FORM_PROCESSOR_ID", "")
LAYOUT_PROCESSOR_ID  = os.getenv("LAYOUT_PROCESSOR_ID", "")
DOCUMENT_OCR_PROCESSOR_ID  = os.getenv("DOCUMENT_OCR_PROCESSOR_ID", "")
VEHICLE_REGISTRATION_PROCESSOR_ID  = os.getenv("VEHICLE_REGISTRATION_PROCESSOR_ID", "")

INPUT_FOLDER = os.getenv("INPUT_FOLDER", "storage/documents/input")
SPLITED_FOLDER = os.getenv("SPLITED_FOLDER", "storage/documents/splited")
CLASSIFIED_FOLDER = os.getenv("CLASSIFIED_FOLDER", "storage/documents/classified")
PROCESSED_FOLDER = os.getenv("PROCESSED_FOLDER", "storage/documents/processed")

def get_documentai_client(location):
    """Zwraca klienta Google Document AI."""
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    return documentai.DocumentProcessorServiceClient(client_options=opts)

def build_request(processor_id, file_content, mime_type):
    """Buduje i zwraca request dla Document AI."""
    resource_name = f"projects/{PROJECT_ID}/locations/{API_LOCATION}/processors/{processor_id}"
    
    # Tworzenie zapytania
    request = {
        "name": resource_name,
        "raw_document": {
            "content": file_content,
            "mime_type": mime_type
        }
    }
    return request
