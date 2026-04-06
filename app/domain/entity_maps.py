# =============================================================================
# Domain Entity Maps — Finance & Manufacturing
# =============================================================================
# These maps define "what matters" in each domain. They are the knowledge base
# that powers the entire intelligence pipeline:
#
#   Entity Extraction  → matches text against these maps
#   Comparison Service → calculates what's covered vs missing
#   Scoring Service    → uses weights to compute weighted coverage
#   Recommendation     → suggests high-weight missing entities
#
# STRUCTURE:
#   {
#     "domain_name": {
#       "category_name": [
#         {
#           "name": "canonical entity name",
#           "aliases": ["alternative", "names", "abbreviations"],
#           "weight": 0.0 - 1.0  (importance score)
#         }
#       ]
#     }
#   }
#
# HOW WEIGHTS WORK:
#   - Weight is a float from 0.0 to 1.0 indicating entity importance
#   - 1.0 = Critical / must-have entity for the domain
#   - 0.7-0.9 = Important, frequently discussed entities
#   - 0.4-0.6 = Moderately important, nice to cover
#   - 0.1-0.3 = Peripheral, bonus if mentioned
#
#   Weights are used in scoring_service.py to compute WEIGHTED coverage.
#   Missing a weight=1.0 entity hurts your score more than missing a
#   weight=0.3 entity. This mirrors real-world content quality — an
#   article about "risk management" that never mentions "risk" is worse
#   than one that skips "Monte Carlo simulation".
#
# HOW ALIASES WORK:
#   Many entities have multiple names in practice:
#     "ROI" = "return on investment"
#     "IoT" = "internet of things"
#     "NPV" = "net present value"
#
#   During entity extraction, if ANY alias matches, it counts as a match
#   for the canonical entity name. This prevents duplicate counting and
#   ensures consistent reporting regardless of which term the author used.
#
# EXTENDING THIS:
#   To add a new domain, simply add a new top-level key with categories.
#   To add entities to an existing domain, append to the relevant category.
#   The rest of the pipeline adapts automatically — no code changes needed.
# =============================================================================

from typing import Any, Dict, List


# Type alias for clarity
EntityMap = Dict[str, Dict[str, List[Dict[str, Any]]]]


