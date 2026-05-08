#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

parse_args <- function(values) {
  out <- list()
  i <- 1L
  while (i <= length(values)) {
    key <- values[[i]]
    if (!startsWith(key, "--")) {
      stop(sprintf("Unexpected argument: %s", key), call. = FALSE)
    }
    if (i == length(values)) {
      stop(sprintf("Missing value for argument: %s", key), call. = FALSE)
    }
    out[[substring(key, 3L)]] <- values[[i + 1L]]
    i <- i + 2L
  }
  out
}

opt <- parse_args(args)

required <- c("workflow-root", "run-root", "output-dir", "cutoff-date", "forecast-start-date")
missing <- required[!vapply(required, function(k) !is.null(opt[[k]]) && nzchar(opt[[k]]), logical(1))]
if (length(missing) > 0L) {
  stop(sprintf("Missing required args: %s", paste(missing, collapse = ", ")), call. = FALSE)
}

project_root <- normalizePath(opt[["workflow-root"]], mustWork = TRUE)
run_root <- normalizePath(opt[["run-root"]], mustWork = TRUE)
out_dir <- normalizePath(opt[["output-dir"]], mustWork = FALSE)
cutoff_date <- opt[["cutoff-date"]]
forecast_start_date <- opt[["forecast-start-date"]]

dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
cache_dir <- file.path(out_dir, "cache")
dir.create(cache_dir, recursive = TRUE, showWarnings = FALSE)

q_paths <- c(
  file.path(run_root, "fit/exdqlm_multivar/keep/q=05/outputs/DISC_variables_5_exAL_synth_DISC.RData"),
  file.path(run_root, "fit/exdqlm_multivar/keep/q=20/outputs/DISC_variables_20_exAL_synth_DISC.RData"),
  file.path(run_root, "fit/exdqlm_multivar/keep/q=35/outputs/DISC_variables_35_exAL_synth_DISC.RData"),
  file.path(run_root, "fit/exdqlm_multivar/keep/q=50/outputs/DISC_variables_50_exAL_synth_DISC.RData"),
  file.path(run_root, "fit/exdqlm_multivar/keep/q=65/outputs/DISC_variables_65_exAL_synth_DISC.RData"),
  file.path(run_root, "fit/exdqlm_multivar/keep/q=80/outputs/DISC_variables_80_exAL_synth_DISC.RData"),
  file.path(run_root, "fit/exdqlm_multivar/keep/q=95/outputs/DISC_variables_95_exAL_synth_DISC.RData")
)

missing_q <- q_paths[!file.exists(q_paths)]
if (length(missing_q) > 0L) {
  stop(sprintf("Missing required multivariate fit artifacts: %s", paste(missing_q, collapse = ", ")), call. = FALSE)
}

Sys.setenv(
  ENV_PROJECT_ROOT = project_root,
  UNIFIED_REQUIRE_RUNSCOPED_POST = "TRUE",
  UNIFIED_ALLOW_LEGACY_POST_FALLBACK = "FALSE",
  UNIFIED_MODEL_RUN_EXDQLM_MULTIVAR = "TRUE",
  UNIFIED_MODEL_RUN_EXDQLM_UNIVAR = "FALSE",
  UNIFIED_MODEL_RUN_NDLM_MAIN = "FALSE",
  UNIFIED_MODEL_RUN_NDLM_UNIVAR = "FALSE",
  UNIFIED_CUTOFF_DATE = cutoff_date,
  UNIFIED_FORECAST_START_DATE = forecast_start_date,
  ENV_USGS_DAILY_PATH = file.path(run_root, "inputs/shared/usgs/usgs_daily.csv"),
  ENV_NWS_FORECAST_PATH = file.path(run_root, "inputs/shared/forecasts/nws_forecast.csv"),
  ENV_GLOFAS_FORECAST_PATH = file.path(run_root, "inputs/shared/forecasts/glofas_forecast.csv"),
  ENV_RETROS_PATH = file.path(run_root, "inputs/shared/retros/retros.csv"),
  ENV_PPT_PATH = file.path(run_root, "inputs/shared/covariates/cov_01_PPT.csv"),
  ENV_SOIL_PATH = file.path(run_root, "inputs/shared/covariates/cov_02_SOIL.csv"),
  ENV_PCA_PATH = file.path(run_root, "inputs/shared/covariates/cov_03_PCA.csv"),
  ENV_COVARIATE_FEATURES_PATH = file.path(run_root, "inputs/shared/covariates/covariate_features.csv"),
  UNIFIED_DISC_W_RDATA_PATHS = paste(q_paths, collapse = ","),
  UNIFIED_POST_CACHE_DIR = cache_dir
)

