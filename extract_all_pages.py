#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
제주시 21대 대통령선거 개표상황표 데이터 추출 스크립트
Extract all election data from Jeju City ballot counting reports (172 pages)

작성일: 2025-11-19
대상: jeju.pdf (172 pages)
"""

import fitz  # PyMuPDF
import re
import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import sys

# 설정
PDF_PATH = "/home/user/k21election/jeju.pdf"
OUTPUT_DIR = Path("/home/user/k21election/jeju_data")
IMAGES_DIR = OUTPUT_DIR / "page_images"

# 5명의 대통령 후보자 (번호 순서)
CANDIDATES = {
    1: {"name": "이재명", "party": "더불어민주당", "name_en": "Lee Jae-myung"},
    2: {"name": "김문수", "party": "국민의힘", "name_en": "Kim Moon-soo"},
    4: {"name": "이준석", "party": "개혁신당", "name_en": "Lee Jun-seok"},
    5: {"name": "권영국", "party": "민주노동당", "name_en": "Kwon Young-guk"},
    8: {"name": "송진호", "party": "무소속", "name_en": "Song Jin-ho"}
}

class JejuElectionExtractor:
    """제주시 선거 데이터 추출기"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = None
        self.page_data = []
        self.stats = {
            "total_pages": 0,
            "processed_pages": 0,
            "failed_pages": 0,
            "total_votes": 0,
            "total_voters": 0,
            "total_eligible": 0
        }

    def open_pdf(self) -> bool:
        """PDF 파일 열기"""
        try:
            self.doc = fitz.open(self.pdf_path)
            self.stats["total_pages"] = len(self.doc)
            print(f"✓ PDF 열기 성공: {self.stats['total_pages']} 페이지")
            return True
        except Exception as e:
            print(f"✗ PDF 열기 실패: {e}")
            return False

    def extract_text_from_page(self, page_num: int) -> str:
        """페이지에서 텍스트 추출 (OCR 대신 내장 텍스트 사용 시도)"""
        try:
            page = self.doc[page_num]
            text = page.get_text()
            return text
        except Exception as e:
            print(f"  ⚠ 페이지 {page_num + 1} 텍스트 추출 실패: {e}")
            return ""

    def save_page_image(self, page_num: int, output_path: Path) -> bool:
        """페이지를 이미지로 저장"""
        try:
            page = self.doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom
            pix.save(str(output_path))
            return True
        except Exception as e:
            print(f"  ⚠ 페이지 {page_num + 1} 이미지 저장 실패: {e}")
            return False

    def parse_page_data(self, page_num: int, text: str) -> Optional[Dict]:
        """
        페이지 데이터 파싱

        구조:
        - 투표함 번호
        - 선거인 수
        - 투표자 수 (투표용지 교부 수)
        - 5명 후보자별 득표 (기계 분류 + 인간 검증)
        - 무효표, 재확인 대상
        """
        data = {
            "page_number": page_num + 1,
            "ballot_box_id": "",
            "vote_type": "",
            "eligible_voters": 0,
            "total_ballots": 0,
            "valid_votes": 0,
            "invalid_votes": 0,
            "candidates": {},
            "machine_classified": {},
            "human_verified": {},
            "recount_target": 0,
            "timestamp": "",
            "extraction_method": "text_parsing"
        }

        # 텍스트에서 숫자 패턴 찾기
        lines = text.split('\n')

        # 투표함 번호 찾기 (예: "㉮중간표", "이종천4" 등)
        for line in lines:
            if '㉮' in line or '이종천' in line or '어중간' in line:
                # 한글 문자 제거하고 숫자만 추출
                ballot_id = re.sub(r'[^\d]', '', line)
                if ballot_id:
                    data["ballot_box_id"] = ballot_id[:10]  # 최대 10자리
                    break

        # 투표 유형 판단
        vote_type = self.determine_vote_type(text, lines)
        data["vote_type"] = vote_type

        # 숫자 추출 (선거인 수, 투표자 수 등)
        numbers = re.findall(r'\d{1,6}', text)

        # 선거인 수와 투표자 수 찾기 (일반적으로 처음 두 개의 큰 숫자)
        if len(numbers) >= 2:
            nums = [int(n) for n in numbers if 100 <= int(n) <= 100000]
            if len(nums) >= 2:
                data["eligible_voters"] = nums[0]
                data["total_ballots"] = nums[1]

        # 후보자별 득표 수 추출 (패턴 기반)
        # 5명의 후보자 득표를 찾아야 함
        candidate_votes = self.extract_candidate_votes(text, lines)
        data["candidates"] = candidate_votes

        # 유효표 계산
        data["valid_votes"] = sum(candidate_votes.values())

        return data

    def determine_vote_type(self, text: str, lines: List[str]) -> str:
        """투표 유형 결정"""
        text_lower = text.lower()

        if '거소' in text or '선상' in text:
            return "거소·선상투표"
        elif '재외' in text:
            return "재외투표"
        elif '관외' in text and '사전' in text:
            return "관외사전투표"
        elif '관내' in text and '사전' in text:
            return "관내사전투표"
        elif '선거일' in text:
            return "선거일투표"
        else:
            return "선거일투표"  # 기본값

    def extract_candidate_votes(self, text: str, lines: List[str]) -> Dict[int, int]:
        """
        후보자별 득표 수 추출

        표 구조에서 후보자 이름과 득표 수를 매칭
        """
        votes = {1: 0, 2: 0, 4: 0, 5: 0, 8: 0}

        # 후보자 이름 패턴
        patterns = {
            1: r'이재명|더불어민주당',
            2: r'김문수|국민의힘',
            4: r'이준석|개혁신당',
            5: r'권영국|민주노동당',
            8: r'송진호|무소속'
        }

        # 각 라인에서 후보자와 숫자 매칭
        for i, line in enumerate(lines):
            for cand_num, pattern in patterns.items():
                if re.search(pattern, line):
                    # 같은 라인이나 다음 라인에서 숫자 찾기
                    nums = re.findall(r'\b(\d{1,5})\b', line)
                    if nums:
                        # 가장 큰 숫자를 득표로 가정
                        vote_count = max([int(n) for n in nums if 0 <= int(n) <= 50000])
                        votes[cand_num] = vote_count
                    elif i + 1 < len(lines):
                        # 다음 라인 확인
                        nums = re.findall(r'\b(\d{1,5})\b', lines[i + 1])
                        if nums:
                            vote_count = max([int(n) for n in nums if 0 <= int(n) <= 50000])
                            votes[cand_num] = vote_count

        return votes

    def extract_all_pages(self, save_images: bool = False) -> List[Dict]:
        """모든 페이지에서 데이터 추출"""

        print(f"\n{'=' * 70}")
        print(f"제주시 선거 데이터 추출 시작")
        print(f"{'=' * 70}")
        print(f"총 페이지: {self.stats['total_pages']}")
        print(f"이미지 저장: {'예' if save_images else '아니오'}")
        print()

        if save_images:
            IMAGES_DIR.mkdir(parents=True, exist_ok=True)

        for page_num in range(self.stats['total_pages']):
            try:
                # 진행 상황 표시
                if (page_num + 1) % 10 == 0 or page_num == 0:
                    print(f"처리 중: 페이지 {page_num + 1}/{self.stats['total_pages']} ({(page_num + 1) / self.stats['total_pages'] * 100:.1f}%)")

                # 텍스트 추출
                text = self.extract_text_from_page(page_num)

                # 데이터 파싱
                page_data = self.parse_page_data(page_num, text)

                if page_data:
                    self.page_data.append(page_data)
                    self.stats["processed_pages"] += 1

                    # 통계 업데이트
                    self.stats["total_votes"] += page_data["valid_votes"]
                    self.stats["total_voters"] += page_data["total_ballots"]
                    self.stats["total_eligible"] += page_data["eligible_voters"]
                else:
                    self.stats["failed_pages"] += 1

                # 이미지 저장 (선택적)
                if save_images and (page_num < 10 or page_num % 50 == 0):
                    image_path = IMAGES_DIR / f"page_{page_num + 1:04d}.png"
                    self.save_page_image(page_num, image_path)

            except Exception as e:
                print(f"  ✗ 페이지 {page_num + 1} 처리 실패: {e}")
                self.stats["failed_pages"] += 1
                continue

        print(f"\n{'=' * 70}")
        print(f"추출 완료!")
        print(f"{'=' * 70}")
        print(f"처리된 페이지: {self.stats['processed_pages']}/{self.stats['total_pages']}")
        print(f"실패한 페이지: {self.stats['failed_pages']}")
        print(f"총 유효 투표: {self.stats['total_votes']:,}")
        print(f"총 투표자: {self.stats['total_voters']:,}")
        print(f"총 선거인: {self.stats['total_eligible']:,}")
        print()

        return self.page_data

    def save_to_csv(self, output_path: Path):
        """CSV 파일로 저장 (투표소별 상세)"""

        fieldnames = [
            "page_number",
            "ballot_box_id",
            "vote_type",
            "eligible_voters",
            "total_ballots",
            "valid_votes",
            "invalid_votes",
            "이재명_득표",
            "김문수_득표",
            "이준석_득표",
            "권영국_득표",
            "송진호_득표",
            "extraction_method"
        ]

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for data in self.page_data:
                row = {
                    "page_number": data["page_number"],
                    "ballot_box_id": data["ballot_box_id"],
                    "vote_type": data["vote_type"],
                    "eligible_voters": data["eligible_voters"],
                    "total_ballots": data["total_ballots"],
                    "valid_votes": data["valid_votes"],
                    "invalid_votes": data["invalid_votes"],
                    "이재명_득표": data["candidates"].get(1, 0),
                    "김문수_득표": data["candidates"].get(2, 0),
                    "이준석_득표": data["candidates"].get(4, 0),
                    "권영국_득표": data["candidates"].get(5, 0),
                    "송진호_득표": data["candidates"].get(8, 0),
                    "extraction_method": data["extraction_method"]
                }
                writer.writerow(row)

        print(f"✓ 투표소별 상세 데이터 저장: {output_path}")

    def save_candidate_summary(self, output_path: Path):
        """후보자별 집계 저장"""

        summary = {}
        for cand_num in CANDIDATES:
            summary[cand_num] = {
                "candidate_number": cand_num,
                "name": CANDIDATES[cand_num]["name"],
                "party": CANDIDATES[cand_num]["party"],
                "total_votes": 0,
                "vote_percentage": 0.0
            }

        # 집계
        total_votes = 0
        for data in self.page_data:
            for cand_num in CANDIDATES:
                votes = data["candidates"].get(cand_num, 0)
                summary[cand_num]["total_votes"] += votes
                total_votes += votes

        # 득표율 계산
        if total_votes > 0:
            for cand_num in summary:
                summary[cand_num]["vote_percentage"] = round(
                    summary[cand_num]["total_votes"] / total_votes * 100, 2
                )

        # CSV 저장
        fieldnames = ["candidate_number", "name", "party", "total_votes", "vote_percentage"]

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # 득표순으로 정렬
            sorted_summary = sorted(summary.values(), key=lambda x: x["total_votes"], reverse=True)

            for row in sorted_summary:
                writer.writerow(row)

        print(f"✓ 후보자별 집계 저장: {output_path}")

        # 콘솔에 결과 출력
        print(f"\n{'=' * 70}")
        print(f"후보자별 득표 집계")
        print(f"{'=' * 70}")
        for row in sorted_summary:
            print(f"{row['candidate_number']}. {row['name']:8s} ({row['party']:12s}): {row['total_votes']:8,}표 ({row['vote_percentage']:6.2f}%)")
        print(f"{'=' * 70}")
        print(f"총 유효표: {total_votes:,}표")
        print(f"{'=' * 70}\n")

    def save_json(self, output_path: Path):
        """JSON 형식으로 저장 (전체 데이터)"""

        output_data = {
            "metadata": {
                "source_file": self.pdf_path,
                "total_pages": self.stats["total_pages"],
                "processed_pages": self.stats["processed_pages"],
                "extraction_date": datetime.now().isoformat(),
                "extractor_version": "1.0"
            },
            "statistics": self.stats,
            "candidates": CANDIDATES,
            "page_data": self.page_data
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"✓ JSON 데이터 저장: {output_path}")

    def close(self):
        """리소스 정리"""
        if self.doc:
            self.doc.close()
            print("✓ PDF 파일 닫기 완료")