# =============================================================================
# FINANCE DOMAIN
# =============================================================================
FINANCE_ENTITY_MAP: Dict[str, List[Dict[str, Any]]] = {

    # -------------------------------------------------------------------------
    # Risk Management — Core pillar of financial analysis
    # -------------------------------------------------------------------------
    "risk_management": [
        {
            "name": "risk management",
            "aliases": ["risk mitigation", "risk control"],
            "weight": 1.0,
        },
        {
            "name": "market risk",
            "aliases": ["systematic risk", "market exposure"],
            "weight": 0.9,
        },
        {
            "name": "credit risk",
            "aliases": ["default risk", "counterparty risk"],
            "weight": 0.9,
        },
        {
            "name": "operational risk",
            "aliases": ["ops risk"],
            "weight": 0.8,
        },
        {
            "name": "liquidity risk",
            "aliases": ["funding risk", "cash flow risk"],
            "weight": 0.8,
        },
        {
            "name": "hedging",
            "aliases": ["hedge", "risk hedging"],
            "weight": 0.7,
        },
        {
            "name": "value at risk",
            "aliases": ["var", "value-at-risk"],
            "weight": 0.7,
        },
        {
            "name": "stress testing",
            "aliases": ["stress test", "scenario analysis"],
            "weight": 0.6,
        },
        {
            "name": "monte carlo simulation",
            "aliases": ["monte carlo", "mcs"],
            "weight": 0.4,
        },
    ],

    # -------------------------------------------------------------------------
    # Valuation & Financial Instruments
    # -------------------------------------------------------------------------
    "valuation": [
        {
            "name": "valuation",
            "aliases": ["asset valuation", "business valuation"],
            "weight": 1.0,
        },
        {
            "name": "discounted cash flow",
            "aliases": ["dcf", "dcf analysis", "dcf model"],
            "weight": 0.9,
        },
        {
            "name": "net present value",
            "aliases": ["npv"],
            "weight": 0.8,
        },
        {
            "name": "internal rate of return",
            "aliases": ["irr"],
            "weight": 0.8,
        },
        {
            "name": "return on investment",
            "aliases": ["roi"],
            "weight": 0.9,
        },
        {
            "name": "earnings per share",
            "aliases": ["eps"],
            "weight": 0.7,
        },
        {
            "name": "price to earnings ratio",
            "aliases": ["pe ratio", "p/e ratio", "pe"],
            "weight": 0.7,
        },
        {
            "name": "capital asset pricing model",
            "aliases": ["capm"],
            "weight": 0.6,
        },
        {
            "name": "weighted average cost of capital",
            "aliases": ["wacc"],
            "weight": 0.6,
        },
    ],

    # -------------------------------------------------------------------------
    # Compliance & Regulation
    # -------------------------------------------------------------------------
    "compliance": [
        {
            "name": "regulatory compliance",
            "aliases": ["compliance", "regulatory requirements"],
            "weight": 1.0,
        },
        {
            "name": "basel framework",
            "aliases": ["basel iii", "basel iv", "basel accords"],
            "weight": 0.8,
        },
        {
            "name": "anti money laundering",
            "aliases": ["aml", "money laundering prevention"],
            "weight": 0.8,
        },
        {
            "name": "know your customer",
            "aliases": ["kyc", "customer due diligence"],
            "weight": 0.7,
        },
        {
            "name": "audit",
            "aliases": ["financial audit", "internal audit", "external audit"],
            "weight": 0.7,
        },
        {
            "name": "sarbanes oxley",
            "aliases": ["sox", "sox compliance"],
            "weight": 0.5,
        },
        {
            "name": "dodd frank",
            "aliases": ["dodd frank act"],
            "weight": 0.5,
        },
    ],

    # -------------------------------------------------------------------------
    # Financial Instruments & Markets
    # -------------------------------------------------------------------------
    "financial_instruments": [
        {
            "name": "derivatives",
            "aliases": ["financial derivatives", "derivative instruments"],
            "weight": 0.8,
        },
        {
            "name": "equity",
            "aliases": ["stocks", "shares", "equity securities"],
            "weight": 0.8,
        },
        {
            "name": "fixed income",
            "aliases": ["bonds", "debt securities", "bond market"],
            "weight": 0.7,
        },
        {
            "name": "options",
            "aliases": ["stock options", "call options", "put options"],
            "weight": 0.6,
        },
        {
            "name": "futures",
            "aliases": ["futures contracts", "commodity futures"],
            "weight": 0.6,
        },
        {
            "name": "exchange traded fund",
            "aliases": ["etf", "etfs"],
            "weight": 0.5,
        },
        {
            "name": "portfolio management",
            "aliases": ["portfolio optimization", "asset allocation"],
            "weight": 0.9,
        },
        {
            "name": "diversification",
            "aliases": ["portfolio diversification"],
            "weight": 0.7,
        },
    ],

    # -------------------------------------------------------------------------
    # Market Analysis
    # -------------------------------------------------------------------------
    "market_analysis": [
        {
            "name": "fundamental analysis",
            "aliases": ["fundamentals"],
            "weight": 0.8,
        },
        {
            "name": "technical analysis",
            "aliases": ["charting", "chart analysis"],
            "weight": 0.7,
        },
        {
            "name": "market sentiment",
            "aliases": ["investor sentiment", "market mood"],
            "weight": 0.6,
        },
        {
            "name": "volatility",
            "aliases": ["market volatility", "price volatility"],
            "weight": 0.7,
        },
        {
            "name": "interest rate",
            "aliases": ["interest rates", "rate of interest"],
            "weight": 0.8,
        },
        {
            "name": "inflation",
            "aliases": ["price inflation", "inflationary pressure"],
            "weight": 0.7,
        },
        {
            "name": "market capitalization",
            "aliases": ["market cap"],
            "weight": 0.5,
        },
    ],
}


