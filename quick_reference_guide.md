# Sejong Election Data - Quick Reference Cheat Sheet

## 📊 Document Overview
- **Type:** 개표상황표 (Vote Count Status Report)
- **Election:** 21st Presidential Election (제21대 대통령선거)
- **Region:** Sejong Special Self-Governing City
- **Total Pages:** 126 pages
- **Date:** June 3, 2025

---

## 🗳️ The 5 Presidential Candidates

| # | Candidate (Korean) | Candidate (English) | Party (Korean) | Party (English) |
|---|-------------------|---------------------|----------------|-----------------|
| **1** | 이재명 | Lee Jae-myung | 더불어민주당 | Democratic Party |
| **2** | 김문수 | Kim Moon-soo | 국민의힘 | People Power Party |
| **4** | 이준석 | Lee Jun-seok | 개혁신당 | Reform Party |
| **5** | 권영국 | Kwon Young-guk | 민주노동당 | Democratic Labor Party |
| **8** | 송진호 | Song Jin-ho | 무소속 | Independent |

---

## 📋 Key Korean Terms Translation

### **Document Sections**
| Korean | English | Purpose |
|--------|---------|---------|
| 개표상황표 | Vote Count Status Report | Main document title |
| 투표함수 | Ballot Box Number | Polling station ID |
| 선거인수 | Registered Voters | Total eligible voters |
| 투표용지 교부수 | Ballots Issued | Number of ballots given out |
| 투표수 | Votes Cast | Actual votes counted |
| 유효투표수 | Valid Votes | Votes that count |
| 무효투표수 | Invalid Votes | Rejected ballots |

### **Vote Counting Process**
| Korean | English | What It Means |
|--------|---------|---------------|
| 분류된 투표지수(②) | Classified Ballots | Machine-sorted votes (initial) |
| 재확인대상 투표지수(③) | Reconfirmation Needed | Ballots flagged for manual review |
| 확인결과(a) | Verification Result | Final confirmed machine count |
| 확인결과(b) | Verification Result | Final confirmed recount |
| 계 | Total | Sum/Total |

### **Vote Types**
| Korean | English | Description |
|--------|---------|-------------|
| 초소선상투표 | Absentee/Ship Voting | Remote/naval voting |
| 관외사전투표 | Out-of-district Early Voting | Early voting outside home district |
| 관내사전투표 | In-district Early Voting | Early voting in home district |
| 선거일투표 | Election Day Voting | Regular voting on election day |
| 재외투표 | Overseas Voting | Voting from abroad |

---

## 🔢 Reading a Typical Page

### **Step 1: Header (Top Section)**
```
제21대 대통령선거 [관외사전]
1. 투표지분류 개시시각: 2025-06-03 22:34:14
2. 투표용지 교부수와 투표수 대조결과
```
**What this tells you:**
- Which type of voting is being counted
- When counting started
- Ballot reconciliation follows

### **Step 2: Ballot Reconciliation Table**
```
| 투표함수 | 선거인수(①) | 투표용지 교부수(②) | 투표수(③) | 차 (①-②-③) |
|---------|-----------|-----------------|---------|-----------|
|    2    |  2,230    |     1,895       |  1,895  |     0     |
```
**What to check:**
- ✓ Discrepancy should be 0 or very small
- ⚠️ Large discrepancy = data quality issue

### **Step 3: Vote Counting - LEFT TABLE (Machine Processing)**
```
구분 | 부서별 | 후보명 | 분류된②  | 재확인③  | 계(②+③)
-----|--------|--------|---------|---------|--------
 1   | 더불어  | 이재명 |  1,227  |    0    | 1,227
 2   | 국민의힘| 김문수 |   375   |    0    |  375
 4   | 개혁신당| 이준석 |   209   |   39    |  248
```
**What this shows:**
- Initial machine count (분류된②)
- How many need manual review (재확인③)
- Machine total before human verification

### **Step 4: Vote Counting - RIGHT TABLE (Manual Verification)**
```
구분 | 부서별 | 후보명 | 확인결과(a) | 확인결과(b) | 계(a+b)
-----|--------|--------|------------|------------|--------
 1   | 더불어  | 이재명 |   1,227    |     13     | 1,240
 2   | 국민의힘| 김문수 |    375     |      0     |  375
 4   | 개혁신당| 이준석 |    209     |      2     |  211
```
**What this shows:**
- Final verified machine count (a)
- Final verified recount (b)
- **FINAL OFFICIAL TOTAL (a+b)** ← This is what matters!

### **Step 5: Invalid Votes**
```
무효투표수: 16
```
**What this shows:**
- Ballots that couldn't be counted (damaged, unclear, etc.)

### **Step 6: Final Totals (Bottom of Left Table)**
```
계: 1,856 (machine) + 39 (reconfirm) = 1,895 total
```
**Must match:** Votes Cast from Step 2!

---

## 🎯 The Two-Stage Verification Process

### **Stage 1: Machine Sorting**
1. Ballots fed into sorting machine
2. Machine reads and classifies: 97% success rate
3. Questionable ballots flagged (3%)
4. Result: **분류된 투표지수(②)** + **재확인대상(③)**

