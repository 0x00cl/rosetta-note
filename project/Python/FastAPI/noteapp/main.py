from typing import Annotated

from fastapi import FastAPI, Request, Depends, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import crud, models, schemas
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


@app.post("/notes", response_class=RedirectResponse)
def create_notes(
    request: Request,
    db: Session = Depends(get_db),
    note: Annotated[schemas.NoteCreate, Form()] = {},
):
    note_info = crud.create_user_note(db, note, 0)
    return RedirectResponse(f"/notes/{note_info.id}", status_code=303)


@app.get("/notes/create", response_class=HTMLResponse)
def read_notes(request: Request):
    return templates.TemplateResponse(
        request=request, name="notes_create.html", context={}
    )


# Should use DELETE method here instead of a POST if we want to follow Restful practices.
# But because we aren't using JavaScript (at least yet) HTML only allows "GET" and "POST" methods.
# So a workaround that limitation is having dedicated endpoints where the verbs are in the url and use "POST" to execute them
@app.post("/notes/{note_id}/delete", response_class=HTMLResponse)
def delete_note(request: Request, db: Session = Depends(get_db), note_id: int = 0):
    note_deleted = crud.delete_note(db, note_id)
    return RedirectResponse("/notes", status_code=303)


@app.get("/notes/{note_id}/delete", response_class=HTMLResponse)
def delete_note(request: Request, db: Session = Depends(get_db), note_id: int = 0):
    note_info = crud.get_note(db, note_id)
    if note_info is None:
        return templates.TemplateResponse(
            request=request,
            status_code=404,
            name="404_note.html",
            context={"note_id": note_id},
        )
    return templates.TemplateResponse(
        request=request, name="note_delete.html", context={"note": note_info}
    )


@app.post("/notes/{note_id}/edit", response_class=HTMLResponse)
def delete_note(
    request: Request,
    db: Session = Depends(get_db),
    note_id: int = 0,
    note: Annotated[schemas.NoteCreate, Form()] = {},
):
    note_deleted = crud.edit_note(db, note_id, note)
    return RedirectResponse("/notes", status_code=303)


@app.get("/notes/{note_id}/edit", response_class=HTMLResponse)
def delete_note(request: Request, db: Session = Depends(get_db), note_id: int = 0):
    note_info = crud.get_note(db, note_id)
    if note_info is None:
        return templates.TemplateResponse(
            request=request,
            status_code=404,
            name="404_note.html",
            context={"note_id": note_id},
        )
    return templates.TemplateResponse(
        request=request, name="note_edit.html", context={"note": note_info}
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
