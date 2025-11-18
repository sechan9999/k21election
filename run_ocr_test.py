#!/usr/bin/env python3
"""
세종시 선거 개표상황표 OCR 테스트 실행 스크립트
Quick test script for Sejong Election Ballot OCR
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트 디렉토리 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def check_dependencies():
    """필요한 라이브러리 확인"""
    required_packages = [
        'easyocr',
        'cv2',
        'numpy',
        'PIL',
        'pdf2image'
    ]

    missing = []
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PIL':
                from PIL import Image
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 설치 필요")
            missing.append(package)

    return missing


def run_sample_ocr_test():
    """샘플 OCR 테스트 (5페이지)"""
    print("\n" + "="*60)
    print("🚀 세종시 선거 개표상황표 OCR 테스트 시작")
    print("="*60)

    # 의존성 확인
    print("\n📦 의존성 확인 중...")
    missing = check_dependencies()

    if missing:
        print(f"\n⚠️  다음 패키지를 설치해야 합니다: {', '.join(missing)}")
        print("설치 명령: pip install " + " ".join(missing))
        return False

    # OCR 프로세서 임포트
    try:
        from ocr_processor import KoreanElectionOCR
        print("✅ OCR 프로세서 임포트 성공")
    except Exception as e:
        print(f"❌ OCR 프로세서 임포트 실패: {e}")
        return False

    # PDF 파일 확인
    pdf_path = project_root / 'sejong.pdf'
    if not pdf_path.exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return False

    print(f"✅ PDF 파일 발견: {pdf_path}")

    # OCR 처리 시작
    try:
        print("\n🔧 OCR 프로세서 초기화 중...")
        ocr = KoreanElectionOCR(gpu=False)

        print("\n📄 샘플 5페이지 처리 시작...")
        results = ocr.process_pdf(
            pdf_path=str(pdf_path),
            output_dir='./ocr_results',
            first_page=1,
            last_page=5,
            dpi=200  # 테스트용으로 낮은 해상도 사용
        )

        print("\n✅ OCR 처리 완료!")
        print(f"   처리된 페이지: {len(results)}개")

        # 간단한 통계
        total_text_blocks = sum(r['text_count'] for r in results)
        avg_confidence = sum(r['avg_confidence'] for r in results) / len(results)

        print(f"   총 텍스트 블록: {total_text_blocks}개")
        print(f"   평균 신뢰도: {avg_confidence:.2%}")

        return True

    except Exception as e:
        print(f"\n❌ OCR 처리 중 오류 발생:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_verification():
    """검증 시스템 실행"""
    print("\n" + "="*60)
    print("🔍 검증 시스템 실행")
    print("="*60)

    try:
        from verification_system import ElectionDataVerifier
        print("✅ 검증 시스템 임포트 성공")

        verifier = ElectionDataVerifier(results_dir='./ocr_results')

        # 결과 로드
        verifier.load_results()

        # 품질 보고서 생성
        report = verifier.generate_quality_report()

        # 보고서 저장
        verifier.save_report()

        # Excel 저장 시도 (openpyxl 있을 경우)
        try:
            verifier.export_to_excel()
        except Exception as e:
            print(f"⚠️  Excel 저장 실패 (openpyxl 필요): {e}")

        return True

    except Exception as e:
        print(f"\n❌ 검증 시스템 실행 중 오류 발생:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("\n" + "🌟"*30)
    print(" "*20 + "세종시 선거 개표상황표 OCR 시스템")
    print(" "*25 + "Korean Election Ballot OCR")
    print("🌟"*30 + "\n")

    # 1. OCR 테스트
    ocr_success = run_sample_ocr_test()

    if not ocr_success:
        print("\n❌ OCR 테스트 실패")
        return 1

    # 2. 검증 시스템 실행
    verification_success = run_verification()

    if not verification_success:
        print("\n⚠️  검증 시스템 실행 실패 (OCR 결과는 정상)")
        return 1

    # 완료
    print("\n" + "="*60)
    print("🎉 모든 처리 완료!")
    print("="*60)
    print("\n📁 결과 파일:")
    print("   - OCR 결과: ./ocr_results/")
    print("   - 검증 보고서: ./ocr_results/verification_report.json")
    print("   - Excel 보고서: ./ocr_results/verification_report.xlsx")
    print("\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
