# Revised Article Repository

This repository is the advisor-facing freeze of the revised manuscript, its manuscript-facing figures and tables, and the article-local artifact bundles used to regenerate them.

## Where to look first

- `wileyNJD-APA.tex`: manuscript source used by Overleaf
- `figures/manuscript/`: the exact figure files used by the manuscript
- `figures/forecast_context_by_cutoff/`: advisor-facing copies of the Figure 4 forecast-context view for all five cutoffs
- `tables/generated_tex/`: the exact generated table blocks included by the manuscript
- `docs/figure_table_provenance.md`: figure/table provenance summary
- `reports/manuscript_asset_review/ARTICLE_ASSET_REVIEW.md`: review report for the current article assets
- `reports/manuscript_asset_review/FIGURE_POLISH_STATUS_AUDIT.md`: point-by-point status audit for the earlier figure-polish request

## Directory roles

- `figures/`: manuscript-facing figures, appendix cutoff panels, and advisor-facing cutoff forecast-context copies
- `tables/`: generated TeX tables used by the manuscript
- `artifacts/`: frozen local bundles copied from validated workflow outputs
- `reports/`: review reports, galleries, audits, and selection manifests
- `docs/`: advisor-facing documentation and provenance notes
- `scripts/`: refresh and audit scripts used to rebuild the article-side bundles

## Standard refresh command

```bash
python3 scripts/refresh_all_generated_assets.py
```

## Standard compile command

```bash
pdflatex -interaction=nonstopmode -halt-on-error -jobname=output wileyNJD-APA.tex
bibtex output
pdflatex -interaction=nonstopmode -halt-on-error -jobname=output wileyNJD-APA.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname=output wileyNJD-APA.tex
```
