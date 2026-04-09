"""
Prediction Service
==================
Predicts the ranking potential of the content based on its intelligence metrics.
"""

from typing import Any, Dict

def predict_ranking(
    coverage_score: float, 
    weighted_score: float, 
    novelty_score: float
) -> Dict[str, Any]:
    """
    Predicts content ranking potential using deterministic heuristics.
    
    Args:
        coverage_score: Raw percentage of domain entities found.
        weighted_score: Coverage score incorporating entity weights.
        novelty_score: Combined metric of coverage and entity density.
        
    Returns:
        Dict containing prediction and confidence.
    """
    
    if weighted_score > 15 and novelty_score > 50:
        ranking = "High Ranking Potential"
    elif 8 <= weighted_score <= 15:
        ranking = "Moderate Ranking Potential"
    else:
        ranking = "Low Ranking Potential"
        
    return {
        "ranking": ranking,
        "confidence_score": weighted_score
    }
