from google.cloud import documentai_v1 as documentai
from config.config import get_documentai_client, build_request, PROJECT_ID, API_LOCATION
from utils.cache_utils import save_result_to_cache, load_result_from_cache

def process_document_via_ai(
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    """
    Processes a document using the Document AI API.
    Sprawdza cache, zanim wyśle zapytanie do Document AI.
    """
    try:
        print(f"Debug: Starting document processing for file {file_path}")

        # Sprawdź cache
        cached_result = load_result_from_cache(file_path, processor_id)
        if cached_result:
            print(f"Debug: Loaded result from cache for file {file_path}")
            return cached_result

        # Wczytaj zawartość pliku
        with open(file_path, "rb") as file:
            file_content = file.read()

        print("Debug: File successfully read, preparing raw document...")

        # Uzyskaj klienta Document AI
        documentai_client = get_documentai_client(location=API_LOCATION)

        # Budowanie zapytania
        request = build_request(processor_id, file_content, mime_type)

        # Wysłanie zapytania do Document AI
        print(f"Debug: Sending request to Document AI for processing...")
        response = documentai_client.process_document(request=request)

        print("Debug: Document successfully processed.")

        # Zapisz wynik do cache
        save_result_to_cache(response, file_path, processor_id)

        # Zwróć pole 'document' z odpowiedzi
        return response.document

    except Exception as e:
        print(f"Error during document processing: {e}")
        raise


def process_form_via_ai(
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    """
    Processes a form using the Document AI Form Parser API.
    Sprawdza cache, zanim wyśle zapytanie do Document AI.
    """
    try:
        print(f"Debug: Starting form processing for file {file_path}")

        # Sprawdź cache
        cached_result = load_result_from_cache(file_path, processor_id)
        if cached_result:
            print(f"Debug: Loaded result from cache for file {file_path}")
            return cached_result

        # Uzyskaj klienta Document AI
        documentai_client = get_documentai_client(location=API_LOCATION)

        # Odczytaj plik do pamięci
        with open(file_path, "rb") as image:
            image_content = image.read()

        print("Debug: File successfully read, preparing raw document...")

        # Załaduj dane binarne do obiektu RawDocument
        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

        # Budowanie zapytania
        request = {
            "name": f"projects/{PROJECT_ID}/locations/{API_LOCATION}/processors/{processor_id}",
            "raw_document": raw_document
        }

        # Wysłanie zapytania do Document AI
        print(f"Debug: Sending request to Document AI for form processing...")
        response = documentai_client.process_document(request=request)

        print("Debug: Form successfully processed.")

        # Zapisz wynik do cache
        save_result_to_cache(response, file_path, processor_id)

        return response.document

    except Exception as e:
        print(f"Error during form processing: {e}")
        raise
