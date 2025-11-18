#!/usr/bin/env python3
"""
전국 선거 개표상황표 배치 처리 시스템
Nationwide Election Ballot Batch Processing System
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class CityConfig:
    """도시별 설정"""
    city_name: str
    city_code: str
    pdf_path: str
    total_pages: int = None
    priority: int = 1  # 1=높음, 2=보통, 3=낮음
    notes: str = ""


class BatchProcessor:
    """배치 처리 시스템"""

    def __init__(self, data_root: str = './election_data'):
        """
        초기화

        Args:
            data_root: 데이터 루트 디렉토리
        """
        self.data_root = Path(data_root)
        self.data_root.mkdir(exist_ok=True)

        # 설정 파일 경로
        self.config_file = self.data_root / 'cities_config.json'
        self.manifest_file = self.data_root / 'data_manifest.json'

        # 도시 목록
        self.cities: List[CityConfig] = []

        print(f"📁 배치 처리 시스템 초기화")
        print(f"   데이터 루트: {self.data_root.absolute()}")

    def add_city(
        self,
        city_name: str,
        city_code: str,
        pdf_path: str,
        total_pages: int = None,
        priority: int = 1,
        notes: str = ""
    ):
        """
        도시 추가

        Args:
            city_name: 도시 이름 (예: "세종특별자치시")
            city_code: 도시 코드 (예: "sejong", "seoul", "busan")
            pdf_path: PDF 파일 경로 (상대 또는 절대)
            total_pages: 총 페이지 수
            priority: 우선순위 (1=높음, 2=보통, 3=낮음)
            notes: 메모
        """
        city = CityConfig(
            city_name=city_name,
            city_code=city_code,
            pdf_path=pdf_path,
            total_pages=total_pages,
            priority=priority,
            notes=notes
        )
        self.cities.append(city)
        print(f"   ✓ {city_name} ({city_code}) 추가됨")

    def save_config(self):
        """설정 저장"""
        config_data = {
            'cities': [asdict(city) for city in self.cities],
            'total_cities': len(self.cities),
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 설정 저장: {self.config_file}")
        print(f"   도시 수: {len(self.cities)}")

    def load_config(self):
        """설정 로드"""
        if not self.config_file.exists():
            print(f"⚠️  설정 파일 없음: {self.config_file}")
            return

        with open(self.config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        self.cities = [CityConfig(**city) for city in config_data['cities']]
        print(f"📂 설정 로드: {len(self.cities)}개 도시")

    def get_pdf_info(self, pdf_path: str) -> Dict[str, Any]:
        """PDF 정보 추출"""
        import fitz

        if not os.path.exists(pdf_path):
            return {'error': 'File not found', 'exists': False}

        doc = fitz.open(pdf_path)
        info = {
            'exists': True,
            'path': pdf_path,
            'size_bytes': os.path.getsize(pdf_path),
            'size_mb': os.path.getsize(pdf_path) / (1024 * 1024),
            'total_pages': len(doc),
            'metadata': doc.metadata
        }
        doc.close()

        return info

    def calculate_file_hash(self, file_path: str) -> str:
        """파일 해시 계산 (대용량 파일 지원)"""
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            # 청크 단위로 읽기 (메모리 효율적)
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    def create_data_manifest(self):
        """데이터 매니페스트 생성"""
        manifest = {
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'cities': []
        }

        print("\n📊 데이터 매니페스트 생성 중...")

        total_size = 0
        total_pages = 0

        for city in self.cities:
            print(f"   - {city.city_name} ({city.city_code}) 분석 중...")

            pdf_info = self.get_pdf_info(city.pdf_path)

            if pdf_info['exists']:
                # 파일 해시 계산 (선택적)
                file_hash = self.calculate_file_hash(city.pdf_path)

                city_manifest = {
                    'city_name': city.city_name,
                    'city_code': city.city_code,
                    'pdf_path': city.pdf_path,
                    'file_size_mb': pdf_info['size_mb'],
                    'total_pages': pdf_info['total_pages'],
                    'file_hash': file_hash,
                    'priority': city.priority,
                    'notes': city.notes
                }

                manifest['cities'].append(city_manifest)
                total_size += pdf_info['size_mb']
                total_pages += pdf_info['total_pages']

                print(f"     ✓ {pdf_info['total_pages']}페이지, "
                      f"{pdf_info['size_mb']:.1f}MB")
            else:
                print(f"     ✗ 파일 없음: {city.pdf_path}")

        manifest['summary'] = {
            'total_cities': len(manifest['cities']),
            'total_size_mb': total_size,
            'total_size_gb': total_size / 1024,
            'total_pages': total_pages
        }

        # 저장
        with open(self.manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 매니페스트 저장: {self.manifest_file}")
        print(f"\n📈 전체 통계:")
        print(f"   - 총 도시: {manifest['summary']['total_cities']}개")
        print(f"   - 총 크기: {manifest['summary']['total_size_gb']:.2f} GB")
        print(f"   - 총 페이지: {manifest['summary']['total_pages']:,}페이지")

        return manifest

    def process_all_cities(
        self,
        num_workers: int = None,
        dpi: int = 200,
        use_ocr: bool = True,
        dry_run: bool = False
    ):
        """
        모든 도시 처리

        Args:
            num_workers: 워커 수
            dpi: 해상도
            use_ocr: OCR 사용 여부
            dry_run: 실제 처리 없이 계획만 출력
        """
        from ocr_processor_multiprocessing import MultiProcessingOCR

        print(f"\n{'='*60}")
        print(f"🚀 전국 배치 처리 시작")
        print(f"{'='*60}")

        if dry_run:
            print("⚠️  DRY RUN 모드: 실제 처리하지 않음\n")

        # 우선순위별 정렬
        sorted_cities = sorted(self.cities, key=lambda x: x.priority)

        processor = MultiProcessingOCR(num_workers=num_workers)

        results_summary = []

        for i, city in enumerate(sorted_cities, 1):
            print(f"\n[{i}/{len(sorted_cities)}] {city.city_name} ({city.city_code})")
            print(f"{'─'*60}")

            pdf_info = self.get_pdf_info(city.pdf_path)

            if not pdf_info['exists']:
                print(f"   ✗ PDF 파일 없음: {city.pdf_path}")
                continue

            output_dir = self.data_root / city.city_code / 'ocr_results'

            print(f"   PDF: {city.pdf_path}")
            print(f"   크기: {pdf_info['size_mb']:.1f} MB")
            print(f"   페이지: {pdf_info['total_pages']}")
            print(f"   출력: {output_dir}")

            if dry_run:
                print(f"   ⏩ 건너뜀 (dry-run)")
                continue

            # 실제 처리
            start_time = time.time()
            try:
                results = processor.process_pdf_parallel(
                    pdf_path=city.pdf_path,
                    output_dir=str(output_dir),
                    dpi=dpi,
                    use_ocr=use_ocr
                )

                processing_time = time.time() - start_time

                city_summary = {
                    'city_name': city.city_name,
                    'city_code': city.city_code,
                    'success': True,
                    'total_pages': len(results),
                    'successful_pages': sum(1 for r in results if r['success']),
                    'processing_time': processing_time
                }

                print(f"   ✅ 완료: {processing_time/60:.1f}분")

            except Exception as e:
                print(f"   ❌ 오류: {e}")
                city_summary = {
                    'city_name': city.city_name,
                    'city_code': city.city_code,
                    'success': False,
                    'error': str(e)
                }

            results_summary.append(city_summary)

        # 전체 요약 저장
        summary_path = self.data_root / 'batch_processing_summary.json'
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'cities': results_summary,
                'total_cities': len(results_summary),
                'successful_cities': sum(1 for c in results_summary if c['success'])
            }, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*60}")
        print(f"🎉 배치 처리 완료")
        print(f"{'='*60}")
        print(f"결과 요약: {summary_path}")


def setup_default_cities():
    """기본 도시 목록 설정 예제"""
    processor = BatchProcessor()

    # 예제: 전국 주요 도시
    cities_data = [
        # (도시명, 코드, PDF 경로, 우선순위, 메모)
        ("세종특별자치시", "sejong", "sejong.pdf", 1, "테스트 완료 - 126페이지"),
        ("서울특별시", "seoul", "data/seoul.pdf", 2, "대용량 예상"),
        ("부산광역시", "busan", "data/busan.pdf", 2, ""),
        ("대구광역시", "daegu", "data/daegu.pdf", 2, ""),
        ("인천광역시", "incheon", "data/incheon.pdf", 2, ""),
        ("광주광역시", "gwangju", "data/gwangju.pdf", 3, ""),
        ("대전광역시", "daejeon", "data/daejeon.pdf", 3, ""),
        ("울산광역시", "ulsan", "data/ulsan.pdf", 3, ""),
        ("경기도", "gyeonggi", "data/gyeonggi.pdf", 1, "최대 규모"),
        ("강원도", "gangwon", "data/gangwon.pdf", 3, ""),
        ("충청북도", "chungbuk", "data/chungbuk.pdf", 3, ""),
        ("충청남도", "chungnam", "data/chungnam.pdf", 3, ""),
        ("전라북도", "jeonbuk", "data/jeonbuk.pdf", 3, ""),
        ("전라남도", "jeonnam", "data/jeonnam.pdf", 3, ""),
        ("경상북도", "gyeongbuk", "data/gyeongbuk.pdf", 3, ""),
        ("경상남도", "gyeongnam", "data/gyeongnam.pdf", 3, ""),
        ("제주특별자치도", "jeju", "data/jeju.pdf", 3, ""),
    ]

    for city_name, code, pdf_path, priority, notes in cities_data:
        processor.add_city(
            city_name=city_name,
            city_code=code,
            pdf_path=pdf_path,
            priority=priority,
            notes=notes
        )

    processor.save_config()
    return processor


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description='전국 선거 개표상황표 배치 처리'
    )
    parser.add_argument(
        '--setup',
        action='store_true',
        help='기본 도시 목록 설정'
    )
    parser.add_argument(
        '--manifest',
        action='store_true',
        help='데이터 매니페스트 생성'
    )
    parser.add_argument(
        '--process',
        action='store_true',
        help='모든 도시 처리'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='실제 처리 없이 계획만 출력'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=None,
        help='워커 수'
    )
    parser.add_argument(
        '--dpi',
        type=int,
        default=200,
        help='해상도'
    )
    parser.add_argument(
        '--no-ocr',
        action='store_true',
        help='OCR 비활성화'
    )

    args = parser.parse_args()

    if args.setup:
        print("🔧 기본 도시 목록 설정 중...")
        processor = setup_default_cities()
        print("✅ 설정 완료!")
        return

    processor = BatchProcessor()

    if args.manifest:
        processor.load_config()
        processor.create_data_manifest()
        return

    if args.process:
        processor.load_config()
        processor.process_all_cities(
            num_workers=args.workers,
            dpi=args.dpi,
            use_ocr=not args.no_ocr,
            dry_run=args.dry_run
        )
        return

    # 기본 동작: 설정 로드 및 정보 표시
    processor.load_config()
    print(f"\n💡 사용 가능한 명령:")
    print(f"   --setup      : 기본 도시 목록 설정")
    print(f"   --manifest   : 데이터 매니페스트 생성")
    print(f"   --process    : 모든 도시 처리")
    print(f"   --dry-run    : 처리 계획 미리보기")


if __name__ == '__main__':
    main()
