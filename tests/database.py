from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.database import get_db,Base
import pytest

# alembic setup
# from alembic import command


# database things 

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Suhani#7820@localhost:5432/fastapi_test'
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=engine)


 
#  gives db object
@pytest.fixture()
def session():
            
     Base.metadata.drop_all(bind=engine)
     Base.metadata.create_all(bind=engine)

     db = TestingSessionLocal()  # session created

     try :
          yield db
     finally : 
          db.close()



# gives client
@pytest.fixture()
def client(session):

    # alembic setup
    #  command.upgrade("head")

    def override_get_db():
    #  When FastAPI asks for a database, give it this existing session
        try :
             yield session
        finally : 
             session.close()

    # overriding test db over db
    app.dependency_overrides[get_db] = override_get_db

    print("before client")
    yield TestClient(app) # This allows pytest to run code after the test finishes.
    print("after client")

    #  command.downgrade("head")

     #Every test that requests the client fixture gets its own execution of that fixture (by default).


# when someone calls test_create_user it needs client
# so it starts creating the client fixture.
# so client works it needs session so session works
# it gives db object it comes to client
# Python creates the function: overide getdb
# Because it's created inside client, it remembers the session object (this is Python's closure feature).
   
# Then this line registers it:
# app.dependency_overrides[get_db] = override_get_db

# then it creates client and goes to test_create_user