# =============================================================================
# MANUFACTURING DOMAIN
# =============================================================================
MANUFACTURING_ENTITY_MAP: Dict[str, List[Dict[str, Any]]] = {

    # -------------------------------------------------------------------------
    # Lean Manufacturing — Efficiency and waste reduction
    # -------------------------------------------------------------------------
    "lean_manufacturing": [
        {
            "name": "lean manufacturing",
            "aliases": ["lean production", "lean methodology", "lean"],
            "weight": 1.0,
        },
        {
            "name": "just in time",
            "aliases": ["jit", "jit manufacturing", "just-in-time"],
            "weight": 0.9,
        },
        {
            "name": "kaizen",
            "aliases": ["continuous improvement", "kaizen methodology"],
            "weight": 0.9,
        },
        {
            "name": "kanban",
            "aliases": ["kanban system", "kanban board"],
            "weight": 0.7,
        },
        {
            "name": "value stream mapping",
            "aliases": ["vsm", "value stream"],
            "weight": 0.7,
        },
        {
            "name": "waste reduction",
            "aliases": ["muda", "waste elimination", "7 wastes"],
            "weight": 0.8,
        },
        {
            "name": "five s",
            "aliases": ["5s", "5s methodology", "workplace organization"],
            "weight": 0.6,
        },
        {
            "name": "poka yoke",
            "aliases": ["error proofing", "mistake proofing"],
            "weight": 0.5,
        },
    ],

    # -------------------------------------------------------------------------
    # Supply Chain Management
    # -------------------------------------------------------------------------
    "supply_chain": [
        {
            "name": "supply chain management",
            "aliases": ["scm", "supply chain", "supply chain optimization"],
            "weight": 1.0,
        },
        {
            "name": "procurement",
            "aliases": ["sourcing", "purchasing", "vendor management"],
            "weight": 0.9,
        },
        {
            "name": "inventory management",
            "aliases": ["stock management", "inventory control", "inventory optimization"],
            "weight": 0.9,
        },
        {
            "name": "logistics",
            "aliases": ["supply chain logistics", "distribution"],
            "weight": 0.8,
        },
        {
            "name": "demand forecasting",
            "aliases": ["demand planning", "forecast", "demand prediction"],
            "weight": 0.8,
        },
        {
            "name": "lead time",
            "aliases": ["lead time reduction", "delivery time"],
            "weight": 0.7,
        },
        {
            "name": "supplier relationship",
            "aliases": ["supplier management", "vendor relationship"],
            "weight": 0.6,
        },
        {
            "name": "bill of materials",
            "aliases": ["bom", "materials list"],
            "weight": 0.6,
        },
    ],

    # -------------------------------------------------------------------------
    # Quality Control & Assurance
    # -------------------------------------------------------------------------
    "quality_control": [
        {
            "name": "quality control",
            "aliases": ["qc", "quality assurance", "qa"],
            "weight": 1.0,
        },
        {
            "name": "six sigma",
            "aliases": ["6 sigma", "six sigma methodology", "dmaic"],
            "weight": 0.9,
        },
        {
            "name": "total quality management",
            "aliases": ["tqm"],
            "weight": 0.8,
        },
        {
            "name": "statistical process control",
            "aliases": ["spc", "process control"],
            "weight": 0.7,
        },
        {
            "name": "iso 9001",
            "aliases": ["iso certification", "iso standards", "iso 9001 certification"],
            "weight": 0.8,
        },
        {
            "name": "defect rate",
            "aliases": ["defect density", "failure rate", "reject rate"],
            "weight": 0.7,
        },
        {
            "name": "root cause analysis",
            "aliases": ["rca", "5 whys", "fishbone diagram", "ishikawa"],
            "weight": 0.6,
        },
        {
            "name": "first pass yield",
            "aliases": ["fpy", "yield rate"],
            "weight": 0.5,
        },
    ],

    # -------------------------------------------------------------------------
    # Production Management
    # -------------------------------------------------------------------------
    "production_management": [
        {
            "name": "production planning",
            "aliases": ["production scheduling", "capacity planning"],
            "weight": 0.9,
        },
        {
            "name": "overall equipment effectiveness",
            "aliases": ["oee", "equipment effectiveness"],
            "weight": 0.8,
        },
        {
            "name": "throughput",
            "aliases": ["production throughput", "output rate"],
            "weight": 0.8,
        },
        {
            "name": "cycle time",
            "aliases": ["process cycle time", "takt time"],
            "weight": 0.7,
        },
        {
            "name": "bottleneck",
            "aliases": ["production bottleneck", "constraint"],
            "weight": 0.7,
        },
        {
            "name": "preventive maintenance",
            "aliases": ["planned maintenance", "scheduled maintenance", "pm"],
            "weight": 0.7,
        },
        {
            "name": "downtime",
            "aliases": ["equipment downtime", "unplanned downtime"],
            "weight": 0.6,
        },
        {
            "name": "batch production",
            "aliases": ["batch manufacturing", "batch processing"],
            "weight": 0.5,
        },
    ],

    # -------------------------------------------------------------------------
    # Industry 4.0 & Smart Manufacturing
    # -------------------------------------------------------------------------
    "industry_4_0": [
        {
            "name": "industry 4.0",
            "aliases": ["smart manufacturing", "fourth industrial revolution", "i4.0"],
            "weight": 0.9,
        },
        {
            "name": "internet of things",
            "aliases": ["iot", "industrial iot", "iiot"],
            "weight": 0.9,
        },
        {
            "name": "digital twin",
            "aliases": ["digital twins", "virtual twin"],
            "weight": 0.8,
        },
        {
            "name": "automation",
            "aliases": ["industrial automation", "process automation", "robotic automation"],
            "weight": 0.9,
        },
        {
            "name": "artificial intelligence",
            "aliases": ["ai", "machine learning", "ml", "ai in manufacturing"],
            "weight": 0.8,
        },
        {
            "name": "additive manufacturing",
            "aliases": ["3d printing", "3d manufacturing"],
            "weight": 0.6,
        },
        {
            "name": "predictive maintenance",
            "aliases": ["predictive analytics", "condition based maintenance"],
            "weight": 0.7,
        },
        {
            "name": "cyber physical systems",
            "aliases": ["cps"],
            "weight": 0.5,
        },
    ],
}


