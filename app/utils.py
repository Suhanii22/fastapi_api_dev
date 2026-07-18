
from passlib.context import CryptContext



pwd_context=CryptContext(schemes=["bcrypt"], deprecated ="auto")

# hashing password
def hash(password : str):
    return pwd_context.hash(password)

# does user pass matched correct pass
def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)