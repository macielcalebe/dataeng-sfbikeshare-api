"""
SF Bike Share FastAPI Application

Main application entry point that configures and initializes the FastAPI app.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import stations, trips, status, weather
print("Iniciando a aplicação FastAPI...")
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint.

    Returns basic API information and status.
    """
    return {
        "status": "healthy",
        "api": settings.api_title,
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc",
    }


app.include_router(stations.router, prefix=settings.api_prefix)
app.include_router(trips.router, prefix=settings.api_prefix)
app.include_router(status.router, prefix=settings.api_prefix)
app.include_router(weather.router, prefix=settings.api_prefix)
