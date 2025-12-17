"""
Main appplication file
"""
import logging
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.utils.rate_limits import limiter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import auth_router, user_router, income_router, expense_router, savings_router


app = FastAPI(
    title="Personal Finance Tracker",
    description="An API to help you track your personal finances, including income, expenses, and savings.",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redocs"
)

API_V1_PREFIX = "/api/v1"

app.include_router(router=auth_router, prefix=API_V1_PREFIX)
app.include_router(router=user_router, prefix=API_V1_PREFIX)
app.include_router(router=income_router, prefix=API_V1_PREFIX)
app.include_router(router=expense_router, prefix=API_V1_PREFIX)
app.include_router(router=savings_router, prefix=API_V1_PREFIX)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Home"])
async def read_root():
    """
    Root endpoint
    """
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Personal Finance Tracker API"}


if __name__  == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
