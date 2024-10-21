import json
import io
from google.cloud import vision
from pdf2image import convert_from_path
from os.path import splitext

def process_pdf_with_vision(pdf_path: str):
    """
    Przetwarza plik PDF przy użyciu Google Vision API i zapisuje cały wynik do pliku JSON.
    """
    try:
        # Initialize the Vision API client
        client = vision.ImageAnnotatorClient()

        # Konwersja PDF na listę obrazów (stron PDF)
        images = convert_from_path(pdf_path)

        # Przetwarzanie każdej strony PDF
        for i, page_image in enumerate(images):
            # Konwersja obrazu strony na format Vision API
            image_content = page_image.convert('RGB')
            image_bytes = io.BytesIO()
            image_content.save(image_bytes, format='PNG')
            image = vision.Image(content=image_bytes.getvalue())

            # Wykonanie wykrywania tekstu
            response = client.text_detection(image=image)

            response_json_str = vision.AnnotateImageResponse.to_json(response)

            # Zapis do pliku JSON
            output_filename = f"{splitext(pdf_path)[0]}_{i}_vision_output.json"
            with open(output_filename, "w", encoding='utf-8') as json_file:
                json_file.write(response_json_str)
            

        print(f"Document saved to {output_filename}")

    except Exception as e:
        print(f"Error while processing PDF with Vision API: {e}")
