import pandas as pd
import os
from config.document_processor import process_document_via_ai
from utils.file_utils import get_validated_mime_type, save_document_to_json

def process_and_parse_invoice(file_path: str, mime_type: str, processor_id: str):
    """
    Processes the invoice and extracts key information, printing the results in a table
    and saving structured data to a JSON file.
    """
    
    try:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        mime_type = get_validated_mime_type(file_path, mime_type)

        document = process_document_via_ai(
            processor_id=processor_id,
            file_path=file_path,
            mime_type=mime_type,
        )

        print("Invoice processing complete.")
        
        save_document_to_json(document, "source", "invoice_parser", file_name)

        types = []
        raw_values = []
        normalized_values = []
        confidence = []
        sub_entity_number = []

        json_data = {"entities": []}

        for entity in document.entities:
            types.append(entity.type_)
            raw_values.append(entity.mention_text)
            normalized_values.append(entity.normalized_value.text)
            confidence.append(entity.confidence) 
            sub_entity_number.append(0) 

            entity_dict = {
                "type": entity.type_,
                "raw_value": entity.mention_text,
                "normalized_value": entity.normalized_value.text,
                "confidence": entity.confidence,
                "sub_entities": [] 
            }

            for i, prop in enumerate(entity.properties, start=1):
                types.append(prop.type_)
                raw_values.append(prop.mention_text)
                normalized_values.append(prop.normalized_value.text)
                confidence.append(prop.confidence)
                sub_entity_number.append(i)

                sub_entity_dict = {
                    "type": prop.type_,
                    "raw_value": prop.mention_text,
                    "normalized_value": prop.normalized_value.text,
                    "confidence": prop.confidence
                }
                entity_dict["sub_entities"].append(sub_entity_dict)

            json_data["entities"].append(entity_dict)

        df = pd.DataFrame(
            {
                "Type": types,
                "Raw Value": raw_values,
                "Normalized Value": normalized_values,
                "Confidence": confidence,
                "Sub-Entity Number": sub_entity_number
            }
        )
        print(df)

        save_document_to_json(json_data, "parsed", "invoice_parser", file_name)

    except Exception as e:
        print(f"Error while processing invoice: {e}")
