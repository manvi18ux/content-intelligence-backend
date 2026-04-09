from typing import Dict, List
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    """Request model for content intelligence analysis."""
    content: str = Field(..., description="The textual content to analyze.")
    domain: str = Field(..., description="The domain to evaluate against (e.g., 'finance', 'manufacturing').")

class GenerateRequest(BaseModel):
    """Request model for content generation pipeline."""
    topic: str = Field(..., description="The topic to generate content for.")
    domain: str = Field(..., description="The domain to evaluate against.")

class Entity(BaseModel):
    """Represents a domain entity with its attributes."""
    name: str = Field(..., description="The canonical name of the entity.")
    category: str = Field(..., description="The category this entity belongs to.")
    weight: float = Field(..., ge=0.0, le=1.0, description="The importance weight of the entity (0.0 to 1.0).")

class AnalyzeResponse(BaseModel):
    """Response model containing all intelligence metrics."""
    domain: str = Field(
        ...,
        description="The domain that was evaluated against."
    )
    coverage_score: float = Field(
        ..., 
        description="Percentage of extracted entities vs total available entities (0-100)."
    )
    weighted_coverage_score: float = Field(
        ..., 
        description="Coverage measured by the sum of matched weights vs total weights (0-100)."
    )
    category_coverage: Dict[str, float] = Field(
        ..., 
        description="Dictionary mapping each category to its coverage percentage."
    )
    matched_entities: List[Entity] = Field(
        ...,
        description="List of domain entities that were found in the content."
    )
    missing_entities: List[Entity] = Field(
        ..., 
        description="List of domain entities that were not found in the content."
    )
    high_priority_missing: List[Entity] = Field(
        ..., 
        description="Missing entities with a weight >= 0.8."
    )
    novelty_score: float = Field(
        ..., 
        description="Score based on heuristics regarding density and balance."
    )
    entity_density: float = Field(
        ..., 
        description="Ratio of total matched entities to total words in the content."
    )
