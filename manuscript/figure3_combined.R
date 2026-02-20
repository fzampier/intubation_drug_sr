###############################################################################
# Figure 3 — Landscape two-panel: (A) Network geometry + (B) Pairwise E vs K
# Layout: 1:2 ratio, A on left, B on right
###############################################################################

projdir <- "/Users/fernandogodinhozampieri/Desktop/intubation_sr"
setwd(projdir)

library(meta)
library(netmeta)
library(ggplot2)
library(dplyr)

if (!requireNamespace("patchwork", quietly = TRUE))
  install.packages("patchwork", repos = "https://cran.r-project.org")
library(patchwork)

mort <- read.csv("data/mortality.csv", stringsAsFactors = FALSE)

# --- Run NMA & pairwise ---
pw_mort <- pairwise(treat = treat, event = events, n = n,
                    studlab = study, data = mort, sm = "OR")

nma_mort <- netmeta(TE, seTE, treat1, treat2, studlab,
                    data = pw_mort, sm = "OR",
                    common = FALSE, random = TRUE,
                    reference.group = "Etomidate")

pw_ek <- pw_mort %>%
  filter((treat1 == "Etomidate" & treat2 == "Ketamine") |
         (treat1 == "Ketamine"  & treat2 == "Etomidate"))

ma_ek <- metagen(TE, seTE, studlab = studlab, data = pw_ek,
                 sm = "OR", common = FALSE, random = TRUE,
                 method.tau = "PM")

###############################################################################
# PANEL A — Network geometry (ggplot)
###############################################################################

node_n <- mort %>%
  group_by(treat) %>%
  summarise(n_total = sum(n), .groups = "drop")

nodes <- data.frame(
  treat = c("Etomidate", "Ketamine", "Ketofol", "Propofol"),
  x     = c(0, 1, -0.15, 1.15),
  y     = c(1, 1, 0, 0)
) %>%
  left_join(node_n, by = "treat")

edges <- data.frame(
  from = c("Etomidate", "Etomidate", "Ketamine"),
  to   = c("Ketamine",  "Ketofol",   "Propofol"),
  k    = c(8, 1, 1)
)
edges <- edges %>%
  left_join(nodes %>% select(treat, x, y), by = c("from" = "treat")) %>%
  rename(x1 = x, y1 = y) %>%
  left_join(nodes %>% select(treat, x, y), by = c("to" = "treat")) %>%
  rename(x2 = x, y2 = y)

edges$lx <- (edges$x1 + edges$x2) / 2
edges$ly <- (edges$y1 + edges$y2) / 2
edges$ly_off <- ifelse(edges$from == "Etomidate" & edges$to == "Ketamine",
                       edges$ly + 0.12, edges$ly + 0.08)
edges$lx_off <- edges$lx
edges$lx_off[edges$from == "Etomidate" & edges$to == "Ketofol"] <-
  edges$lx[edges$from == "Etomidate" & edges$to == "Ketofol"] - 0.12
edges$lx_off[edges$from == "Ketamine" & edges$to == "Propofol"] <-
  edges$lx[edges$from == "Ketamine" & edges$to == "Propofol"] + 0.12
edges$ly_off[edges$from == "Etomidate" & edges$to == "Ketofol"] <-
  edges$ly[edges$from == "Etomidate" & edges$to == "Ketofol"]
edges$ly_off[edges$from == "Ketamine" & edges$to == "Propofol"] <-
  edges$ly[edges$from == "Ketamine" & edges$to == "Propofol"]

p_network <- ggplot() +
  geom_segment(data = edges,
               aes(x = x1, y = y1, xend = x2, yend = y2, linewidth = k),
               colour = "steelblue", alpha = 0.8, lineend = "round") +
  geom_point(data = nodes,
             aes(x = x, y = y, size = n_total),
             colour = "steelblue", alpha = 0.85) +
  geom_text(data = nodes,
            aes(x = x, y = y,
                label = paste0(treat, "\n(n=", format(n_total, big.mark = ","), ")")),
            vjust = -1.8, size = 3.2, fontface = "bold", lineheight = 0.85) +
  geom_text(data = edges,
            aes(x = lx_off, y = ly_off,
                label = ifelse(k == 1, "1 study", paste0(k, " studies"))),
            size = 2.8, colour = "grey30", fontface = "italic") +
  scale_size_continuous(range = c(4, 18), guide = "none") +
  scale_linewidth_continuous(range = c(0.8, 5), guide = "none") +
  coord_fixed(ratio = 1,
              xlim = c(-0.55, 1.55), ylim = c(-0.35, 1.65)) +
  theme_void() +
  ggtitle("A") +
  theme(plot.title = element_text(size = 14, face = "bold", hjust = 0,
                                  margin = margin(b = 2)))

