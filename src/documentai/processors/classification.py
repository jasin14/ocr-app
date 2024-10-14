import pandas as pd
from config.document_processor import process_document_via_ai
from utils.file_utils import get_mime_type, is_supported_file_type

def process_and_classify_documents(file_path: str, mime_type: str, processor_id: str):
    """
    Processes the document and classifies its entities, printing the results in a table.
    """
    
    try:
        # Określ MIME type automatycznie, jeśli nie został podany
        print(f"mime_type try {mime_type}")
        if mime_type is None:
            mime_type = get_mime_type(file_path)
            print(f"Autodetected MIME type: {mime_type}")

        # Sprawdź, czy plik jest obsługiwany
        if not is_supported_file_type(file_path):
            raise ValueError(f"Unsupported file type for analysis: {file_path}")
        
        # Przetwarzanie dokumentu
        document = process_document_via_ai(
            processor_id=processor_id,
            file_path=file_path,
            mime_type=mime_type,
        )

        print("Document processing complete.")
        print("-------------------------------")
        print(f"{file_path}")
        print("-------------------------------")

        types = []
        confidence = []
        pages = []

        classification_type = None
        best_confidence = None

        if document.entities:
            # Inicjalizuj zmienne dla najlepszego entity
            best_entity = None
            best_confidence = 0.0

            # Każdy Document.entity to klasyfikacja
            for entity in document.entities:
                classification = entity.type_
                types.append(classification)
                confidence.append(f"{entity.confidence:.0%}")
                print(entity.confidence)
                print(best_confidence)

                if entity.confidence > best_confidence:
                    best_entity = entity
                    best_confidence = entity.confidence

                # entity.page_anchor zawiera strony, które pasują do klasyfikacji
                pages_list = []
                for page_ref in entity.page_anchor.page_refs:
                    pages_list.append(page_ref.page)
                pages.append(pages_list)

        # Tworzenie tabeli z klasyfikacją za pomocą Pandas DataFrame
        df = pd.DataFrame({"Classification": types, "Confidence": confidence, "Pages": pages})
        print(df)

        if best_entity:
            classification_type = best_entity.type_
            confidence = best_entity.confidence

        return classification_type, confidence

    except Exception as e:
        print(f"Error while processing and classifying document: {e}")