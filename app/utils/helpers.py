# =============================================================================
# Text Processing Utilities
# =============================================================================
# Pure utility functions for text normalization and n-gram generation.
# These are the building blocks used by entity_service.py for matching.
#
# Design decisions:
#   - No external NLP libraries (no spaCy, NLTK, etc.)
#   - Simple but effective: lowercasing + punctuation removal + n-grams
#   - Stateless pure functions — easy to test and reason about
#
# How n-gram matching works:
#   Many domain entities are multi-word phrases (e.g., "supply chain",
#   "risk management", "quality control"). Simple word-by-word matching
#   would miss these. N-grams solve this by generating all contiguous
#   sequences of 1, 2, and 3 words from the text:
#
#   Text: "effective supply chain management"
#   1-grams: ["effective", "supply", "chain", "management"]
#   2-grams: ["effective supply", "supply chain", "chain management"]
#   3-grams: ["effective supply chain", "supply chain management"]
#
#   We then check each n-gram against our entity map to find matches.
# =============================================================================

import re
import string
from typing import List, Set


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent entity matching.

    Steps:
      1. Convert to lowercase (case-insensitive matching)
      2. Replace hyphens and slashes with spaces (e.g., "AI-driven" → "ai driven")
      3. Remove all other punctuation (commas, periods, quotes, etc.)
      4. Collapse multiple spaces into one
      5. Strip leading/trailing whitespace

    Args:
        text: Raw input text

    Returns:
        Cleaned, lowercase text ready for tokenization

    Example:
        >>> normalize_text("Risk Management & Portfolio Optimization!")
        "risk management portfolio optimization"
    """
    if not text:
        return ""

    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Replace hyphens, slashes, and ampersands with spaces
    # This ensures "AI-driven" becomes "ai driven" and matches as two tokens
    text = re.sub(r"[-/&]", " ", text)

    # Step 3: Remove remaining punctuation
    # We keep alphanumeric characters and spaces only
    text = re.sub(r"[^\w\s]", "", text)

    # Step 4: Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Step 5: Strip
    return text.strip()


def tokenize(text: str) -> List[str]:
    """
    Split normalized text into individual word tokens.

    Args:
        text: Normalized text (should be passed through normalize_text first)

    Returns:
        List of word tokens

    Example:
        >>> tokenize("risk management and portfolio optimization")
        ["risk", "management", "and", "portfolio", "optimization"]
    """
    if not text:
        return []

    return text.split()


def generate_ngrams(text: str, max_n: int = 3) -> List[str]:
    """
    Generate all n-grams (1-gram through max_n-gram) from normalized text.

    This is the core of our entity matching strategy. By generating n-grams
    of different sizes, we can match both single-word entities ("derivatives")
    and multi-word entities ("supply chain management").

    Args:
        text: Normalized text (should be passed through normalize_text first)
        max_n: Maximum n-gram size (default: 3 for phrases up to 3 words)

    Returns:
        List of all n-grams, ordered from longest to shortest.
        Longest-first ordering enables greedy matching — we prefer matching
        "supply chain management" over "supply chain" + "management".

    Example:
        >>> generate_ngrams("lean supply chain")
        [
            "lean supply chain",    # 3-gram
            "lean supply",          # 2-grams
            "supply chain",
            "lean",                 # 1-grams
            "supply",
            "chain",
        ]
    """
    tokens = tokenize(text)

    if not tokens:
        return []

    ngrams = []

    # Generate n-grams from largest to smallest (greedy matching order)
    # This way, when we iterate through n-grams for matching, we'll
    # prefer longer (more specific) matches over shorter ones
    for n in range(min(max_n, len(tokens)), 0, -1):
        for i in range(len(tokens) - n + 1):
            ngram = " ".join(tokens[i : i + n])
            ngrams.append(ngram)

    return ngrams


def deduplicate_preserve_order(items: List[str]) -> List[str]:
    """
    Remove duplicates from a list while preserving insertion order.

    Args:
        items: List with potential duplicates

    Returns:
        Deduplicated list maintaining original order

    Example:
        >>> deduplicate_preserve_order(["a", "b", "a", "c", "b"])
        ["a", "b", "c"]
    """
    seen: Set[str] = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
