# =============================================================================
# Services Package
# =============================================================================
# Each service module encapsulates a single responsibility:
#   - entity_service:         Extract domain entities from text
#   - comparison_service:     Compare extracted entities against domain maps
#   - scoring_service:        Compute coverage and novelty scores
#   - prediction_service:     Rule-based ranking prediction
#   - recommendation_service: Generate improvement recommendations
#   - openai_service:         OpenAI API integration for content generation
#
# Services are independent and stateless — they receive input, process it,
# and return output. No service should depend on another directly;
# orchestration happens in the controller layer.
# =============================================================================
