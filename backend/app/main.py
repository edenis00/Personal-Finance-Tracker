"""
Main appplication file
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_router, user_router, income_router, expense_router, savings_router


app = FastAPI(
    title="Personal Finance Tracker",
    description="An API to help you track your personal finances, including income, expenses, and budgets.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router=auth_router)
app.include_router(router=user_router)
app.include_router(router=income_router)
app.include_router(router=expense_router)
app.include_router(router=savings_router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
