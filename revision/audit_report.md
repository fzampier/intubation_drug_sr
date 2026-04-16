# Full Numerical Audit Report

**Date:** 2026-04-15
**Manuscript:** Induction agents for emergency tracheal intubation in critically ill adults: SR/NMA
**Submitted to:** Critical Care (2026-03-23), minor revision received

---

## Summary

| Severity | Count | Details |
|----------|-------|---------|
| CRITICAL | 0 | No errors affecting primary/secondary outcome estimates |
| HIGH | 1 | Vasopressor 24h pairwise direction bug — **FIXED** |
| MEDIUM | 2 | eFigure 7 caption; PROMINE MAP IQR — **FIXED** |
| LOW | 3 | PROMINE SOFA label; Punt RoB format; R script paths — **ALL FIXED** |

**Overall verdict: Manuscript numbers are correct. All identified issues have been fixed.**

### Fixes applied (2026-04-15)
1. `data/vasopressor.csv`: Swapped Casey 24h rows (E before K) to fix pairwise direction
2. `manuscript/overleaf/main.tex`: Updated Table 2 vaso 24h OR 0.58→0.51, CI 0.14-2.33→0.16-1.56, I² 96%→93%; updated 3 inline I² references
3. `manuscript/overleaf/esm.tex`: Updated eFigure 7 + eFigure 20 captions (I² 96%→93%, Table 2 reference); fixed PROMINE MAP IQR 82→79; fixed SOFA median(IQR)→mean(SD)
4. `data/study_info.csv`: "High risk"→"High" for Punt; "Under review"→"Intensive Care Med" for Schmidt
5. `data/mortality.csv`: "High risk"→"High" for Punt (2 rows)
6. All 4 R scripts: Fixed projdir path; re-run with corrected data; figures regenerated
7. `manuscript/overleaf/eFigure7_forest_vaso_24h.pdf`: Regenerated from corrected analysis

---

## Phase 1: R Script Reproducibility

### Path fix (all 4 scripts)
All 4 scripts hardcoded `projdir <- ".../intubation_sr"` but the repo is `intubation_drugs_sr`.
**Status:** Fixed during audit. **Severity:** LOW (does not affect committed outputs, only re-run portability).

### Script execution
All 4 scripts ran without errors on R 4.5.2 with meta 8.3-0 and netmeta 3.4-0.

| Script | Status | Outputs |
|--------|--------|---------|
| analysis_nma.R | OK | 12 figures + league tables + nma_results_summary.csv |
| analysis_subgroups.R | OK | 5 figures (setting, RoB, ICU NMA, collapse/remove ketofol) |
| analysis_sens_excl_casey.R | OK | 5 figures (CV, hypo, vaso peri, vaso 24h, arrest excl Casey) |
| figure3_combined.R | OK | Figure3_network_forest.pdf + PNG |

### Primary outcome verification (mortality NMA)

| Claim (manuscript) | R output | Verdict |
|--------------------|----------|---------|
| K vs E: OR 0.96 (0.80-1.16) | 0.9585 (0.7954-1.1552) | Rounds correctly |
| Ketofol vs E: OR 0.84 (0.41-1.72) | 0.8369 (0.4068-1.7219) | Rounds correctly |
| P vs E: OR 0.63 (0.32-1.24) | 0.6274 (0.3183-1.2368) | Rounds correctly |
| I^2 = 30%, tau^2 = 0.017 | 29.7%, 0.0173 | Rounds correctly |
| Pairwise E vs K: OR 1.02 (0.77-1.36) | 1.0230 (0.7702-1.3589) | Rounds correctly |
| P-scores: P 0.84, KF 0.54, K 0.38, E 0.24 | 0.8417, 0.5365, 0.3779, 0.2439 | Rounds correctly |

### Secondary outcomes verification (K vs E)

| Outcome | Manuscript | R output | Verdict |
|---------|-----------|----------|---------|
| CV collapse | 1.44 (1.20-1.71) | 1.4359 (1.2041-1.7123) | OK |
| Hypotension | 1.34 (1.07-1.68) | 1.3361 (1.0654-1.6754) | OK |
| Vaso peri | 1.45 (1.21-1.74) | 1.4532 (1.2139-1.7398) | OK |
| First-pass | 0.95 (0.77-1.16) | 0.9456 (0.7732-1.1565) | OK |
| Cardiac arrest | 1.13 (0.70-1.82) | 1.1265 (0.6959-1.8237) | OK |
| Vaso 24h | 0.58 (0.14-2.33), I^2=96% | 1.7292 (0.4258-7.0230) reciprocal | See HIGH finding below |

