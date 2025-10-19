from fastapi import APIRouter


router = APIRouter(tags=["tasks"]) # prefix="/todo"

@router.get("/tasks")
async def retrieve_tasks_list():
    return []

@router.get("/tasks/{tasks_id}")
async def retrieve_tasks_item(tasks_id: int):
    return []