source(file.path(project_root, "R/environmetrics/00_setup.R"))
source(file.path(project_root, "R/environmetrics/00_paths.R"))
DATA_CBIND_RDS <- file.path(cache_dir, "data_cbind_tY_X.rds")
DATA_CBIND_CSV <- file.path(cache_dir, "data_cbind_tY_X.csv")
TIMESTAMPS_CSV <- file.path(cache_dir, "timestamps.csv")
source(file.path(project_root, "R/environmetrics/00_constants.R"))
source(file.path(project_root, "R/environmetrics/01_config.R"))
source(file.path(project_root, "R/environmetrics/02_helpers_core.R"))
source(file.path(project_root, "R/environmetrics/utils_data.R"))
source(file.path(project_root, "R/environmetrics/utils_plot.R"))
source(file.path(project_root, "R/environmetrics/10_data_inputs.R"))
source(file.path(project_root, "R/environmetrics/20_model_setup.R"))
if (!exists("dates_ts_usgs", inherits = FALSE)) {
  dates_ts_usgs <- timestamps
}
if (!exists("flood_stage_labels", inherits = FALSE)) {
  flood_stage_labels <- c("Major Flooding", "Minor Flooding")
}

state_cache_path <- file.path(cache_dir, "historical_support_state_summaries.rds")

load_selected_objects <- function(path, object_names) {
  env <- new.env(parent = emptyenv())
  loaded <- load(path, envir = env)
  missing <- setdiff(object_names, loaded)
  if (length(missing) > 0L) {
    stop(sprintf("Missing objects in %s: %s", path, paste(missing, collapse = ", ")), call. = FALSE)
  }
  list2env(mget(object_names, envir = env, inherits = FALSE), envir = .GlobalEnv)
  rm(env)
  invisible(gc())
}

resolve_proj <- function(Ft, Mu, Sigma) {
  p_use <- min(length(Ft), length(Mu), nrow(Sigma), ncol(Sigma))
  Ft_use <- matrix(as.numeric(Ft)[seq_len(p_use)], ncol = 1L)
  Mu_use <- as.numeric(Mu)[seq_len(p_use)]
  Sigma_use <- as.matrix(Sigma)[seq_len(p_use), seq_len(p_use), drop = FALSE]
  c(
    mean = as.numeric(crossprod(Ft_use, Mu_use)),
    sd = sqrt(max(as.numeric(t(Ft_use) %*% Sigma_use %*% Ft_use), 0))
  )
}

build_xbs_retro <- function() {
  objs <- list(
    `5` = new.theta.out_5_exAL_synth_DISC,
    `20` = new.theta.out_20_exAL_synth_DISC,
    `35` = new.theta.out_35_exAL_synth_DISC,
    `50` = new.theta.out_50_exAL_synth_DISC,
    `65` = new.theta.out_65_exAL_synth_DISC,
    `80` = new.theta.out_80_exAL_synth_DISC,
    `95` = new.theta.out_95_exAL_synth_DISC
  )
  qnames <- c("5", "20", "35", "50", "65", "80", "95")

  set.seed(777)
  arr <- array(NA_real_, c(7, TT, n.samp))
  for (t in seq_len(TT)) {
    Ft <- FF[, 1, t]
    stats <- lapply(qnames, function(q) resolve_proj(Ft, objs[[q]]$sm[, t], objs[[q]]$sC[, , t]))
    means <- vapply(stats, `[[`, numeric(1), "mean")
    sds <- vapply(stats, `[[`, numeric(1), "sd")
    draws <- rnorm(
      n = n.samp * length(means),
      mean = rep(means, each = n.samp),
      sd = rep(sds, each = n.samp)
    )
    draws_mat <- matrix(draws, nrow = n.samp, ncol = length(means))
    for (i in seq_along(qnames)) {
      arr[i, t, ] <- sort_keep_na(draws_mat[, i])
    }
  }
  arr
}

