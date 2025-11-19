#!/usr/bin/env python3
"""
한글 파일명 및 압축 파일 자동 처리 스크립트

지원 형식:
- ZIP (.zip)
- 7Z (.7z)
- RAR (.rar)
- PDF (직접)

한글 파일명 자동 인식 및 처리
"""

import os
import sys
import zipfile
import subprocess
from pathlib import Path
import shutil

# 한글 지역명 → 영문 매핑
REGION_NAME_MAP = {
    # 특별시/광역시
    '서울': 'seoul',
    '서울시': 'seoul',
    '서울특별시': 'seoul',
    '부산': 'busan',
    '부산시': 'busan',
    '부산광역시': 'busan',
    '인천': 'incheon',
    '인천시': 'incheon',
    '인천광역시': 'incheon',
    '대구': 'daegu',
    '대구시': 'daegu',
    '대구광역시': 'daegu',
    '광주': 'gwangju',
    '광주시': 'gwangju',
    '광주광역시': 'gwangju',
    '대전': 'daejeon',
    '대전시': 'daejeon',
    '대전광역시': 'daejeon',
    '울산': 'ulsan',
    '울산시': 'ulsan',
    '울산광역시': 'ulsan',
    '세종': 'sejong',
    '세종시': 'sejong',
    '세종특별자치시': 'sejong',

    # 도
    '경기': 'gyeonggi',
    '경기도': 'gyeonggi',
    '강원': 'gangwon',
    '강원도': 'gangwon',
    '충북': 'chungbuk',
    '충청북도': 'chungbuk',
    '충남': 'chungnam',
    '충청남도': 'chungnam',
    '전북': 'jeonbuk',
    '전라북도': 'jeonbuk',
    '전남': 'jeonnam',
    '전라남도': 'jeonnam',
    '경북': 'gyeongbuk',
    '경상북도': 'gyeongbuk',
    '경남': 'gyeongnam',
    '경상남도': 'gyeongnam',
    '제주': 'jeju',
    '제주도': 'jeju',
    '제주특별자치도': 'jeju',

    # 시/군
    '제주시': 'jeju_city',
    '서귀포': 'seogwipo',
    '서귀포시': 'seogwipo',
}


def detect_region_name(filename):
    """파일명에서 지역명 추출"""
    # 확장자 제거
    name = Path(filename).stem

    # 한글 지역명 찾기
    for korean, english in REGION_NAME_MAP.items():
        if korean in name:
            return english, korean

    return None, None


