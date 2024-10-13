from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    description: str | None = None


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    r_password: str

class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    notes: list[Note] = []

    class Config:
        from_attributes = True

