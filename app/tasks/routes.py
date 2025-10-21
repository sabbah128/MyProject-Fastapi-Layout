from fastapi import APIRouter, Path, Depends, HTTPException
from tasks.schemas import *
from tasks.models import TaskModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from fastapi.responses import JSONResponse


router = APIRouter(tags=["tasks"]) # prefix="/todo"

@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(db: Session = Depends(get_db)):
    result = db.query(TaskModel).all()
    return result


@router.get("/tasks/{tasks_id}", response_model=TaskResponseSchema)
async def retrieve_tasks_item(tasks_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id = tasks_id).one_or_none()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found!")
    else:
        return task_obj

@router.post("/tasks") #response_model=TaskResponseSchema, status_code=201
async def create_tasks(request: TaskCreateSchema , db: Session = Depends(get_db)):
    # new_task = TaskModel(
    #     title=request.title,
    #     describtion=request.description,
    #     is_completed=request.is_completed
    #     )
    new_task = TaskModel(**request.model_dump())
    db.add(new_task)
    db.commit()       
    db.refresh(new_task) 
    return new_task

@router.put("/tasks/{tasks_id}", response_model=TaskResponseSchema)
async def update_tasks(tasks_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return {}

@router.delete("/tasks/{tasks_id}", )
async def delete_tasks(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return{}