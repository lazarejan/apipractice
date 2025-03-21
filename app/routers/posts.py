from fastapi import APIRouter, Response, HTTPException, Depends, FastAPI, status
from ..database import get_session, Posts, Votes
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import schemas
from . import oauth

router = APIRouter(
    prefix = "/posts",
    tags = ['posts']
)

@router.get("", response_model=list[schemas.PostOut])
def get_post(db: Session = Depends(get_session), limit: int = 10, skip: int = 0, search: str = ''):
    posts_joined = db.query(Posts, func.count(Votes.post_id).label("votes")).join(
        Votes, Votes.post_id == Posts.post_id, isouter=True).filter(
            Posts.title.contains(search)).group_by(Posts.post_id).limit(limit).offset(skip)
    # this solution in case you dont use schemas. when using the schema this code is not neccessery
    # results = list(map(lambda x: x._mapping, posts_joined))
    # print(results)
    return posts_joined

@router.post('', response_model=schemas.PostResponse)
def posting(post: schemas.PostCreate, db: Session = Depends(get_session), curr_user: Session = Depends(oauth.get_current_user)):
    created_post = Posts(**post.dict(), user_id = curr_user.user_id)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_with_id(id: int, db: Session = Depends(get_session), curr_user: Session = Depends(oauth.get_current_user)):
    
    post = db.query(Posts, func.count(Votes.post_id).label("votes")).join(
        Votes, Votes.post_id == Posts.post_id, isouter=True).filter(Posts.post_id == id).group_by(Posts.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post with that id not found")
    return post

@router.delete("/{id}", response_model=schemas.PostResponse)
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

@router.put("/{id}", response_model=schemas.PostOut)
def updating(post: schemas.PostCreate, id: int, db: Session= Depends(get_session), curr_user: Session = Depends(oauth.get_current_user)):
    upd_post_query = db.query(Posts, func.count(Votes.post_id).label("votes")).join(
        Votes, Votes.post_id == Posts.post_id, isouter=True).filter(Posts.post_id == id).group_by(Posts.post_id)
    upd_post = upd_post_query.first()
    if not upd_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post with that id not found")
    if curr_user.user_id != upd_post.Posts.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authoriezed to perform this action")
    upd_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(upd_post)
    return upd_post
