#!/usr/bin/env python3
"""
멀티프로세싱을 사용한 선거 데이터 분석
- OCR 처리를 병렬화하여 속도 향상
- 세종시 및 제주시 데이터 모두 분석 가능
"""
import os
import json
import csv
from pathlib import Path
from multiprocessing import Pool, cpu_count
from PIL import Image
import time

try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

def analyze_single_page(page_data):
    """
    단일 페이지 분석 (멀티프로세싱용)

    Args:
        page_data: (page_file, pages_dir, page_num)

    Returns:
        dict: 페이지 분석 결과
    """
    page_file, pages_dir, page_num = page_data

    try:
        img_path = os.path.join(pages_dir, page_file)
        img = Image.open(img_path)

        result = {
            'page_num': page_num,
            'page_file': page_file,
            'width': img.width,
            'height': img.height,
            'success': True,
            'error': None
        }

        # OCR 사용 가능 시 텍스트 추출
        if OCR_AVAILABLE:
            # 한글 + 영어 OCR
            text = pytesseract.image_to_string(img, lang='kor+eng')
            result['ocr_text'] = text

            # 투표 유형 감지
            if '관외사전' in text:
                result['voting_type'] = '관외사전투표'
            elif '관내사전' in text:
                result['voting_type'] = '관내사전투표'
            elif '선거일' in text:
                result['voting_type'] = '선거일투표'
            elif '거소' in text or '선상' in text:
                result['voting_type'] = '거소·선상투표'
            else:
                result['voting_type'] = '기타'

        img.close()
        return result

    except Exception as e:
        return {
            'page_num': page_num,
            'page_file': page_file,
            'success': False,
            'error': str(e)
        }

def analyze_all_pages_multiprocess(pages_dir, output_file=None, num_workers=None):
    """
    멀티프로세싱을 사용하여 모든 페이지 분석

    Args:
        pages_dir: 페이지 이미지 디렉토리
        output_file: 결과 저장 파일 (JSON)
        num_workers: 워커 프로세스 수
    """
    if not os.path.exists(pages_dir):
        print(f"오류: 디렉토리를 찾을 수 없습니다: {pages_dir}")
        return None

    pages = sorted([f for f in os.listdir(pages_dir) if f.endswith('.png')])
    total_pages = len(pages)

    if total_pages == 0:
        print(f"오류: {pages_dir}에 PNG 파일이 없습니다")
        return None

    if num_workers is None:
        num_workers = max(1, cpu_count() - 1)

    print("=" * 80)
    print("멀티프로세싱 선거 데이터 분석")
    print("=" * 80)
    print(f"페이지 디렉토리: {pages_dir}")
    print(f"총 페이지 수: {total_pages}")
    print(f"워커 프로세스 수: {num_workers}")
    print(f"OCR 사용 가능: {'예' if OCR_AVAILABLE else '아니오'}")
    print("=" * 80)

    # 페이지 데이터 준비
    page_data_list = [
        (page_file, pages_dir, i + 1)
        for i, page_file in enumerate(pages)
    ]

    # 멀티프로세싱 실행
    start_time = time.time()
    results = []

    with Pool(processes=num_workers) as pool:
        for i, result in enumerate(pool.imap_unordered(analyze_single_page, page_data_list)):
            results.append(result)
            if (i + 1) % 10 == 0:
                print(f"진행률: {i+1}/{total_pages} 페이지 완료 ({(i+1)/total_pages*100:.1f}%)")

    elapsed_time = time.time() - start_time

    # 결과 정렬 (페이지 번호순)
    results.sort(key=lambda x: x['page_num'])

    # 통계 계산
    successful = sum(1 for r in results if r['success'])
    failed = sum(1 for r in results if not r['success'])

    print("=" * 80)
    print("분석 완료!")
    print("=" * 80)
    print(f"✓ 성공: {successful} 페이지")
    if failed > 0:
        print(f"✗ 실패: {failed} 페이지")

    # 투표 유형별 통계
    if OCR_AVAILABLE and successful > 0:
        voting_types = {}
        for r in results:
            if r['success'] and 'voting_type' in r:
                vtype = r['voting_type']
                voting_types[vtype] = voting_types.get(vtype, 0) + 1

        if voting_types:
            print("\n투표 유형별 분포:")
            for vtype, count in sorted(voting_types.items()):
                print(f"  - {vtype}: {count}페이지")

    print(f"\n소요 시간: {elapsed_time:.2f}초")
    print(f"평균 속도: {total_pages/elapsed_time:.2f} 페이지/초")
    print("=" * 80)

    # 결과 저장
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n결과 저장: {output_file}")

    return results

def create_summary_csv(results, output_csv):
    """분석 결과를 CSV로 저장"""
    if not results:
        return

    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['페이지', '파일명', '투표유형', '너비', '높이', '성공'])

        for r in results:
            if r['success']:
                writer.writerow([
                    r['page_num'],
                    r['page_file'],
                    r.get('voting_type', '미확인'),
                    r.get('width', ''),
                    r.get('height', ''),
                    '성공'
                ])
            else:
                writer.writerow([
                    r['page_num'],
                    r['page_file'],
                    '',
                    '',
                    '',
                    f"실패: {r.get('error', '알 수 없는 오류')}"
                ])

    print(f"CSV 요약 저장: {output_csv}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("사용법: python multiprocess_analyzer.py <pages_dir> [output_json] [output_csv]")
        print("\n예시:")
        print("  python multiprocess_analyzer.py sejong_pages")
        print("  python multiprocess_analyzer.py jeju_pages jeju_analysis.json jeju_summary.csv")
        sys.exit(1)

    pages_dir = sys.argv[1]
    output_json = sys.argv[2] if len(sys.argv) > 2 else f"{Path(pages_dir).stem}_analysis.json"
    output_csv = sys.argv[3] if len(sys.argv) > 3 else f"{Path(pages_dir).stem}_summary.csv"

    results = analyze_all_pages_multiprocess(pages_dir, output_json)

    if results:
        create_summary_csv(results, output_csv)
