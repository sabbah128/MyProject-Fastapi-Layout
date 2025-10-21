from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from core.database import Base, engine



tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations related to task management (create, update, delete, list, etc.)",
        "externalDocs": {
            "description": "More details about tasks API",
            "url": "https://example.com/docs/tasks"
        },
    }
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start Application...")
    yield    
    print("Shutting the App down.")


# Add the metadata when creating the app
app = FastAPI(
    title="Task Manager API",
    description="An API for managing tasks with FastAPI.",
    version="1.0.0",
    terms_of_service="https://google.com",
    contact={
        "name": "H.KianAra",
        "url": "https://www.google.com",
        "email": "sabbah128@gmail.com",
    },
    license_info={
        "name": "MIT"
    },
    lifespan=lifespan,
    openapi_tags=tags_metadata
)


app.include_router(tasks_routes) # prefix="/api/v1"
