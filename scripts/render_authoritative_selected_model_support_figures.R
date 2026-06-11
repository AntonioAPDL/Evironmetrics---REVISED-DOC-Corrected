#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

parse_args <- function(values) {
  out <- list()
  i <- 1L
  while (i <= length(values)) {
    key <- values[[i]]
    if (!startsWith(key, "--")) stop(sprintf("Unexpected argument: %s", key), call. = FALSE)
    if (i == length(values)) stop(sprintf("Missing value for argument: %s", key), call. = FALSE)
    out[[substring(key, 3L)]] <- values[[i + 1L]]
    i <- i + 2L
  }
  out
}

opt <- parse_args(args)
required <- c("support-dir", "output-dir")
missing <- required[!vapply(required, function(k) !is.null(opt[[k]]) && nzchar(opt[[k]]), logical(1))]
if (length(missing) > 0L) {
  stop(sprintf("Missing required args: %s", paste(missing, collapse = ", ")), call. = FALSE)
}

support_dir <- normalizePath(opt[["support-dir"]], mustWork = TRUE)
out_dir <- normalizePath(opt[["output-dir"]], mustWork = FALSE)
workflow_root <- opt[["workflow-root"]]
display_flow_scale <- opt[["display-flow-scale"]]
if (is.null(display_flow_scale) || !nzchar(display_flow_scale)) display_flow_scale <- "log1p_cms"

dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

if (!is.null(workflow_root) && nzchar(workflow_root)) {
  style_path <- file.path(normalizePath(workflow_root, mustWork = TRUE), "scripts", "figure_style_contract.R")
  if (file.exists(style_path)) source(style_path)
}

if (!exists("theme_manuscript_standard", mode = "function")) {
  theme_manuscript_standard <- function(...) ggplot2::theme_bw(base_size = 13)
}
if (!exists("figure_flow_axis_label", mode = "function")) {
  figure_flow_axis_label <- function(scale) scale
}

suppressPackageStartupMessages({
  library(ggplot2)
})

FIGURE_A1_COMPONENT_CONTRACT <- "component_6_plus_trend_component_1_samplewise"

hydrologic_regime_periods <- function() {
  data.frame(
    xmin = as.Date(c("2012-01-01", "2017-01-01")),
    xmax = as.Date(c("2016-12-31", "2019-12-31")),
    period = c("Dry", "Wet"),
    fill = c("#fff0b3", "#cfe8f7"),
    stringsAsFactors = FALSE
  )
}

dynamics_path <- file.path(support_dir, "authoritative_usgs_quantile_dynamics_summary.csv")
component_path <- file.path(support_dir, "authoritative_component_summary.csv")
if (!file.exists(dynamics_path)) stop(sprintf("Missing dynamics support CSV: %s", dynamics_path), call. = FALSE)
if (!file.exists(component_path)) stop(sprintf("Missing component support CSV: %s", component_path), call. = FALSE)

dynamics <- utils::read.csv(dynamics_path, stringsAsFactors = FALSE, check.names = FALSE)
components <- utils::read.csv(component_path, stringsAsFactors = FALSE, check.names = FALSE)
dynamics$date <- as.Date(dynamics$date)
components$date <- as.Date(components$date)

