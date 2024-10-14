import argparse
from config.config import (
    get_documentai_client, 
    PROJECT_ID, 
    API_LOCATION, 
    INVOICE_PROCESSOR_ID, 
    CLASSIFICATION_PROCESSOR_ID, 
    LAYOUT_PROCESSOR_ID, 
    FORM_PROCESSOR_ID
)
from config.processor_types import fetch_processor_types, print_processor_types
from config.list_processors import list_processors, print_processors, get_processor
from src.documentai.processors.classification import process_and_classify_documents
from src.documentai.processors.invoice_parser import process_and_parse_invoice
from src.documentai.processors.form_parser import process_and_parse_form
from src.documentai.processors.layout_parser import process_and_parse_layout
from src.cloud_storage.cloud_storage import upload_to_cloud_storage
from src.documentai.managers.folder_processor import process_pdf_folder

# # Ustaw poziom logowania dla całej aplikacji
# logging.basicConfig(level=logging.ERROR)

# # Ustaw poziom logowania tylko dla modułów Google Cloud (jeśli chcesz tylko te ograniczyć)
# logging.getLogger('google.cloud').setLevel(logging.ERROR)
# logging.getLogger('google.auth').setLevel(logging.ERROR)

def main():
    parser = argparse.ArgumentParser(description="Wywoływanie funkcji Document AI i Cloud Storage")
    parser.add_argument("function", choices=[
        "get_client", "get_project_info",
        "fetch_processor_types", "print_processor_types",
        "list_processors", "print_processors", "get_processor_by_name",
        "classify_document", "parse_invoice", "parse_form", "parse_layout", 
        "upload_to_cloud_storage", "process_folder"
    ], help="Wybierz funkcję do wywołania")

    parser.add_argument("--file_path", type=str, help="Ścieżka do pliku do przetworzenia lub przesłania do Cloud Storage")
    parser.add_argument("--mime_type", type=str, help="Typ MIME pliku (dla classify_document, parse_invoice, parse_form, lub parse_layout)")
    parser.add_argument("--processor_id", type=str, help="ID procesora jeśli inny niż defaultowy")
    parser.add_argument("--input_folder", type=str, help="Ścieżka do folderu z plikami PDF do przetworzenia")
    parser.add_argument("--output_folder", type=str, help="Ścieżka do folderu, w którym zostaną zapisane przetworzone pliki")
    parser.add_argument("--display_name", type=str, help="Display name of the processor (for get_processor_by_name)")

    args = parser.parse_args()

    if args.function == "get_client":
        client = get_documentai_client(API_LOCATION)
        print(f"Klient: {client}")
    elif args.function == "get_project_info":
        print(f"Project ID: {PROJECT_ID}")
        print(f"API Location: {API_LOCATION}")
    elif args.function == "fetch_processor_types":
        processor_types = fetch_processor_types()
        print("Fetched processor types successfully.")
        print(processor_types)
    elif args.function == "print_processor_types":
        processor_types = fetch_processor_types()
        print_processor_types(processor_types)
    elif args.function == "list_processors":
        processors = list_processors()
        print(f"Fetched {len(processors)} processors.")
    elif args.function == "print_processors":
        print_processors()
    elif args.function == "get_processor_by_name":
        if args.display_name is None:
            print("Error: --display_name is required for this function")
        else:
            processors = list_processors()
            processor = get_processor(args.display_name, processors)
            if processor:
                print(f"Processor found: {processor}")
            else:
                print(f"No processor found with display name: {args.display_name}")
    elif args.function == "classify_document":
        if not args.file_path:
            print("Error: --file_path is required for classify_document")
        else:
            processor = args.processor_id if args.processor_id else CLASSIFICATION_PROCESSOR_ID
            process_and_classify_documents(
                file_path=args.file_path,
                mime_type=args.mime_type,
                processor_id=processor
            )
    elif args.function == "parse_invoice":
        if not args.file_path:
            print("Error: --file_path is required for parse_invoice")
        else:
            processor = args.processor_id if args.processor_id else INVOICE_PROCESSOR_ID
            process_and_parse_invoice(
                file_path=args.file_path,
                mime_type=args.mime_type,
                processor_id=processor
            )
    elif args.function == "parse_form":
        if not args.file_path:
            print("Error: --file_path is required for parse_form")
        else:
            processor = args.processor_id if args.processor_id else FORM_PROCESSOR_ID
            process_and_parse_form(
                file_path=args.file_path,
                mime_type=args.mime_type,
                processor_id=processor
            )
    elif args.function == "parse_layout":
        if not args.file_path:
            print("Error: --file_path is required for parse_layout")
        else:
            processor = args.processor_id if args.processor_id else LAYOUT_PROCESSOR_ID
            process_and_parse_layout(
                file_path=args.file_path,
                mime_type=args.mime_type,
                processor_id=processor
            )
    elif args.function == "upload_to_cloud_storage":
        if not args.file_path:
            print("Error: --file_path is required for upload_to_cloud_storage")
        else:
            upload_to_cloud_storage(args.file_path)
    elif args.function == "process_folder":
            process_pdf_folder()

if __name__ == "__main__":
    main()