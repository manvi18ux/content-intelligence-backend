# =============================================================================
# Entity Extraction Service
# =============================================================================
# Extracts domain-specific entities from text using n-gram matching.
#
# HOW MATCHING WORKS — STEP BY STEP:
#
#   1. BUILD LOOKUP INDEX
#      Before matching, we build a reverse lookup from the entity map:
#        "risk management"  → {name, category, weight}
#        "risk mitigation"  → {name: "risk management", ...}  (alias → canonical)
#        "risk control"     → {name: "risk management", ...}  (alias → canonical)
#
#      This means every alias points back to its canonical entity.
#
#   2. NORMALIZE INPUT TEXT
#      The raw text is normalized (lowercase, punctuation removed).
#
#   3. GENERATE N-GRAMS
#      We generate all 1-gram, 2-gram, and 3-gram sequences from the text.
#      N-grams are ordered longest-first for greedy matching.
#
#   4. MATCH N-GRAMS AGAINST INDEX
#      Each n-gram is checked against the lookup index.
#      If a match is found:
#        - We record the CANONICAL entity name (not the alias)
#        - We track which n-gram (alias) was actually found in text
#        - We skip overlapping matches to avoid double-counting
#
#   5. RETURN STRUCTURED RESULTS
#      Each matched entity includes:
#        - name: canonical entity name
#        - category: which domain category it belongs to
#        - weight: importance score (used by scoring service later)
#        - matched_term: the actual text that triggered the match
#
# HOW NORMALIZATION WORKS:
#   When text says "Our ROI exceeded expectations", the flow is:
#     1. Normalize: "our roi exceeded expectations"
#     2. N-grams include: "roi"
#     3. Lookup: "roi" → alias of "return on investment"
#     4. Result: {name: "return on investment", matched_term: "roi", ...}
#
#   The entity is always reported by its canonical name regardless of
#   which alias was found. This prevents duplication in reports.
#
# =============================================================================

import logging
from typing import Any, Dict, List, Optional, Set, Tuple

from app.domain.entity_maps import get_all_entities_flat, get_domain_map
from app.utils.helpers import deduplicate_preserve_order, generate_ngrams, normalize_text

logger = logging.getLogger("content_intelligence.entity_service")


# ---------------------------------------------------------------------------
# Type definitions for clarity
# ---------------------------------------------------------------------------
# A single matched entity
MatchedEntity = Dict[str, Any]

# The full extraction result
ExtractionResult = Dict[str, Any]


def _build_lookup_index(
    domain: str,
) -> Dict[str, Dict[str, Any]]:
    """
    Build a reverse lookup index from entity map.

    Creates a dictionary where every possible matching term (entity name +
    all aliases) maps to the canonical entity info.

    Args:
        domain: Domain name ("finance" or "manufacturing")

    Returns:
        Dict mapping lowercase term → {name, category, weight}

    Example output:
        {
            "risk management": {"name": "risk management", "category": "risk_management", "weight": 1.0},
            "risk mitigation": {"name": "risk management", "category": "risk_management", "weight": 1.0},
            "risk control":    {"name": "risk management", "category": "risk_management", "weight": 1.0},
            ...
        }
    """
    index: Dict[str, Dict[str, Any]] = {}
    all_entities = get_all_entities_flat(domain)

    for entity in all_entities:
        canonical_info = {
            "name": entity["name"],
            "category": entity["category"],
            "weight": entity["weight"],
        }

        # Index the canonical name itself
        normalized_name = normalize_text(entity["name"])
        index[normalized_name] = canonical_info

        # Index every alias → points to same canonical entity
        for alias in entity.get("aliases", []):
            normalized_alias = normalize_text(alias)
            index[normalized_alias] = canonical_info

    logger.debug(f"Built lookup index for '{domain}' with {len(index)} terms")
    return index


