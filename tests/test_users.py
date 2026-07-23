

import pytest
from app import schemas

from jose import jwt
from app.config import settings

# when someone calls test_create_user it needs client
# so it starts creating the client fixture.
# so client works it needs session so session works
# it gives db object it comes to client
# Python creates the function: overide getdb
# Because it's created inside client, it remembers the session object (this is Python's closure feature).
   
# Then this line registers it:
# app.dependency_overrides[get_db] = override_get_db

# then it creates client and goes to test_create_user




# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Welcome to my api project'
#     assert res.status_code == 200

def test_create_user(client):
    # it is passing values and getting reponse in res variable
    res = client.post("/users/" , json={"email":"s@gmail.com","password":"password"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "s@gmail.com"
    assert res.status_code == 201

def test_login_user(client , test_user):
     res = client.post("/login" , data={"username": test_user['email'],"password": test_user['password']})
     login_res = schemas.Token(**res.json())
     payload = jwt.decode(login_res.access_token , settings.secret_key  , algorithms=[settings.algorithm])
     id = payload.get("user_id")
     assert id == test_user['id']
     assert login_res.token_type == 'Bearer'
     assert res.status_code == 200

@pytest.mark.parametrize("email,password, status_code" , 
                       [ ("wrongmail@gmail.com","password",403),
                        ("s@gmail.com","wrongpassword",403),
                        ("wrongmail@gmail.com","wrongpassword",403),
                        (None,"password",422), 
                        ("s@gmail.com",None,422)] )
def test_incorrect_login(test_user,client , email , password , status_code):
     res = client.post("/login" , data={"username":email, 'password':password})
     assert res.status_code == status_code
    #  assert res.json().get('detail') == 'Invalid Credentials'
          