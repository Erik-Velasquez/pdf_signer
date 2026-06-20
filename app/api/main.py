from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
)

app.include_router(router)


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.version,
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
    }
