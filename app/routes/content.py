from fastapi import APIRouter, HTTPException
from app.schemas.intelligence import AnalyzeRequest, GenerateRequest
from app.services.generation_service import generate_content as generate_initial_content
from app.services.improvement_service import improve_content
from app.services.entity_service import extract_entities
from app.services.comparison_service import compare_entities
from app.services.scoring_service import compute_scores
from app.services.recommendation_service import generate_recommendations
from app.services.prediction_service import predict_ranking

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /api/v1/analyze
# ---------------------------------------------------------------------------
@router.post(
    "/analyze",
    summary="Analyze Content",
    description=(
        "Accepts content text and a domain (finance/manufacturing), extracts "
        "domain entities, computes coverage and novelty scores, predicts ranking, "
        "and identifies missing important entities."
    ),
)
async def analyze_content(request: AnalyzeRequest):
    """
    Analyze content against a domain entity map.

    Pipeline: extract → compare → score → recommend → predict
    """
    try:
        # Step 1: Extract entities
        extracted = extract_entities(request.content, request.domain)

        # Step 2: Compare
        comparison = compare_entities(extracted["matched_entity_names"], request.domain)
        matched = comparison["matched_entities"]
        missing = comparison["missing_entities"]

        # Step 3: Score
        scores = compute_scores(matched, missing, request.content)

        # Step 4: Recommend
        recommendations = generate_recommendations(missing, scores["category_coverage"])

        # Step 5: Predict
        prediction = predict_ranking(
            scores["coverage_score"], 
            scores["weighted_coverage_score"], 
            scores["novelty_score"]
        )

        # Step 6: Return response
        return {
            "domain": request.domain,
            "coverage_score": scores["coverage_score"],
            "weighted_coverage_score": scores["weighted_coverage_score"],
            "category_coverage": scores["category_coverage"],
            "matched_entities": matched,
            "missing_entities": missing,
            "high_priority_missing": scores["high_priority_missing"],
            "novelty_score": scores["novelty_score"],
            "entity_density": scores["entity_density"],
            "recommendations": recommendations,
            "prediction": prediction,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# POST /api/v1/generate
# ---------------------------------------------------------------------------
@router.post(
    "/generate",
    summary="Generate Optimized Content",
    description=(
        "Accepts a topic and domain, generates initial content via AI, "
        "runs the full analysis pipeline, improves content based on "
        "recommendations, and returns the optimized result."
    ),
)
async def generate_content_endpoint(request: GenerateRequest):
    try:
        # Step 1: Generate initial content
        initial_content = generate_initial_content(request.topic, request.domain)
        
        # Step 2: Run analyze pipeline
        analyze_req_1 = AnalyzeRequest(content=initial_content, domain=request.domain)
        initial_analysis = await analyze_content(analyze_req_1)
        
        # Step 3: Extract recommendations and prediction
        recommendations = initial_analysis.get("recommendations", [])
        prediction = initial_analysis.get("prediction", {})
        
        # Step 4: Improve content
        final_content = improve_content(initial_content, recommendations)
        
        # Step 5: Run analyze again (second pass)
        analyze_req_2 = AnalyzeRequest(content=final_content, domain=request.domain)
        final_analysis = await analyze_content(analyze_req_2)
        
        # Step 6: Return final result
        return {
            "topic": request.topic,
            "domain": request.domain,
            "initial_content": initial_content,
            "final_content": final_content,
            "initial_analysis": initial_analysis,
            "final_analysis": final_analysis,
            "recommendations": recommendations,
            "prediction": prediction,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))