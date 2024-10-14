from google.cloud import vision
import io
from pdf2image import convert_from_path
import os

# Ustawienie ścieżki do pliku z poświadczeniami
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-vision.json"

# Ścieżka do pliku PDF
pdf_path = 'x2.pdf'

# Plik wyjściowy, gdzie zapiszemy cały tekst
output_text_file = 'output.txt'

# Konwersja PDF na listę obrazów (stron PDF)
images = convert_from_path(pdf_path)

# Initialize the Vision API client
client = vision.ImageAnnotatorClient()

# Otwieramy plik tekstowy w trybie zapisu (nadpisanie pliku, jeśli istnieje)
with open(output_text_file, 'w', encoding='utf-8') as f:
    
    # Przetwarzanie każdej strony PDF
    for i, page_image in enumerate(images):
        # Zapisz stronę jako obraz tymczasowy (PNG)
        temp_image_path = f'temp_page_{i+1}.png'
        page_image.save(temp_image_path, 'PNG')

        # Odczytaj obraz
        with io.open(temp_image_path, 'rb') as image_file:
            content = image_file.read()
            image = vision.Image(content=content)

        # Perform text detection
        response = client.text_detection(image=image)
        texts = response.text_annotations

        # Zapisujemy tekst z każdej strony do pliku tekstowego
        f.write(f"\n--- Tekst z strony {i+1} ---\n")
        for text in texts:
            f.write(text.description + "\n")

        # Wyświetlamy tekst w konsoli
        print(f"Tekst z strony {i+1}:")
        for text in texts:
            print(text.description)

        # Usuń tymczasowy plik obrazu
        os.remove(temp_image_path)

print(f"Cały tekst zapisano w pliku {output_text_file}")
