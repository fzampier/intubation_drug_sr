###############################################################################
# Sensitivity Analysis: Excluding Casey 2025 (RSI trial)
# Hemodynamic outcomes only
# Requested by F. Lamontagne — coauthor review
###############################################################################

projdir <- "/Users/fernandogodinhozampieri/Desktop/intubation_sr"
setwd(projdir)

library(meta)
library(netmeta)
library(dplyr)

dir.create("manuscript/figures", showWarnings = FALSE, recursive = TRUE)

# --- Load data ---
cv     <- read.csv("data/cv_collapse.csv",   stringsAsFactors = FALSE)
hypo   <- read.csv("data/hypotension.csv",   stringsAsFactors = FALSE)
arrest <- read.csv("data/cardiac_arrest.csv", stringsAsFactors = FALSE)
vaso   <- read.csv("data/vasopressor.csv",    stringsAsFactors = FALSE)

# Helper: run NMA or pairwise depending on network connectivity
run_analysis <- function(data, label, ref = "Etomidate",
                         small.values = "desirable") {
  cat(paste0("\n=== ", label, " ===\n"))
  cat(paste0("  Studies: ", paste(unique(data$study), collapse = ", "), "\n"))
  cat(paste0("  Treatments: ", paste(sort(unique(data$treat)), collapse = ", "), "\n"))

  pw <- pairwise(treat = treat, event = events, n = n,
                 studlab = study, data = data, sm = "OR")

  treats <- unique(c(pw$treat1, pw$treat2))

  if (length(treats) < 3) {
    cat("  -> 2 treatments: pairwise meta-analysis\n")
    ma <- metagen(TE, seTE, studlab = studlab, data = pw,
                  sm = "OR", common = FALSE, random = TRUE,
                  method.tau = "PM")
    print(summary(ma))
    return(list(type = "pairwise", result = ma))
  }

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
    cat("  -> Fallback to pairwise\n")
    ma <- metagen(TE, seTE, studlab = studlab, data = pw,
                  sm = "OR", common = FALSE, random = TRUE,
                  method.tau = "PM")
    print(summary(ma))
    return(list(type = "pairwise", result = ma))
  }
}

# Helper: save forest plot
save_forest <- function(res, filename, label) {
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

cat("============================================================\n")
cat("  SENSITIVITY: EXCLUDING CASEY 2025 (RSI TRIAL)\n")
cat("  Hemodynamic outcomes\n")
cat("============================================================\n")

# --- 1. CV Collapse (excl Casey) ---
cv_nc <- cv %>% filter(study != "Casey 2025")
res_cv_nc <- run_analysis(cv_nc, "CV Collapse — excl. Casey")
save_forest(res_cv_nc, "forest_sens_excl_casey_cv_collapse.pdf",
            "Sens: CV Collapse excl. Casey")

# --- 2. Hypotension (excl Casey) ---
hypo_nc <- hypo %>% filter(study != "Casey 2025")
res_hypo_nc <- run_analysis(hypo_nc, "Hypotension — excl. Casey")
save_forest(res_hypo_nc, "forest_sens_excl_casey_hypotension.pdf",
            "Sens: Hypotension excl. Casey")

# --- 3. Vasopressor peri-intubation (excl Casey) ---
vaso_peri_nc <- vaso %>%
  filter(timepoint_category == "Peri-intubation" & study != "Casey 2025")
res_vp_nc <- run_analysis(vaso_peri_nc, "Vasopressor peri-intub — excl. Casey")
save_forest(res_vp_nc, "forest_sens_excl_casey_vaso_peri.pdf",
            "Sens: Vasopressor peri-intub excl. Casey")

# --- 4. Vasopressor 24h (excl Casey) ---
vaso_24_nc <- vaso %>%
  filter(timepoint_category == "24 hours" & study != "Casey 2025")
res_v24_nc <- run_analysis(vaso_24_nc, "Vasopressor 24h — excl. Casey")
save_forest(res_v24_nc, "forest_sens_excl_casey_vaso_24h.pdf",
            "Sens: Vasopressor 24h excl. Casey")

# --- 5. Cardiac arrest (excl Casey) ---
arrest_nc <- arrest %>% filter(study != "Casey 2025")
res_arr_nc <- run_analysis(arrest_nc, "Cardiac Arrest — excl. Casey")
save_forest(res_arr_nc, "forest_sens_excl_casey_cardiac_arrest.pdf",
            "Sens: Cardiac Arrest excl. Casey")

cat("\n============================================================\n")
cat("  SENSITIVITY EXCLUDING CASEY — COMPLETE\n")
cat("============================================================\n")
cat("Figures saved to manuscript/figures/\n")
