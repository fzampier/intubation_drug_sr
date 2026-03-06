# Induction Agents for Emergency Tracheal Intubation in Critically Ill Adults: A Systematic Review and Network Meta-Analysis

**Authors:** Fernando G. Zampieri, Raysa C. Schmidt, Bruno A.M.P. Besen, Fernando J.D.S. Ramos, Francois Lamontagne, Neill K.J. Adhikari, Flavio G.R. Freitas, Flavia R. Machado — for the PROMINE Investigators

**PROSPERO:** [CRD420251251225](https://www.crd.york.ac.uk/prospero/display_record.php?RecordID=1251225)

## Summary

Systematic review and network meta-analysis of nine randomized controlled trials (4,672 patients) comparing etomidate, ketamine, propofol, and ketofol for emergency or rapid sequence intubation in critically ill adults. The primary outcome was short-term mortality.

## Repository Structure

```
data/                   Analysis-ready CSVs (mortality, hemodynamic outcomes, RoB, study characteristics)
extractions/            Per-study data extraction forms
search/                 Search strategies (PubMed and Embase)
scripts/                R analysis scripts
  analysis_nma.R        Main NMA and figure generation
  analysis_subgroups.R  Subgroup and sensitivity analyses
  analysis_sens_excl_casey.R  Post-hoc sensitivity excluding Casey 2025
  figure3_combined.R    Figure 3 (network plot + forest plot)
cinema/                 GRADE/CINeMA certainty-of-evidence assessment
manuscript/
  results/              NMA league tables, node-splitting, summary CSVs
  figures/              R-generated figures (PDFs)
  overleaf/             LaTeX source and eFigures for Overleaf
  word/                 Word manuscript, standalone figures, build script
  cover_letter.md       Cover letter
Protocol.pdf            Study protocol
```

## Reproducibility

All analyses were performed in R (version 4.5.2) using the `netmeta` (3.3-1) and `meta` (8.2-1) packages. To reproduce:

1. Open R in the repository root
2. Run `scripts/analysis_nma.R` for the main NMA and figures
3. Run `scripts/analysis_subgroups.R` for subgroup and sensitivity analyses
4. Run `scripts/analysis_sens_excl_casey.R` for the post-hoc Casey sensitivity analysis
5. Run `scripts/figure3_combined.R` for Figure 3

All input data are in `data/`. Figures are written to `manuscript/figures/`.

## License

This repository contains the analysis code and data supporting the manuscript. The manuscript text and figures are copyright of the authors.
