# Sejong Election Data Structure Analysis
## Step-by-Step Breakdown with Explanations

---

## Document Overview

**Document Type:** 개표상황표 (Vote Count Status Report)  
**Election:** 제21대 대통령선거 (21st Presidential Election)  
**Region:** 세종특별자치시 (Sejong Special Self-Governing City)  
**Date:** 2025년 6월 3일 (June 3, 2025)  
**Total Pages:** 126 pages

---

## 1. Document Structure by Page Type

The PDF is organized into different sections based on voting type:

### **Page 1: Cover/Summary Page (초소선상투표)**
- Initial vote count summary
- Total registered voters: 443
- Total ballots cast: 423
- Vote totals by candidate (preliminary counts)

### **Pages 2+: Detailed Vote Count Pages (관외투표)**
Each page represents a different polling station or vote counting location with:
- Polling station number (투표함수)
- Detailed candidate vote breakdowns
- Vote verification data
- Official seals and signatures

---

## 2. Key Data Fields on Each Page

### **Section 1: Header Information (상단부)**
```
제21대 대통령선거 [투표구분]
1. 투표지분류 개시시각: [Date and Time]
2. 투표용지 교부수와 투표수 대조결과
```

**Explanation:**  
- Shows the start time of ballot classification
- Reconciles ballots issued vs. ballots counted

### **Section 2: Ballot Reconciliation Table (투표수 대조)**

| Field | Korean | Meaning |
|-------|---------|---------|
| 선거인수(①) | 선거인수 | Total Registered Voters |
| 투표용지 교부수(②) | 투표용지 교부수 | Ballots Issued |
| 투표수(③) | 투표수 | Actual Votes Cast |
| 차이(①-②-③) | 차 | Discrepancy |

**Example from Page 2:**
- Registered voters: 2,230
- Ballots issued: 1,895
- Votes cast: 1,895
- Discrepancy: 0 ✓

---

## 3. Main Vote Counting Table (투표상황 표)

### **Left Section: 투표지분류기운영부 (Ballot Sorting Machine Operation)**

This section shows votes counted by the automatic sorting machine:

| 구분 | 부서별 | 후보명 | 분류된 투표지수(②) | 재확인대상 투표지수(③) | 계(②+③) |
|------|--------|--------|------------------|---------------------|---------|
| 1 | 더불어민주당 | 이재명 | [count] | [recount] | [total] |
| 2 | 국민의힘 | 김문수 | [count] | [recount] | [total] |
| 4 | 개혁신당 | 이준석 | [count] | [recount] | [total] |
| 5 | 민주노동당 | 권영국 | [count] | [recount] | [total] |
| 8 | 무소속 | 송진호 | [count] | [recount] | [total] |

**Column Explanations:**
- **분류된 투표지수(②):** Ballots classified by machine (initial count)
- **재확인대상 투표지수(③):** Ballots requiring manual reconfirmation
- **계(②+③):** Total = Initial + Reconfirmed ballots

### **Right Section: 심사·집계부 (Review and Tabulation)**

This section shows the final verified counts after manual review:

| 분류된 투표지 확인결과(a) | 재확인대상 투표지 확인결과(b) | 계(a+b) |
|------------------------|---------------------------|---------|
| [verified count] | [verified recount] | [final total] |

**Process Flow:**
1. Machine sorts ballots → **분류된 투표지수(②)**
2. Questionable ballots flagged → **재확인대상(③)**
3. Manual verification of all → **확인결과(a)**
4. Manual review of flagged → **확인결과(b)**
5. Final certified total → **계(a+b)**

---

## 4. Example Data from Page 2 (투표함수 2)

### **Ballot Reconciliation:**
- Registered: 2,230
- Issued: 1,895
- Cast: 1,895
- Discrepancy: 0

### **Candidate Vote Breakdown:**

