###############################################################################
# Subgroup & Additional Sensitivity Analyses — Mortality (Primary Outcome)
# Supplement to analysis_nma.R
###############################################################################

projdir <- "/Users/fernandogodinhozampieri/Desktop/intubation_sr"
setwd(projdir)

library(meta)
library(netmeta)
library(dplyr)

dir.create("manuscript/figures", showWarnings = FALSE, recursive = TRUE)

mort <- read.csv("data/mortality.csv", stringsAsFactors = FALSE)
info <- read.csv("data/study_info.csv", stringsAsFactors = FALSE)

# Merge setting and RoB into mortality data
mort <- mort %>%
  left_join(info %>% select(study, setting, rob_overall),
            by = c("study" = "study"))

# Use setting.x / .y if collision — handle cleanly
if ("setting.x" %in% names(mort)) {
  mort <- mort %>% rename(setting_orig = setting.x, setting = setting.y)
}

cat("============================================================\n")
cat("  SUBGROUP & SENSITIVITY ANALYSES — MORTALITY\n")
cat("============================================================\n\n")

###############################################################################
#  1. SUBGROUP BY SETTING (ED vs ICU vs Mixed)
###############################################################################

cat("--- 1. SUBGROUP BY SETTING ---\n\n")

# Classify: ED, ICU, Mixed
cat("Study settings:\n")
mort %>% distinct(study, setting) %>% print()

# 1a. Pairwise E vs K — subgroup by setting
#     (Only E-K comparison is available across all settings)
pw_mort <- pairwise(treat = treat, event = events, n = n,
                    studlab = study, data = mort, sm = "OR")

pw_ek <- pw_mort %>%
  filter((treat1 == "Etomidate" & treat2 == "Ketamine") |
         (treat1 == "Ketamine" & treat2 == "Etomidate"))

# Add setting to pairwise data (use lookup, avoid column collision)
setting_lookup <- info %>% select(study, setting) %>% rename(studlab = study)
rob_lookup     <- info %>% select(study, rob_overall) %>% rename(studlab = study)

pw_ek$setting     <- setting_lookup$setting[match(pw_ek$studlab, setting_lookup$studlab)]
pw_ek$rob_overall <- rob_lookup$rob_overall[match(pw_ek$studlab, rob_lookup$studlab)]

ma_ek_setting <- metagen(TE, seTE, studlab = studlab, data = pw_ek,
                         sm = "OR", common = FALSE, random = TRUE,
                         method.tau = "PM",
                         subgroup = setting,
                         test.subgroup = TRUE)

cat("\nPairwise E vs K — Subgroup by Setting:\n")
summary(ma_ek_setting)

pdf("manuscript/figures/forest_mortality_subgroup_setting.pdf", width = 11, height = 7)
forest(ma_ek_setting,
       subgroup = TRUE,
       test.subgroup = TRUE,
       prediction = FALSE,
       label.left  = "Favours Etomidate",
       label.right = "Favours Ketamine",
       smlab = "Etomidate vs Ketamine\nMortality by Setting",
       sortvar = TE)
dev.off()

# 1b. NMA within ICU subgroup (has connected network: E-K, E-Ketofol, K-P)
cat("\n--- 1b. NMA within ICU subgroup ---\n")
mort_icu <- mort %>% filter(setting == "ICU")
cat("ICU studies: ", paste(unique(mort_icu$study), collapse = ", "), "\n")

pw_icu <- pairwise(treat = treat, event = events, n = n,
                   studlab = study, data = mort_icu, sm = "OR")

nma_icu <- tryCatch(
  netmeta(TE, seTE, treat1, treat2, studlab,
          data = pw_icu, sm = "OR",
          common = FALSE, random = TRUE,
          reference.group = "Etomidate"),
  error = function(e) { cat("  NMA failed:", e$message, "\n"); NULL })

if (!is.null(nma_icu)) {
  summary(nma_icu)
  cat("\nP-scores (ICU):\n")
  print(netrank(nma_icu, small.values = "desirable"))

  pdf("manuscript/figures/forest_mortality_subgroup_ICU_nma.pdf", width = 10, height = 5)
  forest(nma_icu, reference.group = "Etomidate", sortvar = TE,
         smlab = "Mortality — ICU Subgroup\nOR (95% CI)")
  dev.off()
}

###############################################################################
#  2. SUBGROUP BY RISK OF BIAS
###############################################################################

cat("\n--- 2. SUBGROUP BY RISK OF BIAS ---\n\n")

# Only 1 study is High risk (Dormans), rest are Some concerns.
# Still present the formal subgroup test.
# (rob_overall already added via lookup above)

