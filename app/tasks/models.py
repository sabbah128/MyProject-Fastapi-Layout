from sqlalchemy import Column, String, Integer, Boolean, func, DateTime, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship
from users.models import UserModel


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(150), nullable=False)
    description = Column(String(300), nullable=True)
    is_completed = Column(Boolean, default=False)
    
    created_date = Column(DateTime, server_default=func.now())
    updated_date= Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    user = relationship("UserModel", back_populates="tasks", uselist=False)

