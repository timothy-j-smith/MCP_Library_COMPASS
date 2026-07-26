"""Mathematical fiction analysis helpers for Fiction Reverse Engineering MCP."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

TENSION_WORDS = {
    "blood",
    "danger",
    "dead",
    "death",
    "fear",
    "gun",
    "kill",
    "knife",
    "murder",
    "scream",
    "threat",
    "violence",
    "weapon",
    "wound",
    "chase",
    "escape",
    "terrified",
    "panic",
    "secret",
    "lie",
    "betray",
    "trap",
    "ambush",
    "shot",
    "crash",
}

REVEAL_PATTERNS = [
    r"\brealized\b",
    r"\bdiscovered\b",
    r"\brevealed\b",
    r"\bturned out\b",
    r"\bit was\b.+\ball along\b",
    r"\bsuddenly\b",
    r"\btruth\b",
    r"\bsecret\b",
    r"\bfound out\b",
    r"\blearned that\b",
]

DIALOGUE_TAG_RE = re.compile(
    r"\b(said|asked|whispered|shouted|muttered|replied|answered|yelled|cried|snapped)\b",
    re.IGNORECASE,
)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"[A-Za-z']+")
QUOTE_BLOCKS_RE = re.compile(r'"([^"]+)"')


USAGE_WARNING = (
    "⚠️ LEARNING TOOL WARNING: Use these patterns to learn craft, not to copy formulas. "
    "Maintain your unique voice. Formulas are guides, not templates."
)


def _words(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def _sentences(text: str) -> list[str]:
    parts = SENTENCE_SPLIT_RE.split(text.strip())
    return [p.strip() for p in parts if p.strip()]


def _paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "untitled"


def analyze_pacing_metrics(text: str) -> dict[str, Any]:
    words = _words(text)
    sentences = _sentences(text)
    paragraphs = _paragraphs(text)
    word_count = max(len(words), 1)

    tension_hits = sum(1 for w in words if w in TENSION_WORDS)
    tension_frequency = tension_hits / word_count

    reveal_hits = 0
    for pattern in REVEAL_PATTERNS:
        reveal_hits += len(re.findall(pattern, text, flags=re.IGNORECASE))
    reveal_frequency = reveal_hits / max(len(sentences), 1)

    quote_blocks = QUOTE_BLOCKS_RE.findall(text)
    dialogue_words = sum(len(_words(q)) for q in quote_blocks)
    dialogue_frequency = dialogue_words / word_count

    sentence_lengths = [len(_words(s)) for s in sentences] or [0]
    avg_sentence_len = sum(sentence_lengths) / len(sentence_lengths)
    if len(sentence_lengths) > 1:
        variance = sum((x - avg_sentence_len) ** 2 for x in sentence_lengths) / len(
            sentence_lengths
        )
        sentence_variation = math.sqrt(variance)
    else:
        sentence_variation = 0.0

    # Simple tension curve: tension density per paragraph (normalized 0-1)
    curve: list[float] = []
    for para in paragraphs or [text]:
        pwords = _words(para)
        if not pwords:
            curve.append(0.0)
            continue
        hits = sum(1 for w in pwords if w in TENSION_WORDS)
        curve.append(round(min(1.0, hits / max(len(pwords) * 0.05, 1)), 3))

    if tension_frequency >= 0.02:
        tension_pattern = "high"
    elif tension_frequency >= 0.008:
        tension_pattern = "moderate"
    else:
        tension_pattern = "low"

    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "tension_pattern": tension_pattern,
        "tension_frequency": round(tension_frequency, 4),
        "tension_hits": tension_hits,
        "reveal_frequency": round(reveal_frequency, 4),
        "reveal_hits": reveal_hits,
        "dialogue_frequency": round(dialogue_frequency, 4),
        "dialogue_word_ratio": round(dialogue_frequency, 4),
        "avg_sentence_length": round(avg_sentence_len, 2),
        "sentence_variation": round(sentence_variation, 2),
        "tension_curve": curve,
    }


def extract_dialogue_metrics(text: str) -> dict[str, Any]:
    quotes = QUOTE_BLOCKS_RE.findall(text)
    tags = DIALOGUE_TAG_RE.findall(text)
    tag_counts = Counter(t.lower() for t in tags)
    quote_lengths = [len(_words(q)) for q in quotes] or [0]
    avg_quote_len = sum(quote_lengths) / len(quote_lengths)

    # Beat heuristic: short narrative between quotes
    between = re.split(r'"[^"]+"', text)
    beat_lengths = [len(_words(b)) for b in between if b.strip()]
    avg_beat = sum(beat_lengths) / len(beat_lengths) if beat_lengths else 0.0

    return {
        "dialogue_exchanges": len(quotes),
        "avg_dialogue_length_words": round(avg_quote_len, 2),
        "dialogue_tags": dict(tag_counts.most_common(12)),
        "tag_total": len(tags),
        "avg_beat_words_between_dialogue": round(avg_beat, 2),
        "said_ratio": round(
            tag_counts.get("said", 0) / max(sum(tag_counts.values()), 1), 3
        ),
    }


def extract_chapter_metrics(text: str) -> dict[str, Any]:
    paragraphs = _paragraphs(text)
    pacing = analyze_pacing_metrics(text)
    dialogue = extract_dialogue_metrics(text)

    opening = paragraphs[0] if paragraphs else ""
    closing = paragraphs[-1] if paragraphs else ""
    opening_hook = bool(
        re.search(
            r"\b(blood|dead|gun|secret|why|never|always|remember)\b",
            opening,
            re.IGNORECASE,
        )
    )
    closing_hook = bool(
        re.search(
            r"\b(but|unless|until|tomorrow|next|wait|listen|then)\b|[.!?]\s*$",
            closing,
            re.IGNORECASE,
        )
    )

    # Rough act thirds by paragraph count
    n = max(len(paragraphs), 1)
    thirds = [paragraphs[0 : n // 3], paragraphs[n // 3 : 2 * n // 3], paragraphs[2 * n // 3 :]]
    act_tension = []
    for chunk in thirds:
        chunk_text = "\n\n".join(chunk) if chunk else ""
        act_tension.append(analyze_pacing_metrics(chunk_text)["tension_frequency"])

    return {
        "paragraph_count": len(paragraphs),
        "opening_hook_signal": opening_hook,
        "closing_hook_signal": closing_hook,
        "act_tension_frequencies": [round(x, 4) for x in act_tension],
        "pacing": pacing,
        "dialogue": dialogue,
    }


def build_formula(
    title: str,
    author: str,
    text: str,
) -> dict[str, Any]:
    pacing = analyze_pacing_metrics(text)
    dialogue = extract_dialogue_metrics(text)
    chapter = extract_chapter_metrics(text)
    return {
        "title": title,
        "author": author,
        "slug": slugify(f"{title}-{author}"),
        "disclaimer": (
            "This formula is a LEARNING TOOL, not a template. "
            "Use to understand patterns, not to copy formulas. "
            "Maintain your unique voice."
        ),
        "pacing": pacing,
        "dialogue": dialogue,
        "chapter": {
            "opening_hook_signal": chapter["opening_hook_signal"],
            "closing_hook_signal": chapter["closing_hook_signal"],
            "act_tension_frequencies": chapter["act_tension_frequencies"],
            "paragraph_count": chapter["paragraph_count"],
        },
        "patterns": {
            "tension_pattern": pacing["tension_pattern"],
            "reveal_cadence": pacing["reveal_frequency"],
            "dialogue_density": pacing["dialogue_frequency"],
            "sentence_variation": pacing["sentence_variation"],
        },
    }


def compare_to_formula(text: str, formula: dict[str, Any]) -> dict[str, Any]:
    current = analyze_pacing_metrics(text)
    dialogue = extract_dialogue_metrics(text)
    target_pacing = formula.get("pacing", {})
    target_dialogue = formula.get("dialogue", {})

    def pct_diff(a: float, b: float) -> float:
        if b == 0:
            return 0.0 if a == 0 else 1.0
        return abs(a - b) / abs(b)

    metrics = {
        "tension_frequency": (
            current["tension_frequency"],
            float(target_pacing.get("tension_frequency", 0)),
        ),
        "reveal_frequency": (
            current["reveal_frequency"],
            float(target_pacing.get("reveal_frequency", 0)),
        ),
        "dialogue_frequency": (
            current["dialogue_frequency"],
            float(target_pacing.get("dialogue_frequency", 0)),
        ),
        "avg_sentence_length": (
            current["avg_sentence_length"],
            float(target_pacing.get("avg_sentence_length", 0)),
        ),
        "sentence_variation": (
            current["sentence_variation"],
            float(target_pacing.get("sentence_variation", 0)),
        ),
        "avg_dialogue_length_words": (
            dialogue["avg_dialogue_length_words"],
            float(target_dialogue.get("avg_dialogue_length_words", 0)),
        ),
    }

    deviations = []
    scores = []
    for name, (actual, expected) in metrics.items():
        diff = pct_diff(actual, expected)
        scores.append(max(0.0, 1.0 - min(diff, 1.0)))
        severity = "critical" if diff >= 0.5 else "moderate" if diff >= 0.25 else "minor"
        if diff >= 0.15:
            deviations.append(
                {
                    "metric": name,
                    "actual": actual,
                    "expected": expected,
                    "relative_diff": round(diff, 3),
                    "severity": severity,
                    "recommendation": (
                        f"Adjust {name.replace('_', ' ')} toward {expected} "
                        f"(currently {actual}). Use as a guide, not a hard rule."
                    ),
                }
            )

    match_score = round(sum(scores) / max(len(scores), 1), 3)
    return {
        "formula_title": formula.get("title"),
        "formula_author": formula.get("author"),
        "match_score": match_score,
        "current_pacing": current,
        "deviations": deviations,
        "disclaimer": formula.get("disclaimer"),
    }
