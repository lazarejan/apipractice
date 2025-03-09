from fastapi import APIRouter, Response, HTTPException, Depends, FastAPI, status
from database import get_session, Users
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import schemas
import utils

router = APIRouter(
    prefix = "/users",
    tags = ['users']
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = Users(**user.dict())
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as IE:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this email already exists")

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_session)):
    user = db.query(Users).filter(Users.user_id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User with that id not found")
    return user