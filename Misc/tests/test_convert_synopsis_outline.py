#!/usr/bin/env python3
"""Stdlib-only tests for convert_synopsis_outline_to_book_series.

Run: python3 -m unittest Misc.tests.test_convert_synopsis_outline
  or: python3 Misc/tests/test_convert_synopsis_outline.py
"""

import importlib.util
import unittest
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parents[1] / "convert_synopsis_outline_to_book_series.py"
_spec = importlib.util.spec_from_file_location("cso", _MODULE_PATH)
cso = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cso)


class ParseSynopsisTests(unittest.TestCase):
    def test_metadata_and_premise(self):
        text = (
            "# The Cartographer's Ghost\n\n"
            "Series: Impossible Maps\n"
            "Pen name: A. R. Vale\n"
            "Genre: Literary Mystery\n\n"
            "## Premise\n\n"
            "A grieving cartographer finds a living map.\n"
        )
        s = cso.parse_synopsis(text)
        self.assertEqual(s["title"], "The Cartographer's Ghost")
        self.assertEqual(s["series_name"], "Impossible Maps")
        self.assertEqual(s["pen_name"], "A. R. Vale")
        self.assertEqual(s["genre"], "Literary Mystery")
        self.assertIn("living map", s["premise"])

    def test_title_defaults_and_series_derivation(self):
        s = cso.parse_synopsis("# Solo Book\n\nSome premise text here.\n")
        self.assertEqual(s["title"], "Solo Book")
        self.assertEqual(s["series_name"], "Solo Book Series")
        self.assertEqual(s["genre"], "Fiction")

    def test_themes(self):
        text = "# T\n\n## Themes\n- Grief\n- Memory\n\n## Next\n- not a theme\n"
        self.assertEqual(cso.parse_synopsis(text)["themes"], ["Grief", "Memory"])

    def test_characters_variants(self):
        text = (
            "# T\n\n## Characters\n"
            "- Mara Vale (protagonist): grieving cartographer\n"
            "- **Edmund Vale** - mentor, her father\n"
            "- The Surveyor \u2014 antagonist\n"
        )
        chars = cso.parse_synopsis(text)["characters"]
        self.assertEqual(len(chars), 3)
        self.assertEqual(chars[0]["name"], "Mara Vale")
        self.assertEqual(chars[0]["character_type"], "protagonist")
        self.assertIn("cartographer", chars[0]["description"])
        self.assertEqual(chars[1]["name"], "Edmund Vale")
        self.assertEqual(chars[1]["character_type"], "mentor")
        self.assertEqual(chars[2]["name"], "The Surveyor")
        self.assertEqual(chars[2]["character_type"], "antagonist")


class ParseOutlineTests(unittest.TestCase):
    def test_heading_chapters(self):
        text = (
            "# Outline\n\n"
            "## Chapter 1: The Desk\nMara finds the map.\n\n"
            "## Chapter 2: The Street\nA new avenue appears.\n"
        )
        chapters = cso.parse_outline(text)
        self.assertEqual([c["chapter_number"] for c in chapters], [1, 2])
        self.assertEqual(chapters[0]["title"], "The Desk")
        self.assertIn("finds the map", chapters[0]["summary"])

    def test_bullet_and_bare_formats(self):
        text = (
            "- Ch1: Mara finds the map on a rainy night.\n"
            "Chapter 02 - A new avenue appears overnight.\n"
            "### Chapter 3 second title\nthird summary line here\n"
        )
        chapters = cso.parse_outline(text)
        self.assertEqual([c["chapter_number"] for c in chapters], [1, 2, 3])
        # Sentence-like trailing text is captured as the summary.
        self.assertEqual(chapters[0]["summary"], "Mara finds the map on a rainy night.")
        self.assertEqual(chapters[1]["summary"], "A new avenue appears overnight.")
        # Short trailing text is a title; the summary comes from following lines.
        self.assertEqual(chapters[2]["title"], "second title")
        self.assertEqual(chapters[2]["summary"], "third summary line here")


class BuildBundleTests(unittest.TestCase):
    def _synopsis(self):
        return {
            "title": "T", "series_name": "S", "pen_name": "P", "genre": "G",
            "world_type": None, "logline": "", "premise": "prem",
            "themes": ["Grief"],
            "characters": [{"name": "Mara", "character_type": "protagonist", "description": "lead"}],
        }

    def test_new_series_uses_placeholders(self):
        bundle = cso.build_bundle(self._synopsis(), [{"chapter_number": 1, "title": "A", "summary": "s"}], None, 1)
        tools = [s["tool"] for s in bundle["steps"]]
        self.assertEqual(tools, [
            "create_series", "create_series_book", "create_series_character",
            "create_series_plot_thread", "bulk_chapter_operations",
        ])
        self.assertEqual(bundle["steps"][0]["capture"], "series_id")
        self.assertEqual(bundle["steps"][1]["arguments"]["series_id"], "$series_id")
        self.assertEqual(bundle["steps"][-1]["arguments"]["book_id"], "$book_id")
        self.assertEqual(bundle["meta"]["character_count"], 1)

    def test_existing_series_has_no_create_series(self):
        bundle = cso.build_bundle(self._synopsis(), [], series_id=7, book_number=2)
        tools = [s["tool"] for s in bundle["steps"]]
        self.assertNotIn("create_series", tools)
        self.assertEqual(bundle["steps"][0]["arguments"]["series_id"], 7)
        self.assertEqual(bundle["steps"][0]["arguments"]["book_number"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
