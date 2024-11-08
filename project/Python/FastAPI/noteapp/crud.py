from sqlalchemy.orm import Session
from passlib.hash import pbkdf2_sha256

from . import models, schemas

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pbkdf2_sha256.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, user: schemas.UserLogin):
    user_info = get_user_by_username(db, user.username)
    return pbkdf2_sha256.verify(user.password, user_info.hashed_password)

def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()


def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def delete_note(db: Session, note_id: int):
    note_delete = db.query(models.Note).filter(models.Note.id == note_id).first()
    db.delete(note_delete)
    db.commit()
    return note_delete


def edit_note(db: Session, note_id: int, note: schemas.NoteCreate):
    note_update = db.query(models.Note).filter(models.Note.id == note_id).first()
    note_update.title = note.title
    note_update.description = note.description
    db.commit()
    return note_update


def create_user_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
