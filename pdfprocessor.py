import fitz  # PyMuPDF
import os
import json

def extractTextFromPdf(file_name: str) -> str:
    """
    Locates a PDF in the current directory, extracts its text, and returns it.
    """
    # Get the absolute path of the directory where this script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, file_name)

    # Check if the file exists before processing
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_name}' was not found in {current_directory}")

    try:
        # Open the PDF document
        doc = fitz.open(file_path)
        full_text = ""
        
        # Iterate through pages and collect text
        for page in doc:
            full_text += page.get_text()
            
        doc.close()
        return full_text
        
    except Exception as e:
        return f"An error occurred while processing the PDF: {str(e)}"

def convertToJson(content: str, source_name: str) -> str:
    """
    Takes a string and structures it into a JSON format string.
    """
    data_structure = {
        "metadata": {
            "source_file": source_name,
            "character_count": len(content)
        },
        "clean_content": content.strip()
    }
    
    # ensure_ascii=False handles special characters like 'ñ' or accents correctly
    return json.dumps(data_structure, indent=4, ensure_ascii=False)

# Entry point for testing the module directly
if __name__ == "__main__":
    target_file = "asis-colombia-2024.pdf"  # Replace with your actual file name
    
    try:
        extracted_text = extractTextFromPdf(target_file)
        json_output = convertToJson(extracted_text, target_file)
    except Exception as error:
        print(f"Error: {error}")