| Candidate | Party | Machine Count(②) | Reconfirm(③) | Verified(a) | Verified(b) | Final Total(a+b) |
|-----------|-------|-----------------|--------------|-------------|-------------|------------------|
| 이재명 | 더불어민주당 | 1,227 | - | 1,227 | 13 | 1,240 |
| 김문수 | 국민의힘 | 375 | - | 375 | 0 | 375 |
| 이준석 | 개혁신당 | 209 | 39 | 209 | 2 | 211 |
| 권영국 | 민주노동당 | 44 | (0) | 44 | - | 44 |
| 송진호 | 무소속 | 1 | - | 1 | - | 1 |

### **Invalid Ballots:**
- Machine invalid: 0
- Manual invalid: 16
- Total invalid: 16

### **Totals:**
- Machine classified: 1,856
- Reconfirmation needed: 39
- Machine total: 1,895
- Final verified: 1,895 ✓

---

## 5. Example Data from Page 3 (투표함수 12 - 관외사전)

This page shows **out-of-district early voting** results:

### **Ballot Reconciliation:**
- Registered: 33,676
- Issued: 33,674
- Cast: 33,672
- Discrepancy: 2

### **Candidate Vote Breakdown:**

| Candidate | Party | Machine Count(②) | Reconfirm(③) | Verified(a) | Verified(b) | Final Total(a+b) |
|-----------|-------|-----------------|--------------|-------------|-------------|------------------|
| 이재명 | 더불어민주당 | 19,900 | - | 19,900 | 452 | 20,352 |
| 김문수 | 국민의힘 | 7,679 | - | 7,679 | 280 | 7,959 |
| 이준석 | 개혁신당 | 4,520 | - | 4,520 | 128 | 4,648 |
| 권영국 | 민주노동당 | 354 | - | 354 | 9 | 363 |
| 송진호 | 무소속 | 37 | - | 37 | 5 | 42 |

### **Invalid Ballots:**
- Total invalid: 308

### **Totals:**
- Machine classified: 32,490
- Reconfirmation needed: 1,182
- Machine total: 33,672
- Final verified: 33,672 ✓

---

## 6. The Five Presidential Candidates

Based on the documents, here are the candidates:

| # | Party | Candidate Name | Party Name (English) |
|---|-------|----------------|----------------------|
| 1 | 더불어민주당 | 이재명 | Democratic Party of Korea |
| 2 | 국민의힘 | 김문수 | People Power Party |
| 4 | 개혁신당 | 이준석 | Reform Party |
| 5 | 민주노동당 | 권영국 | Democratic Labor Party |
| 8 | 무소속 | 송진호 | Independent |

**Note:** Numbers 3, 6, 7 are skipped in the ballot numbering.

---

## 7. Bottom Section: Official Verification (위원 검열)

Each page contains:
- **Multiple official seals (위원):** 8 committee member stamps
- **Signature section:** Committee member handwritten signatures
- **Timestamp:** Official completion time (위원장 공표시각)
- **Chairman signature:** Final approval signature (개표상황표 확인자 성명)

---

## 8. Key Statistical Patterns

### **Verification Rates:**
From the sample pages analyzed:
- **Initial machine classification rate: ~97%**
- **Reconfirmation rate: ~3%**
- Most ballots are correctly classified on first pass
- Reconfirmation primarily affects the leading candidate (이재명)

### **Data Quality Checks:**
✓ Ballot counts reconcile between issued and cast  
✓ Machine totals match manual verification totals  
✓ Discrepancies are minimal (0-2 votes per station)  
✓ Multiple verification steps ensure accuracy

---

## 9. Vote Types in the Document

Based on the page headers, the document contains:

| Page Range | Vote Type | Korean Name |
|------------|-----------|-------------|
| Page 1 | Absentee/Ship Voting | 초소선상투표 |
| Pages 2+ | Out-of-District Early Voting | 관외사전투표 |
| Additional | In-District Early Voting | 관내사전투표 |
| Additional | Election Day Voting | 선거일투표 |
| Additional | Overseas Voting | 재외투표 |

