from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ArticleA1AndTableContractTests(unittest.TestCase):
    def test_figure_a1_renderer_uses_samplewise_component_contract(self) -> None:
        script = ROOT / "scripts" / "render_authoritative_selected_model_support_figures.R"
        text = script.read_text(encoding="utf-8")
        self.assertIn(
            'FIGURE_A1_COMPONENT_CONTRACT <- "component_6_plus_trend_component_1_samplewise"',
            text,
        )
        self.assertIn("hydrologic_regime_periods <- function()", text)
        self.assertIn('"2012-01-01"', text)
        self.assertIn('"2016-12-31"', text)
        self.assertIn('"2017-01-01"', text)
        self.assertIn('"2019-12-31"', text)
        self.assertNotIn(
            'components$component_contract == "component_6_shifted_by_posterior_mean_trend_component_1"',
            text,
        )

    def test_figure_a1_render_metadata_records_contract_and_periods(self) -> None:
        meta_path = (
            ROOT
            / "artifacts"
            / "representative_selected_model_2022_12_25"
            / "authoritative_support"
            / "figures"
            / "render_metadata.json"
        )
        self.assertTrue(meta_path.exists(), f"missing render metadata: {meta_path}")
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        self.assertEqual(
            meta.get("figure_a1_component_contract"),
            "component_6_plus_trend_component_1_samplewise",
        )
        periods = meta.get("hydrologic_regime_periods")
        self.assertIsInstance(periods, list)
        self.assertEqual(
            [(row.get("period"), row.get("start"), row.get("end")) for row in periods],
            [("Dry", "2012-01-01", "2016-12-31"), ("Wet", "2017-01-01", "2019-12-31")],
        )

    def test_generated_table_builder_uses_single_five_decimal_policy(self) -> None:
        script = ROOT / "scripts" / "build_generated_table_includes.py"
        text = script.read_text(encoding="utf-8")
        self.assertIn("DISPLAY_DIGITS = 5", text)
        self.assertNotIn(":.4f", text)
        self.assertNotIn(", 3)", text)
        self.assertIn("fmt_display", text)
        self.assertIn("table-format=-1.5", text)

    def test_generated_table_decimal_cells_have_five_places(self) -> None:
        table_dir = ROOT / "tables" / "generated_tex"
        self.assertTrue(table_dir.exists(), f"missing generated table dir: {table_dir}")
        decimal = re.compile(r"(?<![A-Za-z0-9/])-?\d+\.(\d+)")
        bad: list[str] = []
        for path in sorted(table_dir.glob("*.tex")):
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if "&" not in line or line.lstrip().startswith("%"):
                    continue
                if line.startswith("Model &") or line.startswith("Ablation model &") or line.startswith("RAW-"):
                    pass
                for match in decimal.finditer(line):
                    if len(match.group(1)) != 5:
                        bad.append(f"{path.relative_to(ROOT)}:{lineno}:{match.group(0)}")
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
