#!/usr/bin/env python3
"""
세종특별자치시 선거 개표상황표 OCR 처리 시스템
Korean Election Ballot OCR Processing System
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

import easyocr
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image


class KoreanElectionOCR:
    """한글 선거 개표상황표 OCR 처리 클래스"""

    def __init__(self, gpu: bool = False):
        """
        초기화

        Args:
            gpu: GPU 사용 여부 (기본값: False)
        """
        print("🔧 EasyOCR 초기화 중 (한글+영어)...")
        self.reader = easyocr.Reader(['ko', 'en'], gpu=gpu)
        print("✅ OCR 초기화 완료!")

        # 선거 관련 주요 용어 사전
        self.election_terms = {
            '개표상황': '개표상황',
            '투표함': '투표함',
            '관내사전': '관내사전',
            '관외사전': '관외사전',
            '선거일투표': '선거일투표',
            '기표': '기표',
            '미분류': '미분류',
            '무효': '무효',
            '유효': '유효',
        }

        # 후보자 정보 (sejong.pdf 기준)
        self.candidates = {
            1: {'name': '이재명', 'party': '더불어민주당'},
            2: {'name': '김문수', 'party': '국민의힘'},
            4: {'name': '이준석', 'party': '개혁신당'},
            5: {'name': '권영국', 'party': '민주노동당'},
            8: {'name': '송진호', 'party': '무소속'},
        }

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        이미지 전처리

        Args:
            image: 입력 이미지 (numpy array)

        Returns:
            전처리된 이미지
        """
        # 그레이스케일 변환
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # 노이즈 제거
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

        # 대비 향상 (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)

        # 이진화 (적응형 임계값)
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        return binary

    def convert_pdf_to_images(
        self,
        pdf_path: str,
        dpi: int = 300,
        first_page: int = None,
        last_page: int = None
    ) -> List[np.ndarray]:
        """
        PDF를 이미지로 변환

        Args:
            pdf_path: PDF 파일 경로
            dpi: 해상도 (기본값: 300)
            first_page: 시작 페이지 (1-indexed)
            last_page: 끝 페이지 (1-indexed)

        Returns:
            이미지 리스트 (numpy array)
        """
        print(f"📄 PDF 변환 중: {pdf_path}")
        print(f"   DPI: {dpi}, 페이지 범위: {first_page or 1} ~ {last_page or '끝'}")

        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            first_page=first_page,
            last_page=last_page
        )

        # PIL Image를 numpy array로 변환
        np_images = [np.array(img) for img in images]

        print(f"✅ {len(np_images)}개 페이지 변환 완료!")
        return np_images

    def extract_text_from_image(
        self,
        image: np.ndarray,
        preprocess: bool = True
    ) -> List[Tuple[List, str, float]]:
        """
        이미지에서 텍스트 추출

        Args:
            image: 입력 이미지
            preprocess: 전처리 적용 여부

        Returns:
            [(bbox, text, confidence), ...]
        """
        if preprocess:
            processed = self.preprocess_image(image)
        else:
            processed = image

        # EasyOCR로 텍스트 추출
        results = self.reader.readtext(processed)

        return results

    def extract_vote_counts(self, text_results: List[Tuple]) -> Dict[str, Any]:
        """
        투표 집계 데이터 추출

        Args:
            text_results: OCR 결과 [(bbox, text, confidence), ...]

        Returns:
            추출된 투표 데이터
        """
        vote_data = {
            'candidates': {},
            'metadata': {},
            'raw_numbers': []
        }

        # 모든 텍스트 추출
        all_texts = [result[1] for result in text_results]
        all_text = ' '.join(all_texts)

        # 숫자 패턴 추출 (득표수)
        number_pattern = r'\d{1,6}'
        numbers = re.findall(number_pattern, all_text)
        vote_data['raw_numbers'] = [int(n) for n in numbers if int(n) > 0]

        # 후보자별 데이터 추출
        for cand_num, cand_info in self.candidates.items():
            name = cand_info['name']

            # 후보자 이름 찾기
            for i, (bbox, text, conf) in enumerate(text_results):
                if name in text:
                    # 주변 숫자 찾기
                    nearby_numbers = []
                    for j in range(max(0, i-3), min(len(text_results), i+4)):
                        nearby_text = text_results[j][1]
                        nums = re.findall(number_pattern, nearby_text)
                        nearby_numbers.extend([int(n) for n in nums if int(n) > 0])

                    if nearby_numbers:
                        vote_data['candidates'][name] = {
                            'number': cand_num,
                            'party': cand_info['party'],
                            'possible_counts': nearby_numbers[:4],  # 최대 4개까지
                            'bbox': bbox,
                            'confidence': conf
                        }
                    break

        # 투표 유형 식별
        if '관외사전' in all_text:
            vote_data['metadata']['vote_type'] = '관외사전'
        elif '관내사전' in all_text:
            vote_data['metadata']['vote_type'] = '관내사전'
        elif '선거일' in all_text or '선거일투표' in all_text:
            vote_data['metadata']['vote_type'] = '선거일투표'
        else:
            vote_data['metadata']['vote_type'] = '알 수 없음'

        return vote_data

    def process_page(
        self,
        image: np.ndarray,
        page_num: int
    ) -> Dict[str, Any]:
        """
        단일 페이지 처리

        Args:
            image: 페이지 이미지
            page_num: 페이지 번호

        Returns:
            처리 결과
        """
        print(f"\n📝 페이지 {page_num} 처리 중...")

        # OCR 수행
        text_results = self.extract_text_from_image(image)

        print(f"   - {len(text_results)}개 텍스트 블록 인식됨")

        # 투표 데이터 추출
        vote_data = self.extract_vote_counts(text_results)

        # 결과 구성
        result = {
            'page_number': page_num,
            'vote_data': vote_data,
            'raw_ocr_results': [
                {
                    'text': text,
                    'confidence': float(conf),
                    'bbox': bbox
                }
                for bbox, text, conf in text_results
            ],
            'text_count': len(text_results),
            'avg_confidence': np.mean([r[2] for r in text_results]) if text_results else 0.0
        }

        print(f"   ✓ 후보자 {len(vote_data['candidates'])}명 발견")
        print(f"   ✓ 투표 유형: {vote_data['metadata'].get('vote_type', '알 수 없음')}")
        print(f"   ✓ 평균 신뢰도: {result['avg_confidence']:.2%}")

        return result

    def process_pdf(
        self,
        pdf_path: str,
        output_dir: str = './ocr_results',
        first_page: int = None,
        last_page: int = None,
        dpi: int = 300
    ) -> List[Dict[str, Any]]:
        """
        전체 PDF 처리

        Args:
            pdf_path: PDF 파일 경로
            output_dir: 결과 저장 디렉토리
            first_page: 시작 페이지
            last_page: 끝 페이지
            dpi: 해상도

        Returns:
            전체 처리 결과
        """
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)

        # PDF를 이미지로 변환
        images = self.convert_pdf_to_images(
            pdf_path, dpi=dpi,
            first_page=first_page,
            last_page=last_page
        )

        # 각 페이지 처리
        results = []
        start_page = first_page or 1

        for i, image in enumerate(images):
            page_num = start_page + i
            result = self.process_page(image, page_num)
            results.append(result)

            # 중간 결과 저장
            page_output_path = os.path.join(
                output_dir,
                f'page_{page_num:03d}_result.json'
            )
            with open(page_output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

        # 전체 결과 저장
        all_results_path = os.path.join(output_dir, 'all_results.json')
        with open(all_results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 전체 처리 완료!")
        print(f"📁 결과 저장 위치: {output_dir}")

        return results


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description='세종시 선거 개표상황표 OCR 처리'
    )
    parser.add_argument(
        'pdf_path',
        type=str,
        help='처리할 PDF 파일 경로'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./ocr_results',
        help='결과 저장 디렉토리 (기본값: ./ocr_results)'
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
        default=300,
        help='이미지 해상도 (기본값: 300)'
    )
    parser.add_argument(
        '--gpu',
        action='store_true',
        help='GPU 사용'
    )

    args = parser.parse_args()

    # OCR 처리기 초기화
    ocr = KoreanElectionOCR(gpu=args.gpu)

    # PDF 처리
    results = ocr.process_pdf(
        pdf_path=args.pdf_path,
        output_dir=args.output_dir,
        first_page=args.first_page,
        last_page=args.last_page,
        dpi=args.dpi
    )

    print(f"\n🎉 처리 완료: {len(results)}개 페이지")


if __name__ == '__main__':
    main()
