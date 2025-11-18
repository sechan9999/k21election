#!/usr/bin/env python3
"""
Test script to check if PDF has extractable text
"""
import PyPDF2

pdf_path = "sejong.pdf"

# Try to extract text from first 3 pages
with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    print(f"Total pages: {len(pdf_reader.pages)}")
    print("\n" + "="*80)

    for page_num in range(min(3, len(pdf_reader.pages))):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        print(f"\nPage {page_num + 1}:")
        print(f"Text length: {len(text)} characters")
        if len(text) > 0:
            print(f"First 500 characters:\n{text[:500]}")
        else:
            print("No extractable text found (image-based PDF)")
        print("="*80)
