###############################################################################
# Induction Agents for RSI in Critically Ill Adults
# Systematic Review & Network Meta-Analysis
# PROSPERO: CRD420251251225
#
# Authors: Zampieri FG, Schmidt RC, Besen BAMP, Ramos FJDS,
#          Freitas FGR, Machado FR — for the PROMINE Investigators
#
# Packages: meta, netmeta, robvis, ggplot2, dplyr
###############################################################################

# --- 0. SETUP ---------------------------------------------------------------

projdir <- "/Users/fernandogodinhozampieri/Desktop/intubation_sr"
setwd(projdir)

# Install missing packages
required <- c("meta", "netmeta", "ggplot2", "dplyr", "robvis")
missing  <- required[!required %in% installed.packages()[, "Package"]]
if (length(missing)) install.packages(missing, repos = "https://cran.r-project.org")

library(meta)
library(netmeta)
library(ggplot2)
library(dplyr)

has_robvis <- requireNamespace("robvis", quietly = TRUE)
if (has_robvis) library(robvis)

dir.create("manuscript/figures", showWarnings = FALSE, recursive = TRUE)

cat("=== Setup complete ===\n\n")

# --- 1. RISK OF BIAS FIGURES ------------------------------------------------

if (has_robvis) {
  rob <- read.csv("data/rob2_robvis.csv", stringsAsFactors = FALSE)

  p_tl <- rob_traffic_light(rob, tool = "ROB2", psize = 10) +
    theme(axis.text.y = element_text(angle = 0, hjust = 1, size = 10))
  pdf("manuscript/figures/rob2_traffic_light.pdf", width = 14, height = 6)
  print(p_tl)
  dev.off()

  pdf("manuscript/figures/rob2_summary.pdf", width = 8, height = 4)
  print(rob_summary(rob, tool = "ROB2"))
  dev.off()

  cat(">> RoB 2 figures saved\n\n")
} else {
  cat("!! robvis not available — skipping RoB figures. Install with:\n")
  cat("   install.packages('robvis')\n\n")
}

# --- 2. LOAD DATA -----------------------------------------------------------

mort   <- read.csv("data/mortality.csv",      stringsAsFactors = FALSE)
cv     <- read.csv("data/cv_collapse.csv",    stringsAsFactors = FALSE)
hypo   <- read.csv("data/hypotension.csv",    stringsAsFactors = FALSE)
fp     <- read.csv("data/first_pass.csv",     stringsAsFactors = FALSE)
arrest <- read.csv("data/cardiac_arrest.csv",  stringsAsFactors = FALSE)
vaso   <- read.csv("data/vasopressor.csv",    stringsAsFactors = FALSE)

cat(">> Data loaded\n\n")

###############################################################################
#                    3. PRIMARY OUTCOME — MORTALITY NMA                       #
###############################################################################

cat("============================================================\n")
cat("  PRIMARY OUTCOME: SHORT-TERM MORTALITY (NMA)\n")
cat("============================================================\n\n")

# 3a. Pairwise contrasts (arm-level → log OR + SE)
pw_mort <- pairwise(treat = treat, event = events, n = n,
                    studlab = study, data = mort, sm = "OR")

# 3b. Fit random-effects NMA
nma_mort <- netmeta(TE, seTE, treat1, treat2, studlab,
                    data = pw_mort, sm = "OR",
                    common = FALSE, random = TRUE,
                    reference.group = "Etomidate")

summary(nma_mort)

# 3c. Network geometry plot
pdf("manuscript/figures/network_mortality.pdf", width = 7, height = 7)
netgraph(nma_mort,
         plastic = FALSE,
         thickness = "number.of.studies",
         number.of.studies = TRUE,
         points = TRUE, cex.points = 3,
         col = "darkblue")
dev.off()

# 3d. Forest plot — all treatments vs Etomidate (NMA)
pdf("manuscript/figures/forest_mortality_nma.pdf", width = 10, height = 5)
forest(nma_mort,
       reference.group = "Etomidate",
       sortvar = TE,
       label.left  = "Favours treatment",
       label.right = "Favours Etomidate",
       smlab = "Mortality\nOR (95% CI)")
dev.off()

