from google.cloud import documentai_v1 as documentai
import pandas as pd
from config.document_processor import process_form_via_ai
from utils.file_utils import get_mime_type, is_supported_file_type, trim_text
from utils.data_extraction import get_table_data
from os.path import splitext


def process_and_parse_form(file_path: str, mime_type: str, processor_id: str):
    """
    Procesuje formularz, wyciąga kluczowe informacje oraz dane tabelaryczne, drukując je w tabeli.
    """

    try:
        # Określ MIME type automatycznie, jeśli nie został podany
        if mime_type is None:
            mime_type = get_mime_type(file_path)
            print(f"Autodetected MIME type: {mime_type}")

        # Sprawdź, czy plik jest obsługiwany
        if not is_supported_file_type(file_path):
            raise ValueError(f"Unsupported file type for analysis: {file_path}")

        # Przetwarzanie formularza
        document = process_form_via_ai(
            processor_id=processor_id,
            file_path=file_path,
            mime_type=mime_type,
        )

        names = []
        name_confidence = []
        values = []
        value_confidence = []

        # Przetwarzanie formularza i wyciąganie pól
        for page in document.pages:
            for field in page.form_fields:
                # Wyciągnięcie nazw pól formularza
                names.append(trim_text(field.field_name.text_anchor.content))
                # Zaufanie do nazwy pola
                name_confidence.append(field.field_name.confidence)

                # Wyciągnięcie wartości pól formularza
                values.append(trim_text(field.field_value.text_anchor.content))
                # Zaufanie do wartości pola
                value_confidence.append(field.field_value.confidence)

        # Tworzenie Pandas DataFrame do wydrukowania wartości w formacie tabelarycznym
        df = pd.DataFrame({
            "Field Name": names,
            "Field Name Confidence": name_confidence,
            "Field Value": values,
            "Field Value Confidence": value_confidence,
        })

        print(df)

        # Przetwarzanie tabel
        process_and_parse_tables(document, file_path)

    except Exception as e:
        print(f"Error while processing and classifying document: {e}")


def process_and_parse_tables(document: documentai.Document, file_path: str):
    """
    Parsuje i wyciąga dane tabelaryczne z dokumentu.
    """
    header_row_values = []
    body_row_values = []

    # Input Filename without extension
    output_file_prefix = splitext(file_path)[0]

    for page in document.pages:
        for index, table in enumerate(page.tables):
            header_row_values = get_table_data(table.header_rows, document.text)
            body_row_values = get_table_data(table.body_rows, document.text)

            # Tworzenie Pandas Dataframe do wyświetlania danych w tabeli.
            df = pd.DataFrame(
                data=body_row_values,
                columns=pd.MultiIndex.from_arrays(header_row_values),
            )

            print(f"Page {page.page_number} - Table {index}")
            print(df)

            # Zapisz każdą tabelę jako plik CSV
            output_filename = f"{output_file_prefix}_pg{page.page_number}_tb{index}.csv"
            df.to_csv(output_filename, index=False)
            print(f"Table saved to {output_filename}")
