from fastapi import FastAPI
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from . import models
from .database import engine
from .routers import posts, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)

# while True:
#   try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('Database connection successful')
#     break
#   except Exception as error:
#     print('Connecting to database failed')
#     print('Error:', error)
#     time.sleep(2)

@app.get("/")
def root():
  return {"message": "Hello world"}
