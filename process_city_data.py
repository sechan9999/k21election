#!/usr/bin/env python3
"""
도시별 선거 데이터 완전 처리 워크플로우
- PDF 추출 → 분석 → 리포트 생성을 자동화
- 멀티프로세싱으로 최적화
"""
import os
import sys
import json
import subprocess
from pathlib import Path
import time

class CityDataProcessor:
    """도시별 선거 데이터 처리 클래스"""

    def __init__(self, city_name, pdf_path):
        self.city_name = city_name
        self.pdf_path = pdf_path
        self.base_dir = Path(f"{city_name}_election_data")
        self.pages_dir = self.base_dir / "pages"
        self.analysis_dir = self.base_dir / "analysis"
        self.report_dir = self.base_dir / "reports"

    def setup_directories(self):
        """디렉토리 구조 생성"""
        print(f"\n[1] {self.city_name} 디렉토리 설정...")
        self.base_dir.mkdir(exist_ok=True)
        self.pages_dir.mkdir(exist_ok=True)
        self.analysis_dir.mkdir(exist_ok=True)
        self.report_dir.mkdir(exist_ok=True)
        print(f"✓ 디렉토리 생성 완료: {self.base_dir}")

    def extract_pages(self, dpi=150):
        """PDF에서 페이지 추출"""
        print(f"\n[2] PDF 페이지 추출 (멀티프로세싱)...")
        cmd = [
            "python3",
            "multiprocess_pdf_extractor.py",
            self.pdf_path,
            str(self.pages_dir),
            str(dpi)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ 페이지 추출 완료")
            return True
        else:
            print(f"✗ 페이지 추출 실패:\n{result.stderr}")
            return False

    def analyze_pages(self):
        """페이지 분석"""
        print(f"\n[3] 페이지 분석 (멀티프로세싱)...")
        output_json = self.analysis_dir / f"{self.city_name}_analysis.json"
        output_csv = self.analysis_dir / f"{self.city_name}_summary.csv"

        cmd = [
            "python3",
            "multiprocess_analyzer.py",
            str(self.pages_dir),
            str(output_json),
            str(output_csv)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ 페이지 분석 완료")
            return True
        else:
            print(f"✗ 페이지 분석 실패:\n{result.stderr}")
            return False

    def generate_report(self):
        """분석 리포트 생성"""
        print(f"\n[4] 분석 리포트 생성...")

        analysis_file = self.analysis_dir / f"{self.city_name}_analysis.json"
        if not analysis_file.exists():
            print("✗ 분석 파일을 찾을 수 없습니다")
            return False

        with open(analysis_file, 'r', encoding='utf-8') as f:
            results = json.load(f)

        # 리포트 생성
        report_file = self.report_dir / f"{self.city_name}_report.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.city_name} 선거 데이터 분석 리포트\n\n")
            f.write(f"생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            # 기본 통계
            total = len(results)
            successful = sum(1 for r in results if r['success'])
            failed = total - successful

            f.write("## 1. 기본 통계\n\n")
            f.write(f"- **총 페이지 수**: {total}\n")
            f.write(f"- **분석 성공**: {successful}\n")
            f.write(f"- **분석 실패**: {failed}\n")
            f.write(f"- **성공률**: {successful/total*100:.1f}%\n\n")

            # 투표 유형별 통계
            voting_types = {}
            for r in results:
                if r['success'] and 'voting_type' in r:
                    vtype = r['voting_type']
                    voting_types[vtype] = voting_types.get(vtype, 0) + 1

            if voting_types:
                f.write("## 2. 투표 유형별 분포\n\n")
                f.write("| 투표 유형 | 페이지 수 | 비율 |\n")
                f.write("|----------|----------|------|\n")
                for vtype, count in sorted(voting_types.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"| {vtype} | {count} | {count/total*100:.1f}% |\n")
                f.write("\n")

            # 실패 페이지
            if failed > 0:
                f.write("## 3. 분석 실패 페이지\n\n")
                f.write("| 페이지 | 파일명 | 오류 |\n")
                f.write("|--------|--------|------|\n")
                for r in results:
                    if not r['success']:
                        f.write(f"| {r['page_num']} | {r['page_file']} | {r.get('error', '알 수 없음')} |\n")
                f.write("\n")

            # 파일 목록
            f.write("## 4. 생성된 파일\n\n")
            f.write(f"- 페이지 이미지: `{self.pages_dir}/`\n")
            f.write(f"- 분석 데이터 (JSON): `{analysis_file}`\n")
            f.write(f"- 요약 (CSV): `{self.analysis_dir}/{self.city_name}_summary.csv`\n")
            f.write(f"- 리포트: `{report_file}`\n\n")

            # 다음 단계
            f.write("## 5. 다음 단계\n\n")
            f.write("1. 개별 페이지 검토 및 데이터 추출\n")
            f.write("2. OCR 정확도 검증\n")
            f.write("3. 후보자별 득표 집계\n")
            f.write("4. 기계 vs 인간 검증 비교\n")
            f.write("5. 최종 통계 리포트 생성\n")

        print(f"✓ 리포트 생성 완료: {report_file}")
        return True

    def process_all(self, dpi=150):
        """전체 처리 워크플로우"""
        print("=" * 80)
        print(f"{self.city_name.upper()} 선거 데이터 완전 처리")
        print("=" * 80)
        print(f"PDF 파일: {self.pdf_path}")
        print("=" * 80)

        start_time = time.time()

        # 1. 디렉토리 설정
        self.setup_directories()

        # 2. PDF 페이지 추출
        if not self.extract_pages(dpi):
            print("\n✗ 페이지 추출 실패로 중단")
            return False

        # 3. 페이지 분석
        if not self.analyze_pages():
            print("\n✗ 페이지 분석 실패로 중단")
            return False

        # 4. 리포트 생성
        if not self.generate_report():
            print("\n✗ 리포트 생성 실패")
            return False

        elapsed_time = time.time() - start_time

        print("\n" + "=" * 80)
        print("✓ 전체 처리 완료!")
        print("=" * 80)
        print(f"총 소요 시간: {elapsed_time:.2f}초 ({elapsed_time/60:.1f}분)")
        print(f"출력 디렉토리: {self.base_dir}")
        print("=" * 80)

        return True

def main():
    """메인 함수"""
    if len(sys.argv) < 3:
        print("사용법: python process_city_data.py <city_name> <pdf_file> [dpi]")
        print("\n예시:")
        print("  python process_city_data.py sejong sejong.pdf")
        print("  python process_city_data.py jeju jeju.pdf 200")
        print("\n사용 가능한 도시:")
        print("  - sejong (세종)")
        print("  - jeju (제주)")
        sys.exit(1)

    city_name = sys.argv[1].lower()
    pdf_file = sys.argv[2]
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150

    if not os.path.exists(pdf_file):
        print(f"오류: PDF 파일을 찾을 수 없습니다: {pdf_file}")
        sys.exit(1)

    processor = CityDataProcessor(city_name, pdf_file)
    success = processor.process_all(dpi)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