def main():
    """메인 실행 함수"""

    # 출력 디렉토리 생성
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 70}")
    print(f"제주시 21대 대통령선거 개표상황표 데이터 추출기")
    print(f"{'=' * 70}")
    print(f"입력 파일: {PDF_PATH}")
    print(f"출력 디렉토리: {OUTPUT_DIR}")
    print(f"{'=' * 70}\n")

    # 추출기 생성
    extractor = JejuElectionExtractor(PDF_PATH)

    # PDF 열기
    if not extractor.open_pdf():
        print("PDF 파일을 열 수 없습니다.")
        return 1

    # 데이터 추출
    extractor.extract_all_pages(save_images=False)

    # 결과 저장
    extractor.save_to_csv(OUTPUT_DIR / "complete_jeju_voting_location_details.csv")
    extractor.save_candidate_summary(OUTPUT_DIR / "complete_jeju_candidate_summary.csv")
    extractor.save_json(OUTPUT_DIR / "jeju_complete_data.json")

    # 정리
    extractor.close()

    print(f"\n✅ 모든 작업 완료!")
    print(f"\n생성된 파일:")
    print(f"  1. complete_jeju_voting_location_details.csv - 투표소별 상세 결과")
    print(f"  2. complete_jeju_candidate_summary.csv - 후보자별 집계표")
    print(f"  3. jeju_complete_data.json - 전체 데이터 (JSON)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
