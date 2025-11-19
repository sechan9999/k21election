#!/usr/bin/env python3
"""
K21 선거 데이터 자동 다운로드 스크립트

Google Drive에서 대용량 PDF 및 이미지 데이터를 자동으로 다운로드합니다.

사용법:
    python download_data.py --city sejong
    python download_data.py --city jeju --include-pages
    python download_data.py --city all
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import gdown
except ImportError:
    print("gdown 라이브러리가 필요합니다. 설치 중...")
    os.system("pip install gdown -q")
    import gdown

try:
    import requests
except ImportError:
    print("requests 라이브러리가 필요합니다. 설치 중...")
    os.system("pip install requests -q")
    import requests

# Google Drive 파일 ID
# 실제 사용 시 아래 ID들을 실제 Google Drive 파일 ID로 교체하세요
DATASETS = {
    'sejong': {
        'pdf_id': 'REPLACE_WITH_SEJONG_PDF_FILE_ID',
        'pages_folder_id': 'REPLACE_WITH_SEJONG_PAGES_FOLDER_ID',
        'size': '3.7MB',
        'pages_count': 126,
        'pages_size': '35MB'
    },
    'jeju': {
        'pdf_id': 'REPLACE_WITH_JEJU_PDF_FILE_ID',
        'pages_folder_id': 'REPLACE_WITH_JEJU_PAGES_FOLDER_ID',
        'size': '8.6MB',
        'pages_count': 172,
        'pages_size': '69MB'
    },
    'all': {
        'archive_id': 'REPLACE_WITH_ALL_DATA_ARCHIVE_ID',
        'size': '1.5GB',
        'description': '전국 모든 시도 데이터 (압축)'
    }
}

# 대체 다운로드 URL (직접 링크)
ALTERNATIVE_URLS = {
    'sejong': {
        'pdf': 'https://github.com/sechan9999/k21election/raw/main/sejong.pdf',
    },
    'jeju': {
        'pdf': 'https://github.com/sechan9999/k21election/raw/main/jeju.pdf',
    }
}


def check_file_exists(file_path):
    """파일 존재 여부 확인"""
    if Path(file_path).exists():
        print(f"⚠️  파일이 이미 존재합니다: {file_path}")
        response = input("덮어쓰시겠습니까? (y/n): ")
        return response.lower() == 'y'
    return True


def download_from_google_drive(file_id, output_path, description="파일"):
    """Google Drive에서 파일 다운로드"""
    try:
        url = f"https://drive.google.com/uc?id={file_id}"
        print(f"\n📥 {description} 다운로드 중...")
        print(f"   URL: {url}")
        print(f"   저장 위치: {output_path}")

        gdown.download(url, str(output_path), quiet=False)
        print(f"✓ 완료: {output_path}")
        return True
    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        return False


def download_from_github(url, output_path, description="파일"):
    """GitHub에서 직접 다운로드 (대체 방법)"""
    try:
        print(f"\n📥 {description} 다운로드 중 (GitHub)...")
        print(f"   URL: {url}")

        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r   진행률: {percent:.1f}%", end='')

        print(f"\n✓ 완료: {output_path}")
        return True
    except Exception as e:
        print(f"\n✗ 오류 발생: {e}")
        return False


def download_folder_from_google_drive(folder_id, output_dir, description="폴더"):
    """Google Drive 폴더 다운로드"""
    try:
        url = f"https://drive.google.com/drive/folders/{folder_id}"
        print(f"\n📁 {description} 다운로드 중...")
        print(f"   폴더 URL: {url}")
        print(f"   저장 위치: {output_dir}")

        gdown.download_folder(url, str(output_dir), quiet=False)
        print(f"✓ 완료: {output_dir}")
        return True
    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        return False


def download_city_data(city, include_pages=False, use_github=False):
    """특정 도시 데이터 다운로드"""
    if city not in DATASETS:
        print(f"오류: 지원하지 않는 도시입니다: {city}")
        print(f"사용 가능한 도시: {', '.join(DATASETS.keys())}")
        return False

    print("=" * 80)
    print(f"{city.upper()} 선거 데이터 다운로드")
    print("=" * 80)

    dataset = DATASETS[city]
    output_dir = Path('data') / city
    output_dir.mkdir(parents=True, exist_ok=True)

    # PDF 다운로드
    pdf_path = output_dir / f"{city}.pdf"

    if check_file_exists(pdf_path):
        if use_github and city in ALTERNATIVE_URLS:
            # GitHub에서 다운로드 (대체 방법)
            success = download_from_github(
                ALTERNATIVE_URLS[city]['pdf'],
                pdf_path,
                f"{city.upper()} PDF ({dataset['size']})"
            )
        else:
            # Google Drive에서 다운로드
            if dataset['pdf_id'].startswith('REPLACE'):
                print(f"\n⚠️  Google Drive 파일 ID가 설정되지 않았습니다!")
                print(f"   download_data.py 파일을 열어 DATASETS['{city}']['pdf_id']를 설정하세요.")
                print(f"\n   또는 GitHub에서 다운로드하려면 --github 옵션을 사용하세요:")
                print(f"   python download_data.py --city {city} --github")
                return False

            success = download_from_google_drive(
                dataset['pdf_id'],
                pdf_path,
                f"{city.upper()} PDF ({dataset['size']})"
            )

        if not success:
            return False

    # 페이지 이미지 다운로드 (선택사항)
    if include_pages:
        pages_dir = output_dir / 'pages'

        if dataset['pages_folder_id'].startswith('REPLACE'):
            print(f"\n⚠️  Google Drive 폴더 ID가 설정되지 않았습니다!")
            print(f"   페이지 이미지 다운로드를 건너뜁니다.")
        else:
            download_folder_from_google_drive(
                dataset['pages_folder_id'],
                pages_dir,
                f"{city.upper()} 페이지 이미지 ({dataset['pages_count']}개, {dataset['pages_size']})"
            )

    print("\n" + "=" * 80)
    print(f"✓ {city.upper()} 데이터 다운로드 완료!")
    print("=" * 80)
    print(f"저장 위치: {output_dir}")
    print(f"  - PDF: {pdf_path}")
    if include_pages:
        print(f"  - 페이지: {output_dir / 'pages'}")
    print("=" * 80)

    return True


def download_all_data():
    """전체 데이터 압축 파일 다운로드"""
    print("=" * 80)
    print("전체 선거 데이터 다운로드 (압축)")
    print("=" * 80)

    dataset = DATASETS['all']
    output_file = Path('korea_election_data.7z')

    if dataset['archive_id'].startswith('REPLACE'):
        print("\n⚠️  Google Drive 파일 ID가 설정되지 않았습니다!")
        print("   download_data.py 파일을 열어 DATASETS['all']['archive_id']를 설정하세요.")
        return False

    if check_file_exists(output_file):
        success = download_from_google_drive(
            dataset['archive_id'],
            output_file,
            f"전체 데이터 압축 파일 ({dataset['size']})"
        )

        if not success:
            return False

    # 압축 해제
    print("\n📦 압축 해제 중...")
    result = os.system(f"7z x {output_file} -odata/")

    if result == 0:
        print("✓ 압축 해제 완료!")
        print(f"\n압축 파일 삭제 여부 (y/n): ", end='')
        response = input()
        if response.lower() == 'y':
            output_file.unlink()
            print("✓ 압축 파일 삭제 완료")
    else:
        print("✗ 압축 해제 실패")
        print("  7zip이 설치되어 있는지 확인하세요.")

    return True


def verify_downloads():
    """다운로드된 파일 검증"""
    print("\n" + "=" * 80)
    print("다운로드 파일 검증")
    print("=" * 80)

    data_dir = Path('data')
    if not data_dir.exists():
        print("⚠️  data/ 디렉토리가 없습니다.")
        return

    for city in ['sejong', 'jeju']:
        city_dir = data_dir / city
        if city_dir.exists():
            pdf_file = city_dir / f"{city}.pdf"
            pages_dir = city_dir / 'pages'

            print(f"\n{city.upper()}:")
            print(f"  PDF: {'✓' if pdf_file.exists() else '✗'} {pdf_file}")
            if pdf_file.exists():
                size_mb = pdf_file.stat().st_size / 1024 / 1024
                print(f"       크기: {size_mb:.2f} MB")

            if pages_dir.exists():
                page_count = len(list(pages_dir.glob('*.png')))
                print(f"  페이지: ✓ {page_count}개")
        else:
            print(f"\n{city.upper()}: ✗ 없음")


def main():
    parser = argparse.ArgumentParser(
        description='K21 선거 데이터 다운로드 스크립트',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  세종시 PDF만:
    python download_data.py --city sejong

  제주시 PDF + 페이지 이미지:
    python download_data.py --city jeju --include-pages

  GitHub에서 다운로드 (Google Drive ID 미설정 시):
    python download_data.py --city sejong --github

  전체 압축 파일:
    python download_data.py --city all

  다운로드 검증:
    python download_data.py --verify
        """
    )

    parser.add_argument(
        '--city',
        choices=['sejong', 'jeju', 'all'],
        help='다운로드할 도시 선택'
    )

    parser.add_argument(
        '--include-pages',
        action='store_true',
        help='페이지 이미지도 다운로드 (용량 큼)'
    )

    parser.add_argument(
        '--github',
        action='store_true',
        help='GitHub에서 직접 다운로드 (Google Drive 대신)'
    )

    parser.add_argument(
        '--verify',
        action='store_true',
        help='다운로드된 파일 검증'
    )

    args = parser.parse_args()

    # 검증만 수행
    if args.verify:
        verify_downloads()
        return

    # 도시 선택 없이 실행 시 도움말 표시
    if not args.city:
        parser.print_help()
        print("\n" + "=" * 80)
        print("빠른 시작:")
        print("=" * 80)
        print("1. 세종시 데이터 다운로드:")
        print("   python download_data.py --city sejong")
        print("\n2. 제주시 데이터 다운로드:")
        print("   python download_data.py --city jeju")
        print("\n3. 모든 도시 데이터 (압축):")
        print("   python download_data.py --city all")
        return

    # 다운로드 실행
    if args.city == 'all':
        download_all_data()
    else:
        download_city_data(args.city, args.include_pages, args.github)


if __name__ == '__main__':
    main()
