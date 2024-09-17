from fastapi import Depends
from sqlalchemy.orm import Session

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime

from src.auth.models import User 

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/token")
SECRET_KEY = "mySecret_Key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINS = 60 * 24 * 30 # this makes the token expires in 30 days 


async def existing_user(db:Session,username:str, email:str):
    db_user = db.query(User).filter(User.username==username).first()
    db_user = db.query(User).filter(User.email==email).first()
    return db_user 

async def create_access_token(username:str, id:int): 
    encode = {"sub": username, "id":id}
    expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINS)
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(db:Session, token: str = Depends(oauth2bearer)):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id:str = payload.get("id")
        if username is None or id is None: 
            return None 
    except JWTError:
        ...
