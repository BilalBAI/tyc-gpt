"""
Convert AAOIFI Standards PDF to text file for faster access.

Run this script once to create AAOIFI-Standards.txt
The application will then read from the text file instead of parsing PDF.
"""

import os
from typing import Optional


def convert_pdf_to_text(pdf_path: str = "AAOIFI-Standards.pdf", 
                        output_path: str = "AAOIFI-Standards.txt",
                        max_pages: Optional[int] = None):
    """
    Convert PDF to text file.
    
    :param pdf_path: Path to the PDF file
    :param output_path: Path to output text file
    :param max_pages: Maximum pages to process (None for all)
    """
    print(f"Converting {pdf_path} to {output_path}...")
    
    # Try PyPDF2 first
    try:
        import PyPDF2
        text_content = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            pages_to_process = min(total_pages, max_pages) if max_pages else total_pages
            
            print(f"Processing {pages_to_process} of {total_pages} pages...")
            
            for page_num in range(pages_to_process):
                try:
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text and text.strip():
                        text_content.append(f"--- Page {page_num + 1} ---\n{text}")
                    
                    if (page_num + 1) % 100 == 0:
                        print(f"  Processed {page_num + 1} pages...")
                except Exception as e:
                    print(f"  Warning: Could not extract page {page_num + 1}: {e}")
                    continue
        
        full_text = "\n\n".join(text_content)
        
    except ImportError:
        # Try pdfplumber
        try:
            import pdfplumber
            text_content = []
            
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                pages_to_process = min(total_pages, max_pages) if max_pages else total_pages
                
                print(f"Processing {pages_to_process} of {total_pages} pages...")
                
                for page_num in range(pages_to_process):
                    try:
                        page = pdf.pages[page_num]
                        text = page.extract_text()
                        if text and text.strip():
                            text_content.append(f"--- Page {page_num + 1} ---\n{text}")
                        
                        if (page_num + 1) % 100 == 0:
                            print(f"  Processed {page_num + 1} pages...")
                    except Exception as e:
                        print(f"  Warning: Could not extract page {page_num + 1}: {e}")
                        continue
            
            full_text = "\n\n".join(text_content)
            
        except ImportError:
            raise ImportError("Please install PyPDF2 or pdfplumber: pip install PyPDF2 pdfplumber")
    
    # Write to text file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n✓ Conversion complete!")
    print(f"  Output file: {output_path}")
    print(f"  File size: {file_size_mb:.1f} MB")
    print(f"  Pages processed: {pages_to_process}")
    print(f"\nThe application will now use {output_path} instead of parsing the PDF.")


if __name__ == "__main__":
    import sys
    
    # Allow limiting pages for testing
    max_pages = None
    if len(sys.argv) > 1:
        try:
            max_pages = int(sys.argv[1])
            print(f"Limiting to first {max_pages} pages for testing...")
        except ValueError:
            print("Usage: python convert_pdf_to_text.py [max_pages]")
            sys.exit(1)
    
    convert_pdf_to_text(max_pages=max_pages)

