from fastapi.testclient import TestClient
from app.main import app
from app import schemas, models
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.database import get_db,Base
import pytest
from app.oauth2  import create_access_token

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
@pytest.fixture
def test_user2(client):
    user_data = {"email":"s123@gmail.com","password":"password"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email":"s@gmail.com","password":"password"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id" : test_user['id']})

@pytest.fixture
def authorized_client(client,token):
     client.headers = {
          **client.headers,
          "Authorization":f"Bearer {token}"
     }

     return client


@pytest.fixture
def test_posts(test_user , session , test_user2):
     posts_data = [
        {
          "title":"1 title",
          "content":"1 content",
          "owner_id" : test_user['id']
        },
        {
          "title":"2 title",
          "content":"2 content",
          "owner_id" : test_user['id']
        },
         {
          "title":"new title",
          "content":"new content",
          "owner_id" : test_user2['id']
        }
     ]

     def create_post_model(post):
        return  models.Post(**post) 

     post_map = map(create_post_model, posts_data)
     posts = list(post_map)
     session.add_all(posts)

    #  session.add_all([models.Post(title="1 title", content="1 content")])

     session.commit()
     posts = session.query(models.Post).all()

     return posts