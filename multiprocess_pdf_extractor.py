#!/usr/bin/env python3
"""
멀티프로세싱을 사용한 PDF 페이지 추출 및 분석
- 여러 페이지를 병렬로 처리하여 속도 향상
- 세종시 및 제주시 데이터 모두 처리 가능
"""
import fitz  # PyMuPDF
import os
from pathlib import Path
from multiprocessing import Pool, cpu_count
from functools import partial
import time

def extract_single_page(page_data):
    """단일 페이지 추출 (멀티프로세싱용)"""
    pdf_path, page_num, output_dir, dpi = page_data

    try:
        doc = fitz.open(pdf_path)
        page = doc[page_num]

        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=matrix)

        output_file = os.path.join(output_dir, f"page_{page_num+1:03d}.png")
        pix.save(output_file)

        doc.close()
        return (page_num + 1, True, None)
    except Exception as e:
        return (page_num + 1, False, str(e))

def extract_all_pages_multiprocess(pdf_path, output_dir, dpi=150, num_workers=None):
    """
    멀티프로세싱을 사용하여 모든 페이지 추출

    Args:
        pdf_path: PDF 파일 경로
        output_dir: 출력 디렉토리
        dpi: 이미지 해상도 (기본값: 150)
        num_workers: 워커 프로세스 수 (기본값: CPU 코어 수 - 1)
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # PDF 페이지 수 확인
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    if num_workers is None:
        num_workers = max(1, cpu_count() - 1)

    print("=" * 80)
    print(f"멀티프로세싱 PDF 페이지 추출")
    print("=" * 80)
    print(f"PDF 파일: {pdf_path}")
    print(f"총 페이지 수: {total_pages}")
    print(f"출력 디렉토리: {output_dir}")
    print(f"DPI: {dpi}")
    print(f"워커 프로세스 수: {num_workers}")
    print("=" * 80)

    # 페이지 데이터 준비
    page_data_list = [
        (pdf_path, page_num, output_dir, dpi)
        for page_num in range(total_pages)
    ]

    # 멀티프로세싱 실행
    start_time = time.time()

    with Pool(processes=num_workers) as pool:
        results = []
        for i, result in enumerate(pool.imap_unordered(extract_single_page, page_data_list)):
            results.append(result)
            if (i + 1) % 10 == 0:
                print(f"진행률: {i+1}/{total_pages} 페이지 완료 ({(i+1)/total_pages*100:.1f}%)")

    elapsed_time = time.time() - start_time

    # 결과 요약
    successful = sum(1 for r in results if r[1])
    failed = sum(1 for r in results if not r[1])

    print("=" * 80)
    print("추출 완료!")
    print("=" * 80)
    print(f"✓ 성공: {successful} 페이지")
    if failed > 0:
        print(f"✗ 실패: {failed} 페이지")
        for page_num, success, error in results:
            if not success:
                print(f"  - 페이지 {page_num}: {error}")
    print(f"소요 시간: {elapsed_time:.2f}초")
    print(f"평균 속도: {total_pages/elapsed_time:.2f} 페이지/초")
    print("=" * 80)

    return results

def compare_performance(pdf_path, output_dir_single, output_dir_multi, dpi=150):
    """단일 프로세스 vs 멀티프로세스 성능 비교"""
    import shutil

    print("\n" + "=" * 80)
    print("성능 비교 테스트")
    print("=" * 80)

    # 단일 프로세스
    print("\n[1] 단일 프로세스 방식...")
    start_time = time.time()

    Path(output_dir_single).mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    for page_num in range(total_pages):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=matrix)
        output_file = os.path.join(output_dir_single, f"page_{page_num+1:03d}.png")
        pix.save(output_file)

    doc.close()
    single_time = time.time() - start_time

    print(f"✓ 완료: {single_time:.2f}초")

    # 멀티프로세스
    print("\n[2] 멀티프로세스 방식...")
    start_time = time.time()
    extract_all_pages_multiprocess(pdf_path, output_dir_multi, dpi=dpi)
    multi_time = time.time() - start_time

    print(f"✓ 완료: {multi_time:.2f}초")

    # 비교 결과
    print("\n" + "=" * 80)
    print("성능 비교 결과")
    print("=" * 80)
    print(f"단일 프로세스: {single_time:.2f}초")
    print(f"멀티프로세스: {multi_time:.2f}초")
    print(f"속도 향상: {single_time/multi_time:.2f}배 빠름")
    print("=" * 80)

    # 임시 디렉토리 삭제
    shutil.rmtree(output_dir_single, ignore_errors=True)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("사용법: python multiprocess_pdf_extractor.py <pdf_file> [output_dir] [dpi]")
        print("\n예시:")
        print("  python multiprocess_pdf_extractor.py sejong.pdf")
        print("  python multiprocess_pdf_extractor.py jeju.pdf jeju_pages 200")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else f"{Path(pdf_file).stem}_pages"
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150

    if not os.path.exists(pdf_file):
        print(f"오류: PDF 파일을 찾을 수 없습니다: {pdf_file}")
        sys.exit(1)

    extract_all_pages_multiprocess(pdf_file, output_dir, dpi=dpi)
