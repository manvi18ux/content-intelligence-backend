"""
Scoring Service
===============
Evaluates content quality using multiple deterministic scoring metrics without external ML or APIs.

EXPLANATION OF SCORES:
A. Coverage Score:
   The simple percentage of domain entities found in the content. It treats all entities equally.
   Useful for understanding absolute breadth of coverage.

B. Weighted Coverage Score:
   Takes into account the `weight` (importance) of each entity. 
   Why it's important: Simply mentioning 10 peripheral terms (weight=0.1) shouldn't score as high 
   as mentioning 5 absolutely critical core pillars (weight=1.0). Weighted coverage ensures that 
   content is rewarded for hitting the most important concepts, preventing authors from "gaming" 
   the score with low-value vocabulary.

C. Category Coverage:
   A sub-score mapping each domain category to its coverage percentage. Essential for identifying 
   blind spots (e.g., checking if an article completely missed the 'Risk Management' pillar).

D. High Priority Missing:
   Actionable feedback. Filters missing entities with a weight >= 0.8. These are the "must-have" 
   concepts the author should add to improve the content dramatically.

E. Entity Density:
   The ratio of matched entities to total words. Identifies if content is sparse (too much fluff)
   or over-stuffed (keyword spamming).

F. Novelty Score:
   A heuristic quality score. It uses the Coverage Score as a baseline and modifies it based 
   on Entity Density. It penalizes dangerously low or high density, while rewarding a moderate, 
   natural inclusion of domain terms.
"""

from typing import Any, Dict, List

def compute_scores(
    matched_entities: List[Dict[str, Any]],
    missing_entities: List[Dict[str, Any]],
    content: str
) -> Dict[str, Any]:
    """
    Computes all intelligence metrics based on extracted entities and missing data.

    Args:
        matched_entities: List of entity objects found in the content.
        missing_entities: List of entity objects NOT found in the content.
        content: The raw string of the analyzed content (used for density).

    Returns:
        Dict containing coverage, weights, category stats, and heuristics.
    """
    all_entities = matched_entities + missing_entities
    total_entities = len(all_entities)

    if total_entities == 0:
        return _empty_scores()

    # 1. Coverage Score
    coverage_score = (len(matched_entities) / total_entities) * 100.0

    # 2. Weighted Coverage Score
    total_weight = sum([e.get("weight", 0.0) for e in all_entities])
    matched_weight = sum([e.get("weight", 0.0) for e in matched_entities])
    weighted_coverage_score = (matched_weight / total_weight * 100.0) if total_weight > 0 else 0.0

    # 3. Category Coverage
    category_counts_total: Dict[str, int] = {}
    category_counts_matched: Dict[str, int] = {}

    for e in all_entities:
        cat = e.get("category", "unknown")
        category_counts_total[cat] = category_counts_total.get(cat, 0) + 1
        if cat not in category_counts_matched:
            category_counts_matched[cat] = 0

    for e in matched_entities:
        cat = e.get("category", "unknown")
        category_counts_matched[cat] += 1

    category_coverage: Dict[str, float] = {}
    for cat, total in category_counts_total.items():
        if total > 0:
            category_coverage[cat] = category_counts_matched[cat] / total
        else:
            category_coverage[cat] = 0.0

    # 4. High Priority Missing
    high_priority_missing = [e for e in missing_entities if e.get("weight", 0.0) >= 0.8]
    # Sort by weight descending so the most important missing entities are first
    high_priority_missing.sort(key=lambda x: x.get("weight", 0.0), reverse=True)

    # 5. Entity Density
    # Simple whitespace split to approximate word count (fast & no external dependencies)
    words = [w for w in content.split() if w.strip()]
    total_words = len(words)
    
    entity_density = len(matched_entities) / total_words if total_words > 0 else 0.0
    # Clamp entity density to 0.1 to avoid artificially high values for short texts
    entity_density = min(entity_density, 0.1)

    # 6. Novelty Score (heuristic)
    # Convert density (max 0.1) to a 0-100 scale for balance
    density_balance = entity_density * 1000.0
    novelty_score = (coverage_score + density_balance) / 2.0

    # Cap score between 0.0 and 100.0
    novelty_score = max(0.0, min(100.0, novelty_score))

    return {
        "coverage_score": round(coverage_score, 2),
        "weighted_coverage_score": round(weighted_coverage_score, 2),
        "category_coverage": category_coverage,
        "high_priority_missing": high_priority_missing,
        "novelty_score": round(novelty_score, 2),
        "entity_density": round(entity_density, 4)
    }

def _empty_scores() -> Dict[str, Any]:
    """Fallback when no entities exist or content is entirely empty."""
    return {
        "coverage_score": 0.0,
        "weighted_coverage_score": 0.0,
        "category_coverage": {},
        "high_priority_missing": [],
        "novelty_score": 0.0,
        "entity_density": 0.0
    }
