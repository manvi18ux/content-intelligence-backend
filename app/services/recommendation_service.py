"""
Recommendation Service
======================
Generates recommendations to improve content by suggesting which missing 
entities to add, prioritized by their weights and the coverage of their respective categories.
"""

from typing import Any, Dict, List

def generate_recommendations(
    missing_entities: List[Dict[str, Any]], 
    category_coverage: Dict[str, float]
) -> List[Dict[str, Any]]:
    """
    Generates deterministic recommendations based on missing entities.
    
    Priority Logic:
    1. Entities with weight >= 0.8 are 'high' priority.
    2. Others are 'medium' priority.
    3. Sort the final recommendations such that high priority is first,
       and then within priority, categories with lowest coverage rank first.
       
    Args:
        missing_entities: List of entity dicts that are missing.
        category_coverage: Dict mapping category strings to their coverage percentage (0.0 to 1.0).
        
    Returns:
        A list of top 10 recommended actions.
    """
    recommendations = []
    
    for entity in missing_entities:
        weight = entity.get("weight", 0.0)
        category = entity.get("category", "unknown")
        
        if weight >= 0.8:
            priority = "high"
            reason = "High importance missing entity"
            priority_score = 1
        else:
            priority = "medium"
            reason = "Recommended for better coverage"
            priority_score = 2
            
        coverage = category_coverage.get(category, 1.0)
        
        recommendations.append({
            "entity": entity["name"],
            "category": category,
            "reason": reason,
            "priority": priority,
            "_priority_score": priority_score,
            "_coverage": coverage,
            "_weight": weight
        })
        
    # Rank algorithms:
    # 1. priority_score (ascending: 1 'high', 2 'medium')
    # 2. category coverage (ascending: lowest coverage categories first)
    # 3. weight (descending: within same coverage, higher weights first)
    recommendations.sort(key=lambda x: (x["_priority_score"], x["_coverage"], -x["_weight"]))
    
    final_recs = []
    for rec in recommendations[:10]:
        final_recs.append({
            "entity": rec["entity"],
            "category": rec["category"],
            "reason": rec["reason"],
            "priority": rec["priority"]
        })
        
    return final_recs
