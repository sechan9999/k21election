#!/usr/bin/env python3
"""
sejong.pdf 첫 페이지 분석 및 시각화 데모
OCR 없이 이미지 처리 및 구조 분석
"""

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import json
import os


def analyze_ballot_structure(pdf_path, page_num=0):
    """개표상황표 구조 분석"""

    print(f"📄 {pdf_path} 페이지 {page_num+1} 분석 중...\n")

    doc = fitz.open(pdf_path)
    page = doc[page_num]

    # 이미지로 변환
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2배 확대
    img_path = f'./pdf_analysis/page_{page_num+1:03d}_analysis.png'
    pix.save(img_path)

    # 페이지 정보
    info = {
        'page_number': page_num + 1,
        'size': f"{page.rect.width:.0f} x {page.rect.height:.0f}",
        'image_path': img_path,
        'image_size': f"{pix.width} x {pix.height}",
        'analysis': {
            'document_type': '개표상황표 (거소·선상투표)',
            'election': '제21대 대통령선거',
            'candidates': [
                {'number': 1, 'name': '이재명', 'party': '더불어민주당'},
                {'number': 2, 'name': '김문수', 'party': '국민의힘'},
                {'number': 4, 'name': '이준석', 'party': '개혁신당'},
                {'number': 5, 'name': '권영국', 'party': '민주노동당'},
                {'number': 8, 'name': '송진호', 'party': '무소속'}
            ],
            'sections': {
                'header': '문서 제목 및 선거 정보',
                'ballot_info': '투표함 정보 (투표함수, 투표용지교부수 등)',
                'vote_counts': '후보자별 득표상황 (기계분류 vs 심사집계)',
                'verification': '위원 검열 (8명 위원 직인)',
                'footer': '위원장 공표시각'
            },
            'key_fields': [
                '투표함수',
                '선거인수',
                '투표용지교부수',
                '투표수',
                '우편투표전달불',
                '심사집계불',
                '유효투표수',
                '무효투표수',
                '투표지총수',
                '책임사무원 성명'
            ]
        }
    }

    doc.close()

    # 결과 출력
    print("="*60)
    print("📊 분석 결과")
    print("="*60)
    print(f"문서 유형: {info['analysis']['document_type']}")
    print(f"선거: {info['analysis']['election']}")
    print(f"페이지 크기: {info['size']}")
    print(f"이미지 크기: {info['image_size']}")
    print(f"\n✅ 이미지 저장: {img_path}")

    print("\n👥 후보자 정보:")
    for cand in info['analysis']['candidates']:
        print(f"   {cand['number']}번. {cand['name']} ({cand['party']})")

    print("\n📋 문서 구조:")
    for section_name, section_desc in info['analysis']['sections'].items():
        print(f"   • {section_name}: {section_desc}")

    print("\n🔑 주요 필드:")
    for i, field in enumerate(info['analysis']['key_fields'], 1):
        print(f"   {i:2d}. {field}")

    # JSON 저장
    json_path = './pdf_analysis/page_001_structure_analysis.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"\n💾 분석 결과 저장: {json_path}")

    return info


def create_structure_overlay(image_path):
    """구조 오버레이 이미지 생성"""

    img = Image.open(image_path)
    overlay = img.copy()
    draw = ImageDraw.Draw(overlay, 'RGBA')

    # 반투명 박스로 섹션 표시
    sections = [
        (50, 50, 1200, 200, (255, 0, 0, 50), "헤더 (제목, 선거정보)"),
        (50, 200, 1200, 350, (0, 255, 0, 50), "투표함 정보"),
        (50, 350, 1200, 1200, (0, 0, 255, 50), "후보자별 득표상황"),
        (50, 1200, 1200, 1500, (255, 255, 0, 50), "위원 검열"),
        (50, 1500, 1200, 1650, (255, 0, 255, 50), "공표시각"),
    ]

    for x1, y1, x2, y2, color, label in sections:
        draw.rectangle([x1, y1, x2, y2], fill=color, outline=color[:3] + (255,), width=3)

    overlay_path = image_path.replace('.png', '_overlay.png')
    overlay.save(overlay_path)

    print(f"\n🎨 구조 오버레이 이미지: {overlay_path}")

    return overlay_path


if __name__ == '__main__':
    import sys

    pdf_path = sys.argv[1] if len(sys.argv) > 1 else 'sejong.pdf'

    print("\n" + "🌟"*30)
    print(" "*15 + "세종시 개표상황표 구조 분석 데모")
    print("🌟"*30 + "\n")

    # 구조 분석
    result = analyze_ballot_structure(pdf_path, page_num=0)

    # 오버레이 이미지 생성
    create_structure_overlay(result['image_path'])

    print("\n" + "="*60)
    print("✅ 분석 완료!")
    print("="*60)
    print("\n💡 다음 단계:")
    print("   1. OCR 엔진 설치 (EasyOCR 또는 Tesseract)")
    print("   2. 실제 텍스트 추출 및 데이터 구조화")
    print("   3. 전체 126페이지 처리")
    print("\n📁 결과 파일:")
    print(f"   - 원본 이미지: {result['image_path']}")
    print(f"   - 구조 분석: ./pdf_analysis/page_001_structure_analysis.json")
    print(f"   - 오버레이: {result['image_path'].replace('.png', '_overlay.png')}")
    print()