### **Stage 2: Manual Verification**
1. Humans verify ALL machine-sorted ballots → **확인결과(a)**
2. Humans review ALL flagged ballots → **확인결과(b)**
3. Result: **Final Official Count = (a) + (b)**

### **Why Two Stages?**
- ✓ Double-checking ensures accuracy
- ✓ Catches machine errors
- ✓ Resolves ambiguous ballots
- ✓ Creates audit trail

---

## 📊 Example Calculation Walkthrough

### **Page 2 - Ballot Box 2 - Candidate 이재명**

**Machine Stage:**
- Machine sorted: 1,227 votes (②)
- Needed recount: 0 votes (③)
- Machine total: 1,227

**Manual Stage:**
- Verified machine count: 1,227 (a)
- Verified recount: 13 (b) ← Found 13 more votes!
- **Final total: 1,240** ✓

**Key insight:** Manual review found 13 additional votes for 이재명 that weren't in the initial machine count.

---

## 🔍 Data Quality Checkpoints

### **Green Flags (Good Data)** ✓
- [ ] Discrepancy = 0 in ballot reconciliation
- [ ] Machine total matches ballots cast
- [ ] Final verified total matches machine total
- [ ] All 8 committee member seals present
- [ ] Timestamp recorded
- [ ] Chairman signature present

### **Red Flags (Check Data)** ⚠️
- [ ] Large discrepancy in ballot reconciliation
- [ ] Totals don't match across tables
- [ ] Missing seals or signatures
- [ ] No timestamp
- [ ] Illegible handwriting in verification columns

---

## 📈 Aggregation Formula

To get overall election results:

```
For each candidate:
  Total Votes = Sum of all (a+b) across all pages
  
Valid Votes = Sum of all candidate totals
Invalid Votes = Sum of all 무효투표수
Total Votes Cast = Valid + Invalid

Vote Share % = (Candidate Total / Valid Votes) × 100%
Turnout % = (Total Cast / Registered Voters) × 100%
```

---

## 🗂️ Page Organization

### **By Vote Type:**
- **Pages 1:** Cover/Summary
- **Pages 2-15:** Out-of-district Early Voting (관외사전)
- **Pages 16-38:** In-district Early Voting (관내사전)
- **Pages 39-125:** Election Day Voting (선거일)
- **Page 126:** Overseas/Special Voting (재외)

### **By Polling Station:**
Each page = One polling station's complete count

---

## 💡 Pro Tips for Data Extraction

### **1. OCR Challenges**
- Korean text requires proper OCR library
- Handwritten numbers in right column
- Circular official seals may interfere

### **2. Table Structure**
- Tables are fixed-position
- Candidate order always same (1,2,4,5,8)
- Some pages have different layouts

### **3. Number Formats**
- Large numbers use commas: 19,900
- Must strip commas before parsing
- Watch for handwritten vs. printed numbers

### **4. Verification Logic**
```python
# Pseudocode for validation
if machine_total == ballots_cast:
    if verified_total == machine_total:
        if discrepancy == 0:
            status = "VALID"
```

---

## 🎓 Common Questions Answered

**Q: Why are candidate numbers 3, 6, 7 missing?**  
A: Not all ballot positions were used in this election.

**Q: What's the difference between (②+③) and (a+b)?**  
A: (②+③) = Machine's count before human review  
(a+b) = Final verified count after human review

**Q: Which number should I use for final results?**  
A: Always use (a+b) - the final verified total from the right table.

**Q: Why does (b) sometimes show more votes than (③)?**  
A: Manual review can discover additional votes that the machine classified as something else.

**Q: How do I identify which vote type a page represents?**  
A: Look at the header right after "제21대 대통령선거" - it shows the vote type in brackets.

---

## 📦 Data Structure Summary

```
Sejong Election PDF
├── Page 1: Summary
└── Pages 2-126: Detailed Counts
    ├── Header Info
    │   ├── Vote Type
    │   ├── Timestamp
    │   └── Ballot Reconciliation
    ├── Machine Sorting Table (LEFT)
    │   ├── Candidate 1-8 (5 total)
    │   ├── Machine Count (②)
    │   ├── Reconfirm Needed (③)
    │   └── Invalid Votes
    └── Manual Verification Table (RIGHT)
        ├── Candidate 1-8 (5 total)
        ├── Verified Count (a)
        ├── Verified Recount (b)
        └── FINAL TOTAL (a+b) ← Use This!
```

---

## ✅ Quick Extraction Checklist

When processing each page:
- [ ] Extract page number and vote type
- [ ] Get ballot reconciliation numbers
- [ ] Extract all candidate names (verify 5 total)
- [ ] Get final totals (a+b) for each candidate
- [ ] Get invalid vote count
- [ ] Verify totals match
- [ ] Record timestamp
- [ ] Note any quality issues

---

**Remember:** The most important number is the **(a+b) Final Total** in the right table. This is the official certified count after both machine and human verification!