# =============================================================================
# Master Registry — Maps domain name to its entity map
# =============================================================================
DOMAIN_REGISTRY: EntityMap = {
    "finance": FINANCE_ENTITY_MAP,
    "manufacturing": MANUFACTURING_ENTITY_MAP,
}


# ---------------------------------------------------------------------------
# Helper: Get supported domain names
# ---------------------------------------------------------------------------
def get_supported_domains() -> List[str]:
    """Return list of all supported domain names."""
    return list(DOMAIN_REGISTRY.keys())


def get_domain_map(domain: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Retrieve the entity map for a given domain.

    Args:
        domain: Domain name (case-insensitive)

    Returns:
        The entity map dictionary for the requested domain

    Raises:
        ValueError: If the domain is not supported
    """
    domain_lower = domain.lower().strip()

    if domain_lower not in DOMAIN_REGISTRY:
        supported = ", ".join(get_supported_domains())
        raise ValueError(
            f"Unsupported domain: '{domain}'. Supported domains: {supported}"
        )

    return DOMAIN_REGISTRY[domain_lower]


def get_all_entities_flat(domain: str) -> List[Dict[str, Any]]:
    """
    Return a flat list of all entities across all categories for a domain,
    with the category name added to each entity dict.

    Useful for building lookup indices.

    Args:
        domain: Domain name

    Returns:
        Flat list of entity dicts, each augmented with a "category" key
    """
    domain_map = get_domain_map(domain)
    flat = []

    for category_name, entities in domain_map.items():
        for entity in entities:
            flat.append({**entity, "category": category_name})

    return flat