# 3e. League table
league_mort <- netleague(nma_mort, digits = 2, bracket = "(", separator = " to ")
write.csv(as.data.frame(league_mort$random),
          "manuscript/league_table_mortality.csv", row.names = TRUE)

# 3f. P-scores (lower mortality = better)
cat("\n--- P-scores (mortality) ---\n")
rank_mort <- netrank(nma_mort, small.values = "desirable")
print(rank_mort)

# 3g. Node-splitting consistency test
cat("\n--- Node-splitting (consistency) ---\n")
split_mort <- netsplit(nma_mort)
print(split_mort)

# Save node-splitting results
sink("manuscript/netsplit_mortality.txt")
print(split_mort)
sink()

# 3h. Funnel plot (comparison-adjusted)
pdf("manuscript/figures/funnel_mortality.pdf", width = 8, height = 6)
funnel(nma_mort, order = c("Etomidate", "Ketamine", "Ketofol", "Propofol"),
       pch = 16, col = "darkblue",
       legend = TRUE)
dev.off()

cat("\n>> Mortality NMA complete\n\n")

###############################################################################
#     4. DIRECT PAIRWISE MA — ETOMIDATE vs KETAMINE (MORTALITY)              #
###############################################################################

cat("============================================================\n")
cat("  PAIRWISE: ETOMIDATE vs KETAMINE (MORTALITY)\n")
cat("============================================================\n\n")

pw_ek <- pw_mort %>% filter(treat1 == "Etomidate" & treat2 == "Ketamine" |
                            treat1 == "Ketamine"  & treat2 == "Etomidate")

ma_ek <- metagen(TE, seTE, studlab = studlab, data = pw_ek,
                 sm = "OR", common = FALSE, random = TRUE,
                 method.tau = "PM")
summary(ma_ek)

pdf("manuscript/figures/forest_mortality_pairwise_EvsK.pdf", width = 10, height = 6)
forest(ma_ek,
       label.left  = "Favours Etomidate",
       label.right = "Favours Ketamine",
       smlab = "Etomidate vs Ketamine\nMortality — OR (95% CI)",
       prediction = TRUE,
       sortvar = TE)
dev.off()

cat(">> Pairwise E vs K complete\n\n")

###############################################################################
#              5. SENSITIVITY ANALYSES (MORTALITY)                            #
###############################################################################

cat("============================================================\n")
cat("  SENSITIVITY ANALYSES (MORTALITY)\n")
cat("============================================================\n\n")

run_sensitivity <- function(data, label) {
  pw <- pairwise(treat = treat, event = events, n = n,
                 studlab = study, data = data, sm = "OR")
  nma <- tryCatch(
    netmeta(TE, seTE, treat1, treat2, studlab,
            data = pw, sm = "OR",
            common = FALSE, random = TRUE,
            reference.group = "Etomidate"),
    error = function(e) {
      cat(paste0("  !! NMA failed for ", label, ": ", e$message, "\n"))
      NULL
    })
  if (!is.null(nma)) {
    cat(paste0("\n--- ", label, " ---\n"))
    print(summary(nma))
    cat("\nP-scores:\n")
    print(netrank(nma, small.values = "desirable"))
  }
  return(nma)
}

# 5a. Exclude midazolam adjunct studies (Cinar 2011 + Dormans 2014)
cat("--- Sensitivity 1: Excluding midazolam adjunct studies ---\n")
mort_s1 <- mort %>% filter(is.na(sensitivity_flag) | sensitivity_flag == "")
nma_s1  <- run_sensitivity(mort_s1, "No midazolam adjunct (8 studies)")

pdf("manuscript/figures/forest_mortality_sens1_no_midaz.pdf", width = 10, height = 5)
if (!is.null(nma_s1)) {
  forest(nma_s1, reference.group = "Etomidate", sortvar = TE,
         smlab = "Sensitivity: Excl. midazolam adjunct\nOR (95% CI)")
}
dev.off()

# 5b. Exclude high risk of bias (Dormans 2014)
cat("--- Sensitivity 2: Excluding high RoB ---\n")
mort_s2 <- mort %>% filter(rob_overall != "High risk")
nma_s2  <- run_sensitivity(mort_s2, "Excluding high RoB (9 studies)")

