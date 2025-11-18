#!/usr/bin/env python3
"""
Extract ALL 126 pages from sejong.pdf as images
"""
import fitz  # PyMuPDF
import os
from pathlib import Path

def extract_all_pages(pdf_path, output_dir, dpi=150):
    """Extract all PDF pages as PNG images"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    print(f"Extracting all {total_pages} pages...")
    print(f"Output directory: {output_dir}")
    print("=" * 80)

    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    for page_num in range(total_pages):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=matrix)

        output_file = os.path.join(output_dir, f"page_{page_num+1:03d}.png")
        pix.save(output_file)

        if (page_num + 1) % 10 == 0:
            print(f"Progress: {page_num+1}/{total_pages} pages extracted")

    doc.close()
    print("=" * 80)
    print(f"✓ Completed! All {total_pages} pages saved to: {output_dir}")

if __name__ == "__main__":
    extract_all_pages(
        pdf_path="sejong.pdf",
        output_dir="pdf_pages_all",
        dpi=150
    )
