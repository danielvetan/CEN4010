from fastapi import FastAPI, Depends, status, HTTPException
from typing import List

# Settings For Fast API & DB
from config.settings import settings

# DB
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine

# Create Table
# DO NOT DELETE BASE
from db.models import Base
Base.metadata.create_all(bind=engine)

# Import the rest of the models under here
from db.models import User

# Schema
import schemas

#Gets the Database DONT DELETE
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Boilerplate stuff for fastapi
def start_app():
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION
    )

    return app
app = start_app()

# Put your creating APIS/ENDPOINT UNDER HERE
#
# Root Welcome Message
@app.get('/', tags=['ROOT API'])
def root():
    return 'This is the root page, use /docs to use restfulAPI'

# PROFILE MANAGEMENT
@app.post('/api/users', status_code=status.HTTP_201_CREATED, tags=['Profile Management'])
def create_users(user: schemas.User, db: Session = Depends(get_db)):
    new_user = User(
        email = user.email,
        password = user.password,
        username = user.email,
        name = user.name,
        home_address = user.home_address
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail='User already exists')

@app.get('/api/users', response_model=List[schemas.ShowUser] , tags=['Profile Management'])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Could not find users')
    print(type(users))
    return users

@app.get('/api/users/{username}', response_model=List[schemas.ShowUser], tags=['Profile Management'])
def get_user(username, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'No query found with username: {username}')
    return user

@app.put('/api/users/{username}', status_code=status.HTTP_202_ACCEPTED, tags=['Profile Management'])
def update_user(username, user: schemas.User, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).update({
        'password': user.password,
        'name': user.name,
        'home_address': user.home_address
    })
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'No query found with username: {username}')
    db.commit()
    return {'detail': f'Update user {username}'}

@app.delete('/api/users/{username}', status_code=status.HTTP_204_NO_CONTENT, tags=['Profile Management'])
def delete_user(username, db: Session = Depends(get_db)):
    db.query(User).filter(User.username == username).delete()
    db.commit()
    return {'detail': f'Deleted user {username}'}
