#!/usr/bin/env python3
"""
Extract pages from sejong.pdf as images for analysis
"""
import fitz  # PyMuPDF
import os
from pathlib import Path

def extract_pages_as_images(pdf_path, output_dir, page_range=None, dpi=150):
    """
    Extract PDF pages as PNG images

    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save images
        page_range: Tuple (start, end) or None for all pages
        dpi: Resolution for images
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Open PDF
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    print(f"Total pages in PDF: {total_pages}")

    # Determine which pages to process
    if page_range:
        start, end = page_range
        pages_to_process = range(start, min(end, total_pages))
    else:
        pages_to_process = range(total_pages)

    # Extract pages
    zoom = dpi / 72  # Convert DPI to zoom factor
    matrix = fitz.Matrix(zoom, zoom)

    for page_num in pages_to_process:
        page = doc[page_num]
        pix = page.get_pixmap(matrix=matrix)

        output_file = os.path.join(output_dir, f"page_{page_num+1:03d}.png")
        pix.save(output_file)

        print(f"Extracted page {page_num+1}/{total_pages}: {output_file}")

    doc.close()
    print(f"\nCompleted! Images saved to: {output_dir}")

if __name__ == "__main__":
    # Extract first 10 pages as a sample
    extract_pages_as_images(
        pdf_path="sejong.pdf",
        output_dir="pdf_pages",
        page_range=(0, 10),  # First 10 pages
        dpi=150
    )
