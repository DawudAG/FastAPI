from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True

while True:
  try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('Database connection successful')
    break
  except Exception as error:
    print('Connecting to database failed')
    print('Error:', error)
    time.sleep(2)

@app.get("/")
def root():
  return {"message": "Hello world"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
  posts = db.query(models.Post).all()
  return posts

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  return post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
  new_post = models.Post(**post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  if post_query.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  post_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  post_query.update(updated_post.model_dump(), synchronize_session=False)
  db.commit()
  db.refresh(post)
  return post
