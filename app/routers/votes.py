from fastapi import APIRouter, Response, HTTPException, Depends, FastAPI, status
import schemas
from . import oauth
from database import Votes, Posts, get_session
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post('', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_session), curr_user: Session = Depends(oauth.get_current_user)):
    post = db.query(Posts).filter(Posts.post_id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="post not found")
    vote_query = db.query(Votes).filter(Votes.post_id == vote.post_id, Votes.user_id == curr_user.user_id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        new_vote = Votes(post_id = vote.post_id, user_id = curr_user.user_id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message": "you've deleted vote"}
