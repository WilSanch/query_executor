from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.query_executor import run_query_and_upload
from app.schemas.query_execution import QueryExecutionRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/execute-query/{query_id}")
def execute_query(
    query_id: int,
    request: QueryExecutionRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    background_tasks.add_task(run_query_and_upload, db, query_id, request)
    return {"message": "Tarea en ejecución"}