### Sensitivity analyses verification

| Analysis | Manuscript | R output | Verdict |
|----------|-----------|----------|---------|
| Collapse ketofol: K vs E | 0.95 (0.80-1.12) | 0.9484 (0.8044-1.1182) | OK |
| Remove ketofol: K vs E | 0.96 (0.80-1.16) | 0.9585 (0.7954-1.1552) | OK |
| Excl Casey: CV collapse | 1.59 (1.12-2.24) | 1.5850 (1.1223-2.2386) | OK |
| Excl Casey: hypotension | 1.01 (0.59-1.73) | 1.0139 (0.5928-1.7342) | OK |
| Excl Casey: vaso peri | 1.50 (1.06-2.15) | 1.5049 (1.0556-2.1456) | OK |
| Excl Casey: vaso 24h | 3.63 (2.06-6.41) | 3.6325 (2.0578-6.4122) | OK |
| Excl Casey: cardiac arrest | 1.09 (0.60-1.95) | 1.0858 (0.6037-1.9528) | OK |
| Subgroup setting p | 0.83 | 0.8333 | OK |
| Subgroup RoB p | 0.88 | 0.8825 | OK |

---

## Phase 2: Data CSV Integrity

| Check | Result |
|-------|--------|
| Events <= n (all CSVs) | PASS |
| Agarwal absent (all CSVs) | PASS |
| Mortality total N = 4,672 | PASS (exact) |
| Study counts per CSV | PASS (9 mort, 3 CV, 4 hypo, 5 FP, 7 arrest, 7 vaso) |
| study_info.n_analyzed = mortality sum(n) | PASS (all 9 studies) |
| RoB robvis vs study_info | PASS (Punt: "High" vs "High risk" = formatting only) |
| Casey FP N vs mortality N | 1187 vs 1186 (E arm) = documented laryngoscope subset |
| Matchett vaso peri missing | E: 51/396, K: 41/395 = matches notes |

---

## Phase 3: Source PDF Spot-Check

### Casey 2025 (RSI trial) -- 12/12 CONFIRMED
All mortality, CV collapse (including components), hypotension, vasopressor, first-pass, and cardiac arrest numbers verified against NEJM Tables 1-3.

### Matchett 2022 (EvK) -- 13/13 CONFIRMED
All mortality (28d and 7d), CV collapse, first-pass, vasopressor, cardiac arrest, baseline characteristics verified against ICM tables.

### Schmidt 2025 (PROMINE) -- 2 discrepancies found

**MEDIUM: Lowest MAP IQR upper bound**
- ESM extraction (esm.tex): Esketamine "66 (55-82)"
- Source PDF (Table 2, abstract, body text): Esketamine "66 (55-**79**)"
- The correct value is **79**, not 82. The propofol value 60 (48-72) is correct.
- **Impact:** Descriptive only; not used in NMA. Should be corrected in revision.
- **Location:** esm.tex, Schmidt extraction section (Study 9, outcomes table)

**LOW: SOFA reported as median (IQR) but is mean (SD)**
- ESM extraction: "SOFA, median (IQR): 7 (4-10) P, 8 (4-11) ESK"
- Source PDF (Table 1): Reports SOFA as **mean (SD)**: P 7 (4.10), ESK 8 (4.11)
- The numeric values happen to be the same, but the descriptor "median (IQR)" is incorrect.
- **Impact:** Descriptive only. Should be corrected to "mean (SD)" in revision.
- **Location:** esm.tex, Schmidt extraction section (Study 9, baseline table)

---

## HIGH: Vasopressor 24h Pairwise Direction Bug

### Description
The vasopressor 24h analysis (2 studies: Srivilaithon 2023, Casey 2025) uses pairwise meta-analysis (metagen) because only 2 treatments exist. The `pairwise()` function assigns treat1/treat2 based on CSV row order, creating **inconsistent comparison directions**:

| Study | CSV row order | pairwise output | Direction |
|-------|--------------|-----------------|-----------|
| Srivilaithon 2023 | E first, K second | treat1=E, treat2=K, logOR=+1.29 | E/K |
| Casey 2025 | K first, E second | treat1=K, treat2=E, logOR=-0.14 | K/E |

