# Induction Agents for Emergency Tracheal Intubation in Critically Ill Adults: A Systematic Review and Network Meta-Analysis

[![PROSPERO](https://img.shields.io/badge/PROSPERO-CRD420251251225-blue)](https://www.crd.york.ac.uk/prospero/display_record.php?RecordID=1251225)

**Authors:** Fernando G. Zampieri, Raysa C. Schmidt, Bruno A.M.P. Besen, Fernando J.D.S. Ramos, Francois Lamontagne, Neill K.J. Adhikari, Flavio G.R. Freitas, Flavia R. Machado — for the PROMINE Investigators

**Published:** *Critical Care* 2026;30(1) — 12 May 2026. PMID 42121165, PMCID PMC13245039, DOI [10.1186/s13054-026-06067-w](https://doi.org/10.1186/s13054-026-06067-w). Open access. (Submitted March 2026; revision submitted 17 April 2026.)

## Summary

Systematic review and network meta-analysis of nine randomized controlled trials (4,672 patients) comparing etomidate, ketamine, propofol, and ketofol for emergency or rapid sequence intubation in critically ill adults. The primary outcome was short-term mortality.

### Key Findings

- **Ketamine vs etomidate mortality:** OR 0.96 (95% CI 0.80-1.16; I^2 = 30%; moderate certainty) - probably similar
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
data/                        Analysis-ready CSVs
  mortality.csv              Primary outcome (9 studies, arm-level events/n)
  cv_collapse.csv            Cardiovascular collapse composite (3 studies)
  hypotension.csv            Post-induction hypotension (4 studies)
  vasopressor.csv            Vasopressor use by timepoint (7 studies)
  first_pass.csv             First-pass intubation success (5 studies)
  cardiac_arrest.csv         Peri-intubation cardiac arrest (7 studies)
  study_info.csv             Trial-level metadata
  rob2_robvis.csv            Cochrane RoB 2 domain scores
extractions/                 Per-study data extraction forms (verified against source PDFs)
search/                      Search strategies (PubMed and Embase exports)
scripts/
  analysis_nma.R             Main NMA, pairwise MA, forest plots, league tables
  analysis_subgroups.R       Subgroup (setting, RoB) and sensitivity analyses
  analysis_sens_excl_casey.R Post-hoc sensitivity excluding Casey 2025
  figure3_combined.R         Figure 3 (network geometry + pairwise forest)
cinema/                      GRADE/CINeMA certainty-of-evidence assessments
protocol/                    PROSPERO-registered study protocol (PDF)
manuscript/
  overleaf/                  LaTeX source (main.tex, esm.tex) and figure PDFs
  figures/                   All R-generated figures (26+ PDFs)
  results/                   NMA summary CSV, league tables, node-splitting output
  word/                      Word manuscript and build script (build_docx.py)
revision/                    Reviewer responses, revised manuscript, audit report
```

Note: Source PDFs (`Included Papers/`) are excluded from the repository due to copyright. The per-study extraction forms in `extractions/` contain all data used in the analysis.

## Reproducibility

### Requirements

- **R** >= 4.5.0
- **R packages:** `meta`, `netmeta`, `ggplot2`, `dplyr`, `robvis`
  
Missing packages are installed automatically by `analysis_nma.R`.

### Running the Analysis

```bash
# From the repository root:
Rscript scripts/analysis_nma.R              # Main NMA + all forest plots + league tables
Rscript scripts/analysis_subgroups.R        # Subgroup and sensitivity analyses (mortality)
Rscript scripts/analysis_sens_excl_casey.R  # Post-hoc Casey exclusion (hemodynamics)
Rscript scripts/figure3_combined.R          # Publication Figure 3 (network + forest)
```

### Input/Output

| Input | Location |
|-------|----------|
| Outcome data | `data/*.csv` |
| RoB scores | `data/rob2_robvis.csv` |
| Study metadata | `data/study_info.csv` |

| Output | Location |
|--------|----------|
| Forest plots, funnel plot, RoB figures | `manuscript/figures/` |
| NMA summary table | `manuscript/results/nma_results_summary.csv` |
| League tables | `manuscript/results/league_table_*.csv` |
| Node-splitting | `manuscript/results/netsplit_mortality.txt` |
| Figure 3 (publication) | `manuscript/figures/Figure3_network_forest.pdf` |

### Verification

A full numerical audit was performed on 2026-04-15:
- All extracted data verified against source PDFs (3 load-bearing trials spot-checked in full)
- All R scripts re-run from clean state; outputs match manuscript
- Every OR, CI, I^2, and p-value in the manuscript traced to R output

See `revision/audit_report.md` for the complete audit findings.

## Citation

> Zampieri FG, Schmidt RC, Besen BAMP, Ramos FJDS, Lamontagne F, Adhikari NKJ, Freitas FGR, Machado FR, for the PROMINE Investigators. Induction agents for emergency tracheal intubation in critically ill adults: a systematic review and network meta-analysis. *Crit Care*. 2026;30(1). doi:10.1186/s13054-026-06067-w. PMID 42121165.

## Related Publications

- **PROMINE trial:** Schmidt RC, Zampieri FG, Ramos FJDS, et al. Propofol versus esketamine for rapid sequence intubation of critically ill patients (PROMINE): a randomized clinical trial. *Intensive Care Med*. 2026. [doi:10.1007/s00134-026-08351-3](https://doi.org/10.1007/s00134-026-08351-3)
- **RSI trial:** Casey JD, Seitz KP, Driver BE, et al. Ketamine or etomidate for tracheal intubation of critically ill adults. *N Engl J Med*. 2025. [doi:10.1056/NEJMoa2511420](https://doi.org/10.1056/NEJMoa2511420)

## License

This repository contains the analysis code and data supporting the manuscript. Code is available under the [MIT License](LICENSE). The manuscript text and figures are copyright of the authors.
