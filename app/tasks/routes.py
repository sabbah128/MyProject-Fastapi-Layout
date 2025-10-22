from fastapi import APIRouter, Path, Depends, HTTPException, Query
from tasks.schemas import *
from tasks.models import TaskModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from fastapi.responses import JSONResponse


router = APIRouter(tags=["tasks"]) # prefix="/todo"

@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(db: Session = Depends(get_db),
                              limit: int= Query(10, gt=0, le=50, description="Limit items"),
                              offset: int= Query(0, ge=0, description="Use for paginating"),                            
                              completed: bool = Query(None, description="Filter tasks on Complete ot not")):
    
    result = db.query(TaskModel)

    if completed is not None:
        result = result.filter_by(is_completed = completed)
    
    return result.limit(limit).offset(offset).all()
    # return result.all()


@router.get("/tasks/{tasks_id}", response_model=TaskResponseSchema)
async def retrieve_tasks_item(tasks_id: int = Path(..., gt=0), 
                              db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id = tasks_id).one_or_none()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found!")
    else:
        return task_obj

@router.post("/tasks", response_model=TaskResponseSchema, status_code=201)
async def create_tasks(request: TaskCreateSchema, 
                       db: Session = Depends(get_db)):
    new_task = TaskModel(
        title=request.title,
        description=request.description,
        is_completed=request.is_completed
        )
    # new_task = TaskModel(**request.model_dump())
    db.add(new_task)
    db.commit()       
    db.refresh(new_task) 
    return new_task

@router.put("/tasks/{tasks_id}", response_model=TaskResponseSchema)
async def update_tasks(request: TaskUpdateSchema, 
                       tasks_id: int = Path(..., gt=0), 
                       db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id = tasks_id).one_or_none()
    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task_obj, key, value)

    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.delete("/tasks/{tasks_id}", status_code=204)
async def delete_tasks(tasks_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id = tasks_id).one_or_none()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found!")
    db.delete(task_obj)
    db.commit()
    # return JSONResponse(status_code=200, content="Task remove successfully.")