from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings



       
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# dependancy
def get_db():
     db = SessionLocal()
     try :
          yield db
     finally : 
          db.close()




# previously used 


# # while True:
# try :
#      conn = psycopg2.connect(
#      host="localhost",
#      database="postgres",
#      user="postgres",
#      password="Suhani#7820",
#      cursor_factory=RealDictCursor
#      )
          
#      # DATABASE_URL = "postgresql://postgres:password@localhost/fastapi"
#      # engine = create_engine(DATABASE_URL)

     
#      cursor = conn.cursor()

#      # SessionLocal = sessionmaker(bind=engine)
#      # db = SessionLocal()

#      print("connecting to db successful")
#      # break
# except Exception as error:
#           print("connecting to db failed")    
#           print("error" , error)
#           time.sleep(3)
