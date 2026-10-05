from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routers import api, auth, pages, planners


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered budget planning and recommendation "
        "assistant for home interiors, parties and jewelry."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    planners.router
)

app.include_router(
    api.router
)


@app.get(
    "/startup",
    tags=["System"],
)
def startup():
    return {
        "status": "started",
        "application": settings.app_name,
        "environment": settings.environment,
    }


@app.get(
    "/health",
    tags=["System"],
)
def health():
    return {
        "status": "healthy",
        "application": settings.app_name,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )