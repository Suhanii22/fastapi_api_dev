
from .. import models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends , APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db



router = APIRouter(
     prefix="/users",
     tags = ['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED , response_model = schemas.UserOut)
def create_user(user : schemas.UserCreate , db : Session = Depends(get_db)):
    # new_user = models.User(  **user.model_dump()   )
    #  hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(  **user.model_dump()   )


    # hashed_password = utils.hash(user.password)
    # new_user = models.User(
    #    email=user.email,
    #    password=hashed_password
    # )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    return new_user



# @router.post("/users", status_code=status.HTTP_201_CREATED)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

#     print("Reached create_user")

#     hashed_password = utils.hash(user.password)
#     print("Password hashed")

#     new_user = models.User(
#         email=user.email,
#         password=hashed_password
#     )

#     print("User object created")

#     db.add(new_user)
#     print("Added to session")

#     db.commit()
#     print("Committed")

#     db.refresh(new_user)
#     print("Refreshed")

#     return new_user




@router.get("/{id}" , response_model = schemas.UserOut)
def get_user(id : int , db : Session = Depends(get_db) ):
     user = db.query(models.User).filter(models.User.id == id).first()

     if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"User with this id : {id} does not exist")
     

     return user