build_quant_df <- function(arr, idx, dates) {
  percentiles <- c(0.025, 0.5, 0.975)

  get_quantile_trajectory <- function(qidx, quantile_name) {
    mat <- arr[qidx, idx, , drop = FALSE]
    mat <- matrix(mat, nrow = length(idx), ncol = dim(arr)[3])
    qt_res <- t(fast_row_quantiles_t(mat, probs = percentiles))
    colnames(qt_res) <- c("Lower", "Median", "Upper")
    data.frame(
      Date = dates,
      Quantile = quantile_name,
      Lower = qt_res[, "Lower"],
      Median = qt_res[, "Median"],
      Upper = qt_res[, "Upper"]
    )
  }

  quantiles_map <- list(
    "5th" = 1,
    "20th" = 2,
    "35th" = 3,
    "50th" = 4,
    "65th" = 5,
    "80th" = 6,
    "95th" = 7
  )

  bind_rows(lapply(names(quantiles_map), function(qname) {
    get_quantile_trajectory(quantiles_map[[qname]], qname)
  }))
}

render_quantile_window <- function(xbs_retro, idx, title_text, out_file) {
  flood_stages_ft <- c(21.76, 16.5)^3
  flood_stages_cm <- flood_stages_ft * CFSToCMS_CONVERSION_FACTOR
  flood_stages_trans <- log(log(flood_stages_cm + 1))
  dates <- as.Date(dates_ts_usgs[idx])
  quant_df <- build_quant_df(xbs_retro, idx, dates)
  obs_df <- data.frame(Date = dates, Value = Y[1, idx])
  flood_lines <- data.frame(y = flood_stages_trans)

  alpha_val <- 0.11
  p <- ggplot() +
    annotate(
      "text",
      x = max(as.Date(dates_ts_usgs[idx])),
      y = flood_stages_trans,
      label = flood_stage_labels,
      hjust = 10.5,
      vjust = -0.5,
      color = "black",
      fontface = "italic",
      size = 3.5
    ) +
    geom_hline(
      data = flood_lines,
      aes(yintercept = y),
      linetype = "dashed",
      color = "gray50",
      linewidth = 0.6
    ) +
    geom_ribbon(
      data = quant_df %>% filter(Quantile == "95th"),
      aes(x = Date, ymin = Lower, ymax = Upper),
      fill = "#2171b5",
      alpha = alpha_val
    ) +
    geom_line(
      data = quant_df %>% filter(Quantile == "95th"),
      aes(x = Date, y = Median),
      color = "#2171b5",
      linewidth = 0.2
    ) +
    geom_line(
      data = quant_df %>% filter(Quantile == "95th"),
      aes(x = Date, y = Lower),
      color = "blue",
      linewidth = 0.05
    ) +
    geom_line(
      data = quant_df %>% filter(Quantile == "95th"),
      aes(x = Date, y = Upper),
      color = "blue",
      linewidth = 0.05
    ) +
    geom_ribbon(
      data = quant_df %>% filter(Quantile == "5th"),
      aes(x = Date, ymin = Lower, ymax = Upper),
      fill = "#b2182b",
      alpha = alpha_val
    ) +
    geom_line(
      data = quant_df %>% filter(Quantile == "5th"),
      aes(x = Date, y = Median),
      color = "#b2182b",
      linewidth = 0.2
    ) +
    geom_line(
      data = quant_df %>% filter(Quantile == "5th"),
      aes(x = Date, y = Lower),
      color = "red",
      linewidth = 0.05
    ) +
    geom_line(
      data = quant_df %>% filter(Quantile == "5th"),
      aes(x = Date, y = Upper),
      color = "red",
      linewidth = 0.05
    ) +
    geom_ribbon(
      data = quant_df %>% filter(Quantile == "50th"),
      aes(x = Date, ymin = Lower, ymax = Upper),
      fill = "#238b45",
      alpha = alpha_val
    ) +
    geom_line(
      data = quant_df %>% filter(Quantile == "50th"),
      aes(x = Date, y = Median),
      color = "#238b45",
      linewidth = 0.2
    ) +
    geom_line(
      data = quant_df %>% filter(Quantile == "50th"),
      aes(x = Date, y = Lower),
      color = "green",
      linewidth = 0.05
    ) +
    geom_line(
      data = quant_df %>% filter(Quantile == "50th"),
      aes(x = Date, y = Upper),
      color = "green",
      linewidth = 0.05
    ) +
    geom_point(
      data = obs_df,
      aes(x = Date, y = Value),
      color = "black",
      size = 0.2
    ) +
    geom_line(
      data = obs_df,
      aes(x = Date, y = Value),
      color = "black",
      linewidth = 0.1
    ) +
    labs(
      title = title_text,
      x = NULL,
      y = expression("Water Flow (Log-Log cm^3/s)")
    ) +
    scale_x_date(date_breaks = "6 months", date_labels = "%Y-%m") +
    coord_cartesian(ylim = c(-2, 3)) +
    theme_minimal(base_size = 14) +
    theme(
      plot.title = element_text(size = 15, face = "bold", hjust = 0.5),
      axis.title = element_text(face = "bold"),
      panel.grid.minor = element_blank()
    )

  ggsave(out_file, plot = p, width = 12, height = 6, units = "in", dpi = 900)
}

