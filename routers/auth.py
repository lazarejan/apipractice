from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_session, Users
import schemas, utils
from . import oauth

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.query(Users).filter(Users.email == user_info.username).first()

    if not user or not utils.verify(user_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "user not found")
    
    access_token = oauth.create_access_token(data = {"user_id": user.user_id})

    return {"access_token": access_token}
