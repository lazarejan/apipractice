from .. import schemas
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt  # type: ignore
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from ..database import Users, get_session
from sqlalchemy.orm import Session
from ..config import settings

aouth_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded

def verify_access_token(token: str, cred_exp):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")
        if not id:
            raise cred_exp
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise cred_exp
    return token_data
    
def get_current_user(token: str = Depends(aouth_scheme), db: Session = Depends(get_session)):
    cred_exp= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized", headers= {"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, cred_exp)
    cur_user = db.query(Users).filter(Users.user_id == token.id).first()
    return cur_user