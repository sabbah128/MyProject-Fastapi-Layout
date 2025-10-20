from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=150, min_length=5, description="Title of the task")
    description: Optional[str] = Field(None, max_length=500, description="description of the task")
    is_completed: bool = Field(..., description="State of the task")


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description="ID")
    
    create_date: datetime = Field(..., description="Creation date & time")
    update_date: datetime = Field(..., description="Updating date & time")

