from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="A REST API for stamping transparent PNG signatures onto PDF documents.",
)

app.include_router(router)


@app.get("/", tags=["General"])
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "version": settings.version,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    return {"status": "healthy"}
