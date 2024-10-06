from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="../../../assets"), name="static")

templates = Jinja2Templates(directory="noteapp/templates")

# Sort-of in-memory DB just for testing purposes before setting up a Database
notes_db = [
    {
        "title": "Ex soluta",
        "description": "Omnis dolore quia est beatae libero. Atque vel ex soluta quia et quod. Magni cum culpa quos alias blanditiis laboriosam.",
    },
    {
        "title": "Voluptatum ut",
        "description": "Autem eveniet dolore delectus corporis quae nihil quae. Explicabo minima unde et voluptatum asperiores ab eum. Consequatur esse sapiente minus culpa. Voluptatum ut deleniti beatae sed. Esse iusto consequatur veniam ad libero et beatae. Aut est voluptatibus impedit dignissimos",
    },
    {
        "title": "Rerum quibusdam",
        "description": "Sit quo iure vero in. Rerum quibusdam sit est. Possimus vero quam temporibus cumque amet possimus eligendi voluptas. Fugit alias iure inventore ipsum eligendi et sit.",
    },
    {
        "title": "Consequatur voluptas",
        "description": "Incidunt tenetur qui aut. Nobis consequatur voluptas non minima qui quis non magnam. Tenetur est illum omnis omnis voluptatem quia omnis. Quam nemo minus et et atque hic.",
    },
]


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/notes", response_class=HTMLResponse)
def read_notes(request: Request):
    return templates.TemplateResponse(request=request, name="notes.html", context={"notes": notes_db})

@app.get("/notes/{note_id}", response_class=HTMLResponse)
def read_notes(request: Request, note_id: int):
    try:
        note_info = notes_db[note_id-1]
    except IndexError:
        return templates.TemplateResponse(request=request, status_code=404, name="404_note.html", context={"note_id": note_id})
    return templates.TemplateResponse(request=request, name="note.html", context={"note": note_info})

# TODO: Create, update and delete operations over the notes.