from fastapi import APIRouter, Depends, HTTPException, status
from users.schemas import UserLoginSchema
from users.schemas import UserRegisterSchema
from users.schemas import UserrefreshtokenSchema
from users.models import UserModel
from sqlalchemy.orm import Session
from core.database import get_db
from fastapi.responses import JSONResponse
from core.auth.jwt_auth import (
    generate_access_token,
    generate_refresh_token,
    decode_refresh_token,
)


router = APIRouter(tags=["users"], prefix="/users")


@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesnt exists!",
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password doesnt match!",
        )

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return JSONResponse(
        content={
            "detail": "Login successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


@router.post("/register")
async def user_register(
    request: UserRegisterSchema, db: Session = Depends(get_db)
):
    if (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists!",
        )
    user_obj = UserModel(username=request.username.lower())

    print("Password input:", request.password)
    print("Password length:", len(request.password))

    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    return JSONResponse(content={"detail": "User registerd successfully"})


@router.post("/refresh-token")
async def user_refresh_token(
    request: UserrefreshtokenSchema, db: Session = Depends(get_db)
):
    user_id = decode_refresh_token(request.token)
    access_token = generate_access_token(user_id)
    return JSONResponse(content={"access token": access_token})
