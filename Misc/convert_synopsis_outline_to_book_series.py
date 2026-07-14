#!/usr/bin/env python3
"""
Synopsis + Outline -> Book Series MCP import bundle.

Part of COMPASS Writing System.

Parses a free-form Story Bible ``synopsis.md`` and ``outline.md`` and emits a
JSON "import bundle" whose steps map directly onto Book Series MCP
(https://github.com/RLRyals/book-series-mcp) tool calls:

  * create_series            (book-series-manager)
  * create_series_book       (book-series-manager)
  * create_series_plot_thread(book-series-manager)  -- one per theme/arc
  * bulk_chapter_operations  (writing-production)   -- create_outline_batch

The bundle is applied to a running Book Series MCP instance with the companion
``import_to_book_series.mjs`` script. This converter has no third-party
dependencies and does not call any external API, so it is fully deterministic.

Unlike ``build_story_structure_mcp.py`` (which uses the Anthropic API to emit a
standalone ``story_structure.json``), this script targets the Book Series MCP
PostgreSQL-backed servers directly.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ----------------------------------------------------------------------------
# Markdown parsing helpers
# ----------------------------------------------------------------------------

# "Key: value" metadata lines, optionally wrapped in markdown emphasis/heading.
_META_RE = re.compile(r"^[#>\s*_-]*\**([A-Za-z][A-Za-z /]+?)\**\s*:\s*(.+?)\s*$")

# Chapter headers in several common shapes:
#   "## Chapter 1: Title" / "### Chapter 00 - Title" / "Chapter 12"
#   "- Ch1: summary" / "* Chapter 3 - summary"
_CHAPTER_RES = [
    re.compile(r"^#{1,6}\s*chapter\s+(\d+)\s*[:\-\u2013.]?\s*(.*)$", re.I),
    re.compile(r"^[-*]\s*ch(?:apter)?\.?\s*(\d+)\s*[:\-\u2013.]?\s*(.*)$", re.I),
    re.compile(r"^chapter\s+(\d+)\s*[:\-\u2013.]?\s*(.*)$", re.I),
]

# A markdown heading of any level (used to end a chapter's summary block).
_HEADING_RE = re.compile(r"^#{1,6}\s+\S")


def _read(path: Path) -> str:
    if path and path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _collect_meta(text: str) -> dict:
    """Collect simple ``Key: value`` metadata lines from the top-matter."""
    meta = {}
    for line in text.splitlines():
        m = _META_RE.match(line)
        if not m:
            continue
        key = m.group(1).strip().lower()
        val = m.group(2).strip().strip("*_")
        if key and val and key not in meta:
            meta[key] = val
    return meta


def _first_heading(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            title = s.lstrip("#").strip()
            if title and title.lower() not in ("synopsis", "outline"):
                return title
    return ""


def _extract_themes(text: str) -> list:
    """Bulleted list items under a heading/line containing 'theme'."""
    themes = []
    in_theme_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if re.search(r"theme", stripped, re.I) and (
            stripped.startswith("#") or stripped.rstrip().endswith(":")
        ):
            in_theme_block = True
            continue
        if in_theme_block:
            if stripped.startswith(("-", "*")):
                theme = stripped.lstrip("-*").strip().strip("*_")
                if theme:
                    themes.append(theme)
            elif stripped == "":
                continue
            else:
                # Non-list, non-blank line ends the theme block.
                in_theme_block = False
    return themes


def _first_paragraph(text: str) -> str:
    """First non-heading, non-metadata paragraph -- used as the premise."""
    paras, current = [], []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if _META_RE.match(stripped):
            continue
        if stripped == "":
            if current:
                paras.append(" ".join(current).strip())
                current = []
            continue
        current.append(stripped.lstrip("-*").strip())
    if current:
        paras.append(" ".join(current).strip())
    for p in paras:
        if len(p) > 20:
            return p
    return paras[0] if paras else ""


def parse_synopsis(text: str) -> dict:
    meta = _collect_meta(text)
    title = meta.get("title") or _first_heading(text) or "Untitled"
    return {
        "title": title,
        "series_name": meta.get("series") or f"{title} Series",
        "pen_name": meta.get("pen name") or meta.get("author") or "Unknown Author",
        "genre": meta.get("genre") or "Fiction",
        "world_type": meta.get("world type") or meta.get("setting") or None,
        "logline": meta.get("logline") or "",
        "premise": meta.get("premise") or _first_paragraph(text),
        "themes": _extract_themes(text),
    }


def _match_chapter(line: str):
    for rx in _CHAPTER_RES:
        m = rx.match(line.strip())
        if m:
            return int(m.group(1)), m.group(2).strip().strip("*_")
    return None


def parse_outline(text: str) -> list:
    """Return an ordered list of {chapter_number, title, summary} dicts."""
    chapters = []
    current = None
    summary_lines = []

    def _flush():
        if current is not None:
            current["summary"] = " ".join(summary_lines).strip()
            chapters.append(current)

    for line in text.splitlines():
        matched = _match_chapter(line)
        if matched:
            _flush()
            num, title = matched
            current = {"chapter_number": num, "title": title, "summary": ""}
            summary_lines = []
            continue
        if current is not None:
            stripped = line.strip()
            if _HEADING_RE.match(stripped):
                # A non-chapter heading closes the current chapter block.
                _flush()
                current = None
                summary_lines = []
                continue
            if stripped:
                summary_lines.append(stripped.lstrip("-*").strip())
    _flush()
    return chapters


# ----------------------------------------------------------------------------
# Bundle construction
# ----------------------------------------------------------------------------

def build_bundle(synopsis: dict, chapters: list, series_id, book_number: int) -> dict:
    """Build an ordered list of Book Series MCP tool-call steps.

    ``series_id`` may be an integer (use an existing series) or ``None`` (create
    a new series and reference its id via the ``$series_id`` placeholder).
    """
    steps = []

    if series_id is None:
        steps.append({
            "server": "manager",
            "tool": "create_series",
            "arguments": {
                "name": synopsis["series_name"],
                "pen_name": synopsis["pen_name"],
                "genre": synopsis["genre"],
                "world_type": synopsis["world_type"],
                "description": synopsis["premise"] or synopsis["logline"],
            },
            "capture": "series_id",
        })
        series_ref = "$series_id"
    else:
        series_ref = series_id

    main_case = synopsis["premise"] or synopsis["logline"] or synopsis["title"]
    steps.append({
        "server": "manager",
        "tool": "create_series_book",
        "arguments": {
            "series_id": series_ref,
            "book_number": book_number,
            "title": synopsis["title"],
            "main_case_description": main_case,
            "target_chapters": max(len(chapters), 1),
        },
        "capture": "book_id",
    })

    for theme in synopsis["themes"]:
        steps.append({
            "server": "manager",
            "tool": "create_series_plot_thread",
            "arguments": {
                "series_id": series_ref,
                "thread_type": "series_arc",
                "title": theme,
                "description": f"Thematic arc: {theme}",
                "start_book": book_number,
            },
        })

    if chapters:
        chapter_outlines = [
            {
                "chapter_number": c["chapter_number"],
                "title": c["title"] or f"Chapter {c['chapter_number']}",
                "summary": c["summary"],
                "outline": c["summary"],
            }
            for c in chapters
        ]
        steps.append({
            "server": "writing",
            "tool": "bulk_chapter_operations",
            "arguments": {
                "book_id": "$book_id",
                "operation": "create_outline_batch",
                "operation_data": {"chapter_outlines": chapter_outlines},
            },
        })

    return {
        "meta": {
            "title": synopsis["title"],
            "series_name": synopsis["series_name"],
            "theme_count": len(synopsis["themes"]),
            "chapter_count": len(chapters),
        },
        "steps": steps,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--synopsis", default="Story_Bible/synopsis.md",
                        help="Path to synopsis markdown (default: Story_Bible/synopsis.md)")
    parser.add_argument("--outline", default="Story_Bible/outline.md",
                        help="Path to outline markdown (default: Story_Bible/outline.md)")
    parser.add_argument("--out", default="-",
                        help="Output bundle JSON path, or '-' for stdout (default: -)")
    parser.add_argument("--series-id", type=int, default=None,
                        help="Existing series id to import into. Omit to create a new series.")
    parser.add_argument("--book-number", type=int, default=1,
                        help="Book number within the series (default: 1)")
    args = parser.parse_args()

    synopsis_text = _read(Path(args.synopsis))
    outline_text = _read(Path(args.outline))

    if not synopsis_text and not outline_text:
        print(f"No source files found ({args.synopsis}, {args.outline}).", file=sys.stderr)
        return 1

    synopsis = parse_synopsis(synopsis_text)
    chapters = parse_outline(outline_text)
    bundle = build_bundle(synopsis, chapters, args.series_id, args.book_number)

    output = json.dumps(bundle, indent=2)
    if args.out == "-":
        print(output)
    else:
        Path(args.out).write_text(output + "\n", encoding="utf-8")
        print(f"Wrote import bundle to {args.out}", file=sys.stderr)
        print(f"  Title: {synopsis['title']}", file=sys.stderr)
        print(f"  Themes: {len(synopsis['themes'])}  Chapters: {len(chapters)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
