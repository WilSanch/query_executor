from fastapi import FastAPI
from app.api.execute_query import router as query_router
from app.api.applications import router as applications
from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.application import Application
from app.db.models.query_definition import QueryDefinition
from app.utils.crypto_utils import encrypt_string, decrypt_string
from fastapi.staticfiles import StaticFiles


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Query Executor API")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(query_router, prefix="/api")
app.include_router(applications, prefix="/applications")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/applications", response_class=HTMLResponse)
def list_applications(request: Request, db: Session = Depends(get_db)):
    apps = db.query(Application).all()
    for a in apps:
        a.blob_connection_string = decrypt_string(a.blob_connection_string)
    return templates.TemplateResponse("applications/list.html", {"request": request, "applications": apps})

@app.get("/applications/create", response_class=HTMLResponse)
def create_application_form(request: Request):
    return templates.TemplateResponse("applications/create.html", {"request": request})

@app.post("/applications/create")
def create_application(
    request: Request,
    name: str = Form(...),
    description: str = Form(None),
    active: bool = Form(False),
    blob_connection_string: str = Form(...),
    blob_container: str = Form(...),
    db: Session = Depends(get_db)
):
    new_app = Application(
        name=name,
        description=description,
        active=active,
        blob_connection_string=encrypt_string(blob_connection_string),
        blob_container=blob_container,
    )
    db.add(new_app)
    db.commit()
    return RedirectResponse(url="/applications", status_code=303)


@app.get("/queries", response_class=HTMLResponse)
def list_queries(request: Request, db: Session = Depends(get_db)):
    queries = db.query(QueryDefinition).all()
    for q in queries:
        q.db_url = decrypt_string(q.db_url)
    return templates.TemplateResponse("queries/list.html", {"request": request, "queries": queries})

@app.get("/queries/create", response_class=HTMLResponse)
def create_query_form(request: Request, db: Session = Depends(get_db)):
    apps = db.query(Application).filter_by(active=True).all()
    return templates.TemplateResponse("queries/create.html", {"request": request, "applications": apps})

@app.post("/queries/create")
def create_query(
    request: Request,
    app_id: int = Form(...),
    name: str = Form(...),
    sql_template: str = Form(...),
    db_url: str = Form(...),
    active: bool = Form(False),
    db: Session = Depends(get_db)
):
    new_query = QueryDefinition(
        app_id=app_id,
        name=name,
        sql_template=sql_template,
        db_url=encrypt_string(db_url),
        active=active,
    )
    db.add(new_query)
    db.commit()
    return RedirectResponse(url="/queries", status_code=303)