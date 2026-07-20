from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional,List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models ,schemas , utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# we are removing this coz we are using alembic so no need of this
# it creates tables when they are not present
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app = FastAPI()

# origins = [
#     "https://www.google.com",
#     "https://www.youtube.com " ,
#     "http://localhost:8080",
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router) 

app.include_router(vote.router) 



@app.get("/")
def root():
     return {"message":"Welcome to my api project"}
  














#  uvicorn app.main:app --reload




# my_posts = [{"title":"title of one" , "content":"content of onw","id": 1 } ,
#             {"title":"title of two" , "content":"content of two","id": 2 } ]

# # //finding Post
# def find_post(id):
#      for p in my_posts:
#           if p['id']==id:
#                return p
          

# # //find index by id
# def find_index_post(id):
#      for i,p in enumerate(my_posts):
#           if p['id']==id:
#                return i
