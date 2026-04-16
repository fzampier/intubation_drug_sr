# Induction Agents for Emergency Tracheal Intubation in Critically Ill Adults: A Systematic Review and Network Meta-Analysis

**Authors:** Fernando G. Zampieri, Raysa C. Schmidt, Bruno A.M.P. Besen, Fernando J.D.S. Ramos, Francois Lamontagne, Neill K.J. Adhikari, Flavio G.R. Freitas, Flavia R. Machado — for the PROMINE Investigators

**PROSPERO:** [CRD420251251225](https://www.crd.york.ac.uk/prospero/display_record.php?RecordID=1251225)

**Status:** Submitted to *Critical Care* (March 2026); minor revision in progress

## Summary

Systematic review and network meta-analysis of nine randomized controlled trials (4,672 patients) comparing etomidate, ketamine, propofol, and ketofol for emergency or rapid sequence intubation in critically ill adults. The primary outcome was short-term mortality.

### Key findings

- **Ketamine vs etomidate mortality:** OR 0.96 (95% CI 0.80–1.16; I² = 30%; moderate certainty) — probably similar
- **Hemodynamic instability:** Ketamine probably increases cardiovascular collapse (OR 1.44), post-induction hypotension (OR 1.34), and peri-intubation vasopressor use (OR 1.45) compared with etomidate
- **Propofol:** Single trial (PROMINE); evidence insufficient to guide practice
- **Ketofol:** Single trial (KEEP PACE); limited generalizability

## Included Trials

| Study | Year | N | Comparison | Setting |
|-------|------|---|-----------|---------|
| Jabre (KETASED) | 2009 | 469 | E vs K | Mixed |
| Cinar | 2011 | 22 | E vs K | ICU |
| Punt | 2014 | 301 | E vs SK | ICU |
| Smischney (KEEP PACE) | 2019 | 152 | E vs KF | ICU |
| Matchett (EvK) | 2022 | 791 | E vs K | ICU |
| Knack | 2023 | 143 | E vs K | ED |
| Srivilaithon | 2023 | 260 | E vs K | ED |
| Casey (RSI) | 2025 | 2,359 | E vs K | Mixed |
| Schmidt (PROMINE) | 2025 | 175 | P vs ESK | ICU |

E = etomidate; K = ketamine; SK = S-ketamine; ESK = esketamine; P = propofol; KF = ketofol

## Repository Structure

```
data/                   Analysis-ready CSVs (9 outcome files + study metadata + RoB)
extractions/            Per-study data extraction forms (verified against source PDFs)
Included Papers/        Source PDFs for all included and excluded studies
search/                 Search strategies (PubMed and Embase exports)
scripts/
  analysis_nma.R        Main NMA, pairwise MA, forest plots, league tables
  analysis_subgroups.R  Subgroup (setting, RoB) and sensitivity analyses (mortality)
  analysis_sens_excl_casey.R  Post-hoc sensitivity excluding Casey 2025 (hemodynamics)
  figure3_combined.R    Figure 3 (network geometry + pairwise E vs K forest)
cinema/                 GRADE/CINeMA certainty-of-evidence assessments
manuscript/
  overleaf/             LaTeX source (main.tex, esm.tex) and figure PDFs for Overleaf
  figures/              All R-generated figures (26 PDFs)
  results/              NMA summary CSV, league tables, node-splitting output
  word/                 Submission-ready Word manuscript and build script
protocol/               PROSPERO-registered study protocol
revision/               Reviewer comments, audit report, revision materials
```

## Reproducibility

All analyses were performed in R (version 4.5.2) using `netmeta` (3.4-0) and `meta` (8.3-0).

```bash
# From the repository root:
Rscript scripts/analysis_nma.R            # Main NMA + all forest plots
Rscript scripts/analysis_subgroups.R      # Subgroup and sensitivity analyses
Rscript scripts/analysis_sens_excl_casey.R # Post-hoc Casey exclusion sensitivity
Rscript scripts/figure3_combined.R        # Publication Figure 3
```

Input data: `data/`. Output figures: `manuscript/figures/`. Output tables: `manuscript/results/`.

A full numerical audit was performed on 2026-04-15 verifying all extracted data against source PDFs and all manuscript numbers against R outputs (see `revision/audit_report.md`).

## License

This repository contains the analysis code and data supporting the manuscript. The manuscript text and figures are copyright of the authors.
