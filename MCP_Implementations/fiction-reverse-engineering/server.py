#!/usr/bin/env python3
"""Fiction Reverse Engineering MCP — mathematical pacing & bestseller comparison.

Reconstructed from COMPASS documentation (Style_MCPs/FICTION_REVERSE_ENGINEERING_*.md)
because the original local server.py was never committed to a git remote.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
# Ensure sibling imports work even when launched via absolute path / wrappers.
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from mcp.server.fastmcp import FastMCP

from analyzer import (
    USAGE_WARNING,
    analyze_pacing_metrics,
    build_formula,
    compare_to_formula,
    extract_chapter_metrics,
    extract_dialogue_metrics,
    slugify,
)

mcp = FastMCP("fiction-reverse-engineering")

REPO_ROOT = BASE_DIR.parent.parent


def _resolve_formulas_dir() -> Path:
    raw = os.environ.get("FICTION_RE_FORMULAS_DIR")
    if not raw:
        return BASE_DIR / "formulas"
    path = Path(raw)
    if path.is_absolute():
        return path
    # Relative env values are repo-root-relative (see run.sh / mcp.json).
    return (REPO_ROOT / path).resolve()


FORMULAS_DIR = _resolve_formulas_dir()
FORMULAS_DIR.mkdir(parents=True, exist_ok=True)


def _formula_path(slug: str) -> Path:
    return FORMULAS_DIR / f"{slug}.json"


def _load_formula(name_or_slug: str) -> dict[str, Any] | None:
    direct = _formula_path(slugify(name_or_slug))
    if direct.exists():
        return json.loads(direct.read_text(encoding="utf-8"))
    needle = name_or_slug.lower().strip()
    for path in FORMULAS_DIR.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if needle in {
            str(data.get("title", "")).lower(),
            str(data.get("slug", "")).lower(),
            path.stem.lower(),
        } or needle in str(data.get("title", "")).lower():
            return data
    return None


def _wrap(payload: dict[str, Any]) -> str:
    payload = dict(payload)
    payload["usage_warning"] = USAGE_WARNING
    payload["voice_reminder"] = (
        "Use insights to enhance, not replace creativity. "
        "Your unique voice is your greatest asset."
    )
    return json.dumps(payload, indent=2)


@mcp.tool()
def reverse_engineer_novel(title: str, author: str, text: str) -> str:
    """Extract a structural formula from a bestseller (or any sample text).

    Use during a learning phase to study patterns — not to copy formulas.
    Saves the formula for later comparison via compare_to_bestseller.
    """
    formula = build_formula(title=title, author=author, text=text)
    path = _formula_path(formula["slug"])
    path.write_text(json.dumps(formula, indent=2), encoding="utf-8")
    return _wrap(
        {
            "status": "saved",
            "formula_path": str(path),
            "formula": formula,
            "when_to_use": "Learning from masters — study patterns, adapt to your voice",
            "when_not_to_use": "During creative drafting; do not treat as a template",
        }
    )


@mcp.tool()
def compare_to_bestseller(text: str, bestseller_name: str) -> str:
    """Compare your writing to a previously reverse-engineered bestseller formula.

    Use for diagnostic analysis or revision refinement — not to copy.
    """
    formula = _load_formula(bestseller_name)
    if formula is None:
        available = [p.stem for p in sorted(FORMULAS_DIR.glob("*.json"))]
        return _wrap(
            {
                "status": "error",
                "error": f"No formula found for '{bestseller_name}'.",
                "available_formulas": available,
                "hint": "Run reverse_engineer_novel first to create a formula.",
            }
        )
    comparison = compare_to_formula(text, formula)
    return _wrap(
        {
            "status": "ok",
            "comparison": comparison,
            "when_to_use": "Diagnostic or revision phases",
            "when_not_to_use": "As a checklist that replaces your voice",
        }
    )


@mcp.tool()
def analyze_pacing(text: str, compare_to: str | None = None) -> str:
    """Mathematical pacing analysis: tension, reveals, dialogue, sentence variation.

    Use during revision for objective data. Optionally compare to a saved formula.
    """
    metrics = analyze_pacing_metrics(text)
    result: dict[str, Any] = {
        "status": "ok",
        "pacing": metrics,
        "when_to_use": "Revision / quality-assurance — data informs, intuition decides",
    }
    if compare_to:
        formula = _load_formula(compare_to)
        if formula is None:
            result["comparison_error"] = f"No formula found for '{compare_to}'."
        else:
            result["comparison"] = compare_to_formula(text, formula)
    return _wrap(result)


@mcp.tool()
def extract_dialogue_formula(text: str, save_as: str | None = None) -> str:
    """Extract dialogue patterns (tags, beats, exchange lengths).

    Learn techniques, then adapt them to your voice.
    """
    dialogue = extract_dialogue_metrics(text)
    result: dict[str, Any] = {
        "status": "ok",
        "dialogue_formula": dialogue,
        "when_to_use": "Learning dialogue craft from masters or diagnosing flat dialogue",
    }
    if save_as:
        formula = build_formula(title=save_as, author="dialogue-extract", text=text)
        path = _formula_path(formula["slug"])
        path.write_text(json.dumps(formula, indent=2), encoding="utf-8")
        result["saved_formula"] = str(path)
    return _wrap(result)


@mcp.tool()
def find_chapter_formula(text: str, chapter_label: str | None = None) -> str:
    """Extract chapter-level structural patterns (hooks, act tension thirds).

    Understand patterns; maintain variety across chapters.
    """
    chapter = extract_chapter_metrics(text)
    return _wrap(
        {
            "status": "ok",
            "chapter_label": chapter_label or "untitled-chapter",
            "chapter_formula": chapter,
            "when_to_use": "Understanding chapter structure during revision",
            "when_not_to_use": "Forcing every chapter into the same shape",
        }
    )


@mcp.tool()
def list_available_formulas() -> str:
    """List all saved reverse-engineered formulas available for comparison."""
    items = []
    for path in sorted(FORMULAS_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            items.append(
                {
                    "slug": path.stem,
                    "title": data.get("title"),
                    "author": data.get("author"),
                    "tension_pattern": data.get("patterns", {}).get("tension_pattern"),
                }
            )
        except (json.JSONDecodeError, OSError) as exc:
            items.append({"slug": path.stem, "error": str(exc)})
    return _wrap(
        {
            "status": "ok",
            "count": len(items),
            "formulas": items,
            "formulas_dir": str(FORMULAS_DIR),
        }
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
