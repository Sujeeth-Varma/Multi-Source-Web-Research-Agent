import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.api.research import router as research_router
from backend.core.config import settings
from backend.core.exceptions import BaseResearchException

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Multi-Source Web Research Agent API",
    description="FastAPI service for multi-source web research, claim verification, and grounded answer synthesis.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for future frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", summary="Health Check")
async def health_check():
    return {"status": "ok"}


@app.exception_handler(BaseResearchException)
async def research_exception_handler(request: Request, exc: BaseResearchException):
    return JSONResponse(
        status_code=500 if exc.code != "INVALID_REQUEST" else 400,
        content={"error": {"code": exc.code, "message": exc.message}}
    )


app.include_router(research_router, prefix="/api/v1", tags=["Research"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
