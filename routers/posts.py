from fastapi import APIRouter, Response, HTTPException, Depends, FastAPI, status
from database import get_session, Posts
from sqlalchemy.orm import Session
import schemas
from . import oauth

router = APIRouter(
    prefix = "/posts",
    tags = ['posts']
)

@router.get("", response_model=list[schemas.postResponse])
def get_post(db: Session = Depends(get_session), limit: int = 10, skip: int = 0, search: str = ''):
    posts = db.query(Posts).filter(Posts.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post('', response_model=schemas.postResponse)
def posting(post: schemas.PostCreate, db: Session = Depends(get_session), curr_user: Session = Depends(oauth.get_current_user)):
    created_post = Posts(**post.dict(), user_id = curr_user.user_id)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post

@router.get("/{id}", response_model=schemas.postResponse)
def get_with_id(id: int, db: Session = Depends(get_session), curr_user: Session = Depends(oauth.get_current_user)):
    post_query = db.query(Posts).filter(Posts.post_id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post with that id not found")
    return post

@router.delete("/{id}", response_model=schemas.postResponse)
def deleting(id: int, db: Session = Depends(get_session), curr_user: Session = Depends(oauth.get_current_user)):
    del_post = db.query(Posts).filter(Posts.post_id == id)
    post = del_post.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post with that id not found")
    if curr_user.user_id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authoriezed to perform this action")
    del_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.postResponse)
def updating(post: schemas.PostCreate, id: int, db: Session= Depends(get_session), curr_user: Session = Depends(oauth.get_current_user)):
    upd_post_query = db.query(Posts).filter(Posts.post_id == id)
    upd_post = upd_post_query.first()
    if not upd_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post with that id not found")
    if curr_user.user_id != upd_post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authoriezed to perform this achtion")
    upd_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(upd_post)
    return upd_post
