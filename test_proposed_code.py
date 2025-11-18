#!/usr/bin/env python3
"""
Test the proposed PyPDF2 code on sejong.pdf
"""
import re
import PyPDF2

def test_pypdf2_extraction(pdf_path):
    """Test if PyPDF2 can extract text from sejong.pdf"""

    print("="*80)
    print("Testing PyPDF2 Text Extraction")
    print("="*80)

    pdf_reader = PyPDF2.PdfReader(pdf_path)
    total_pages = len(pdf_reader.pages)

    print(f"\nTotal pages: {total_pages}")
    print("\nTesting first 5 pages...")

    total_text_extracted = 0
    candidates_found = 0

    for page_num in range(min(5, total_pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        text_length = len(text.strip())
        total_text_extracted += text_length

        print(f"\nPage {page_num + 1}:")
        print(f"  Text extracted: {text_length} characters")

        if text_length > 0:
            print(f"  First 200 chars: {text[:200]}")

            # Try to find candidate names
            if re.search(r"(이재명|김문수|이준석|권영국|송진호)", text):
                candidates_found += 1
                print("  ✓ Candidate names found")
            else:
                print("  ✗ No candidate names found")
        else:
            print("  ✗ No text extracted (image-based PDF)")

    print("\n" + "="*80)
    print("SUMMARY:")
    print("="*80)
    print(f"Total text extracted: {total_text_extracted} characters")
    print(f"Candidates found: {candidates_found} pages")

    if total_text_extracted == 0:
        print("\n❌ CONCLUSION: PyPDF2 cannot extract text from this PDF")
        print("   Reason: Image-based PDF (scanned document)")
        print("   Solution: OCR required (Tesseract, EasyOCR, etc.)")
    else:
        print("\n✓ Text extraction successful")

    return total_text_extracted > 0

if __name__ == "__main__":
    result = test_pypdf2_extraction("sejong.pdf")

    if not result:
        print("\n" + "="*80)
        print("ALTERNATIVE APPROACHES:")
        print("="*80)
        print("1. Manual data entry (most accurate)")
        print("2. OCR with Tesseract + Korean language pack")
        print("3. EasyOCR for Korean handwriting")
        print("4. Hybrid: OCR for printed text + manual for handwriting")
