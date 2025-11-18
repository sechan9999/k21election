#!/usr/bin/env python3
"""
Simple PDF analyzer using PyMuPDF (no external dependencies needed)
"""

import fitz  # PyMuPDF
import json
import os
from PIL import Image
import io


def analyze_pdf(pdf_path, output_dir='./pdf_analysis'):
    """PDF 기본 분석 및 이미지 추출"""

    os.makedirs(output_dir, exist_ok=True)

    print(f"📄 PDF 분석 시작: {pdf_path}")

    # PDF 열기
    doc = fitz.open(pdf_path)

    info = {
        'filename': pdf_path,
        'pages': len(doc),
        'metadata': doc.metadata,
        'page_info': []
    }

    print(f"   총 페이지 수: {len(doc)}")
    print(f"   제목: {doc.metadata.get('title', 'N/A')}")
    print(f"   작성자: {doc.metadata.get('author', 'N/A')}")

    # 처음 3페이지 이미지로 추출
    print("\n📸 처음 3페이지 이미지 추출 중...")

    for page_num in range(min(3, len(doc))):
        page = doc[page_num]

        # 페이지 정보
        page_info = {
            'page_number': page_num + 1,
            'width': page.rect.width,
            'height': page.rect.height,
            'rotation': page.rotation
        }

        # 텍스트 추출 시도 (스캔 문서면 비어있을 것)
        text = page.get_text()
        page_info['text_length'] = len(text)
        page_info['has_text'] = len(text.strip()) > 0

        # 이미지로 변환 (150 DPI)
        pix = page.get_pixmap(matrix=fitz.Matrix(150/72, 150/72))

        # PNG로 저장
        img_path = os.path.join(output_dir, f'page_{page_num+1:03d}.png')
        pix.save(img_path)

        page_info['image_path'] = img_path
        page_info['image_size'] = os.path.getsize(img_path)

        info['page_info'].append(page_info)

        print(f"   ✓ 페이지 {page_num+1}: {pix.width}x{pix.height} → {img_path}")

    doc.close()

    # 결과 저장
    json_path = os.path.join(output_dir, 'pdf_analysis.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 분석 완료! 결과: {json_path}")

    return info


if __name__ == '__main__':
    import sys

    pdf_path = sys.argv[1] if len(sys.argv) > 1 else 'sejong.pdf'

    result = analyze_pdf(pdf_path)

    print("\n" + "="*60)
    print("📊 요약")
    print("="*60)
    print(f"총 페이지: {result['pages']}")
    print(f"이미지 추출: {len(result['page_info'])}개")

    for page_info in result['page_info']:
        has_text = "✓ 텍스트 있음" if page_info['has_text'] else "✗ 스캔 이미지"
        print(f"  페이지 {page_info['page_number']}: {has_text}")

    print("\n💡 다음 단계: OCR 처리가 필요합니다 (EasyOCR 또는 Tesseract)")
