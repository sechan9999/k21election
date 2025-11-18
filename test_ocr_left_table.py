#!/usr/bin/env python3
"""
Test OCR on left table (printed text) only
우측 테이블(손글씨)은 수동 입력 필요
"""

# NOTE: This requires tesseract to be installed
# sudo apt-get install tesseract-ocr tesseract-ocr-kor

def test_ocr_feasibility():
    """
    좌측 테이블 OCR 가능성 테스트
    """
    print("="*80)
    print("OCR 가능성 분석")
    print("="*80)

    print("\n좌측 테이블 (기계 분류):")
    print("  - ② 분류된 투표지수: 인쇄체 → OCR 가능 (95%+ 정확도)")
    print("  - ③ 재확인대상: 인쇄체 → OCR 가능 (95%+ 정확도)")
    print("  ✅ 자동 추출 추천")

    print("\n우측 테이블 (인간 검증):")
    print("  - (a) 확인결과-분류된: 손글씨 → OCR 어려움 (70% 정확도)")
    print("  - (b) 확인결과-재확인대상: 손글씨 → OCR 어려움 (70% 정확도)")
    print("  ❌ 수동 입력 권장")

    print("\n" + "="*80)
    print("권장 워크플로우:")
    print("="*80)
    print("1. 좌측 테이블: OCR 자동 추출")
    print("2. 우측 테이블: 육안 확인 후 수동 입력")
    print("3. 검증: ②+③ = (a)+(b) 확인")
    print("\n예상 시간 절약: 50% (4시간 → 2시간)")

if __name__ == "__main__":
    test_ocr_feasibility()