build_component_df <- function(component, idx, q_d_50, q_d_05, q_d_95) {
  build_quantile_df <- function(arr, component, idx, date_vec, quantile_name) {
    vals <- arr[component, idx, , drop = FALSE]
    vals <- matrix(vals, nrow = length(idx), ncol = dim(arr)[3])
    qts <- t(fast_row_quantiles_t(vals, probs = c(0.025, 0.5, 0.975)))
    colnames(qts) <- c("Lower", "Median", "Upper")
    tibble(
      Date = as.Date(date_vec[idx]),
      Quantile = quantile_name,
      Lower = qts[, "Lower"],
      Median = qts[, "Median"],
      Upper = qts[, "Upper"]
    )
  }

  bind_rows(
    build_quantile_df(q_d_50, component, idx, dates_ts_usgs, "50th"),
    build_quantile_df(q_d_05, component, idx, dates_ts_usgs, "5th"),
    build_quantile_df(q_d_95, component, idx, dates_ts_usgs, "95th")
  )
}

render_component_quantiles <- function(comp_df, obs_df, time_cuts, ylab, title_text, ylim, out_file) {
  shade_periods <- tibble(
    xmin = as.Date(dates_ts_usgs[time_cuts[c(1, 3)]]),
    xmax = as.Date(dates_ts_usgs[time_cuts[c(2, 4)]]),
    period = c("Dry", "Rainy"),
    fill = c("#ffeead", "#c9e4f6")
  )

  col_50 <- "#238b45"
  band_50 <- "#b2df8a"
  col_05 <- "#b2182b"
  band_05 <- "#fdbba1"
  col_95 <- "#2171b5"
  band_95 <- "#a6bddb"
  obs_line <- "#222222"
  obs_point <- "#222222"
  ribbon_alpha <- 0.11
  lnn <- 0.4

  p <- ggplot() +
    geom_rect(
      data = shade_periods,
      aes(xmin = xmin, xmax = xmax, ymin = -Inf, ymax = Inf, fill = period),
      alpha = 0.6,
      inherit.aes = FALSE,
      show.legend = FALSE
    ) +
    scale_fill_manual(values = setNames(shade_periods$fill, shade_periods$period)) +
    geom_ribbon(
      data = comp_df %>% filter(Quantile == "50th"),
      aes(x = Date, ymin = Lower, ymax = Upper),
      fill = band_50,
      alpha = ribbon_alpha
    ) +
    geom_ribbon(
      data = comp_df %>% filter(Quantile == "5th"),
      aes(x = Date, ymin = Lower, ymax = Upper),
      fill = band_05,
      alpha = ribbon_alpha
    ) +
    geom_ribbon(
      data = comp_df %>% filter(Quantile == "95th"),
      aes(x = Date, ymin = Lower, ymax = Upper),
      fill = band_95,
      alpha = ribbon_alpha
    ) +
    geom_line(
      data = comp_df %>% filter(Quantile == "50th"),
      aes(x = Date, y = Median),
      color = col_50,
      linewidth = lnn
    ) +
    geom_line(
      data = comp_df %>% filter(Quantile == "5th"),
      aes(x = Date, y = Median),
      color = col_05,
      linewidth = lnn
    ) +
    geom_line(
      data = comp_df %>% filter(Quantile == "95th"),
      aes(x = Date, y = Median),
      color = col_95,
      linewidth = lnn
    ) +
    geom_line(
      data = comp_df %>% filter(Quantile == "50th"),
      aes(x = Date, y = Lower),
      color = "green",
      linewidth = 0.1
    ) +
    geom_line(
      data = comp_df %>% filter(Quantile == "50th"),
      aes(x = Date, y = Upper),
      color = "green",
      linewidth = 0.1
    ) +
    geom_line(
      data = comp_df %>% filter(Quantile == "5th"),
      aes(x = Date, y = Lower),
      color = "red",
      linewidth = 0.1
    ) +
    geom_line(
      data = comp_df %>% filter(Quantile == "5th"),
      aes(x = Date, y = Upper),
      color = "red",
      linewidth = 0.1
    ) +
    geom_line(
      data = comp_df %>% filter(Quantile == "95th"),
      aes(x = Date, y = Lower),
      color = "blue",
      linewidth = 0.1
    ) +
    geom_line(
      data = comp_df %>% filter(Quantile == "95th"),
      aes(x = Date, y = Upper),
      color = "blue",
      linewidth = 0.1
    ) +
    geom_line(data = obs_df, aes(x = Date, y = Value), color = obs_line, linewidth = 0.1) +
    geom_point(data = obs_df, aes(x = Date, y = Value), color = obs_point, size = 0.1, alpha = 0.95) +
    annotate(
      "text",
      x = shade_periods$xmin + (shade_periods$xmax - shade_periods$xmin) / 2,
      y = ylim[1] + 0.01 * diff(ylim),
      label = shade_periods$period,
      size = 3.4,
      color = "#565656",
      fontface = "italic"
    ) +
    labs(title = title_text, x = NULL, y = ylab) +
    coord_cartesian(ylim = ylim, expand = TRUE) +
    scale_x_date(date_breaks = "24 months", date_labels = "%Y-%m") +
    theme_minimal(base_size = 15) +
    theme(
      plot.title = element_text(size = 16, face = "bold", hjust = 0.5, margin = margin(b = 8)),
      axis.title = element_text(face = "bold"),
      axis.text.x = element_text(angle = 35, hjust = 1, vjust = 1, size = 11),
      axis.text.y = element_text(size = 12),
      panel.grid.minor = element_blank(),
      panel.grid.major.x = element_line(linewidth = 0.3, color = "#e5e5e5"),
      panel.grid.major.y = element_line(linewidth = 0.4, color = "#e5e5e5"),
      plot.margin = margin(12, 12, 12, 12)
    )

  ggsave(out_file, plot = p, width = 12, height = 6, units = "in", dpi = 350)
}

