from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from PyPDF2 import PdfReader
import fitz 

def find_pdfs(folder_path: str) -> list:
    '''
    Find all PDF files in a folder and its subfolders

    Parameters:
    - folder_path: path to the folder to search

    Returns:
    - list of paths to PDF files
    '''
    pdfs = []
    folder_path = Path(folder_path)
    for file_path in folder_path.rglob("*"):
        if file_path.is_file():
            if file_path.suffix == ".pdf":
                pdfs.append(str(file_path))
    return pdfs

def set_pdf_title(input_path: str, output_path: str, title: str):
    '''
    Set the title of a PDF file

    Parameters:
    - input_path: path to the input PDF file
    - output_path: path to the output PDF file
    - title: title to set

    Returns: None
    '''
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Copy pages
    for page in reader.pages:
        writer.add_page(page)
    
    # Add metadata
    writer.add_metadata({
        '/Title': title
    })
    
    # Save the new PDF
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

def get_pdf(input_path: str):
    '''
    Get a PDF reader object

    Parameters:
    - input_path: path to the PDF file

    Returns:
    - PDF reader object
    '''
    reader = PdfReader(input_path)
    return reader


def count_pdf_pages(pdf_path: str) -> int:
    '''
    Count the number of pages in a PDF file

    Parameters:
    - pdf_path: path to the PDF file

    Returns:
    - number of pages in the PDF file
    '''
    # Create a PDF reader object
    reader = PdfReader(pdf_path)
    
    # Get the number of pages
    num_pages = len(reader.pages)
    
    return num_pages

def pdf_page_to_jpeg(pdf_path: str, page_number: int, output_path: str, zoom: int = 2) -> None:
    """
    Convert a specific page of a PDF to JPEG using PyMuPDF
    
    Parameters:
    - pdf_path: path to PDF file
    - page_number: page number to convert (0-based index)
    - output_path: where to save the JPEG
    - zoom: zoom factor for resolution (default 2)

    Returns: None
    """
    try:
        # Open PDF file
        pdf = fitz.open(pdf_path)
        
        # Get the specified page
        page = pdf[page_number - 1]  # Convert to 0-based index
        
        # Create matrix for better resolution
        mat = fitz.Matrix(zoom, zoom)
        
        # Get the page's pixmap (image)
        pix = page.get_pixmap(matrix=mat)
        
        # Save as JPEG
        pix.save(output_path)
        
        pdf.close()
        print(f"Successfully converted page {page_number} to JPEG")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")