###############################################################################
# PANEL B — Forest plot: pairwise E vs K (ggplot, linear-axis approach)
###############################################################################

# Get arm-level data
ek_arms <- mort %>%
  filter(treat %in% c("Etomidate", "Ketamine")) %>%
  group_by(study) %>% filter(n() == 2) %>% ungroup()

e_arms <- ek_arms %>% filter(treat == "Etomidate") %>%
  select(study, e_events = events, e_n = n)
k_arms <- ek_arms %>% filter(treat == "Ketamine") %>%
  select(study, k_events = events, k_n = n)

study_data <- pw_ek %>%
  select(studlab, TE, seTE) %>%
  mutate(or = exp(TE),
         lower = exp(TE - qnorm(0.975) * seTE),
         upper = exp(TE + qnorm(0.975) * seTE),
         w = 1 / seTE^2) %>%
  left_join(e_arms, by = c("studlab" = "study")) %>%
  left_join(k_arms, by = c("studlab" = "study"))
study_data$w_pct <- round(100 * study_data$w / sum(study_data$w), 1)
study_data <- study_data %>% arrange(as.numeric(gsub("\\D", "", studlab)))

# Add pooled
pooled <- data.frame(
  studlab = "Random-effects model", TE = ma_ek$TE.random,
  seTE = ma_ek$seTE.random, or = exp(ma_ek$TE.random),
  lower = exp(ma_ek$lower.random), upper = exp(ma_ek$upper.random),
  w = NA, w_pct = NA,
  e_events = sum(study_data$e_events), e_n = sum(study_data$e_n),
  k_events = sum(study_data$k_events), k_n = sum(study_data$k_n))

all_data <- bind_rows(study_data, pooled)
all_data$is_pooled <- all_data$studlab == "Random-effects model"
all_data$ypos <- rev(seq_len(nrow(all_data)))

# --- Map OR to linear x-axis ---
forest_left  <- 3.5
forest_right <- 7.5
forest_mid   <- (forest_left + forest_right) / 2
log_range <- c(-0.8, 0.8)

map_or <- function(or_val) {
  log_val <- log10(pmax(pmin(or_val, 10^log_range[2]), 10^log_range[1]))
  forest_left + (log_val - log_range[1]) / diff(log_range) * (forest_right - forest_left)
}

all_data$x_or    <- map_or(all_data$or)
all_data$x_lower <- map_or(all_data$lower)
all_data$x_upper <- map_or(all_data$upper)
x_null <- map_or(1)

# Text labels
all_data$events_e <- paste0(all_data$e_events, "/", all_data$e_n)
all_data$events_k <- paste0(all_data$k_events, "/", all_data$k_n)
all_data$or_label <- sprintf("%.2f [%.2f, %.2f]", all_data$or, all_data$lower, all_data$upper)
all_data$w_label  <- ifelse(all_data$is_pooled, "", sprintf("%.1f%%", all_data$w_pct))

het_text <- sprintf("Heterogeneity: I2 = %.0f%%, tau2 = %.3f, p = %.2f",
                    ma_ek$I2 * 100, ma_ek$tau2, ma_ek$pval.Q)

or_ticks <- c(0.25, 0.5, 1, 2, 4)
x_ticks  <- map_or(or_ticks)