if (file.exists(state_cache_path)) {
  message("Loading cached historical-support state summaries...")
  cached <- readRDS(state_cache_path)
  xbs_retro <- cached$xbs_retro
  q_d_50 <- cached$q_d_50
  q_d_05 <- cached$q_d_05
  q_d_95 <- cached$q_d_95
  time_cuts <- cached$time_cuts
} else {
  message("Loading only the state objects needed for the support figures...")
  load_selected_objects(
    q_paths[[1]],
    c("new.theta.out_5_exAL_synth_DISC", "samp.theta_5_exAL_synth_DISC")
  )
  load_selected_objects(q_paths[[2]], c("new.theta.out_20_exAL_synth_DISC"))
  load_selected_objects(q_paths[[3]], c("new.theta.out_35_exAL_synth_DISC"))
  load_selected_objects(
    q_paths[[4]],
    c("new.theta.out_50_exAL_synth_DISC", "samp.theta_50_exAL_synth_DISC")
  )
  load_selected_objects(q_paths[[5]], c("new.theta.out_65_exAL_synth_DISC"))
  load_selected_objects(q_paths[[6]], c("new.theta.out_80_exAL_synth_DISC"))
  load_selected_objects(
    q_paths[[7]],
    c("new.theta.out_95_exAL_synth_DISC", "samp.theta_95_exAL_synth_DISC")
  )
  message("Building historical-support state summaries from current run...")
  xbs_retro <- build_xbs_retro()
  rm(
    new.theta.out_5_exAL_synth_DISC,
    new.theta.out_20_exAL_synth_DISC,
    new.theta.out_35_exAL_synth_DISC,
    new.theta.out_50_exAL_synth_DISC,
    new.theta.out_65_exAL_synth_DISC,
    new.theta.out_80_exAL_synth_DISC,
    new.theta.out_95_exAL_synth_DISC
  )
  invisible(gc())
  q_d_50 <- fast_prepare_quantile_data(samp.theta_50_exAL_synth_DISC$samp_theta, probs = c(0.975, 0.5, 0.025), type = 7L)
  q_d_05 <- fast_prepare_quantile_data(samp.theta_5_exAL_synth_DISC$samp_theta, probs = c(0.975, 0.5, 0.025), type = 7L)
  q_d_95 <- fast_prepare_quantile_data(samp.theta_95_exAL_synth_DISC$samp_theta, probs = c(0.975, 0.5, 0.025), type = 7L)
  rm(
    samp.theta_5_exAL_synth_DISC,
    samp.theta_50_exAL_synth_DISC,
    samp.theta_95_exAL_synth_DISC
  )
  invisible(gc())
  time_cuts <- resolve_time_cuts(timestamps = timestamps, cutoff_date = as.Date(cutoff_date), context = "current_model_output_support")
  saveRDS(
    list(
      xbs_retro = xbs_retro,
      q_d_50 = q_d_50,
      q_d_05 = q_d_05,
      q_d_95 = q_d_95,
      time_cuts = time_cuts
    ),
    state_cache_path
  )
}

