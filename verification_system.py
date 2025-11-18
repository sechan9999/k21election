#!/usr/bin/env python3
"""
선거 개표상황표 데이터 검증 시스템
Election Ballot Data Verification System
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import defaultdict
import pandas as pd
import numpy as np
from datetime import datetime


class ElectionDataVerifier:
    """선거 데이터 검증 클래스"""

    def __init__(self, results_dir: str = './ocr_results'):
        """
        초기화

        Args:
            results_dir: OCR 결과 디렉토리
        """
        self.results_dir = results_dir
        self.results = []
        self.verification_report = {}

        # 후보자 정보
        self.candidates = {
            '이재명': {'number': 1, 'party': '더불어민주당'},
            '김문수': {'number': 2, 'party': '국민의힘'},
            '이준석': {'number': 4, 'party': '개혁신당'},
            '권영국': {'number': 5, 'party': '민주노동당'},
            '송진호': {'number': 8, 'party': '무소속'},
        }

    def load_results(self) -> List[Dict[str, Any]]:
        """
        OCR 결과 로드

        Returns:
            OCR 결과 리스트
        """
        all_results_path = os.path.join(self.results_dir, 'all_results.json')

        if os.path.exists(all_results_path):
            print(f"📂 결과 파일 로드: {all_results_path}")
            with open(all_results_path, 'r', encoding='utf-8') as f:
                self.results = json.load(f)
        else:
            print(f"⚠️  통합 결과 파일 없음. 개별 파일 로드 시도...")
            # 개별 JSON 파일 로드
            json_files = sorted(Path(self.results_dir).glob('page_*.json'))
            self.results = []
            for json_file in json_files:
                with open(json_file, 'r', encoding='utf-8') as f:
                    self.results.append(json.load(f))

        print(f"✅ {len(self.results)}개 페이지 결과 로드 완료")
        return self.results

    def verify_candidate_consistency(self) -> Dict[str, Any]:
        """
        후보자 인식 일관성 검증

        Returns:
            검증 결과
        """
        print("\n🔍 후보자 인식 일관성 검증 중...")

        candidate_stats = defaultdict(lambda: {
            'found_count': 0,
            'missing_count': 0,
            'pages': []
        })

        for result in self.results:
            page_num = result['page_number']
            candidates_found = result['vote_data']['candidates']

            for cand_name in self.candidates.keys():
                if cand_name in candidates_found:
                    candidate_stats[cand_name]['found_count'] += 1
                    candidate_stats[cand_name]['pages'].append(page_num)
                else:
                    candidate_stats[cand_name]['missing_count'] += 1

        # 결과 정리
        total_pages = len(self.results)
        verification = {}

        for cand_name, stats in candidate_stats.items():
            recognition_rate = stats['found_count'] / total_pages if total_pages > 0 else 0
            verification[cand_name] = {
                'found_count': stats['found_count'],
                'missing_count': stats['missing_count'],
                'recognition_rate': recognition_rate,
                'pages_found': stats['pages']
            }

            status = "✅" if recognition_rate > 0.8 else "⚠️" if recognition_rate > 0.5 else "❌"
            print(f"   {status} {cand_name}: {stats['found_count']}/{total_pages} ({recognition_rate:.1%})")

        return verification

    def verify_vote_type_distribution(self) -> Dict[str, Any]:
        """
        투표 유형 분포 검증

        Returns:
            검증 결과
        """
        print("\n🔍 투표 유형 분포 검증 중...")

        vote_type_stats = defaultdict(lambda: {'count': 0, 'pages': []})

        for result in self.results:
            page_num = result['page_number']
            vote_type = result['vote_data']['metadata'].get('vote_type', '알 수 없음')

            vote_type_stats[vote_type]['count'] += 1
            vote_type_stats[vote_type]['pages'].append(page_num)

        # 결과 정리
        verification = {}
        for vote_type, stats in vote_type_stats.items():
            verification[vote_type] = stats
            print(f"   📊 {vote_type}: {stats['count']}페이지")

        return verification

    def verify_ocr_quality(self) -> Dict[str, Any]:
        """
        OCR 품질 검증

        Returns:
            검증 결과
        """
        print("\n🔍 OCR 품질 검증 중...")

        confidences = []
        text_counts = []
        low_quality_pages = []

        for result in self.results:
            page_num = result['page_number']
            avg_conf = result['avg_confidence']
            text_count = result['text_count']

            confidences.append(avg_conf)
            text_counts.append(text_count)

            if avg_conf < 0.5:
                low_quality_pages.append({
                    'page': page_num,
                    'confidence': avg_conf
                })

        verification = {
            'average_confidence': np.mean(confidences) if confidences else 0.0,
            'min_confidence': np.min(confidences) if confidences else 0.0,
            'max_confidence': np.max(confidences) if confidences else 0.0,
            'std_confidence': np.std(confidences) if confidences else 0.0,
            'average_text_count': np.mean(text_counts) if text_counts else 0,
            'low_quality_pages': low_quality_pages,
            'low_quality_count': len(low_quality_pages)
        }

        print(f"   📈 평균 신뢰도: {verification['average_confidence']:.2%}")
        print(f"   📈 평균 텍스트 블록 수: {verification['average_text_count']:.0f}")
        print(f"   ⚠️  낮은 품질 페이지: {verification['low_quality_count']}개")

        return verification

    def extract_vote_counts_summary(self) -> Dict[str, Any]:
        """
        득표수 요약 추출

        Returns:
            득표수 요약
        """
        print("\n📊 득표수 데이터 요약 중...")

        candidate_totals = defaultdict(lambda: {
            'possible_votes': [],
            'pages_with_data': []
        })

        for result in self.results:
            page_num = result['page_number']
            candidates_data = result['vote_data']['candidates']

            for cand_name, cand_data in candidates_data.items():
                if 'possible_counts' in cand_data and cand_data['possible_counts']:
                    candidate_totals[cand_name]['possible_votes'].extend(
                        cand_data['possible_counts']
                    )
                    candidate_totals[cand_name]['pages_with_data'].append(page_num)

        # 요약 계산
        summary = {}
        for cand_name, data in candidate_totals.items():
            if data['possible_votes']:
                summary[cand_name] = {
                    'total_numbers_found': len(data['possible_votes']),
                    'pages_with_data': len(data['pages_with_data']),
                    'min_value': min(data['possible_votes']),
                    'max_value': max(data['possible_votes']),
                    'sum_all': sum(data['possible_votes']),
                    'average': np.mean(data['possible_votes'])
                }

                print(f"   👤 {cand_name}:")
                print(f"      - 숫자 발견: {summary[cand_name]['total_numbers_found']}개")
                print(f"      - 데이터 있는 페이지: {summary[cand_name]['pages_with_data']}개")
                print(f"      - 범위: {summary[cand_name]['min_value']} ~ {summary[cand_name]['max_value']}")

        return summary

    def generate_quality_report(self) -> Dict[str, Any]:
        """
        종합 품질 보고서 생성

        Returns:
            품질 보고서
        """
        print("\n" + "="*60)
        print("📋 종합 품질 보고서 생성")
        print("="*60)

        # 각종 검증 수행
        candidate_verification = self.verify_candidate_consistency()
        vote_type_verification = self.verify_vote_type_distribution()
        ocr_quality = self.verify_ocr_quality()
        vote_summary = self.extract_vote_counts_summary()

        # 보고서 작성
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_pages': len(self.results),
            'candidate_verification': candidate_verification,
            'vote_type_distribution': vote_type_verification,
            'ocr_quality': ocr_quality,
            'vote_counts_summary': vote_summary,
            'overall_quality': self._calculate_overall_quality(
                candidate_verification, ocr_quality
            )
        }

        self.verification_report = report
        return report

    def _calculate_overall_quality(
        self,
        candidate_verification: Dict,
        ocr_quality: Dict
    ) -> Dict[str, Any]:
        """
        전체 품질 점수 계산

        Args:
            candidate_verification: 후보자 검증 결과
            ocr_quality: OCR 품질 결과

        Returns:
            전체 품질 평가
        """
        # 후보자 인식률 평균
        recognition_rates = [
            v['recognition_rate'] for v in candidate_verification.values()
        ]
        avg_recognition = np.mean(recognition_rates) if recognition_rates else 0.0

        # OCR 신뢰도
        avg_confidence = ocr_quality['average_confidence']

        # 종합 점수 (가중 평균)
        overall_score = (avg_recognition * 0.6 + avg_confidence * 0.4)

        # 등급 판정
        if overall_score >= 0.9:
            grade = "A (우수)"
        elif overall_score >= 0.8:
            grade = "B (양호)"
        elif overall_score >= 0.7:
            grade = "C (보통)"
        elif overall_score >= 0.6:
            grade = "D (미흡)"
        else:
            grade = "F (불량)"

        quality = {
            'overall_score': overall_score,
            'grade': grade,
            'recognition_rate': avg_recognition,
            'confidence_score': avg_confidence
        }

        print("\n" + "="*60)
        print("🏆 최종 품질 평가")
        print("="*60)
        print(f"   종합 점수: {overall_score:.1%}")
        print(f"   등급: {grade}")
        print(f"   후보자 인식률: {avg_recognition:.1%}")
        print(f"   OCR 신뢰도: {avg_confidence:.1%}")
        print("="*60)

        return quality

    def save_report(self, output_path: str = None) -> str:
        """
        보고서 저장

        Args:
            output_path: 저장 경로 (기본값: results_dir/verification_report.json)

        Returns:
            저장된 파일 경로
        """
        if output_path is None:
            output_path = os.path.join(
                self.results_dir,
                'verification_report.json'
            )

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(
                self.verification_report,
                f,
                ensure_ascii=False,
                indent=2
            )

        print(f"\n💾 보고서 저장 완료: {output_path}")
        return output_path

    def export_to_excel(self, output_path: str = None) -> str:
        """
        Excel 형식으로 내보내기

        Args:
            output_path: 저장 경로

        Returns:
            저장된 파일 경로
        """
        if output_path is None:
            output_path = os.path.join(
                self.results_dir,
                'verification_report.xlsx'
            )

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # 1. 페이지별 요약
            page_summary = []
            for result in self.results:
                page_summary.append({
                    '페이지': result['page_number'],
                    '투표유형': result['vote_data']['metadata'].get('vote_type', '알 수 없음'),
                    '텍스트수': result['text_count'],
                    '평균신뢰도': f"{result['avg_confidence']:.2%}",
                    '후보자수': len(result['vote_data']['candidates'])
                })

            df_pages = pd.DataFrame(page_summary)
            df_pages.to_excel(writer, sheet_name='페이지별요약', index=False)

            # 2. 후보자별 통계
            if self.verification_report:
                cand_stats = []
                for cand_name, stats in self.verification_report['candidate_verification'].items():
                    cand_stats.append({
                        '후보자': cand_name,
                        '발견횟수': stats['found_count'],
                        '누락횟수': stats['missing_count'],
                        '인식률': f"{stats['recognition_rate']:.2%}"
                    })

                df_cand = pd.DataFrame(cand_stats)
                df_cand.to_excel(writer, sheet_name='후보자별통계', index=False)

            # 3. 품질 요약
            if self.verification_report:
                quality = self.verification_report['overall_quality']
                quality_data = [{
                    '항목': '종합점수',
                    '값': f"{quality['overall_score']:.2%}"
                }, {
                    '항목': '등급',
                    '값': quality['grade']
                }, {
                    '항목': '후보자 인식률',
                    '값': f"{quality['recognition_rate']:.2%}"
                }, {
                    '항목': 'OCR 신뢰도',
                    '값': f"{quality['confidence_score']:.2%}"
                }]

                df_quality = pd.DataFrame(quality_data)
                df_quality.to_excel(writer, sheet_name='품질요약', index=False)

        print(f"📊 Excel 보고서 저장 완료: {output_path}")
        return output_path


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description='선거 개표상황표 데이터 검증'
    )
    parser.add_argument(
        '--results-dir',
        type=str,
        default='./ocr_results',
        help='OCR 결과 디렉토리 (기본값: ./ocr_results)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='보고서 저장 경로'
    )
    parser.add_argument(
        '--excel',
        action='store_true',
        help='Excel 형식으로도 저장'
    )

    args = parser.parse_args()

    # 검증 시스템 초기화
    verifier = ElectionDataVerifier(results_dir=args.results_dir)

    # 결과 로드
    verifier.load_results()

    # 품질 보고서 생성
    report = verifier.generate_quality_report()

    # 보고서 저장
    verifier.save_report(args.output)

    # Excel 저장 (옵션)
    if args.excel:
        verifier.export_to_excel()

    print("\n✅ 검증 완료!")


if __name__ == '__main__':
    main()