def extract_archive(archive_path, output_dir):
    """압축 파일 해제"""
    archive_path = Path(archive_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📦 압축 파일 해제: {archive_path.name}")

    ext = archive_path.suffix.lower()

    try:
        if ext == '.zip':
            # ZIP 파일
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                # 한글 파일명 인코딩 문제 해결
                for member in zip_ref.namelist():
                    try:
                        # UTF-8로 시도
                        member_name = member
                    except:
                        # CP949로 재시도 (Windows)
                        member_name = member.encode('cp437').decode('cp949', errors='ignore')

                    zip_ref.extract(member, output_dir)
                    print(f"  ✓ {member_name}")

            print(f"✓ ZIP 압축 해제 완료: {output_dir}")
            return True

        elif ext == '.7z':
            # 7Z 파일
            result = subprocess.run(
                ['7z', 'x', str(archive_path), f'-o{output_dir}', '-y'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✓ 7Z 압축 해제 완료: {output_dir}")
                return True
            else:
                print(f"✗ 7Z 압축 해제 실패: {result.stderr}")
                return False

        elif ext == '.rar':
            # RAR 파일
            result = subprocess.run(
                ['unrar', 'x', '-y', str(archive_path), str(output_dir)],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✓ RAR 압축 해제 완료: {output_dir}")
                return True
            else:
                print(f"✗ RAR 압축 해제 실패: {result.stderr}")
                return False

        else:
            print(f"⚠️  지원하지 않는 압축 형식: {ext}")
            return False

    except Exception as e:
        print(f"✗ 압축 해제 오류: {e}")
        return False


def find_pdf_in_directory(directory):
    """디렉토리에서 PDF 파일 찾기"""
    pdf_files = list(Path(directory).rglob('*.pdf'))

    if not pdf_files:
        print(f"⚠️  PDF 파일을 찾을 수 없습니다: {directory}")
        return None

    if len(pdf_files) == 1:
        return pdf_files[0]

    # 여러 PDF 파일이 있는 경우, 가장 큰 파일 선택
    largest_pdf = max(pdf_files, key=lambda p: p.stat().st_size)
    print(f"ℹ️  {len(pdf_files)}개 PDF 발견, 가장 큰 파일 선택: {largest_pdf.name}")
    return largest_pdf


def process_region_data(file_path):
    """지역 데이터 처리"""
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"✗ 파일을 찾을 수 없습니다: {file_path}")
        return None

    # 지역명 추출
    region_en, region_kr = detect_region_name(file_path.name)

    if not region_en:
        print(f"⚠️  파일명에서 지역명을 인식할 수 없습니다: {file_path.name}")
        print(f"   지원 지역: {', '.join(set(REGION_NAME_MAP.values()))}")
        return None

    print(f"\n{'='*80}")
    print(f"📍 지역 인식: {region_kr} ({region_en.upper()})")
    print(f"{'='*80}")

    # 출력 디렉토리
    output_dir = Path('regional_data') / region_en
    output_dir.mkdir(parents=True, exist_ok=True)

    # PDF 파일인 경우
    if file_path.suffix.lower() == '.pdf':
        print(f"✓ PDF 파일 직접 처리")
        pdf_path = output_dir / f"{region_en}.pdf"
        shutil.copy(file_path, pdf_path)

        return {
            'region_en': region_en,
            'region_kr': region_kr,
            'pdf_path': pdf_path,
            'source': 'direct'
        }

    # 압축 파일인 경우
    elif file_path.suffix.lower() in ['.zip', '.7z', '.rar']:
        extract_dir = output_dir / 'extracted'

        if extract_archive(file_path, extract_dir):
            # 압축 해제 후 PDF 찾기
            pdf_path = find_pdf_in_directory(extract_dir)

            if pdf_path:
                # PDF를 루트로 이동
                final_pdf_path = output_dir / f"{region_en}.pdf"
                shutil.copy(pdf_path, final_pdf_path)

                print(f"✓ PDF 추출 완료: {final_pdf_path}")

                return {
                    'region_en': region_en,
                    'region_kr': region_kr,
                    'pdf_path': final_pdf_path,
                    'source': 'archive'
                }

        return None

    else:
        print(f"⚠️  지원하지 않는 파일 형식: {file_path.suffix}")
        return None


def analyze_region(region_data):
    """지역 데이터 분석"""
    if not region_data:
        return

    print(f"\n{'='*80}")
    print(f"📊 {region_data['region_kr']} 분석 시작")
    print(f"{'='*80}")

    pdf_path = region_data['pdf_path']
    region_en = region_data['region_en']

    # PDF 정보 확인
    try:
        import fitz
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        file_size = pdf_path.stat().st_size / 1024 / 1024
        doc.close()

        print(f"\n📄 PDF 정보:")
        print(f"  - 파일: {pdf_path.name}")
        print(f"  - 크기: {file_size:.2f} MB")
        print(f"  - 페이지: {page_count}개")

        # 페이지 추출
        print(f"\n🔄 멀티프로세싱 페이지 추출 중...")
        pages_dir = pdf_path.parent / 'pages'

        result = subprocess.run(
            ['python3', 'multiprocess_pdf_extractor.py',
             str(pdf_path), str(pages_dir), '150'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(result.stdout)

            return {
                **region_data,
                'page_count': page_count,
                'file_size_mb': file_size,
                'pages_dir': pages_dir,
                'status': 'success'
            }
        else:
            print(f"✗ 페이지 추출 실패:")
            print(result.stderr)
            return None

    except ImportError:
        print("⚠️  PyMuPDF가 설치되지 않았습니다: pip install PyMuPDF")
        return None
    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        return None


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description='한글 파일명 및 압축 파일 자동 처리',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'files',
        nargs='+',
        help='처리할 파일 (PDF 또는 압축 파일)'
    )

    parser.add_argument(
        '--analyze',
        action='store_true',
        help='페이지 추출 및 분석 수행'
    )

    args = parser.parse_args()

    results = []

    for file_path in args.files:
        print(f"\n{'='*80}")
        print(f"파일 처리: {file_path}")
        print(f"{'='*80}")

        region_data = process_region_data(file_path)

        if region_data and args.analyze:
            result = analyze_region(region_data)
            if result:
                results.append(result)
        elif region_data:
            results.append(region_data)

    # 최종 요약
    if results:
        print(f"\n{'='*80}")
        print(f"처리 완료 요약")
        print(f"{'='*80}")

        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['region_kr']} ({result['region_en'].upper()})")
            print(f"   PDF: {result['pdf_path']}")
            if 'page_count' in result:
                print(f"   페이지: {result['page_count']}개")
                print(f"   크기: {result['file_size_mb']:.2f} MB")
            print(f"   상태: {'✓ 완료' if result.get('status') == 'success' else '✓ 추출됨'}")


if __name__ == '__main__':
    main()
