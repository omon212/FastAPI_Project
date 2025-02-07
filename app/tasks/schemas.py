from pydantic import BaseModel
from typing import Optional


class TaskSchema(BaseModel):
    title: str
    time: str
    description: str
    status: str
    user_id: int

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    time: Optional[str] = None