render_quantile_window <- function(start_date, end_date, title_text, out_file, ylim = c(0, 7)) {
  dd <- dynamics[
    dynamics$quantile %in% c("q05", "q50", "q95") &
      !is.na(dynamics$date) &
      dynamics$date >= as.Date(start_date) &
      dynamics$date <= as.Date(end_date),
    ,
    drop = FALSE
  ]
  if (nrow(dd) < 1L) stop(sprintf("No dynamics rows for %s to %s", start_date, end_date), call. = FALSE)
  obs <- dd[dd$quantile == "q50", c("date", "observed_usgs"), drop = FALSE]
  obs <- obs[is.finite(obs$observed_usgs), , drop = FALSE]
  col <- c(q05 = "#b2182b", q50 = "#238b45", q95 = "#2171b5")
  fill <- c(q05 = "#fdbba1", q50 = "#b2df8a", q95 = "#a6bddb")
  p <- ggplot() +
    geom_ribbon(
      data = dd,
      aes(x = date, ymin = lower_025, ymax = upper_975, fill = quantile),
      alpha = 0.12
    ) +
    geom_line(
      data = dd,
      aes(x = date, y = median_500, color = quantile),
      linewidth = 0.45
    ) +
    geom_line(
      data = dd,
      aes(x = date, y = lower_025, color = quantile),
      linewidth = 0.12
    ) +
    geom_line(
      data = dd,
      aes(x = date, y = upper_975, color = quantile),
      linewidth = 0.12
    ) +
    geom_line(data = obs, aes(x = date, y = observed_usgs), color = "black", linewidth = 0.22) +
    geom_point(data = obs, aes(x = date, y = observed_usgs), color = "black", size = 0.35) +
    scale_color_manual(values = col, breaks = c("q05", "q50", "q95")) +
    scale_fill_manual(values = fill, breaks = c("q05", "q50", "q95")) +
    coord_cartesian(ylim = ylim) +
    scale_x_date(date_breaks = "1 year", date_labels = "%Y-%m") +
    labs(title = title_text, x = NULL, y = figure_flow_axis_label(display_flow_scale)) +
    theme_manuscript_standard(
      base_size = 14,
      title_size = 15,
      legend_position = "none",
      axis_text_y_size = 12,
      x_angle = 35,
      major_grid_x = TRUE,
      major_grid_y = TRUE,
      plot_margin = margin(12, 12, 12, 12)
    )
  ggsave(out_file, plot = p, width = 12, height = 6, units = "in", dpi = 900)
}

