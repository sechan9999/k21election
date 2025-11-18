#!/usr/bin/env python3
"""
Extract ALL 126 pages - Complete Sejong City Election Data
수작업으로 모든 페이지 데이터 추출
"""
import pandas as pd

def get_all_voting_results():
    """
    Extract (a) and (b) values from ALL 126 pages
    완전한 세종시 선거 결과 집계
    """

    results = [
        # Page 1: Summary page - skip

        # Page 2: 관외투표
        {
            "page": 2,
            "voting_location": "관외투표",
            "type": "Out-of-district voting",
            "C1_a": 1227, "C1_b": 13,
            "C2_a": 375, "C2_b": 0,
            "C4_a": 209, "C4_b": 39,
            "C5_a": 44, "C5_b": 1,
            "C8_a": 1, "C8_b": 1,
            "invalid_a": 0, "invalid_b": 0
        },

        # Page 3: 관내사전
        {
            "page": 3,
            "voting_location": "관내사전",
            "type": "In-district advance voting",
            "C1_a": 19900, "C1_b": 452,
            "C2_a": 7679, "C2_b": 280,
            "C4_a": 4520, "C4_b": 128,
            "C5_a": 354, "C5_b": 9,
            "C8_a": 37, "C8_b": 5,
            "invalid_a": 0, "invalid_b": 308
        },

        # Page 4: 투표함 1
        {
            "page": 4,
            "voting_location": "투표함 1",
            "type": "Ballot box 1",
            "C1_a": 1862, "C1_b": 49,
            "C2_a": 624, "C2_b": 14,
            "C4_a": 362, "C4_b": 14,
            "C5_a": 25, "C5_b": 1,
            "C8_a": 4, "C8_b": 1,
            "invalid_a": 0, "invalid_b": 27
        },

        # Page 5: 투표함 2
        {
            "page": 5,
            "voting_location": "투표함 2",
            "type": "Ballot box 2",
            "C1_a": 1865, "C1_b": 56,
            "C2_a": 616, "C2_b": 28,
            "C4_a": 370, "C4_b": 14,
            "C5_a": 29, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 21
        },

        # Page 6: 투표함 3
        {
            "page": 6,
            "voting_location": "투표함 3",
            "type": "Ballot box 3",
            "C1_a": 1873, "C1_b": 25,
            "C2_a": 610, "C2_b": 14,
            "C4_a": 402, "C4_b": 12,
            "C5_a": 28, "C5_b": 0,
            "C8_a": 4, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 32
        },

        # Page 7: 투표함 4 (NEW)
        {
            "page": 7,
            "voting_location": "투표함 4",
            "type": "Ballot box 4",
            "C1_a": 1106, "C1_b": 39,
            "C2_a": 537, "C2_b": 23,
            "C4_a": 361, "C4_b": 3,
            "C5_a": 34, "C5_b": 2,
            "C8_a": 5, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 24
        },

        # Page 8: 투표함 5 (NEW)
        {
            "page": 8,
            "voting_location": "투표함 5",
            "type": "Ballot box 5",
            "C1_a": 1796, "C1_b": 24,
            "C2_a": 598, "C2_b": 16,
            "C4_a": 357, "C4_b": 7,
            "C5_a": 24, "C5_b": 2,
            "C8_a": 4, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 24
        },

        # Page 9: 투표함 6 (NEW)
        {
            "page": 9,
            "voting_location": "투표함 6",
            "type": "Ballot box 6",
            "C1_a": 1859, "C1_b": 38,
            "C2_a": 669, "C2_b": 15,
            "C4_a": 350, "C4_b": 5,
            "C5_a": 27, "C5_b": 1,
            "C8_a": 5, "C8_b": 2,
            "invalid_a": 0, "invalid_b": 21
        },

        # Page 10: 투표함 7
        {
            "page": 10,
            "voting_location": "투표함 7",
            "type": "Ballot box 7",
            "C1_a": 1649, "C1_b": 43,
            "C2_a": 787, "C2_b": 29,
            "C4_a": 428, "C4_b": 11,
            "C5_a": 22, "C5_b": 0,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 28
        },

        # Page 11: 투표함 8 (NEW)
        {
            "page": 11,
            "voting_location": "투표함 8",
            "type": "Ballot box 8",
            "C1_a": 1673, "C1_b": 28,
            "C2_a": 747, "C2_b": 18,
            "C4_a": 455, "C4_b": 12,
            "C5_a": 35, "C5_b": 0,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 29
        },

        # Page 12: 투표함 9 (NEW)
        {
            "page": 12,
            "voting_location": "투표함 9",
            "type": "Ballot box 9",
            "C1_a": 1658, "C1_b": 75,
            "C2_a": 714, "C2_b": 50,
            "C4_a": 398, "C4_b": 24,
            "C5_a": 47, "C5_b": 3,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 33
        },

        # Page 13: 투표함 10 (NEW)
        {
            "page": 13,
            "voting_location": "투표함 10",
            "type": "Ballot box 10",
            "C1_a": 1632, "C1_b": 25,
            "C2_a": 764, "C2_b": 24,
            "C4_a": 473, "C4_b": 9,
            "C5_a": 42, "C5_b": 3,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 29
        },

        # Page 14: 투표함 11 (NEW)
        {
            "page": 14,
            "voting_location": "투표함 11",
            "type": "Ballot box 11",
            "C1_a": 1613, "C1_b": 26,
            "C2_a": 770, "C2_b": 30,
            "C4_a": 473, "C4_b": 18,
            "C5_a": 33, "C5_b": 0,
            "C8_a": 3, "C8_b": 1,
            "invalid_a": 0, "invalid_b": 25
        },

        # Page 15: 투표함 12 (NEW)
        {
            "page": 15,
            "voting_location": "투표함 12",
            "type": "Ballot box 12",
            "C1_a": 364, "C1_b": 11,
            "C2_a": 187, "C2_b": 5,
            "C4_a": 91, "C4_b": 1,
            "C5_a": 8, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 6
        },

        # Page 16: 관내선거일
        {
            "page": 16,
            "voting_location": "관내선거일",
            "type": "In-district election day",
            "C1_a": 4044, "C1_b": 301,
            "C2_a": 1760, "C2_b": 104,
            "C4_a": 584, "C4_b": 18,
            "C5_a": 66, "C5_b": 0,
            "C8_a": 11, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 82
        },

        # Page 17: 역기역
        {
            "page": 17,
            "voting_location": "역기역",
            "type": "Yeokgi Station",
            "C1_a": 606, "C1_b": 11,
            "C2_a": 296, "C2_b": 4,
            "C4_a": 77, "C4_b": 0,
            "C5_a": 5, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 6
        },

        # Page 18: 역등역
        {
            "page": 18,
            "voting_location": "역등역",
            "type": "Yeokdeung Station",
            "C1_a": 563, "C1_b": 8,
            "C2_a": 293, "C2_b": 5,
            "C4_a": 68, "C4_b": 0,
            "C5_a": 8, "C5_b": 0,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 7
        },

        # Page 19: 발전면
        {
            "page": 19,
            "voting_location": "발전면",
            "type": "Baljeon-myeon",
            "C1_a": 1107, "C1_b": 18,
            "C2_a": 619, "C2_b": 14,
            "C4_a": 173, "C4_b": 2,
            "C5_a": 14, "C5_b": 0,
            "C8_a": 6, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 22
        },

        # Page 20: 금남면
        {
            "page": 20,
            "voting_location": "금남면",
            "type": "Geumnam-myeon",
            "C1_a": 1167, "C1_b": 24,
            "C2_a": 686, "C2_b": 22,
            "C4_a": 136, "C4_b": 1,
            "C5_a": 14, "C5_b": 0,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 21
        },

        # Page 21: 광군면
        {
            "page": 21,
            "voting_location": "광군면",
            "type": "Gwanggun-myeon",
            "C1_a": 942, "C1_b": 12,
            "C2_a": 462, "C2_b": 13,
            "C4_a": 91, "C4_b": 0,
            "C5_a": 4, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 8
        },

        # Page 22: 역사역
        {
            "page": 22,
            "voting_location": "역사역",
            "type": "Yeoksa Station",
            "C1_a": 1540, "C1_b": 19,
            "C2_a": 643, "C2_b": 14,
            "C4_a": 198, "C4_b": 2,
            "C5_a": 26, "C5_b": 1,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 18
        },

        # Page 23: 전의면
        {
            "page": 23,
            "voting_location": "전의면",
            "type": "Jeonui-myeon",
            "C1_a": 958, "C1_b": 16,
            "C2_a": 502, "C2_b": 25,
            "C4_a": 90, "C4_b": 1,
            "C5_a": 11, "C5_b": 1,
            "C8_a": 5, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 25
        },

        # Page 24: 전동면
        {
            "page": 24,
            "voting_location": "전동면",
            "type": "Jeondong-myeon",
            "C1_a": 536, "C1_b": 16,
            "C2_a": 326, "C2_b": 7,
            "C4_a": 47, "C4_b": 2,
            "C5_a": 11, "C5_b": 1,
            "C8_a": 4, "C8_b": 2,
            "invalid_a": 0, "invalid_b": 29
        },

        # Page 25: 소정면
        {
            "page": 25,
            "voting_location": "소정면",
            "type": "Sojeong-myeon",
            "C1_a": 345, "C1_b": 9,
            "C2_a": 245, "C2_b": 8,
            "C4_a": 34, "C4_b": 1,
            "C5_a": 8, "C5_b": 1,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 3
        },

        # Page 26: 한솔동
        {
            "page": 26,
            "voting_location": "한솔동",
            "type": "Hansol-dong",
            "C1_a": 2604, "C1_b": 34,
            "C2_a": 912, "C2_b": 9,
            "C4_a": 296, "C4_b": 5,
            "C5_a": 45, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 16
        },

        # Page 27: 도담동
        {
            "page": 27,
            "voting_location": "도담동",
            "type": "Dodam-dong",
            "C1_a": 4238, "C1_b": 39,
            "C2_a": 1287, "C2_b": 14,
            "C4_a": 578, "C4_b": 11,
            "C5_a": 65, "C5_b": 1,
            "C8_a": 4, "C8_b": 1,
            "invalid_a": 0, "invalid_b": 35
        },

        # Page 28: 아름동
        {
            "page": 28,
            "voting_location": "아름동",
            "type": "Areum-dong",
            "C1_a": 4107, "C1_b": 49,
            "C2_a": 996, "C2_b": 7,
            "C4_a": 524, "C4_b": 3,
            "C5_a": 70, "C5_b": 0,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 40
        },

        # Page 29: 종촌동
        {
            "page": 29,
            "voting_location": "종촌동",
            "type": "Jongchon-dong",
            "C1_a": 4227, "C1_b": 40,
            "C2_a": 1142, "C2_b": 14,
            "C4_a": 555, "C4_b": 7,
            "C5_a": 69, "C5_b": 0,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 48
        },

        # Page 30: 고운동
        {
            "page": 30,
            "voting_location": "고운동",
            "type": "Goun-dong",
            "C1_a": 4286, "C1_b": 29,
            "C2_a": 980, "C2_b": 6,
            "C4_a": 387, "C4_b": 6,
            "C5_a": 56, "C5_b": 1,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 50
        },

        # Page 31: 새롬동
        {
            "page": 31,
            "voting_location": "새롬동",
            "type": "Saerom-dong",
            "C1_a": 4185, "C1_b": 22,
            "C2_a": 1052, "C2_b": 10,
            "C4_a": 611, "C4_b": 8,
            "C5_a": 68, "C5_b": 1,
            "C8_a": 5, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 46
        },

        # Page 32: 보람동
        {
            "page": 32,
            "voting_location": "보람동",
            "type": "Boram-dong",
            "C1_a": 3771, "C1_b": 41,
            "C2_a": 972, "C2_b": 14,
            "C4_a": 530, "C4_b": 7,
            "C5_a": 69, "C5_b": 1,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 107
        },

        # Page 33: 단업동
        {
            "page": 33,
            "voting_location": "단업동",
            "type": "Daneop-dong",
            "C1_a": 2150, "C1_b": 29,
            "C2_a": 597, "C2_b": 16,
            "C4_a": 287, "C4_b": 3,
            "C5_a": 33, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 11
        },

        # Page 34: 소담동
        {
            "page": 34,
            "voting_location": "소담동",
            "type": "Sodam-dong",
            "C1_a": 4102, "C1_b": 44,
            "C2_a": 1060, "C2_b": 15,
            "C4_a": 546, "C4_b": 7,
            "C5_a": 68, "C5_b": 1,
            "C8_a": 1, "C8_b": 1,
            "invalid_a": 0, "invalid_b": 38
        },

        # Page 35: 다정동
        {
            "page": 35,
            "voting_location": "다정동",
            "type": "Dajeong-dong",
            "C1_a": 4315, "C1_b": 22,
            "C2_a": 1156, "C2_b": 15,
            "C4_a": 588, "C4_b": 9,
            "C5_a": 81, "C5_b": 1,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 241
        },

        # Page 36: 해밀동
        {
            "page": 36,
            "voting_location": "해밀동",
            "type": "Haemil-dong",
            "C1_a": 3011, "C1_b": 19,
            "C2_a": 661, "C2_b": 15,
            "C4_a": 405, "C4_b": 3,
            "C5_a": 43, "C5_b": 1,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 33
        },

        # Page 37: 반곡동
        {
            "page": 37,
            "voting_location": "반곡동",
            "type": "Bangok-dong",
            "C1_a": 3923, "C1_b": 70,
            "C2_a": 950, "C2_b": 14,
            "C4_a": 577, "C4_b": 16,
            "C5_a": 74, "C5_b": 1,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 35
        },

        # Page 38: 나성동
        {
            "page": 38,
            "voting_location": "나성동",
            "type": "Naseong-dong",
            "C1_a": 2759, "C1_b": 33,
            "C2_a": 684, "C2_b": 11,
            "C4_a": 475, "C4_b": 7,
            "C5_a": 66, "C5_b": 0,
            "C8_a": 6, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 31
        },

        # Page 39: 아리온동
        {
            "page": 39,
            "voting_location": "아리온동",
            "type": "Arion-dong",
            "C1_a": 2484, "C1_b": 25,
            "C2_a": 720, "C2_b": 8,
            "C4_a": 472, "C4_b": 12,
            "C5_a": 64, "C5_b": 0,
            "C8_a": 6, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 23
        },

        # Page 40: 조치원읍 제1투표구
        {
            "page": 40,
            "voting_location": "조치원읍제1투",
            "type": "Jochiwon-eup Precinct 1",
            "C1_a": 359, "C1_b": 8,
            "C2_a": 621, "C2_b": 14,
            "C4_a": 66, "C4_b": 3,
            "C5_a": 4, "C5_b": 1,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 10
        },

        # Page 41: 조치원읍 제2투표구
        {
            "page": 41,
            "voting_location": "조치원읍제2투",
            "type": "Jochiwon-eup Precinct 2",
            "C1_a": 230, "C1_b": 9,
            "C2_a": 400, "C2_b": 10,
            "C4_a": 36, "C4_b": 2,
            "C5_a": 3, "C5_b": 0,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 7
        },

        # Page 42: 조치원읍 제3투표구
        {
            "page": 42,
            "voting_location": "조치원읍제3투",
            "type": "Jochiwon-eup Precinct 3",
            "C1_a": 436, "C1_b": 9,
            "C2_a": 644, "C2_b": 24,
            "C4_a": 78, "C4_b": 2,
            "C5_a": 8, "C5_b": 1,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 12
        },

        # Page 43: 조치원읍 제4투표구
        {
            "page": 43,
            "voting_location": "조치원읍제4투",
            "type": "Jochiwon-eup Precinct 4",
            "C1_a": 763, "C1_b": 15,
            "C2_a": 992, "C2_b": 21,
            "C4_a": 167, "C4_b": 1,
            "C5_a": 15, "C5_b": 0,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 13
        },

        # Page 44: 조치원읍 제5투표구
        {
            "page": 44,
            "voting_location": "조치원읍제5투",
            "type": "Jochiwon-eup Precinct 5",
            "C1_a": 732, "C1_b": 12,
            "C2_a": 851, "C2_b": 12,
            "C4_a": 154, "C4_b": 10,
            "C5_a": 21, "C5_b": 1,
            "C8_a": 0, "C8_b": 1,
            "invalid_a": 0, "invalid_b": 19
        },

        # Page 45: 조치원읍 제6투표구
        {
            "page": 45,
            "voting_location": "조치원읍제6투",
            "type": "Jochiwon-eup Precinct 6",
            "C1_a": 116, "C1_b": 9,
            "C2_a": 233, "C2_b": 9,
            "C4_a": 21, "C4_b": 0,
            "C5_a": 1, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 0
        },

        # Page 46: 조치원읍 제7투표구
        {
            "page": 46,
            "voting_location": "조치원읍제7투",
            "type": "Jochiwon-eup Precinct 7",
            "C1_a": 254, "C1_b": 8,
            "C2_a": 369, "C2_b": 9,
            "C4_a": 135, "C4_b": 3,
            "C5_a": 11, "C5_b": 1,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 2
        },

        # Page 47: 조치원읍 제8투표구
        {
            "page": 47,
            "voting_location": "조치원읍제8투",
            "type": "Jochiwon-eup Precinct 8",
            "C1_a": 1057, "C1_b": 23,
            "C2_a": 1093, "C2_b": 19,
            "C4_a": 153, "C4_b": 2,
            "C5_a": 21, "C5_b": 1,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 12
        },

        # Page 48: 조치원읍 제9투표구
        {
            "page": 48,
            "voting_location": "조치원읍제9투",
            "type": "Jochiwon-eup Precinct 9",
            "C1_a": 569, "C1_b": 7,
            "C2_a": 670, "C2_b": 21,
            "C4_a": 94, "C4_b": 0,
            "C5_a": 12, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 8
        },

        # Page 49: 조치원읍 제10투표구
        {
            "page": 49,
            "voting_location": "조치원읍제10투",
            "type": "Jochiwon-eup Precinct 10",
            "C1_a": 646, "C1_b": 20,
            "C2_a": 874, "C2_b": 26,
            "C4_a": 110, "C4_b": 3,
            "C5_a": 11, "C5_b": 1,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 19
        },

        # Page 50: 조치원읍 제11투표구
        {
            "page": 50,
            "voting_location": "조치원읍제11투",
            "type": "Jochiwon-eup Precinct 11",
            "C1_a": 1171, "C1_b": 23,
            "C2_a": 1011, "C2_b": 20,
            "C4_a": 160, "C4_b": 3,
            "C5_a": 32, "C5_b": 1,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 10
        },

        # Page 51: 역기역동투표소
        {
            "page": 51,
            "voting_location": "역기역동투표소",
            "type": "Yeokgi-Yeokdong Precinct",
            "C1_a": 231, "C1_b": 8,
            "C2_a": 453, "C2_b": 6,
            "C4_a": 32, "C4_b": 1,
            "C5_a": 3, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 1
        },

        # Page 52: 연동면제1투
        {
            "page": 52,
            "voting_location": "연동면제1투",
            "type": "Yeondong-myeon Precinct 1",
            "C1_a": 137, "C1_b": 5,
            "C2_a": 336, "C2_b": 10,
            "C4_a": 21, "C4_b": 0,
            "C5_a": 2, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 4
        },

        # Page 53: 연동면제2투
        {
            "page": 53,
            "voting_location": "연동면제2투",
            "type": "Yeondong-myeon Precinct 2",
            "C1_a": 168, "C1_b": 7,
            "C2_a": 296, "C2_b": 14,
            "C4_a": 31, "C4_b": 0,
            "C5_a": 1, "C5_b": 1,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 3
        },

        # Page 54: 부강면제1투
        {
            "page": 54,
            "voting_location": "부강면제1투",
            "type": "Bugang-myeon Precinct 1",
            "C1_a": 370, "C1_b": 15,
            "C2_a": 626, "C2_b": 29,
            "C4_a": 80, "C4_b": 3,
            "C5_a": 11, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 6
        },

        # Page 55: 부강면제2투
        {
            "page": 55,
            "voting_location": "부강면제2투",
            "type": "Bugang-myeon Precinct 2",
            "C1_a": 182, "C1_b": 8,
            "C2_a": 312, "C2_b": 21,
            "C4_a": 27, "C4_b": 5,
            "C5_a": 4, "C5_b": 1,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 2
        },

        # Page 56: 금남면제1투
        {
            "page": 56,
            "voting_location": "금남면제1투",
            "type": "Geumnam-myeon Precinct 1",
            "C1_a": 355, "C1_b": 14,
            "C2_a": 424, "C2_b": 13,
            "C4_a": 82, "C4_b": 3,
            "C5_a": 9, "C5_b": 0,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 18
        },

        # Page 57: 금남면제2투
        {
            "page": 57,
            "voting_location": "금남면제2투",
            "type": "Geumnam-myeon Precinct 2",
            "C1_a": 162, "C1_b": 9,
            "C2_a": 358, "C2_b": 6,
            "C4_a": 22, "C4_b": 1,
            "C5_a": 2, "C5_b": 1,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 4
        },

        # Page 58: 금남면제3투
        {
            "page": 58,
            "voting_location": "금남면제3투",
            "type": "Geumnam-myeon Precinct 3",
            "C1_a": 161, "C1_b": 10,
            "C2_a": 353, "C2_b": 1,
            "C4_a": 26, "C4_b": 2,
            "C5_a": 4, "C5_b": 1,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 7
        },

        # Page 59: 금남면제4투
        {
            "page": 59,
            "voting_location": "금남면제4투",
            "type": "Geumnam-myeon Precinct 4",
            "C1_a": 141, "C1_b": 10,
            "C2_a": 308, "C2_b": 18,
            "C4_a": 17, "C4_b": 0,
            "C5_a": 1, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 0
        },

        # Page 60: 장군면제1투
        {
            "page": 60,
            "voting_location": "장군면제1투",
            "type": "Janggun-myeon Precinct 1",
            "C1_a": 283, "C1_b": 10,
            "C2_a": 490, "C2_b": 9,
            "C4_a": 69, "C4_b": 5,
            "C5_a": 6, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 9
        },

        # Page 61: 장군면제2투
        {
            "page": 61,
            "voting_location": "장군면제2투",
            "type": "Janggun-myeon Precinct 2",
            "C1_a": 262, "C1_b": 8,
            "C2_a": 495, "C2_b": 17,
            "C4_a": 72, "C4_b": 0,
            "C5_a": 3, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 5
        },

        # Page 62: 장군면제3투
        {
            "page": 62,
            "voting_location": "장군면제3투",
            "type": "Janggun-myeon Precinct 3",
            "C1_a": 75, "C1_b": 4,
            "C2_a": 144, "C2_b": 13,
            "C4_a": 16, "C4_b": 0,
            "C5_a": 1, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 2
        },

        # Page 63: 연서면제1투
        {
            "page": 63,
            "voting_location": "연서면제1투",
            "type": "Yeonseo-myeon Precinct 1",
            "C1_a": 151, "C1_b": 15,
            "C2_a": 290, "C2_b": 18,
            "C4_a": 18, "C4_b": 1,
            "C5_a": 4, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 5
        },

        # Page 64: 연서면제2투
        {
            "page": 64,
            "voting_location": "연서면제2투",
            "type": "Yeonseo-myeon Precinct 2",
            "C1_a": 114, "C1_b": 5,
            "C2_a": 173, "C2_b": 3,
            "C4_a": 11, "C4_b": 0,
            "C5_a": 3, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 4
        },

        # Page 65: 연서면제3투
        {
            "page": 65,
            "voting_location": "연서면제3투",
            "type": "Yeonseo-myeon Precinct 3",
            "C1_a": 89, "C1_b": 5,
            "C2_a": 230, "C2_b": 1,
            "C4_a": 9, "C4_b": 0,
            "C5_a": 0, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 2
        },

        # Page 66: 연서면제4투
        {
            "page": 66,
            "voting_location": "연서면제4투",
            "type": "Yeonseo-myeon Precinct 4",
            "C1_a": 426, "C1_b": 17,
            "C2_a": 709, "C2_b": 14,
            "C4_a": 92, "C4_b": 3,
            "C5_a": 11, "C5_b": 0,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 20
        },

        # Page 67: 전의면제1투
        {
            "page": 67,
            "voting_location": "전의면제1투",
            "type": "Jeonui-myeon Precinct 1",
            "C1_a": 206, "C1_b": 3,
            "C2_a": 453, "C2_b": 1,
            "C4_a": 25, "C4_b": 3,
            "C5_a": 2, "C5_b": 1,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 5
        },

        # Page 68: 전의면제2투
        {
            "page": 68,
            "voting_location": "전의면제2투",
            "type": "Jeonui-myeon Precinct 2",
            "C1_a": 228, "C1_b": 4,
            "C2_a": 476, "C2_b": 13,
            "C4_a": 31, "C4_b": 1,
            "C5_a": 3, "C5_b": 1,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 5
        },

        # Page 69: 전의면제3투
        {
            "page": 69,
            "voting_location": "전의면제3투",
            "type": "Jeonui-myeon Precinct 3",
            "C1_a": 99, "C1_b": 4,
            "C2_a": 198, "C2_b": 4,
            "C4_a": 15, "C4_b": 0,
            "C5_a": 3, "C5_b": 1,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 2
        },

        # Page 70: 전동면제1투
        {
            "page": 70,
            "voting_location": "전동면제1투",
            "type": "Jeondong-myeon Precinct 1",
            "C1_a": 147, "C1_b": 6,
            "C2_a": 303, "C2_b": 12,
            "C4_a": 28, "C4_b": 1,
            "C5_a": 1, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 4
        },

        # Page 71: 전동면제2투
        {
            "page": 71,
            "voting_location": "전동면제2투",
            "type": "Jeondong-myeon Precinct 2",
            "C1_a": 84, "C1_b": 2,
            "C2_a": 152, "C2_b": 6,
            "C4_a": 11, "C4_b": 0,
            "C5_a": 0, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 1
        },

        # Page 72: 기전역
        {
            "page": 72,
            "voting_location": "기전역",
            "type": "Gijeon Station",
            "C1_a": 72, "C1_b": 4,
            "C2_a": 178, "C2_b": 7,
            "C4_a": 8, "C4_b": 0,
            "C5_a": 0, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 1
        },

        # Page 73: 소정면제1투
        {
            "page": 73,
            "voting_location": "소정면제1투",
            "type": "Sojeong-myeon Precinct 1",
            "C1_a": 181, "C1_b": 1,
            "C2_a": 442, "C2_b": 11,
            "C4_a": 32, "C4_b": 1,
            "C5_a": 7, "C5_b": 1,
            "C8_a": 1, "C8_b": 1,
            "invalid_a": 0, "invalid_b": 5
        },

        # Page 74: 한솔동제1투
        {
            "page": 74,
            "voting_location": "한솔동제1투",
            "type": "Hansol-dong Precinct 1",
            "C1_a": 814, "C1_b": 12,
            "C2_a": 631, "C2_b": 7,
            "C4_a": 191, "C4_b": 1,
            "C5_a": 15, "C5_b": 1,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 11
        },

        # Page 75: 한솔동제2투
        {
            "page": 75,
            "voting_location": "한솔동제2투",
            "type": "Hansol-dong Precinct 2",
            "C1_a": 674, "C1_b": 8,
            "C2_a": 525, "C2_b": 6,
            "C4_a": 119, "C4_b": 3,
            "C5_a": 13, "C5_b": 1,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 6
        },

        # Page 76: 한솔동제3투
        {
            "page": 76,
            "voting_location": "한솔동제3투",
            "type": "Hansol-dong Precinct 3",
            "C1_a": 581, "C1_b": 3,
            "C2_a": 552, "C2_b": 2,
            "C4_a": 117, "C4_b": 1,
            "C5_a": 15, "C5_b": 1,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 12
        },

        # Page 77: 한솔동제4투
        {
            "page": 77,
            "voting_location": "한솔동제4투",
            "type": "Hansol-dong Precinct 4",
            "C1_a": 703, "C1_b": 7,
            "C2_a": 778, "C2_b": 2,
            "C4_a": 176, "C4_b": 2,
            "C5_a": 24, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 20
        },

        # Page 78: 도담동제1투
        {
            "page": 78,
            "voting_location": "도담동제1투",
            "type": "Dodam-dong Precinct 1",
            "C1_a": 413, "C1_b": 3,
            "C2_a": 411, "C2_b": 7,
            "C4_a": 151, "C4_b": 3,
            "C5_a": 10, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 14
        },

        # Page 79: 도담동제2투
        {
            "page": 79,
            "voting_location": "도담동제2투",
            "type": "Dodam-dong Precinct 2",
            "C1_a": 436, "C1_b": 28,
            "C2_a": 640, "C2_b": 33,
            "C4_a": 85, "C4_b": 0,
            "C5_a": 25, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 19
        },

        # Page 80: 도담동제3투
        {
            "page": 80,
            "voting_location": "도담동제3투",
            "type": "Dodam-dong Precinct 3",
            "C1_a": 1087, "C1_b": 6,
            "C2_a": 1195, "C2_b": 12,
            "C4_a": 252, "C4_b": 1,
            "C5_a": 27, "C5_b": 0,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 17
        },

        # Page 81: 도담동제4투
        {
            "page": 81,
            "voting_location": "도담동제4투",
            "type": "Dodam-dong Precinct 4",
            "C1_a": 642, "C1_b": 3,
            "C2_a": 541, "C2_b": 12,
            "C4_a": 137, "C4_b": 2,
            "C5_a": 25, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 6
        },

        # Page 82: 도담동제5투
        {
            "page": 82,
            "voting_location": "도담동제5투",
            "type": "Dodam-dong Precinct 5",
            "C1_a": 708, "C1_b": 9,
            "C2_a": 784, "C2_b": 17,
            "C4_a": 154, "C4_b": 1,
            "C5_a": 21, "C5_b": 1,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 9
        },

        # Page 83: 아름동제1투
        {
            "page": 83,
            "voting_location": "아름동제1투",
            "type": "Areum-dong Precinct 1",
            "C1_a": 844, "C1_b": 5,
            "C2_a": 599, "C2_b": 15,
            "C4_a": 212, "C4_b": 3,
            "C5_a": 25, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 12
        },

        # Page 84: 아름동제2투
        {
            "page": 84,
            "voting_location": "아름동제2투",
            "type": "Areum-dong Precinct 2",
            "C1_a": 721, "C1_b": 9,
            "C2_a": 551, "C2_b": 6,
            "C4_a": 112, "C4_b": 4,
            "C5_a": 12, "C5_b": 0,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 10
        },

        # Page 85: 아름동제3투
        {
            "page": 85,
            "voting_location": "아름동제3투",
            "type": "Areum-dong Precinct 3",
            "C1_a": 899, "C1_b": 17,
            "C2_a": 743, "C2_b": 14,
            "C4_a": 142, "C4_b": 4,
            "C5_a": 22, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 17
        },

        # Page 86: 아름동제4투
        {
            "page": 86,
            "voting_location": "아름동제4투",
            "type": "Areum-dong Precinct 4",
            "C1_a": 1177, "C1_b": 15,
            "C2_a": 722, "C2_b": 20,
            "C4_a": 194, "C4_b": 1,
            "C5_a": 41, "C5_b": 0,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 18
        },

        # Page 87: 종촌동제1투
        {
            "page": 87,
            "voting_location": "종촌동제1투",
            "type": "Jongchon-dong Precinct 1",
            "C1_a": 840, "C1_b": 10,
            "C2_a": 647, "C2_b": 7,
            "C4_a": 160, "C4_b": 3,
            "C5_a": 19, "C5_b": 0,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 9
        },

        # Page 88: 종촌동제2투
        {
            "page": 88,
            "voting_location": "종촌동제2투",
            "type": "Jongchon-dong Precinct 2",
            "C1_a": 450, "C1_b": 3,
            "C2_a": 387, "C2_b": 10,
            "C4_a": 79, "C4_b": 1,
            "C5_a": 15, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 9
        },

        # Page 89: 종촌동제3투
        {
            "page": 89,
            "voting_location": "종촌동제3투",
            "type": "Jongchon-dong Precinct 3",
            "C1_a": 968, "C1_b": 7,
            "C2_a": 741, "C2_b": 7,
            "C4_a": 160, "C4_b": 4,
            "C5_a": 20, "C5_b": 0,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 15
        },

        # Page 90: 종촌동제4투
        {
            "page": 90,
            "voting_location": "종촌동제4투",
            "type": "Jongchon-dong Precinct 4",
            "C1_a": 671, "C1_b": 9,
            "C2_a": 596, "C2_b": 13,
            "C4_a": 124, "C4_b": 3,
            "C5_a": 19, "C5_b": 1,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 5
        },

        # TO BE CONTINUED with Pages 91-126...
        # 계속해서 나머지 페이지 추가 필요

    ]

    return results

# Progress tracker
if __name__ == "__main__":
    results = get_all_voting_results()
    print(f"Currently extracted: {len(results)} pages")
    print(f"Remaining: {126 - len(results) - 1} pages")  # -1 for page 1 (summary)
    print(f"Progress: {len(results)}/{125} pages ({len(results)/125*100:.1f}%)")
    print("\n진행 중: 전체 126페이지 데이터 추출 작업")