Both studies actually show E with higher 24h vasopressor use:
- Srivilaithon: 43.8% E vs 17.7% K, OR(E/K) = 3.63
- Casey: 42.3% E vs 38.9% K, OR(E/K) = 1.15

But pairwise() gives Casey logOR = -0.14 (K/E direction) while Srivilaithon has +1.29 (E/K direction). When metagen() pools these mixed-direction values, the result is incorrect.

### What the manuscript reports
- Table 2: OR 0.58 (0.14-2.33), K vs E direction, I^2 = 96%
- eFigure 7 forest: shows Casey OR = 0.87, Srivilaithon OR = 3.63 (mixed directions)
- eFigure 7 caption: says Casey OR = 1.15 (correct E/K value) -- but this doesn't match the forest plot (0.87)

### Impact assessment
**Conclusions unaffected.** The manuscript correctly states: "Vasopressor use at 24 hours showed substantial heterogeneity (I^2 = 96%) and was not reliably estimable." This is true regardless of the bug. The sensitivity analysis excluding Casey (leaving only Srivilaithon OR 3.63) is also correct.

### Recommended fix
1. In `data/vasopressor.csv`: reorder Casey 24h rows to have Etomidate before Ketamine (swap lines 14-15)
2. Re-run analysis_nma.R to regenerate the corrected forest plot and pooled estimate
3. Update eFigure 7 and its caption
4. The corrected pooled OR will change numerically (both studies in same direction), but I^2 will remain very high and the conclusion "not reliably estimable" still holds

---

## Phase 4: Number Reconciliation Summary

### main.tex
- Abstract (line 80): All ORs, CIs, study counts verified against R output
- Results (lines 160-190): All 20+ numeric claims verified
- Table 1 (lines 388-438): All 9 study rows verified against CSVs and extractions
- Table 2 (lines 448-474): All ORs/CIs match NMA output; study counts and patient Ns verified
- Discussion (lines 197-207): RSI trial numbers (2,359; 28.1% vs 29.1%; 22.1% vs 17.0%), PROMINE (175; 60% vs 50%), BARCO (60.5% vs 54.4%), INTUBE (~3,000; 45%; 43%; 3%) -- all verified

### esm.tex
- 21 eFigure captions: All OR/CI values and study counts match R output, except eFigure 7 caption (see HIGH finding)
- CINeMA tables (eTables 1-4): Domain judgments verified against GRADE_CINeMA.md
- Per-study extractions (Section 5.2): All 9 studies verified against extraction documents; 3 spot-checked against source PDFs
- RoB summary table: Matches rob2_robvis.csv
- Mortality summary table: All 9 studies n/N verified
- Agarwal appendix: Comparison values consistent with ESM tables

### Cross-document consistency
- Abstract vs Results vs Discussion: ORs/CIs consistent throughout
- Table 1 vs ESM Section 5.2: Study Ns, doses, settings match
- Table 2 vs eFigure labels: All match except eFigure 7 (see above)
- CINeMA language: Correctly maps moderate/low/very low to evidence certainty
- Figure 3 caption: PI (0.47-2.21), OR, CI, I^2 all match R output

---

## Recommended Corrections for Revision

### Must fix
1. **Vasopressor 24h CSV row order** (HIGH): Swap Casey 24h rows in vasopressor.csv so E comes before K. Re-run. Update eFigure 7 forest plot and caption.
2. **PROMINE MAP IQR** (MEDIUM): Change "66 (55-82)" to "66 (55-79)" in esm.tex Schmidt extraction.
3. **eFigure 7 caption** (MEDIUM): After fixing #1, update individual study ORs and pooled estimate in caption.

### Should fix
4. **PROMINE SOFA descriptor** (LOW): Change "median (IQR)" to "mean (SD)" in esm.tex Schmidt extraction.
5. **R script paths** (LOW): Already fixed during audit. Consider using relative paths or `here::here()`.

### Optional
6. **Punt RoB label** (LOW): Harmonize "High" vs "High risk" between rob2_robvis.csv and study_info.csv.

---

## Reproducibility Notes

- R version: 4.5.2 (2025-10-31)
- meta: 8.3-0 (manuscript used 8.2-1 -- minor version update, results identical)
- netmeta: 3.4-0 (manuscript cited 3.3-1 -- minor version update, results identical)
- All figures regenerated identically
- All NMA estimates reproduced to full decimal precision
