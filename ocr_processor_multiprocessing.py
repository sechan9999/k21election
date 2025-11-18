#!/usr/bin/env python3
"""
멀티프로세싱 기반 대용량 선거 개표상황표 OCR 처리 시스템
Multi-processing Korean Election Ballot OCR System for Large-scale Processing
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
from multiprocessing import Pool, cpu_count, Manager
from functools import partial
import warnings
warnings.filterwarnings('ignore')

import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import cv2


class MultiProcessingOCR:
    """멀티프로세싱 OCR 처리 클래스"""

    def __init__(self, num_workers: int = None, gpu: bool = False):
        """
        초기화

        Args:
            num_workers: 워커 프로세스 수 (기본값: CPU 코어 수)
            gpu: GPU 사용 여부 (멀티프로세싱 시 주의 필요)
        """
        self.num_workers = num_workers or max(1, cpu_count() - 1)
        self.gpu = gpu

        print(f"🔧 멀티프로세싱 OCR 초기화")
        print(f"   - 워커 수: {self.num_workers}")
        print(f"   - CPU 코어: {cpu_count()}")
        print(f"   - GPU 사용: {self.gpu}")

        # 후보자 정보
        self.candidates = {
            1: {'name': '이재명', 'party': '더불어민주당'},
            2: {'name': '김문수', 'party': '국민의힘'},
            4: {'name': '이준석', 'party': '개혁신당'},
            5: {'name': '권영국', 'party': '민주노동당'},
            8: {'name': '송진호', 'party': '무소속'},
        }

    @staticmethod
    def extract_page_as_image(pdf_path: str, page_num: int, dpi: int = 200) -> Tuple[int, np.ndarray]:
        """
        PDF 페이지를 이미지로 추출 (워커 프로세스용)

        Args:
            pdf_path: PDF 파일 경로
            page_num: 페이지 번호 (0-indexed)
            dpi: 해상도

        Returns:
            (page_num, image_array)
        """
        doc = fitz.open(pdf_path)
        page = doc[page_num]

        # 이미지로 변환
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)

        # numpy array로 변환
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

        # RGB 변환 (필요시)
        if pix.n == 4:  # RGBA
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        doc.close()

        return page_num, img

    @staticmethod
    def preprocess_image(image: np.ndarray) -> np.ndarray:
        """이미지 전처리"""
        # 그레이스케일
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image

        # 노이즈 제거
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

        # 대비 향상
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)

        return enhanced

    @staticmethod
    def process_page_worker(
        args: Tuple[str, int, int, str, bool]
    ) -> Dict[str, Any]:
        """
        단일 페이지 처리 워커 함수 (멀티프로세싱용)

        Args:
            args: (pdf_path, page_num, dpi, output_dir, use_ocr)

        Returns:
            처리 결과 딕셔너리
        """
        pdf_path, page_num, dpi, output_dir, use_ocr = args

        start_time = time.time()

        try:
            # 이미지 추출
            _, image = MultiProcessingOCR.extract_page_as_image(pdf_path, page_num, dpi)

            # 전처리
            processed = MultiProcessingOCR.preprocess_image(image)

            # OCR 수행 (선택적)
            ocr_result = None
            if use_ocr:
                try:
                    # EasyOCR 초기화 (각 프로세스별)
                    import easyocr
                    reader = easyocr.Reader(['ko', 'en'], gpu=False)  # 멀티프로세싱 시 GPU 비활성화
                    ocr_result = reader.readtext(processed)
                except ImportError:
                    ocr_result = None
                    print(f"⚠️  페이지 {page_num + 1}: EasyOCR 미설치됨")

            # 결과 저장
            result = {
                'page_number': page_num + 1,
                'success': True,
                'image_shape': image.shape,
                'processing_time': time.time() - start_time,
                'has_ocr': ocr_result is not None,
                'ocr_text_count': len(ocr_result) if ocr_result else 0
            }

            # OCR 결과 저장 (있을 경우)
            if ocr_result:
                result['ocr_results'] = [
                    {
                        'text': text,
                        'confidence': float(conf),
                        'bbox': bbox
                    }
                    for bbox, text, conf in ocr_result
                ]
                result['avg_confidence'] = np.mean([r[2] for r in ocr_result]) if ocr_result else 0.0

            # 이미지 저장
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                img_path = os.path.join(output_dir, f'page_{page_num + 1:04d}.png')
                cv2.imwrite(img_path, processed)
                result['image_path'] = img_path

            # JSON 저장
            if output_dir:
                json_path = os.path.join(output_dir, f'page_{page_num + 1:04d}.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

            return result

        except Exception as e:
            return {
                'page_number': page_num + 1,
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time
            }

    def process_pdf_parallel(
        self,
        pdf_path: str,
        output_dir: str = './ocr_results_mp',
        dpi: int = 200,
        first_page: int = None,
        last_page: int = None,
        use_ocr: bool = True,
        chunk_size: int = 10
    ) -> List[Dict[str, Any]]:
        """
        PDF를 병렬로 처리

        Args:
            pdf_path: PDF 파일 경로
            output_dir: 결과 저장 디렉토리
            dpi: 해상도
            first_page: 시작 페이지 (1-indexed)
            last_page: 끝 페이지 (1-indexed)
            use_ocr: OCR 수행 여부
            chunk_size: 청크 크기 (한번에 처리할 페이지 수)

        Returns:
            처리 결과 리스트
        """
        # PDF 정보 가져오기
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        doc.close()

        # 페이지 범위 설정
        start_idx = (first_page - 1) if first_page else 0
        end_idx = last_page if last_page else total_pages
        page_range = range(start_idx, end_idx)

        print(f"\n📄 PDF 병렬 처리 시작")
        print(f"   파일: {pdf_path}")
        print(f"   총 페이지: {total_pages}")
        print(f"   처리 범위: {start_idx + 1} ~ {end_idx}")
        print(f"   워커 수: {self.num_workers}")
        print(f"   DPI: {dpi}")
        print(f"   OCR 사용: {use_ocr}")

        # 작업 인자 준비
        tasks = [
            (pdf_path, page_num, dpi, output_dir, use_ocr)
            for page_num in page_range
        ]

        # 멀티프로세싱 풀로 처리
        results = []
        start_time = time.time()

        with Pool(processes=self.num_workers) as pool:
            # imap으로 진행상황 표시
            for i, result in enumerate(pool.imap(self.process_page_worker, tasks, chunksize=chunk_size), 1):
                results.append(result)

                # 진행상황 출력
                if result['success']:
                    print(f"   ✓ [{i}/{len(tasks)}] 페이지 {result['page_number']}: "
                          f"{result['processing_time']:.2f}초", end='')
                    if result.get('has_ocr'):
                        print(f" (OCR: {result['ocr_text_count']}개)", end='')
                    print()
                else:
                    print(f"   ✗ [{i}/{len(tasks)}] 페이지 {result['page_number']}: "
                          f"실패 - {result.get('error', 'Unknown error')}")

        # 통합 결과 저장
        total_time = time.time() - start_time
        summary = {
            'pdf_path': pdf_path,
            'total_pages': total_pages,
            'processed_pages': len(results),
            'successful_pages': sum(1 for r in results if r['success']),
            'failed_pages': sum(1 for r in results if not r['success']),
            'total_processing_time': total_time,
            'average_time_per_page': total_time / len(results) if results else 0,
            'num_workers': self.num_workers,
            'results': results
        }

        # 통합 JSON 저장
        os.makedirs(output_dir, exist_ok=True)
        summary_path = os.path.join(output_dir, 'processing_summary.json')
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        # 결과 출력
        print(f"\n{'='*60}")
        print(f"✅ 병렬 처리 완료!")
        print(f"{'='*60}")
        print(f"총 처리 시간: {total_time:.2f}초 ({total_time/60:.1f}분)")
        print(f"성공: {summary['successful_pages']}/{summary['processed_pages']}페이지")
        print(f"평균 처리 속도: {summary['average_time_per_page']:.2f}초/페이지")
        print(f"예상 126페이지 처리 시간: {summary['average_time_per_page'] * 126 / 60:.1f}분")
        print(f"\n📁 결과 저장: {output_dir}")
        print(f"   - 요약: {summary_path}")
        print(f"   - 이미지: {summary['successful_pages']}개 PNG 파일")
        print(f"   - 데이터: {summary['successful_pages']}개 JSON 파일")

        return results


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description='멀티프로세싱 기반 선거 개표상황표 OCR 처리'
    )
    parser.add_argument(
        'pdf_path',
        type=str,
        help='처리할 PDF 파일 경로'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./ocr_results_mp',
        help='결과 저장 디렉토리 (기본값: ./ocr_results_mp)'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=None,
        help='워커 프로세스 수 (기본값: CPU 코어 수 - 1)'
    )
    parser.add_argument(
        '--first-page',
        type=int,
        default=None,
        help='시작 페이지 (1-indexed)'
    )
    parser.add_argument(
        '--last-page',
        type=int,
        default=None,
        help='끝 페이지 (1-indexed)'
    )
    parser.add_argument(
        '--dpi',
        type=int,
        default=200,
        help='이미지 해상도 (기본값: 200)'
    )
    parser.add_argument(
        '--no-ocr',
        action='store_true',
        help='OCR 비활성화 (이미지 추출만)'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=10,
        help='청크 크기 (기본값: 10)'
    )

    args = parser.parse_args()

    # 처리기 초기화
    processor = MultiProcessingOCR(num_workers=args.workers)

    # PDF 처리
    results = processor.process_pdf_parallel(
        pdf_path=args.pdf_path,
        output_dir=args.output_dir,
        dpi=args.dpi,
        first_page=args.first_page,
        last_page=args.last_page,
        use_ocr=not args.no_ocr,
        chunk_size=args.chunk_size
    )

    print(f"\n🎉 완료: {len(results)}개 페이지 처리됨")


if __name__ == '__main__':
    main()
