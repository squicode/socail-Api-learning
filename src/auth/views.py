from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime

from src.auth.schemas import UserCreate, UserUpdate, User as UserSchema 
from src.database import get_db 
from src.auth.service import create_access_token, existing_user, get_current_user,get_user_from_user_id, create_user_srv

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate, db:Session = Depends(get_db)):
    # check for existing user 
    db_user = await existing_user(db, user.username, user.email)
    if db_user:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT, 
            detail="username or email already in use", 
        )
    db_user = create_user_srv(db, user)
    access_token = await create_access_token(user.username, db_user.id)

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "username": user.username
    }

@router.post("/token", status_code=status.HTTP_201_CREATED)
async def login(form_data: OAuth2PasswordBearer = Depends(), db:Session = Depends(get_db)):
    db_user =   ...