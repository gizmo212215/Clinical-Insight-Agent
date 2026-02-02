from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.api.routes import router as api_router
from backend.core.config import settings
from backend.core.logger import get_logger

logger = get_logger("main_server")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 {settings.PROJECT_NAME} v{settings.VERSION} is starting up...")
    logger.info(f"📂 Log Directory: {settings.LOG_DIR}")
    yield

    logger.info("🛑 Server is shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    logger.info("🔌 Starting Uvicorn Server manually...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
