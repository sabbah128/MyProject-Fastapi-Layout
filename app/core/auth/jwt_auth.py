import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from users.models import UserModel
from core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from core.config import settings
from jwt.exceptions import DecodeError, InvalidSignatureError


security = HTTPBearer()

def get_authenticated_user(
        credentials: HTTPAuthorizationCredentials = Depends(security), 
        db: Session = Depends(get_db)
        ):
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, settings.ALGORITHM)
        user_id = decoded.get("user_id", None)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed, User ID not in payload")
        if decoded.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed, Token type not valid")
        if datetime.now() > datetime.fromtimestamp(decoded.get("exp")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed, Token expired")
        user_obj = db.query(UserModel).filter_by(id = user_id).one()
        return user_obj

    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed, Invalid Signature")
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication failed, Decode Error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Authentication failed(1), {e}")    

def generate_access_token(user_id: int, expires_in: int = 120) -> str:
    now = datetime.now(timezone.utc)
    payload={
        "type": "access",
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in)
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)


def generate_refresh_token(user_id: int, expires_in: int = 600) -> str:
    now = datetime.now(timezone.utc)
    payload={
        "type": "refresh",
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in)
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)