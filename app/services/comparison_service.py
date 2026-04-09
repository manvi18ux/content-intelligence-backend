"""
Comparison Service
==================
Compares extracted entities against a domain entity map to identify matched and missing entities.

WHY FLATTENING IS NEEDED:
The original domain entity map is hierarchical (domain -> category -> entities). 
To compare extracted entities against the entire domain, traversing nested structures 
repeatedly is inefficient. Flattening converts the hierarchy into a single, uniform 
1D list (where each entity retains its category as an attribute). This allows standard, 
linear operations without recursive or nested loops.

HOW LOOKUP IMPROVES PERFORMANCE:
If we iteratively search for each domain entity in a list of extracted entities, 
the time complexity is O(N * M), where N is the number of domain entities and M 
is the number of extracted entities. 
By converting the `extracted_entities` list into a hash set (lookup structure), 
we achieve O(1) constant-time membership lookups. This drops the comparison 
time complexity to O(N + M), ensuring high efficiency even with large domain maps.
"""

from typing import Any, Dict, List, Set
from app.domain.entity_maps import get_all_entities_flat

def compare_entities(extracted_entities: List[str], domain: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Compare extracted entity names with the domain entity map.

    Args:
        extracted_entities: A list of normalized entity names found in the text.
        domain: The domain name (e.g., 'finance', 'manufacturing').

    Returns:
        A dictionary containing:
        - "matched_entities": List of entity objects present in the extraction.
        - "missing_entities": List of entity objects NOT present in the extraction.
        Each entity object preserves its 'name', 'category', and 'weight'.
    """
    # 1. Flatten entity map using the existing helper function
    # Each item in `flat_domain_entities` has 'name', 'category', 'weight', 'aliases'
    flat_domain_entities = get_all_entities_flat(domain)

    # 2. Create lookup structure
    # Converts list to a set for O(1) lookups
    extracted_lookup: Set[str] = set(extracted_entities)

    matched_entities: List[Dict[str, Any]] = []
    missing_entities: List[Dict[str, Any]] = []

    # 3. Compare matched vs missing
    for entity in flat_domain_entities:
        # Create output object preserving only name, category, and weight
        entity_obj = {
            "name": entity["name"],
            "category": entity["category"],
            "weight": entity["weight"]
        }

        # 4. Check for membership using the lookup structure
        if entity["name"] in extracted_lookup:
            matched_entities.append(entity_obj)
        else:
            missing_entities.append(entity_obj)

    return {
        "matched_entities": matched_entities,
        "missing_entities": missing_entities
    }
