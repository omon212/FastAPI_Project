from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from app.databace import Base
from app.tasks.models import Task


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(16), unique=True)
    password = Column(String(128))

    tasks = relationship("Task", back_populates="user")
