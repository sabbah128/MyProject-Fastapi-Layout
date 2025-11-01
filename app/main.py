from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes
from core.database import Base, engine
from users.models import UserModel
from fastapi.middleware.cors import CORSMiddleware



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
app.include_router(users_routes)

from core.auth.jwt_auth import get_authenticated_user
@app.get("/public")
def public_route():
    return {"msg": "this is a public route"}

@app.get("/private")
def private_route(user = Depends(get_authenticated_user)):
    print(">>>>>", user.id)
    return {"msg": "this is a private route"}



origins=[
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# import time
# from fastapi import FastAPI, Request
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.perf_counter()
#     response = await call_next(request)
#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response