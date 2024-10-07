from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import crud, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="../../../assets"), name="static")

templates = Jinja2Templates(directory="noteapp/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/notes", response_class=HTMLResponse)
def read_notes(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    notes_db = crud.get_notes(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        request=request, name="notes.html", context={"notes": notes_db}
    )


@app.post("/notes", response_class=HTMLResponse)
def create_notes(request: Request, db: Session = Depends(get_db)):
    notes_db = crud.create_user_note(db)
    return templates.TemplateResponse(
        request=request, name="notes.html", context={"notes": notes_db}
    )


@app.get("/notes/{note_id}", response_class=HTMLResponse)
def read_notes(request: Request, db: Session = Depends(get_db), note_id: int = 0):
    note_info = crud.get_note(db, note_id)
    if note_info is None:
        return templates.TemplateResponse(
            request=request,
            status_code=404,
            name="404_note.html",
            context={"note_id": note_id},
        )
    return templates.TemplateResponse(
        request=request, name="note.html", context={"note": note_info}
    )
