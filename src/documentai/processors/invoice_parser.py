import pandas as pd
from config.document_processor import process_document_via_ai
from utils.file_utils import get_mime_type, is_supported_file_type

def process_and_parse_invoice(file_path: str, mime_type: str, processor_id: str):
    """
    Processes the invoice and extracts key information, printing the results in a table.
    """
    
    try:
        # Określ MIME type automatycznie, jeśli nie został podany
        if mime_type is None:
            mime_type = get_mime_type(file_path)
            print(f"Autodetected MIME type: {mime_type}")

        # Sprawdź, czy plik jest obsługiwany
        if not is_supported_file_type(file_path):
            raise ValueError(f"Unsupported file type for analysis: {file_path}")

        # Przetwarzanie faktury
        document = process_document_via_ai(
            processor_id=processor_id,
            file_path=file_path,
            mime_type=mime_type,
        )

        print("-------------------------------")
        print(f"{file_path}")
        print("-------------------------------")
        print("Invoice processing complete.")

        fields = []
        values = []
        confidence = []

        # Extracting key-value pairs from the invoice
        for entity in document.entities:
            fields.append(entity.type_)
            values.append(entity.mention_text)
            confidence.append(f"{entity.confidence:.0%}")

        # Tworzenie Pandas DataFrame do prezentacji wyników w tabeli
        df = pd.DataFrame({"Field": fields, "Value": values, "Confidence": confidence})
        print(df)

    except Exception as e:
        print(f"Error while processing invoice: {e}")