ma_ek_rob <- metagen(TE, seTE, studlab = studlab, data = pw_ek,
                     sm = "OR", common = FALSE, random = TRUE,
                     method.tau = "PM",
                     subgroup = rob_overall,
                     test.subgroup = TRUE)

cat("Pairwise E vs K — Subgroup by RoB:\n")
summary(ma_ek_rob)

pdf("manuscript/figures/forest_mortality_subgroup_rob.pdf", width = 11, height = 7)
forest(ma_ek_rob,
       subgroup = TRUE,
       test.subgroup = TRUE,
       prediction = FALSE,
       label.left  = "Favours Etomidate",
       label.right = "Favours Ketamine",
       smlab = "Etomidate vs Ketamine\nMortality by Risk of Bias")
dev.off()

###############################################################################
#  3. SUBGROUP BY BASELINE VASOPRESSOR USE
###############################################################################

cat("\n--- 3. SUBGROUP BY BASELINE VASOPRESSOR USE ---\n")
cat("Only 3 of 10 studies report explicit baseline vasopressor %\n")
cat("(Smischney 2019: ~25%, Casey 2025: ~22%, Schmidt 2025: ~35%)\n")
cat("Subgroup analysis NOT FEASIBLE — insufficient data.\n")
cat("This limitation will be reported in the manuscript.\n\n")

###############################################################################
#  4. SENSITIVITY: COLLAPSE KETOFOL INTO KETAMINE
###############################################################################

cat("--- 4a. SENSITIVITY: Collapse Ketofol → Ketamine ---\n\n")

mort_collapse <- mort %>%
  mutate(treat = ifelse(treat == "Ketofol", "Ketamine", treat))

pw_collapse <- pairwise(treat = treat, event = events, n = n,
                        studlab = study, data = mort_collapse, sm = "OR")

nma_collapse <- netmeta(TE, seTE, treat1, treat2, studlab,
                        data = pw_collapse, sm = "OR",
                        common = FALSE, random = TRUE,
                        reference.group = "Etomidate")

cat("NMA with Ketofol collapsed into Ketamine (3 treatments):\n")
summary(nma_collapse)
cat("\nP-scores:\n")
print(netrank(nma_collapse, small.values = "desirable"))

pdf("manuscript/figures/forest_mortality_sens_collapse_ketofol.pdf", width = 10, height = 5)
forest(nma_collapse, reference.group = "Etomidate", sortvar = TE,
       smlab = "Sensitivity: Ketofol collapsed into Ketamine\nOR (95% CI)")
dev.off()

###############################################################################
#  5. SENSITIVITY: REMOVE KETOFOL NODE ENTIRELY
###############################################################################

cat("\n--- 4b. SENSITIVITY: Remove Ketofol node ---\n\n")

mort_no_ketofol <- mort %>% filter(treat != "Ketofol")
# Also remove the study that only has Ketofol (Smischney)
mort_no_ketofol <- mort_no_ketofol %>%
  group_by(study) %>%
  filter(n() == 2) %>%
  ungroup()

pw_no_ketofol <- pairwise(treat = treat, event = events, n = n,
                          studlab = study, data = mort_no_ketofol, sm = "OR")

nma_no_ketofol <- netmeta(TE, seTE, treat1, treat2, studlab,
                          data = pw_no_ketofol, sm = "OR",
                          common = FALSE, random = TRUE,
                          reference.group = "Etomidate")

cat("NMA without Ketofol (Smischney excluded; 3 treatments, 9 studies):\n")
summary(nma_no_ketofol)
cat("\nP-scores:\n")
print(netrank(nma_no_ketofol, small.values = "desirable"))

pdf("manuscript/figures/forest_mortality_sens_remove_ketofol.pdf", width = 10, height = 5)
forest(nma_no_ketofol, reference.group = "Etomidate", sortvar = TE,
       smlab = "Sensitivity: Ketofol removed\nOR (95% CI)")
dev.off()

###############################################################################
#  SUMMARY
###############################################################################

cat("\n============================================================\n")
cat("  SUBGROUP & SENSITIVITY ANALYSES COMPLETE\n")
cat("============================================================\n\n")
cat("Figures saved:\n")
cat("  - forest_mortality_subgroup_setting.pdf\n")
cat("  - forest_mortality_subgroup_ICU_nma.pdf\n")
cat("  - forest_mortality_subgroup_rob.pdf\n")
cat("  - forest_mortality_sens_collapse_ketofol.pdf\n")
cat("  - forest_mortality_sens_remove_ketofol.pdf\n")
