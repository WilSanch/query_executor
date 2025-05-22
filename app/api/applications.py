from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.db.models.application import Application
from fastapi.templating import Jinja2Templates
from app.db.session import SessionLocal
from app.utils.crypto_utils import encrypt_string, decrypt_string

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def list_applications(request: Request, db: Session = Depends(get_db)):
    apps = db.query(Application).all()
    return templates.TemplateResponse("applications.html", {"request": request, "apps": apps})

@router.post("/create")
def create_application(
    name: str = Form(...),
    description: str = Form(...),
    blob_connection_string: str = Form(...),
    blob_container: str = Form(...),
    db: Session = Depends(get_db),
):
    app = Application(name=name,description=description,blob_container=blob_container)
    app.blob_connection_string = encrypt_string(blob_connection_string)
    db.add(app)
    db.commit()
    return RedirectResponse("/applications", status_code=303)