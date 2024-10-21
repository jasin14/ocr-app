import pandas as pd
from config.document_processor import process_document_via_ai
from utils.file_utils import get_validated_mime_type

def extract_text_from_text_anchor(text_anchor, full_text):
    """
    Wyodrębnia tekst z obiektu TextAnchor, używając pełnego tekstu dokumentu.
    """
    extracted_text = ""
    for segment in text_anchor.text_segments:
        start_index = segment.start_index
        end_index = segment.end_index
        extracted_text += full_text[start_index:end_index]
    return extracted_text

def process_and_perform_ocr(file_path: str, mime_type: str, processor_id: str):
    """
    Processes the document using OCR and prints the extracted text and confidence levels.
    """
    try:
        mime_type = get_validated_mime_type(file_path, mime_type)

        # Przetwarzanie dokumentu za pomocą OCR
        document = process_document_via_ai(
            processor_id=processor_id,
            file_path=file_path,
            mime_type=mime_type,
        )

        print("Document OCR processing complete.")

        # Zmienna do przechowywania tekstu i poziomów pewności (confidence)
        extracted_text = []
        confidence = []

        # Uzyskaj pełny tekst z dokumentu
        full_text = document.text

        # Przechodzenie po stronach dokumentu
        for page in document.pages:
            page_text = extract_text_from_text_anchor(page.layout.text_anchor, full_text)  # Uzyskujemy pełen tekst ze strony
            extracted_text.append(page_text)

            # Dodanie confidence z layoutu strony
            confidence.append(f"{page.layout.confidence:.0%}")
            print(f"Extracted Text (Page {page.page_number}): {page_text}")
            print(f"Confidence (Page {page.page_number}): {page.layout.confidence:.0%}")

        # Tworzenie tabeli z tekstem i poziomami pewności za pomocą Pandas DataFrame
        df = pd.DataFrame({"Extracted Text": extracted_text, "Confidence": confidence})
        print(df)

        # Możesz opcjonalnie zapisać tekst do pliku lub zwrócić wyciągnięty tekst
        return extracted_text, confidence

    except Exception as e:
        print(f"Error while performing OCR on document: {e}")
