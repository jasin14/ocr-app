import os
import pandas as pd
from config.document_processor import process_document_via_ai
from utils.file_utils import get_validated_mime_type, save_document_to_json

def process_and_parse_form(file_path: str, mime_type: str, processor_id: str):
    """
    Processes the form, extracts key information and table data, and saves the structured data to a JSON file.
    """
    try:
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        mime_type = get_validated_mime_type(file_path, mime_type)

        document = process_document_via_ai(
            processor_id=processor_id,
            file_path=file_path,
            mime_type=mime_type,
        )

        print("Form processing complete.")

        # Zapisanie przetworzonego dokumentu do pliku JSON
        save_document_to_json(document, "source", "form_parser", file_name)

        # Klucz-Wartość (Form fields) oraz Tabele w JSON
        json_data = {
            "entities": [],
            "tables": []
        }

        # Wyodrębnianie par klucz-wartość z formularzy
        for page in document.pages:
            for field in page.form_fields:
                entity_dict = {
                    "field_name": extract_text_from_text_anchor(field.field_name.text_anchor, document.text),
                    "field_name_confidence": field.field_name.confidence,
                    "field_value": extract_text_from_text_anchor(field.field_value.text_anchor, document.text),
                    "field_value_confidence": field.field_value.confidence
                }
                json_data["entities"].append(entity_dict)

        # Wyodrębnianie tabel z formularzy
        for page in document.pages:
            for table in page.tables:
                table_data = {
                    "header_rows": [],
                    "table_rows": []
                }

                # Pobierz wiersze nagłówków
                for header_row in table.header_rows:
                    header_row_data = []
                    for header_cell in header_row.cells:
                        header_row_data.append({
                            "text": extract_text_from_text_anchor(header_cell.layout.text_anchor, document.text),
                            "confidence": header_cell.layout.confidence
                        })
                    table_data["header_rows"].append(header_row_data)

                # Pobierz wiersze z danymi
                for body_row in table.body_rows:
                    row_data = []
                    for cell in body_row.cells:
                        row_data.append({
                            "text": extract_text_from_text_anchor(cell.layout.text_anchor, document.text),
                            "confidence": cell.layout.confidence
                        })
                    table_data["table_rows"].append(row_data)

                json_data["tables"].append(table_data)


        save_document_to_json(json_data, "parsed", "form_parser", file_name)

    except Exception as e:
        print(f"Error while processing and parsing form: {e}")

def extract_text_from_text_anchor(text_anchor, full_text):
    """
    Wyodrębnia tekst z obiektu TextAnchor, używając pełnego tekstu dokumentu.
    """
    extracted_text = ""
    for segment in text_anchor.text_segments:
        start_index = segment.start_index
        end_index = segment.end_index
        extracted_text += full_text[start_index:end_index]
    return extracted_text.strip()