---

## 10. Data Extraction Strategy

To extract this data programmatically:

### **Step 1: Page Classification**
- Identify page type from header text
- Extract polling station number (투표함수)
- Determine voting category

### **Step 2: Table Extraction**
- Locate the main vote counting table
- Parse candidate names and party affiliations
- Extract numerical data from fixed table positions

### **Step 3: Vote Count Extraction**
For each candidate:
```python
{
    'polling_station': 2,
    'vote_type': '관외사전',
    'candidate': '이재명',
    'party': '더불어민주당',
    'machine_count': 1227,
    'reconfirm_count': 0,
    'verified_a': 1227,
    'verified_b': 13,
    'final_total': 1240
}
```

### **Step 4: Verification Data**
- Extract invalid ballot counts
- Verify totals match across columns
- Check reconciliation between issued and cast ballots

### **Step 5: Aggregation**
Sum all polling stations by:
- Candidate
- Vote type
- Region
- Total election results

---

## 11. Data Quality Indicators

### **Red Flags to Check:**
- ⚠️ Discrepancies in ballot reconciliation (①-②-③ ≠ 0)
- ⚠️ Machine totals don't match final verified totals
- ⚠️ Missing reconfirmation data
- ⚠️ Unsigned or unsealed pages

### **Green Flags (Good Data):**
- ✓ Zero discrepancy in ballot counts
- ✓ All committee member seals present
- ✓ Timestamps recorded
- ✓ Manual verification matches machine counts

---

## 12. Summary Statistics Formula

To calculate overall results:

```
Total Valid Votes = Sum of all candidate final totals
Total Invalid Votes = Sum of all invalid ballot counts  
Total Votes Cast = Valid + Invalid
Voter Turnout = (Total Votes Cast / Registered Voters) × 100%
Candidate Vote Share = (Candidate Votes / Total Valid Votes) × 100%
```

---

## 13. Important Notes for Data Processing

1. **Korean Text Recognition:** OCR must handle Korean characters (Hangul)
2. **Number Formats:** Some counts use commas (e.g., 19,900)
3. **Handwritten Data:** Right column often contains handwritten numbers
4. **Machine vs. Human:** Distinguish between machine (left) and verified (right) columns
5. **Multiple Tables:** Each page has 2-3 interconnected tables
6. **Official Seals:** Circular stamps confirm authenticity

---

## 14. Expected Output Format

After full extraction, create summary tables:

### **By Candidate (All Vote Types Combined):**
| Candidate | Party | Total Votes | Vote Share % |
|-----------|-------|-------------|--------------|
| 이재명 | 더불어민주당 | [sum] | [%] |
| 김문수 | 국민의힘 | [sum] | [%] |
| 이준석 | 개혁신당 | [sum] | [%] |
| 권영국 | 민주노동당 | [sum] | [%] |
| 송진호 | 무소속 | [sum] | [%] |

### **By Vote Type:**
| Vote Type | Total Votes | Valid | Invalid |
|-----------|-------------|-------|---------|
| 관외사전투표 | [sum] | [sum] | [sum] |
| 관내사전투표 | [sum] | [sum] | [sum] |
| 선거일투표 | [sum] | [sum] | [sum] |
| etc. | [sum] | [sum] | [sum] |

---

## 15. Conclusion

The Sejong election data is well-structured with:
- **Clear organizational hierarchy** (by voting type and station)
- **Dual verification system** (machine + manual)
- **Built-in error checking** (reconciliation tables)
- **Official authentication** (seals and signatures)
- **Transparent audit trail** (timestamps and committee records)

This document format ensures election integrity through multiple layers of verification and provides a comprehensive record of the vote counting process.

---

**Document prepared for:** Data extraction and analysis  
**Next steps:** Implement OCR or table extraction to digitize all 126 pages  
**Expected output:** Complete vote database for Sejong region
