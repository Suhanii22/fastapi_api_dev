
from .. import models,schemas,utils , oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends , APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db




router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db : Session=Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):


    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first

#  if post does not exists
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"Post with id {vote.post_id} does not exists")


    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , models.Vote.user_id == current_user.id)
    # print("Current User ID:", current_user.id)
    # print("Post ID:", vote.post_id)

    found_vote = vote_query.first()

    # print("Found Vote:", found_vote)

#   Did the user ask to
#   add a vote = yes coz 1
    if(vote.dir == 1):

        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail = f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id , user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return { "message" : " Successfully added Vote" }
    
#    remove vote
    else:
        if not found_vote:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"vote does not exists")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : " Successfully deleted vote"}
      

