import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.core.database import Base, engine
from backend.app.api.v1.messages import router as messages_router
from backend.app.api.v1.drafts import router as drafts_router
from backend.app.api.v1.stock import router as stock_router
from backend.app.api.v1.assistant import router as assistant_router
from backend.app.api.v1.analytics import router as analytics_router
from backend.app.api.v1.audit import router as audit_router
from backend.app.api.v1.settings import router as settings_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("opspilot.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("OpsPilot AI Backend initialized successfully.")
    yield
    logger.info("Shutting down OpsPilot AI Backend.")

app = FastAPI(
    title="OpsPilot AI — Trentar Operations Platform",
    version="2.0.0",
    description="Digitized operations co-pilot for Trentar Private Limited.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(messages_router, prefix="/api/v1")
app.include_router(drafts_router, prefix="/api/v1")
app.include_router(stock_router, prefix="/api/v1")
app.include_router(assistant_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(audit_router, prefix="/api/v1")
app.include_router(settings_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "product": "OpsPilot AI",
        "company": "Trentar Private Limited",
        "mock_llm": settings.is_mock_active,
        "auto_approve_delay_minutes": settings.AUTO_APPROVE_DELAY_MINUTES
    }

@app.get("/")
def root():
    return {
        "message": "Welcome to OpsPilot AI API (Trentar Pvt Ltd)",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
