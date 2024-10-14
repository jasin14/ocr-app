from src.documentai.processors.invoice_parser import process_and_parse_invoice
from config.config import INVOICE_PROCESSOR_ID
from utils.pdf_utils import move_file_to_folder
import os

# from src.documentai.processors.form_parser import process_and_parse_form
# from src.documentai.processors.custom_extractor import process_and_extract_vehicle_registration

def process_with_appropriate_processor(file_path, classification_type, processed_folder):
    """
    Uruchamia odpowiedni procesor na podstawie wyniku klasyfikacji.
    """
    if classification_type == "invoice":
        processor_name = "invoice_parser"
        print(f"Processing invoice for file {file_path}")
        process_and_parse_invoice(file_path, mime_type="application/pdf", processor_id=INVOICE_PROCESSOR_ID)
    # elif classification_type == "vehicle_registration":
    #     print(f"Processing vehicle registration for file {file_path}")
        # process_and_extract_vehicle_registration(file_path)
    else:
        processor_name = "unknown_classification"
        print(f"Unknown classification type: {classification_type}. Skipping file {file_path}.")

    
    # Przenieś plik do folderu przetworzonego
    move_file_to_folder(
        file_path, 
        os.path.join(processed_folder, processor_name), 
        new_name=os.path.basename(file_path)
    )