def extract_entities(
    content: str,
    domain: str,
) -> ExtractionResult:
    """
    Extract domain-specific entities from content text.

    This is the main entry point for entity extraction. It:
      1. Builds the lookup index for the domain
      2. Normalizes the input text
      3. Generates n-grams from the text
      4. Matches n-grams against the index (greedy, longest-first)
      5. Returns structured results

    Args:
        content: Raw text content to analyze
        domain: Domain name ("finance" or "manufacturing")

    Returns:
        ExtractionResult dict with:
          - domain: the domain used
          - total_entities_in_domain: how many entities exist in the map
          - matched_entities: list of matched entity dicts
          - matched_count: number of unique entities matched
          - matched_entity_names: list of canonical names matched

    Example:
        >>> result = extract_entities(
        ...     "Our risk management strategy uses hedging and DCF analysis.",
        ...     "finance"
        ... )
        >>> result["matched_count"]
        3  # risk management, hedging, discounted cash flow
    """
    # Validate inputs
    if not content or not content.strip():
        return _empty_result(domain)

    # Step 1: Build the lookup index (term → canonical entity)
    lookup = _build_lookup_index(domain)

    # Step 2: Normalize the text
    normalized = normalize_text(content)

    # Step 3: Generate n-grams (longest first for greedy matching)
    ngrams = generate_ngrams(normalized, max_n=3)

    # Step 4: Match n-grams against the index
    matched_entities: List[MatchedEntity] = []
    seen_canonical_names: Set[str] = set()  # Prevent duplicate canonical matches
    consumed_positions: Set[int] = set()    # Track consumed word positions

    # Tokenize for position tracking
    tokens = normalized.split()

    for ngram in ngrams:
        if ngram not in lookup:
            continue

        # Find the position of this n-gram in the token list
        ngram_tokens = ngram.split()
        ngram_len = len(ngram_tokens)
        position = _find_ngram_position(tokens, ngram_tokens, consumed_positions)

        if position is None:
            continue  # This n-gram's tokens are already consumed

        entity_info = lookup[ngram]
        canonical_name = entity_info["name"]

        # Skip if we already matched this canonical entity
        # (e.g., "ROI" and "return on investment" both in text — count once)
        if canonical_name in seen_canonical_names:
            continue

        # Record the match
        seen_canonical_names.add(canonical_name)
        matched_entities.append({
            "name": canonical_name,
            "category": entity_info["category"],
            "weight": entity_info["weight"],
            "matched_term": ngram,  # The actual text fragment that matched
        })

        # Mark these token positions as consumed
        for i in range(position, position + ngram_len):
            consumed_positions.add(i)

        logger.debug(f"Matched: '{ngram}' → '{canonical_name}' (weight={entity_info['weight']})")

    # Step 5: Sort by weight (most important first) then alphabetically
    matched_entities.sort(key=lambda e: (-e["weight"], e["name"]))

    # Count total entities in the domain map
    all_domain_entities = get_all_entities_flat(domain)
    total = len(all_domain_entities)

    logger.info(
        f"Entity extraction complete: {len(matched_entities)}/{total} entities matched "
        f"in domain '{domain}'"
    )

    return {
        "domain": domain,
        "total_entities_in_domain": total,
        "matched_entities": matched_entities,
        "matched_count": len(matched_entities),
        "matched_entity_names": [e["name"] for e in matched_entities],
    }


def _find_ngram_position(
    tokens: List[str],
    ngram_tokens: List[str],
    consumed: Set[int],
) -> Optional[int]:
    """
    Find the first unconsumed position of an n-gram in the token list.

    This prevents double-counting: if "supply chain" was already matched
    as part of "supply chain management", those tokens are consumed and
    won't match again.

    Args:
        tokens: Full list of tokens from the text
        ngram_tokens: Tokens of the n-gram we're looking for
        consumed: Set of already-consumed token positions

    Returns:
        Starting position (index) if found, None otherwise
    """
    ngram_len = len(ngram_tokens)

    for i in range(len(tokens) - ngram_len + 1):
        # Check if all positions are unconsumed
        if any(i + j in consumed for j in range(ngram_len)):
            continue

        # Check if tokens match
        if tokens[i : i + ngram_len] == ngram_tokens:
            return i

    return None


def _empty_result(domain: str) -> ExtractionResult:
    """Return an empty extraction result for edge cases (empty text, etc.)."""
    try:
        all_entities = get_all_entities_flat(domain)
        total = len(all_entities)
    except ValueError:
        total = 0

    return {
        "domain": domain,
        "total_entities_in_domain": total,
        "matched_entities": [],
        "matched_count": 0,
        "matched_entity_names": [],
    }
