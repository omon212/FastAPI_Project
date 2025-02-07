from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from app.databace import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128))
    time = Column(String(16))
    description = Column(String(256))
    status = Column(String(16))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")
