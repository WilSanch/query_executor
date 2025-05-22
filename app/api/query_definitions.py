from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.query_definition import QueryDefinition
from app.db.models.application import Application
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def list_queries(request: Request, db: Session = Depends(get_db)):
    queries = db.query(QueryDefinition).all()
    apps = db.query(Application).all()
    return templates.TemplateResponse("queries.html", {"request": request, "queries": queries, "apps": apps})

@router.post("/create")
def create_query(
    name: str = Form(...),
    sql_template: str = Form(...),
    db_url: str = Form(...),
    app_id: int = Form(...),
    db: Session = Depends(get_db),
):
    query = QueryDefinition(name=name, sql_template=sql_template, app_id=app_id)
    query.db_url = db_url
    db.add(query)
    db.commit()
    return RedirectResponse("/queries", status_code=303)