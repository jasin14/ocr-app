import pandas as pd
from config.document_processor import process_document_via_ai
from utils.file_utils import get_mime_type, is_supported_file_type

def process_and_parse_layout(file_path: str, mime_type: str, processor_id: str):
    """
    Processes a document using the Layout Parser and extracts structural information, printing the results in a table.
    """
    
    try:
        # Określ MIME type automatycznie, jeśli nie został podany
        if mime_type is None:
            mime_type = get_mime_type(file_path)
            print(f"Autodetected MIME type: {mime_type}")

        # Sprawdź, czy plik jest obsługiwany
        if not is_supported_file_type(file_path):
            raise ValueError(f"Unsupported file type for analysis: {file_path}")
        
        # Przetwarzanie dokumentu za pomocą Layout Parsera
        document = process_document_via_ai(
            processor_id=processor_id,
            file_path=file_path,
            mime_type=mime_type,
        )

        print("Layout processing complete.")

        page_info = []

        # Wyciąganie informacji o strukturze dokumentu
        for page in document.pages:
            layout_info = {
                "page_number": page.page_number,
                "width": page.dimension.width,
                "height": page.dimension.height,
                "text_content": page.text_anchor.content if page.text_anchor else "No content",
            }
            page_info.append(layout_info)

        # Tworzenie tabeli z informacjami o layoutach za pomocą Pandas DataFrame
        df = pd.DataFrame(page_info)
        print(df)

    except Exception as e:
        print(f"Error while processing the layout: {e}")
