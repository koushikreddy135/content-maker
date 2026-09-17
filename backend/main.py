import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database.db import init_db
from backend.api.routes import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("contentmaker")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing ContentMaker backend database...")
    await init_db()
    logger.info("ContentMaker ready.")
    yield
    logger.info("Shutting down ContentMaker backend.")

app = FastAPI(
    title="ContentMaker API",
    description="Autonomous Cyclic Multi-Agent YouTube Production Engine with Decoupled Quality Gating",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API endpoints
app.include_router(api_router)

@app.get("/")
async def health_check():
    return {
        "service": "ContentMaker Multi-Agent Engine",
        "status": "operational",
        "architecture": "Decoupled Tri-Agent (Writer -> Auditor -> Script Doctor)",
        "model": settings.LLM_MODEL,
        "max_revisions": settings.MAX_REVISION_LOOPS
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
