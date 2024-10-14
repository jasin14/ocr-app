from utils.pdf_utils import get_pdf_files, split_pdf, move_file_to_folder
from src.documentai.processors.classification import process_and_classify_documents
from src.documentai.managers.processor_dispatcher import process_with_appropriate_processor
import os
from config.config import CLASSIFICATION_PROCESSOR_ID, INPUT_FOLDER, SPLITED_FOLDER, CLASSIFIED_FOLDER, PROCESSED_FOLDER


def process_pdf_folder():
    """
    Główna funkcja: Dzieli pliki PDF, klasyfikuje je i uruchamia odpowiednie procesory.
    """
    pdf_files = get_pdf_files(INPUT_FOLDER)
    
    for pdf_file in pdf_files:
        print(f"Processing file: {pdf_file}")
        
        # Dziel plik na strony i zapisz do folderu splited
        split_pdf(pdf_file, SPLITED_FOLDER)
        
        # Przeanalizuj każdą stronę
        for page_file in os.listdir(SPLITED_FOLDER):
            if page_file.endswith(".pdf"):
                page_file_path = os.path.join(SPLITED_FOLDER, page_file)
                
                # Klasyfikacja strony
                classification_type, confidence = process_and_classify_documents(
                    file_path=page_file_path,
                    mime_type="application/pdf",
                    processor_id=CLASSIFICATION_PROCESSOR_ID
                )
                
                print(f"Classified {page_file_path} as {classification_type} with confidence {confidence:.2f}")
                
                # Przeniesienie do folderu classified
                new_classified_path = move_file_to_folder(
                    page_file_path, 
                    CLASSIFIED_FOLDER, 
                    new_name=f"{classification_type}_{page_file}"
                )
                
                # Przetwarzanie odpowiednim procesorem na podstawie klasyfikacji
                process_with_appropriate_processor(new_classified_path, classification_type, PROCESSED_FOLDER)
