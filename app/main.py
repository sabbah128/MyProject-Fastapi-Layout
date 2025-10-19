from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start Application...")
    yield    
    print("Shutting the App down.")


app = FastAPI(lifespan=lifespan)