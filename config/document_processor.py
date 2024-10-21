from google.cloud import documentai_v1 as documentai
from config.config import get_documentai_client, build_request, API_LOCATION
from utils.cache_utils import save_result_to_cache, load_result_from_cache

def process_document_via_ai(
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    """
    Processes a document using the Document AI API, checking cache first.
    """
    try:
        print(f"Debug: Starting document processing for file {file_path}")

        cached_result = load_result_from_cache(file_path, processor_id)
        if cached_result:
            print(f"Debug: Loaded result from cache for file {file_path}")
            return cached_result

        with open(file_path, "rb") as file:
            file_content = file.read()
        print("Debug: File successfully read, preparing request...")

        documentai_client = get_documentai_client(location=API_LOCATION)
        request = build_request(processor_id, file_content, mime_type)
        print("Debug: Sending request to Document AI for processing...")
        
        response = documentai_client.process_document(request=request)
        print("Debug: Document successfully processed.")

        save_result_to_cache(response, file_path, processor_id)

        return response.document

    except Exception as e:
        print(f"Error during document processing: {e}")
        raise
