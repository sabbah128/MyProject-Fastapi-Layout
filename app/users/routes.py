from fastapi import APIRouter, Path, Depends, HTTPException, Query
from users.schemas import *
from users.models import UserModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from fastapi.responses import JSONResponse


router = APIRouter(tags=["users"]) # prefix="/todo"


@router.post("/login")
async def user_login(request: UserLoginSchema, 
                       db: Session = Depends(get_db)):
    return {}


@router.post("/register")
async def user_register(request: UserRegisterSchema, 
                       db: Session = Depends(get_db)):
    return {}
