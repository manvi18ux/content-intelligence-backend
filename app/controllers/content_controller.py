"""
Content Controller
==================
Orchestrates the content intelligence pipeline, acting as the bridge between 
the API routes and the business logic services. It connects entity extraction, 
comparison, and scoring to generate the final analytical response.

HOW SERVICES CONNECT (FULL FLOW):
1. Receive Request: 
   The controller accepts the predefined `AnalyzeRequest` (content, domain).
   
2. Entity Extraction (`entity_service`):
   Passes the raw content to `extract_entities()`. This service normalizes the text, 
   generates n-grams, and matches them against our domain aliases. It returns a list 
   of found canonical entity names.

3. Comparison (`comparison_service`):
   Passes the extracted names and the domain to `compare_entities()`. This service 
   flattens the entire domain schema and cross-references it with the extracted list 
   using a high-speed set lookup. It partitions the data into exactly what was `matched` 
   and what is `missing`.

4. Scoring (`scoring_service`):
   The partitioned lists (`matched` and `missing`) and the original content string 
   are passed to `compute_scores()`. The scoring engine deterministically computes 
   density, categorical coverage ratios, and high-priority action items.

5. Combine Results:
   The outputs are aggregated into a single `AnalyzeResponse` strictly matching 
   our formalized Pydantic schema schemas/intelligence.py.
"""

import logging
from app.schemas.intelligence import AnalyzeRequest, AnalyzeResponse
from app.services.entity_service import extract_entities
from app.services.comparison_service import compare_entities
from app.services.scoring_service import compute_scores

logger = logging.getLogger("content_intelligence.controller")

def analyze_content(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Executes the intelligence analysis pipeline to evaluate content quality.

    Args:
        request: The structured request payload containing raw text and domain target.

    Returns:
        AnalyzeResponse: Structured metrics mapped to the Pydantic schema.
        
    Raises:
        ValueError: If the domain is unsupported or processing fails.
    """
    content = request.content
    domain = request.domain

    try:
        # Step 1: Extract entities from the text (find canonical occurrences)
        extraction_result = extract_entities(content, domain)
        extracted_names = extraction_result.get("matched_entity_names", [])

        # Step 2: Compare against domain map (separate into matched and missing)
        comparison_result = compare_entities(extracted_names, domain)
        matched_entities = comparison_result.get("matched_entities", [])
        missing_entities = comparison_result.get("missing_entities", [])

        # Step 3: Compute deterministic heuristics and coverage scores
        scores = compute_scores(matched_entities, missing_entities, content)

        # Step 4: Construct the final structured response
        return AnalyzeResponse(
            domain=domain,
            coverage_score=scores.get("coverage_score", 0.0),
            weighted_coverage_score=scores.get("weighted_coverage_score", 0.0),
            category_coverage=scores.get("category_coverage", {}),
            matched_entities=matched_entities,
            missing_entities=missing_entities,
            high_priority_missing=scores.get("high_priority_missing", []),
            novelty_score=scores.get("novelty_score", 0.0),
            entity_density=scores.get("entity_density", 0.0)
        )

    except ValueError as val_err:
        logger.error(f"Validation error during content analysis: {str(val_err)}")
        raise val_err
    except Exception as ex:
        logger.error(f"Unexpected error during content analysis: {str(ex)}")
        raise ValueError(f"Analysis pipeline failed: {str(ex)}")
