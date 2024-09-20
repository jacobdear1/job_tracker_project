# crud operations
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from passlib.context import CryptContext
from fastapi import HTTPException

# adds the necessary context for password authorisation 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, email: str):
    print(db)
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    try: 
        db_user = models.User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        HTTPException(status_code=409, detail="Email already registered, try again!")

    #return db_user

def create_application(db: Session, application: schemas.JobApplicationCreate, user_id: int):
    db_application = models.JobApplication(**application.dict(), owner_id=user_id)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_applications(db: Session, user_id: int):
    return db.query(models.JobApplication).filter(models.JobApplication.owner_id == user_id).all()

def get_one_application(db:Session, application_id: int, user_id:int):
    # Query the application by application_id
    return db.query(models.JobApplication).filter(models.JobApplication.id == application_id).first()

def update_application(db: Session, application_id: int, application: schemas.JobApplicationCreate):
    db_application = db.query(models.JobApplication).get(application_id)
    for key, value in application.dict().items():
        setattr(db_application, key, value)
    db.commit()
    return db_application

def delete_application(db: Session, application_id: int):
    db_application = db.query(models.JobApplication).get(application_id)
        # If the application doesn't exist, return a 404 error
    if not db_application:
        raise HTTPException(status_code=407, detail="Application not found")

    # If the application exists, delete it
    db.delete(db_application)
    db.commit()
    db.delete(db_application)
    db.commit()