# Build forest plot
p_forest <- ggplot(all_data, aes(y = ypos)) +
  # Null line
  geom_segment(x = x_null, xend = x_null,
               y = 0.3, yend = max(all_data$ypos) + 0.5,
               linetype = "dashed", colour = "grey50") +
  # CI lines (studies)
  geom_segment(data = filter(all_data, !is_pooled),
               aes(x = x_lower, xend = x_upper, yend = ypos),
               linewidth = 0.5) +
  # Study squares
  geom_point(data = filter(all_data, !is_pooled),
             aes(x = x_or, size = w_pct), shape = 15) +
  # Pooled CI line
  geom_segment(data = filter(all_data, is_pooled),
               aes(x = x_lower, xend = x_upper, yend = ypos),
               linewidth = 0.7) +
  # Pooled diamond
  geom_point(data = filter(all_data, is_pooled),
             aes(x = x_or), shape = 18, size = 5) +
  # Separator above pooled
  geom_segment(x = forest_left, xend = forest_right,
               y = 1.55, yend = 1.55, colour = "grey70", linewidth = 0.3) +
  # X-axis line
  geom_segment(x = forest_left, xend = forest_right,
               y = 0.3, yend = 0.3, colour = "black", linewidth = 0.3) +
  # X-axis ticks
  annotate("segment", x = x_ticks, xend = x_ticks,
           y = 0.3, yend = 0.15, colour = "black", linewidth = 0.3) +
  annotate("text", x = x_ticks, y = -0.05,
           label = as.character(or_ticks), size = 2.5) +
  # Direction labels (well below axis, no overlap)
  annotate("text", x = map_or(0.35), y = -0.4,
           label = "<-- Favours Etomidate", hjust = 0.5, size = 2.3,
           colour = "grey40", fontface = "italic") +
  annotate("text", x = map_or(2.8), y = -0.4,
           label = "Favours Ketamine -->", hjust = 0.5, size = 2.3,
           colour = "grey40", fontface = "italic") +
  # --- Left text columns ---
  geom_text(aes(x = 0, label = studlab), hjust = 0, size = 2.8,
            fontface = ifelse(all_data$is_pooled, "bold", "plain")) +
  # Etomidate events/n
  geom_text(aes(x = 2.2, label = events_e), hjust = 1, size = 2.5,
            colour = "grey20") +
  # Ketamine events/n
  geom_text(aes(x = 2.5, label = events_k), hjust = 0, size = 2.5,
            colour = "grey20") +
  # --- Right text columns ---
  geom_text(aes(x = 8.0, label = or_label), hjust = 0, size = 2.5,
            fontface = ifelse(all_data$is_pooled, "bold", "plain")) +
  geom_text(aes(x = 10.0, label = w_label), hjust = 1, size = 2.5,
            colour = "grey30") +
  # --- Column headers ---
  annotate("text", x = 0, y = max(all_data$ypos) + 1,
           label = "Study", hjust = 0, size = 3, fontface = "bold") +
  annotate("text", x = 2.05, y = max(all_data$ypos) + 1,
           label = "Etomidate", hjust = 0.5, size = 2.6, fontface = "bold") +
  annotate("text", x = 2.65, y = max(all_data$ypos) + 1,
           label = "Ketamine", hjust = 0.5, size = 2.6, fontface = "bold") +
  annotate("text", x = 8.0, y = max(all_data$ypos) + 1,
           label = "OR [95% CI]", hjust = 0, size = 3, fontface = "bold") +
  annotate("text", x = 10.0, y = max(all_data$ypos) + 1,
           label = "Weight", hjust = 1, size = 3, fontface = "bold") +
  # Heterogeneity (below pooled, left side)
  annotate("text", x = 0, y = 0.3,
           label = het_text, hjust = 0, size = 2.3, colour = "grey40") +
  # --- Scales ---
  scale_x_continuous(limits = c(-0.5, 10.5), expand = c(0, 0)) +
  scale_y_continuous(limits = c(-0.7, max(all_data$ypos) + 1.5), expand = c(0, 0)) +
  scale_size_continuous(range = c(1.5, 6), guide = "none") +
  coord_cartesian(clip = "off") +
  theme_void() +
  ggtitle("B") +
  theme(plot.title = element_text(size = 14, face = "bold", hjust = 0,
                                  margin = margin(b = 5)),
        plot.margin = margin(t = 5, r = 10, b = 10, l = 5))

###############################################################################
# COMBINE & SAVE — Landscape, 1:2 ratio (A left, B right)
###############################################################################

combined <- p_network + p_forest +
  plot_layout(widths = c(1, 2))

# Landscape dimensions
pdf("manuscript/figures/Figure3_network_forest.pdf", width = 15, height = 7)
print(combined)
dev.off()

png("manuscript/figures/Figure3_network_forest.png", width = 15, height = 7,
    units = "in", res = 300)
print(combined)
dev.off()

# Copy to overleaf
file.copy("manuscript/figures/Figure3_network_forest.pdf",
          "manuscript/overleaf/Figure3_network_forest.pdf",
          overwrite = TRUE)

cat(">> Figure 3 saved (landscape, 1:2, overlap fixed)\n")
