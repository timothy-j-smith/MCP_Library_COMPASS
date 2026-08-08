#!/usr/bin/env python3
"""Lightweight analyzer tests (stdlib unittest)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analyzer import (  # noqa: E402
    analyze_pacing_metrics,
    build_formula,
    compare_to_formula,
    extract_dialogue_metrics,
)


SAMPLE = """
Jimmy knew the river held secrets. Blood on the stones meant danger.

"Did you see him?" she whispered.
"No," Jimmy said. "But I heard the shot."

He realized the truth all along: the killer had never left town. Fear tightened
his throat as he remembered the murder. Suddenly the secret was clear.

Tomorrow would decide everything.
"""


class AnalyzerTests(unittest.TestCase):
    def test_pacing_metrics(self) -> None:
        metrics = analyze_pacing_metrics(SAMPLE)
        self.assertGreater(metrics["word_count"], 20)
        self.assertIn(metrics["tension_pattern"], {"low", "moderate", "high"})
        self.assertGreaterEqual(metrics["tension_frequency"], 0.0)

    def test_dialogue_metrics(self) -> None:
        dialogue = extract_dialogue_metrics(SAMPLE)
        self.assertGreaterEqual(dialogue["dialogue_exchanges"], 2)
        self.assertIn("said", dialogue["dialogue_tags"])

    def test_formula_roundtrip_compare(self) -> None:
        formula = build_formula("Mystic River", "Dennis Lehane", SAMPLE)
        comparison = compare_to_formula(SAMPLE, formula)
        self.assertGreaterEqual(comparison["match_score"], 0.9)

    def test_server_tools_persist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            import os

            os.environ["FICTION_RE_FORMULAS_DIR"] = tmp
            # Re-import server helpers after env set
            import importlib

            import server as srv

            importlib.reload(srv)
            out = json.loads(
                srv.reverse_engineer_novel("Mystic River", "Dennis Lehane", SAMPLE)
            )
            self.assertEqual(out["status"], "saved")
            listed = json.loads(srv.list_available_formulas())
            self.assertEqual(listed["count"], 1)
            cmp = json.loads(srv.compare_to_bestseller(SAMPLE, "Mystic River"))
            self.assertEqual(cmp["status"], "ok")
            pacing = json.loads(srv.analyze_pacing(SAMPLE, compare_to="Mystic River"))
            self.assertEqual(pacing["status"], "ok")
            chapter = json.loads(srv.find_chapter_formula(SAMPLE, "Ch1"))
            self.assertEqual(chapter["status"], "ok")
            dialogue = json.loads(srv.extract_dialogue_formula(SAMPLE))
            self.assertEqual(dialogue["status"], "ok")


if __name__ == "__main__":
    unittest.main()
