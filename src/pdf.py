from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import toml

def find_pdfs(folder_path):
    pdfs = []
    folder_path = Path(folder_path)
    for file_path in folder_path.rglob("*"):
        if file_path.is_file():
            if file_path.suffix == ".pdf":
                pdfs.append(str(file_path))
    return pdfs

def read_frontmatter(md_file):
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content.lstrip().startswith('+++'):
                _, frontmatter, _ = content.split('+++', 2)
                return toml.loads(frontmatter.strip())
            return {}
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
        return {}

def set_pdf_title(input_path, output_path, title):
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

def get_pdf(input_path):
    reader = PdfReader(input_path)
    return reader