pdf("manuscript/figures/forest_mortality_sens2_no_high_rob.pdf", width = 10, height = 5)
if (!is.null(nma_s2)) {
  forest(nma_s2, reference.group = "Etomidate", sortvar = TE,
         smlab = "Sensitivity: Excl. high RoB\nOR (95% CI)")
}
dev.off()

# 5c. Exclude small studies (<30 per arm)
cat("--- Sensitivity 3: Excluding small studies ---\n")
mort_s3 <- mort %>% group_by(study) %>% filter(all(n >= 30)) %>% ungroup()
nma_s3  <- run_sensitivity(mort_s3, "Excluding small studies (8 studies)")

pdf("manuscript/figures/forest_mortality_sens3_no_small.pdf", width = 10, height = 5)
if (!is.null(nma_s3)) {
  forest(nma_s3, reference.group = "Etomidate", sortvar = TE,
         smlab = "Sensitivity: Excl. <30/arm\nOR (95% CI)")
}
dev.off()

cat("\n>> Sensitivity analyses complete\n\n")

###############################################################################
#                   6. SECONDARY OUTCOMES                                     #
###############################################################################

cat("============================================================\n")
cat("  SECONDARY OUTCOMES\n")
cat("============================================================\n\n")

# Helper: run NMA if network is connected, else pairwise MA
run_outcome <- function(data, label, ref = "Etomidate",
                        small.values = "desirable") {
  cat(paste0("\n--- ", label, " ---\n"))
  cat(paste0("  Studies: ", length(unique(data$study)),
             " | Treatments: ", paste(sort(unique(data$treat)), collapse = ", "), "\n"))

  pw <- pairwise(treat = treat, event = events, n = n,
                 studlab = study, data = data, sm = "OR")

  treats <- unique(c(pw$treat1, pw$treat2))
  if (length(treats) < 3) {
    # Only 2 treatments → standard pairwise MA
    cat("  -> 2 treatments only: running pairwise meta-analysis\n")
    ma <- metagen(TE, seTE, studlab = studlab, data = pw,
                  sm = "OR", common = FALSE, random = TRUE,
                  method.tau = "PM")
    print(summary(ma))
    return(list(type = "pairwise", result = ma))
  }

  # ≥ 3 treatments → attempt NMA
  nma <- tryCatch(
    netmeta(TE, seTE, treat1, treat2, studlab,
            data = pw, sm = "OR",
            common = FALSE, random = TRUE,
            reference.group = ref),
    error = function(e) {
      cat(paste0("  !! NMA failed: ", e$message, "\n"))
      NULL
    })

  if (!is.null(nma)) {
    cat("  -> NMA fit OK\n")
    print(summary(nma))
    cat("\n  P-scores:\n")
    print(netrank(nma, small.values = small.values))
    return(list(type = "nma", result = nma))
  } else {
    cat("  -> Falling back to pairwise MA\n")
    ma <- metagen(TE, seTE, studlab = studlab, data = pw,
                  sm = "OR", common = FALSE, random = TRUE)
    print(summary(ma))
    return(list(type = "pairwise", result = ma))
  }
}

# 6a. Cardiovascular collapse
res_cv <- run_outcome(cv, "Cardiovascular Collapse")

# 6b. Hypotension
res_hypo <- run_outcome(hypo, "Post-induction Hypotension")

# 6c. First-pass intubation success (higher = better)
res_fp <- run_outcome(fp, "First-Pass Intubation Success",
                      small.values = "undesirable")

# 6d. Cardiac arrest
res_arrest <- run_outcome(arrest, "Peri-intubation Cardiac Arrest")

# 6e. Vasopressor use — by timepoint
res_vaso <- list()
for (tp in sort(unique(vaso$timepoint_category))) {
  dat_tp <- vaso %>% filter(timepoint_category == tp)
  res_vaso[[tp]] <- run_outcome(dat_tp, paste0("Vasopressor — ", tp))
}

cat("\n>> Secondary outcomes complete\n\n")

###############################################################################
#                   7. FOREST PLOTS — SECONDARY OUTCOMES                      #
###############################################################################

