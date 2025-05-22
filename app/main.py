from fastapi import FastAPI
from app.api.execute_query import router as query_router

app = FastAPI(title="Query Executor API")

app.include_router(query_router, prefix="/api")