render_component_80month <- function(out_file) {
  dd <- components[
    components$quantile %in% c("q05", "q50", "q95") &
      components$component == 6 &
      components$component_contract == FIGURE_A1_COMPONENT_CONTRACT &
      !is.na(components$date),
    ,
    drop = FALSE
  ]
  if (nrow(dd) < 1L) {
    stop(
      sprintf("No component-6 rows found for required contract `%s` in authoritative component summary.", FIGURE_A1_COMPONENT_CONTRACT),
      call. = FALSE
    )
  }
  min_time <- ceiling(max(dd$time_index, na.rm = TRUE) / 10)
  dd <- dd[dd$time_index >= min_time, , drop = FALSE]
  obs <- dynamics[dynamics$quantile == "q50", c("date", "observed_usgs"), drop = FALSE]
  obs <- obs[!is.na(obs$date) & is.finite(obs$observed_usgs), , drop = FALSE]
  obs <- obs[obs$date >= min(dd$date, na.rm = TRUE) & obs$date <= max(dd$date, na.rm = TRUE), , drop = FALSE]
  ylim <- range(c(dd$lower_025, dd$upper_975, obs$observed_usgs), na.rm = TRUE)
  if (!all(is.finite(ylim)) || diff(ylim) <= 0) ylim <- c(0, 1)
  ylim <- c(min(0, ylim[[1L]]), ylim[[2L]] + diff(ylim) * 0.08)
  shade_periods <- hydrologic_regime_periods()
  shade_periods <- shade_periods[shade_periods$xmax >= min(dd$date, na.rm = TRUE) & shade_periods$xmin <= max(dd$date, na.rm = TRUE), , drop = FALSE]
  shade_periods$xmin <- pmax(shade_periods$xmin, min(dd$date, na.rm = TRUE))
  shade_periods$xmax <- pmin(shade_periods$xmax, max(dd$date, na.rm = TRUE))
  label_y <- ylim[[1L]] + 0.035 * diff(ylim)
  col <- c(q05 = "#b2182b", q50 = "#238b45", q95 = "#2171b5")
  fill <- c(q05 = "#fdbba1", q50 = "#b2df8a", q95 = "#a6bddb")
  p <- ggplot() +
    geom_rect(
      data = shade_periods,
      aes(xmin = xmin, xmax = xmax, ymin = -Inf, ymax = Inf, fill = period),
      alpha = 0.48,
      inherit.aes = FALSE,
      show.legend = FALSE
    ) +
    geom_ribbon(
      data = dd,
      aes(x = date, ymin = lower_025, ymax = upper_975, fill = quantile),
      alpha = 0.12
    ) +
    geom_line(data = dd, aes(x = date, y = median_500, color = quantile), linewidth = 0.45) +
    geom_line(data = dd, aes(x = date, y = lower_025, color = quantile), linewidth = 0.12) +
    geom_line(data = dd, aes(x = date, y = upper_975, color = quantile), linewidth = 0.12) +
    geom_line(data = obs, aes(x = date, y = observed_usgs), color = "black", linewidth = 0.12) +
    geom_point(data = obs, aes(x = date, y = observed_usgs), color = "black", size = 0.1, alpha = 0.9) +
    scale_color_manual(values = col, breaks = c("q05", "q50", "q95")) +
    scale_fill_manual(values = c(fill, setNames(shade_periods$fill, shade_periods$period))) +
    annotate(
      "text",
      x = shade_periods$xmin + (shade_periods$xmax - shade_periods$xmin) / 2,
      y = label_y,
      label = shade_periods$period,
      size = 3.4,
      color = "#555555",
      fontface = "italic"
    ) +
    coord_cartesian(ylim = ylim) +
    scale_x_date(date_breaks = "24 months", date_labels = "%Y-%m") +
    labs(
      title = "80-month Component Evolution: selected 2022-12-25 model",
      x = NULL,
      y = figure_flow_axis_label(display_flow_scale)
    ) +
    theme_manuscript_standard(
      base_size = 15,
      title_size = 16,
      legend_position = "none",
      axis_text_y_size = 12,
      x_angle = 35,
      major_grid_x = TRUE,
      major_grid_y = TRUE,
      plot_margin = margin(12, 12, 12, 12)
    )
  ggsave(out_file, plot = p, width = 12, height = 6, units = "in", dpi = 350)
}

render_quantile_window(
  "2012-01-01",
  "2016-12-31",
  "Selected-model Quantile Dynamics: 2012-2016",
  file.path(out_dir, "selected_model_quantile_dry_period.png"),
  ylim = c(0, 7)
)
render_quantile_window(
  "2017-01-01",
  "2019-12-31",
  "Selected-model Quantile Dynamics: 2017-2019",
  file.path(out_dir, "selected_model_quantile_wet_period.png"),
  ylim = c(0, 7)
)
render_component_80month(file.path(out_dir, "selected_model_component_80month.png"))

meta <- list(
  support_dir = support_dir,
  output_dir = out_dir,
  display_flow_scale = display_flow_scale,
  figure_a1_component_contract = FIGURE_A1_COMPONENT_CONTRACT,
  figure_a1_article_display_label = "80-month seasonal component",
  hydrologic_regime_periods = lapply(seq_len(nrow(hydrologic_regime_periods())), function(i) {
    row <- hydrologic_regime_periods()[i, , drop = FALSE]
    list(
      period = row$period[[1L]],
      start = as.character(row$xmin[[1L]]),
      end = as.character(row$xmax[[1L]]),
      fill = row$fill[[1L]]
    )
  }),
  rendered_files = c(
    "selected_model_quantile_dry_period.png",
    "selected_model_quantile_wet_period.png",
    "selected_model_component_80month.png"
  ),
  generated_at_utc = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
)
if (requireNamespace("jsonlite", quietly = TRUE)) {
  jsonlite::write_json(meta, file.path(out_dir, "render_metadata.json"), auto_unbox = TRUE, pretty = TRUE)
}
message("Rendered authoritative selected-model support figures.")
