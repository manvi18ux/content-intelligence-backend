# =============================================================================
# Content Intelligence System — Application Entry Point
# =============================================================================
# This is the FastAPI application factory and server entry point.
#
# Responsibilities:
#   1. Create and configure the FastAPI application instance
#   2. Register CORS middleware for cross-origin requests
#   3. Mount all API routers under versioned prefixes
#   4. Provide a health check endpoint for monitoring
#
# Run the server:
#   uvicorn app.main:app --reload              (development)
#   uvicorn app.main:app --host 0.0.0.0        (production)
# =============================================================================

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.content import router as content_router


# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("content_intelligence")


# ---------------------------------------------------------------------------
# Application Lifespan (startup / shutdown hooks)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application lifecycle events.

    Startup:
      - Log configuration summary
      - Validate critical settings (warn if OpenAI key missing)

    Shutdown:
      - Clean up resources (future: close DB connections, caches, etc.)
    """
    # --- Startup ---
    logger.info("=" * 60)
    logger.info("Content Intelligence System — Starting Up")
    logger.info("=" * 60)
    logger.info(f"Environment : {settings.APP_ENV}")
    logger.info(f"Server      : {settings.HOST}:{settings.PORT}")
    logger.info(f"OpenAI Model: {settings.OPENAI_MODEL}")
    logger.info(f"OpenAI Key  : {'✓ Configured' if settings.has_openai_key else '✗ NOT SET (mock mode)'}")
    logger.info(f"Max Iters   : {settings.MAX_PIPELINE_ITERATIONS}")
    logger.info("=" * 60)

    if not settings.has_openai_key:
        logger.warning(
            "OPENAI_API_KEY is not set. Content generation will return mock responses. "
            "Set the key in your .env file for real AI-generated content."
        )

    yield  # Application runs here

    # --- Shutdown ---
    logger.info("Content Intelligence System — Shutting Down")


# ---------------------------------------------------------------------------
# FastAPI Application Instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Content Intelligence System",
    description=(
        "Domain-specific content intelligence backend for Finance and Manufacturing. "
        "Analyzes content for entity coverage, computes quality scores, predicts "
        "ranking, and generates optimized content using AI."
    ),
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc alternative docs
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Middleware Configuration
# ---------------------------------------------------------------------------
# CORS: Allow cross-origin requests.
# In production, replace ["*"] with your actual frontend domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],                  # Allow all HTTP methods
    allow_headers=["*"],                  # Allow all headers
)


# ---------------------------------------------------------------------------
# Router Registration
# ---------------------------------------------------------------------------
# All content intelligence endpoints live under /api/v1
# Versioned prefix allows future breaking changes via /api/v2, etc.
app.include_router(
    content_router,
    prefix="/api/v1",
    tags=["Content Intelligence"],
)


# ---------------------------------------------------------------------------
# Root & Health Check Endpoints
# ---------------------------------------------------------------------------
@app.get(
    "/",
    summary="Root",
    description="Redirects to API documentation.",
    tags=["System"],
)
async def root():
    """Root endpoint — provides API overview and navigation links."""
    return {
        "system": "Content Intelligence System",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health",
        "api_base": "/api/v1",
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Returns system health status for monitoring and load balancers.",
    tags=["System"],
)
async def health_check():
    """
    Health check endpoint.

    Used by:
      - Load balancers to determine if this instance is healthy
      - Monitoring systems (Datadog, Prometheus, etc.)
      - CI/CD pipelines to verify deployment success

    Returns:
      - status: "healthy" if the server is running
      - timestamp: current UTC time
      - environment: current deployment environment
      - openai_configured: whether OpenAI key is set
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": settings.APP_ENV,
        "openai_configured": settings.has_openai_key,
    }


# ---------------------------------------------------------------------------
# Direct Execution (for development convenience)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.is_development,  # Auto-reload only in dev
        log_level=settings.LOG_LEVEL.lower(),
    )
