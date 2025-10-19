from sqlalchemy import Column, String, Integer, Boolean, func, DateTime
from core.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    describtion = Column(String(300), nullable=True)
    is_completed = Column(Boolean, default=False)
    
    created_date = Column(DateTime, server_default=func.now())
    updateed_date= Column(DateTime, server_default=func.now(), server_onupdate=func.now())