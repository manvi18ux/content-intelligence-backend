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

    # -------------------------------------------------------------------------
    # Fintech & Digital Payments — Modern payment ecosystems
    # -------------------------------------------------------------------------
    "fintech_and_digital_payments": [
        {
            "name": "fintech",
            "aliases": ["financial technology", "fin tech"],
            "weight": 0.9,
        },
        {
            "name": "unified payments interface",
            "aliases": ["upi", "upi payments", "upi transaction"],
            "weight": 0.9,
        },
        {
            "name": "digital payments",
            "aliases": ["digital payment", "electronic payment", "e-payment", "online payment"],
            "weight": 0.9,
        },
        {
            "name": "payment gateway",
            "aliases": ["payment processor", "payment processing", "payment aggregator"],
            "weight": 0.8,
        },
        {
            "name": "mobile wallet",
            "aliases": ["digital wallet", "e-wallet", "mobile money"],
            "weight": 0.8,
        },
        {
            "name": "neobank",
            "aliases": ["neobanking", "digital-only bank", "challenger bank"],
            "weight": 0.7,
        },
        {
            "name": "buy now pay later",
            "aliases": ["bnpl", "pay later", "deferred payment"],
            "weight": 0.7,
        },
        {
            "name": "peer to peer lending",
            "aliases": ["p2p lending", "peer lending", "marketplace lending"],
            "weight": 0.6,
        },
        {
            "name": "fraud detection",
            "aliases": ["fraud prevention", "anti fraud", "transaction monitoring"],
            "weight": 0.8,
        },
        {
            "name": "real time gross settlement",
            "aliases": ["rtgs", "real time settlement"],
            "weight": 0.6,
        },
        {
            "name": "national electronic funds transfer",
            "aliases": ["neft", "electronic funds transfer"],
            "weight": 0.5,
        },
        {
            "name": "qr code payments",
            "aliases": ["qr payment", "scan and pay", "qr code"],
            "weight": 0.6,
        },
        {
            "name": "cryptocurrency",
            "aliases": ["crypto", "digital currency", "bitcoin", "blockchain"],
            "weight": 0.7,
        },
        {
            "name": "central bank digital currency",
            "aliases": ["cbdc", "digital rupee", "e-rupee"],
            "weight": 0.6,
        },
        {
            "name": "embedded finance",
            "aliases": ["embedded payments", "banking as a service", "baas"],
            "weight": 0.5,
        },
    ],

    # -------------------------------------------------------------------------
    # Banking Systems — Core banking and institutional infrastructure
    # -------------------------------------------------------------------------
    "banking_systems": [
        {
            "name": "reserve bank of india",
            "aliases": ["rbi", "central bank", "rbi guidelines"],
            "weight": 0.9,
        },
        {
            "name": "core banking system",
            "aliases": ["cbs", "core banking", "core banking solution"],
            "weight": 0.8,
        },
        {
            "name": "net banking",
            "aliases": ["internet banking", "online banking", "e-banking"],
            "weight": 0.7,
        },
        {
            "name": "non performing asset",
            "aliases": ["npa", "non performing loan", "bad loan", "npl"],
            "weight": 0.8,
        },
        {
            "name": "capital adequacy ratio",
            "aliases": ["car", "crar", "capital adequacy"],
            "weight": 0.7,
        },
        {
            "name": "deposit insurance",
            "aliases": ["dicgc", "deposit guarantee", "insured deposits"],
            "weight": 0.5,
        },
        {
            "name": "priority sector lending",
            "aliases": ["psl", "priority lending"],
            "weight": 0.6,
        },
        {
            "name": "credit score",
            "aliases": ["cibil score", "credit rating", "credit bureau", "fico score"],
            "weight": 0.7,
        },
        {
            "name": "mortgage",
            "aliases": ["home loan", "housing loan", "mortgage lending"],
            "weight": 0.6,
        },
        {
            "name": "trade finance",
            "aliases": ["letter of credit", "lc", "export finance", "import finance"],
            "weight": 0.6,
        },
        {
            "name": "treasury management",
            "aliases": ["treasury operations", "treasury"],
            "weight": 0.5,
        },
    ],

    # -------------------------------------------------------------------------
    # Financial Technology Infrastructure — APIs, data, and platforms
    # -------------------------------------------------------------------------
    "financial_technology_infrastructure": [
        {
            "name": "open banking",
            "aliases": ["open banking api", "account aggregation", "open finance"],
            "weight": 0.8,
        },
        {
            "name": "api banking",
            "aliases": ["banking api", "financial api", "api integration"],
            "weight": 0.7,
        },
        {
            "name": "payment orchestration",
            "aliases": ["payment routing", "payment switch", "payment hub"],
            "weight": 0.6,
        },
        {
            "name": "regtech",
            "aliases": ["regulatory technology", "compliance technology", "compliance automation"],
            "weight": 0.7,
        },
        {
            "name": "insurtech",
            "aliases": ["insurance technology", "digital insurance"],
            "weight": 0.6,
        },
        {
            "name": "wealthtech",
            "aliases": ["wealth technology", "robo advisor", "robo advisory", "automated investing"],
            "weight": 0.6,
        },
        {
            "name": "data analytics in finance",
            "aliases": ["financial analytics", "big data finance", "financial data analytics"],
            "weight": 0.7,
        },
        {
            "name": "cloud banking",
            "aliases": ["cloud infrastructure", "cloud native banking", "saas banking"],
            "weight": 0.5,
        },
        {
            "name": "tokenization",
            "aliases": ["asset tokenization", "payment tokenization", "token"],
            "weight": 0.5,
        },
        {
            "name": "account aggregator",
            "aliases": ["aa framework", "financial data sharing", "consent based data"],
            "weight": 0.6,
        },

        {
            "name": "digital lending",
            "aliases": ["online lending", "lending platform", "digital loan"],
            "weight": 0.7,
        },
    ],

    # -------------------------------------------------------------------------
    # Corporate Finance & Investment Banking
    # -------------------------------------------------------------------------
    "investment_banking": [
        {
            "name": "mergers and acquisitions",
            "aliases": ["m&a", "merger", "acquisition", "corporate restructuring"],
            "weight": 0.9,
        },
        {
            "name": "initial public offering",
            "aliases": ["ipo", "going public", "public listing"],
            "weight": 0.8,
        },
        {
            "name": "private equity",
            "aliases": ["pe", "pe firm", "buyout"],
            "weight": 0.8,
        },
        {
            "name": "venture capital",
            "aliases": ["vc", "seed funding", "series a", "startup funding"],
            "weight": 0.7,
        },
        {
            "name": "leveraged buyout",
            "aliases": ["lbo", "leveraged buyout transaction"],
            "weight": 0.6,
        },
        {
            "name": "underwriting",
            "aliases": ["underwriter", "securities underwriting"],
            "weight": 0.7,
        },
        {
            "name": "syndicated loan",
            "aliases": ["loan syndication", "syndicated lending"],
            "weight": 0.6,
        },
        {
            "name": "special purpose acquisition company",
            "aliases": ["spac", "blank check company"],
            "weight": 0.5,
        },
    ],

    # -------------------------------------------------------------------------
    # Accounting & Taxation
    # -------------------------------------------------------------------------
    "accounting_and_taxation": [
        {
            "name": "generally accepted accounting principles",
            "aliases": ["gaap", "us gaap"],
            "weight": 0.8,
        },
        {
            "name": "international financial reporting standards",
            "aliases": ["ifrs", "international accounting standards"],
            "weight": 0.8,
        },
        {
            "name": "audited financial statements",
            "aliases": ["financial statements", "balance sheet", "income statement", "cash flow statement"],
            "weight": 0.9,
        },
        {
            "name": "tax planning",
            "aliases": ["tax optimization", "tax strategy", "corporate tax planning"],
            "weight": 0.7,
        },
        {
            "name": "goods and services tax",
            "aliases": ["gst", "value added tax", "vat"],
            "weight": 0.7,
        },
        {
            "name": "depreciation and amortization",
            "aliases": ["depreciation", "amortization", "ebitda"],
            "weight": 0.7,
        },
        {
            "name": "transfer pricing",
            "aliases": ["transfer price", "arm's length principle"],
            "weight": 0.6,
        },
        {
            "name": "working capital management",
            "aliases": ["working capital", "net working capital"],
            "weight": 0.8,
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

    # -------------------------------------------------------------------------
    # Robotics & CNC — Physical automation and machining
    # -------------------------------------------------------------------------
    "robotics_and_cnc": [
        {
            "name": "industrial robot",
            "aliases": ["industrial robotics", "robotic arm", "robot arm", "manufacturing robot"],
            "weight": 0.9,
        },
        {
            "name": "cnc machining",
            "aliases": ["cnc", "cnc machine", "computer numerical control", "cnc milling"],
            "weight": 0.9,
        },
        {
            "name": "collaborative robot",
            "aliases": ["cobot", "cobots", "human robot collaboration"],
            "weight": 0.8,
        },
        {
            "name": "robotic process automation",
            "aliases": ["rpa", "rpa in manufacturing"],
            "weight": 0.7,
        },
        {
            "name": "computer aided manufacturing",
            "aliases": ["cam", "cam software"],
            "weight": 0.7,
        },
        {
            "name": "computer aided design",
            "aliases": ["cad", "cad software", "cad modeling"],
            "weight": 0.7,
        },
        {
            "name": "programmable logic controller",
            "aliases": ["plc", "plc programming", "plc controller"],
            "weight": 0.8,
        },
        {
            "name": "servo motor",
            "aliases": ["servo drive", "servo system", "stepper motor"],
            "weight": 0.5,
        },

        {
            "name": "machine vision",
            "aliases": ["computer vision", "vision system", "vision inspection"],
            "weight": 0.7,
        },
        {
            "name": "laser cutting",
            "aliases": ["laser cutter", "laser machining", "laser processing"],
            "weight": 0.5,
        },
        {
            "name": "pick and place",
            "aliases": ["pick and place robot", "pick place automation"],
            "weight": 0.5,
        },
        {
            "name": "welding robot",
            "aliases": ["robotic welding", "automated welding", "arc welding robot"],
            "weight": 0.5,
        },
    ],

    # -------------------------------------------------------------------------
    # Factory Automation & IIoT — Connected systems and smart factories
    # -------------------------------------------------------------------------
    "factory_automation_and_iiot": [
        {
            "name": "industrial internet of things",
            "aliases": ["iiot", "industrial iot", "iiot platform", "iiot sensors"],
            "weight": 0.9,
        },
        {
            "name": "scada",
            "aliases": ["supervisory control", "scada system", "supervisory control and data acquisition"],
            "weight": 0.8,
        },
        {
            "name": "manufacturing execution system",
            "aliases": ["mes", "mes software", "shop floor system"],
            "weight": 0.8,
        },
        {
            "name": "enterprise resource planning",
            "aliases": ["erp", "erp system", "erp software", "sap"],
            "weight": 0.8,
        },
        {
            "name": "distributed control system",
            "aliases": ["dcs", "dcs controller"],
            "weight": 0.6,
        },
        {
            "name": "human machine interface",
            "aliases": ["hmi", "hmi panel", "operator interface"],
            "weight": 0.7,
        },
        {
            "name": "edge computing",
            "aliases": ["edge analytics", "edge device", "edge processing"],
            "weight": 0.7,
        },
        {
            "name": "industrial sensor",
            "aliases": ["sensor network", "smart sensor", "industrial sensors", "proximity sensor"],
            "weight": 0.7,
        },
        {
            "name": "factory floor connectivity",
            "aliases": ["industrial ethernet", "profinet", "modbus", "opc ua"],
            "weight": 0.6,
        },
        {
            "name": "automated guided vehicle",
            "aliases": ["agv", "autonomous mobile robot", "amr"],
            "weight": 0.6,
        },
        {
            "name": "conveyor system",
            "aliases": ["conveyor belt", "material handling", "conveyor automation"],
            "weight": 0.6,
        },
        {
            "name": "smart factory",
            "aliases": ["connected factory", "lights out manufacturing", "dark factory"],
            "weight": 0.7,
        },
        {
            "name": "real time monitoring",
            "aliases": ["condition monitoring", "remote monitoring", "live monitoring"],
            "weight": 0.7,
        },
        {
            "name": "digital thread",
            "aliases": ["digital continuity", "product lifecycle data"],
            "weight": 0.5,
        },
    ],

    # -------------------------------------------------------------------------
    # Industrial Safety & Sustainability — Compliance, safety, and green mfg
    # -------------------------------------------------------------------------
    "industrial_safety_and_sustainability": [
        {
            "name": "occupational safety",
            "aliases": ["osha", "workplace safety", "industrial safety", "safety compliance"],
            "weight": 0.8,
        },
        {
            "name": "environmental health and safety",
            "aliases": ["ehs", "ehs management", "ehs compliance"],
            "weight": 0.7,
        },
        {
            "name": "lockout tagout",
            "aliases": ["loto", "lock out tag out", "energy isolation"],
            "weight": 0.5,
        },
        {
            "name": "personal protective equipment",
            "aliases": ["ppe", "safety gear", "safety equipment"],
            "weight": 0.6,
        },
        {
            "name": "hazard analysis",
            "aliases": ["hazop", "risk assessment", "hazard identification"],
            "weight": 0.6,
        },
        {
            "name": "carbon footprint",
            "aliases": ["carbon emissions", "co2 emissions", "greenhouse gas"],
            "weight": 0.7,
        },
        {
            "name": "sustainable manufacturing",
            "aliases": ["green manufacturing", "eco friendly manufacturing", "sustainability"],
            "weight": 0.8,
        },
        {
            "name": "circular economy",
            "aliases": ["circular manufacturing", "closed loop manufacturing", "recycling"],
            "weight": 0.6,
        },
        {
            "name": "energy efficiency",
            "aliases": ["energy management", "power consumption", "energy optimization"],
            "weight": 0.7,
        },
        {
            "name": "waste management",
            "aliases": ["industrial waste", "waste disposal", "effluent treatment"],
            "weight": 0.6,
        },
        {
            "name": "iso 14001",
            "aliases": ["environmental management system", "ems certification", "iso 14001 certification"],
            "weight": 0.5,
        },
        {
            "name": "iso 45001",
            "aliases": ["occupational health", "ohsms", "safety management system"],
            "weight": 0.5,
        },
    ],

    # -------------------------------------------------------------------------
    # Product Lifecycle & Engineering
    # -------------------------------------------------------------------------
    "product_lifecycle_management": [
        {
            "name": "product lifecycle management",
            "aliases": ["plm", "product lifecycle", "plm software"],
            "weight": 0.9,
        },
        {
            "name": "rapid prototyping",
            "aliases": ["prototyping", "functional prototype", "mockup"],
            "weight": 0.7,
        },
        {
            "name": "concurrent engineering",
            "aliases": ["simultaneous engineering", "integrated product development"],
            "weight": 0.6,
        },
        {
            "name": "reverse engineering",
            "aliases": ["reverse engineered", "back engineering"],
            "weight": 0.5,
        },
        {
            "name": "design for manufacturability",
            "aliases": ["dfm", "design for manufacturing", "dfma"],
            "weight": 0.8,
        },
        {
            "name": "computer aided engineering",
            "aliases": ["cae", "finite element analysis", "fea"],
            "weight": 0.7,
        },
        {
            "name": "new product development",
            "aliases": ["npd", "product development process"],
            "weight": 0.8,
        },
    ],

    # -------------------------------------------------------------------------
    # Advanced Materials & Processing
    # -------------------------------------------------------------------------
    "advanced_materials": [
        {
            "name": "composite materials",
            "aliases": ["composites", "carbon fiber", "fiberglass", "frp"],
            "weight": 0.8,
        },
        {
            "name": "nanomaterials",
            "aliases": ["nanotechnology", "nanoparticles", "nanotech in manufacturing"],
            "weight": 0.7,
        },
        {
            "name": "smart materials",
            "aliases": ["shape memory alloys", "piezoelectric materials"],
            "weight": 0.6,
        },
        {
            "name": "lightweighting",
            "aliases": ["lightweight materials", "weight reduction strategy"],
            "weight": 0.7,
        },
        {
            "name": "metallurgy",
            "aliases": ["metal alloy", "heat treatment", "alloys"],
            "weight": 0.7,
        },
        {
            "name": "surface engineering",
            "aliases": ["surface coating", "thin films", "plating"],
            "weight": 0.5,
        },
        {
            "name": "polymer processing",
            "aliases": ["injection molding", "extrusion", "thermoplastics"],
            "weight": 0.8,
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
