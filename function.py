doc_name = "251114_JPM_Forecasts_Report.pdf"
folder_path2 = "research_database"

import os
from PyPDF2 import PdfReader
from typing import Dict, List
def read_pdf_content(document_path: str = doc_name) -> str:
    """
    Reads the full text content from the PDF file at the given path.
    Returns the raw text for further processing.
    
    Args:
        document_path: Path to PDF file
        
    Returns:
        Raw text content as string
    """
    # Normalize path (handle Windows backslashes)
    document_path = os.path.normpath(document_path)
    
    # Check if file exists
    if not os.path.exists(document_path):
        raise FileNotFoundError(f"Could not find or read the specified PDF document: {document_path}")
    
    # Read the PDF
    reader = PdfReader(document_path)
    
    # Extract text from all pages
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    
    return full_text.strip()

def read_all_pdfs_in_folder(folder_path: str = folder_path2) -> Dict[str, str]:
    """
    Reads all PDF files from a specified folder.
    
    Args:
        folder_path: Path to the folder containing PDF files
        
    Returns:
        Dictionary with filename as key and extracted text as value
    """
    # Normalize path
    folder_path = os.path.normpath(folder_path)
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"Path is not a directory: {folder_path}")
    
    # Dictionary to store results
    pdf_contents = {}
    
    # Get all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"Warning: No PDF files found in {folder_path}")
        return pdf_contents
    
    print(f"Found {len(pdf_files)} PDF file(s) in {folder_path}")
    
    # Read each PDF
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        try:
            print(f"Reading: {pdf_file}...")
            content = read_pdf_content(pdf_path)
            pdf_contents[pdf_file] = content
            print(f"✓ Successfully read {pdf_file} ({len(content)} characters)")
        except Exception as e:
            print(f"✗ Error reading {pdf_file}: {str(e)}")
            pdf_contents[pdf_file] = f"ERROR: {str(e)}"
    
    return pdf_contents

read_all_pdfs_in_folder()

# This is the function that the RefinerAgent will call to exit the loop.
def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished and no more changes are needed."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}

def exit_loop2():
    """Call this function ONLY when the number of iteration is > total iteration', indicating the simulation is finished."""
    return {"status": "approved", "message": "Simulation Done. Exiting loop."}

print("✅ exit_loop function created.")

print("✅ exit_loop function created.")