save_forest_secondary <- function(res, filename, label) {
  pdf(paste0("manuscript/figures/", filename), width = 10, height = 6)
  obj <- res$result
  if (res$type == "nma") {
    forest(obj, reference.group = "Etomidate", sortvar = TE,
           smlab = paste0(label, "\nOR (95% CI)"))
  } else {
    forest(obj, smlab = paste0(label, "\nOR (95% CI)"),
           prediction = TRUE)
  }
  dev.off()
}

save_forest_secondary(res_cv,     "forest_cv_collapse.pdf",
                      "Cardiovascular Collapse")
save_forest_secondary(res_hypo,   "forest_hypotension.pdf",
                      "Post-induction Hypotension")
save_forest_secondary(res_fp,     "forest_first_pass.pdf",
                      "First-Pass Intubation Success")
save_forest_secondary(res_arrest, "forest_cardiac_arrest.pdf",
                      "Cardiac Arrest")

for (tp in names(res_vaso)) {
  fn <- paste0("forest_vasopressor_", gsub(" ", "_", tolower(tp)), ".pdf")
  save_forest_secondary(res_vaso[[tp]], fn, paste0("Vasopressor — ", tp))
}

cat(">> Forest plots saved\n\n")

###############################################################################
#                   8. SUMMARY RESULTS TABLE                                  #
###############################################################################

extract_nma_results <- function(nma_obj, outcome, ref = "Etomidate") {
  if (is.null(nma_obj) || !inherits(nma_obj, "netmeta")) return(NULL)
  treats <- nma_obj$trts[nma_obj$trts != ref]
  do.call(rbind, lapply(treats, function(t) {
    # TE.random[t, ref] = log OR for treatment t vs reference
    data.frame(
      Outcome    = outcome,
      Comparison = paste(t, "vs", ref),
      OR         = round(exp(nma_obj$TE.random[t, ref]), 2),
      CI_lower   = round(exp(nma_obj$lower.random[t, ref]), 2),
      CI_upper   = round(exp(nma_obj$upper.random[t, ref]), 2),
      pval       = round(nma_obj$pval.random[t, ref], 3),
      stringsAsFactors = FALSE)
  }))
}

results <- bind_rows(
  extract_nma_results(nma_mort, "Mortality"),
  if (res_cv$type == "nma")     extract_nma_results(res_cv$result, "CV Collapse"),
  if (res_hypo$type == "nma")   extract_nma_results(res_hypo$result, "Hypotension"),
  if (res_fp$type == "nma")     extract_nma_results(res_fp$result, "First-Pass Success"),
  if (res_arrest$type == "nma") extract_nma_results(res_arrest$result, "Cardiac Arrest")
)

if (!is.null(results) && nrow(results) > 0) {
  cat("\n--- NMA Summary Table ---\n")
  print(results)
  write.csv(results, "manuscript/nma_results_summary.csv", row.names = FALSE)
}

cat("\n>> Summary table saved\n\n")

###############################################################################
#                   9. LEAGUE TABLE (ALL OUTCOMES)                            #
###############################################################################

# Mortality league table already saved above.
# Save league tables for secondary NMAs where available.

save_league <- function(nma_obj, filename) {
  if (is.null(nma_obj) || !inherits(nma_obj, "netmeta")) return()
  lt <- netleague(nma_obj, digits = 2, bracket = "(", separator = " to ")
  write.csv(as.data.frame(lt$random), filename, row.names = TRUE)
}

if (res_cv$type == "nma")
  save_league(res_cv$result, "manuscript/league_table_cv_collapse.csv")
if (res_fp$type == "nma")
  save_league(res_fp$result, "manuscript/league_table_first_pass.csv")
if (res_arrest$type == "nma")
  save_league(res_arrest$result, "manuscript/league_table_cardiac_arrest.csv")

###############################################################################
#                   10. SESSION INFO                                          #
###############################################################################

cat("\n============================================================\n")
cat("  ALL ANALYSES COMPLETE\n")
cat("============================================================\n")
cat("Figures saved to: manuscript/figures/\n")
cat("Tables saved to:  manuscript/\n\n")

sessionInfo()