render_quantile_window(
  xbs_retro = xbs_retro,
  idx = time_cuts[1]:time_cuts[2],
  title_text = "Quantile Dynamics: 2012–2016",
  out_file = file.path(out_dir, "All_exal_2012-2016_DISC.png")
)
render_quantile_window(
  xbs_retro = xbs_retro,
  idx = time_cuts[3]:time_cuts[4],
  title_text = "Quantile Dynamics: 2017–2019",
  out_file = file.path(out_dir, "All_exal_2017-2019_DISC.png")
)

idx_component <- ceiling(TT / 10):TT
obs_df <- tibble(Date = as.Date(dates_ts_usgs[idx_component]), Value = Y[1, idx_component])
comp_df <- build_component_df(component = 6, idx = idx_component, q_d_50 = q_d_50, q_d_05 = q_d_05, q_d_95 = q_d_95)
render_component_quantiles(
  comp_df = comp_df,
  obs_df = obs_df,
  time_cuts = time_cuts,
  ylab = expression("Water Flow (Log-Log cm^3/s)"),
  title_text = "80-month Effect – 1991–2022",
  ylim = c(-2, 2),
  out_file = file.path(out_dir, "80_component_1991_2022.png")
)

meta <- list(
  workflow_root = project_root,
  multivar_run_root = run_root,
  cutoff_date = cutoff_date,
  forecast_start_date = forecast_start_date,
  rendered_files = c(
    "All_exal_2012-2016_DISC.png",
    "All_exal_2017-2019_DISC.png",
    "80_component_1991_2022.png"
  ),
  time_cuts = as.integer(time_cuts),
  time_cut_dates = as.character(as.Date(timestamps[time_cuts])),
  rendered_at_utc = format(Sys.time(), tz = "UTC", usetz = TRUE)
)
writeLines(jsonlite::toJSON(meta, auto_unbox = TRUE, pretty = TRUE), file.path(out_dir, "render_metadata.json"))
stale_helper_files <- file.path(out_dir, c("data_cbind_tY_X.rds", "data_cbind_tY_X.csv", "timestamps.csv"))
unlink(stale_helper_files[file.exists(stale_helper_files)])
message("Rendered current-model historical support figures successfully.")
