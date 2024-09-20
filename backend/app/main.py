from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import crud, schemas, models, database, auth, deps
from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Add CORS middleware, allows for communication with React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can restrict this to your frontend's URL)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# tested and works 
# this here either creates a new user or informs the user has already been registered
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, email=user.email)
    # checks if the user already exists, if so then will return a 400 status code; already registered
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # else we will return this newly created user and populate the database
    return crud.create_user(db=db, user=user)


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print(database.get_db)
    print(form_data.username)
    user = crud.get_user(db, email=form_data.username)
    print(user)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/applications/", response_model=schemas.JobApplication)
def create_job_application(application: schemas.JobApplicationCreate, 
                           current_user: models.User = Depends(deps.get_current_user), 
                           db: Session = Depends(database.get_db)):
    return crud.create_application(db=db, application=application, user_id=current_user.id)

# get all applications for specified user
@app.get("/applications/", response_model=list[schemas.JobApplication])
def get_applications(current_user: models.User = Depends(deps.get_current_user), 
                     db: Session = Depends(database.get_db)):
    return crud.get_applications(db=db, user_id=current_user.id)

@app.get("/applications/{application_id}/", response_model=schemas.JobApplication)
def get_single_application(application_id: int,
                    current_user: models.User = Depends(deps.get_current_user), 
                     db: Session = Depends(database.get_db)):
    application = crud.get_one_application(db=db, application_id=application_id, user_id=current_user.id)
    # If the application doesn't exist, return a 404 error
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # If the application exists, check if the owner_id matches the user_id
    if application.owner_id != current_user.id:
        raise HTTPException(status_code=406, detail="User does not have permission to access this application")
    
    # if successful we return the application
    return application

@app.put("/applications/{application_id}/", response_model=schemas.JobApplication)
def update_application(application_id: int, application: schemas.JobApplicationCreate, 
                       current_user: models.User = Depends(deps.get_current_user), 
                       db: Session = Depends(database.get_db)):
    return crud.update_application(db=db, application_id=application_id, application=application)

@app.delete("/applications/{application_id}/")
def delete_application(application_id: int, 
                       current_user: models.User = Depends(deps.get_current_user), 
                       db: Session = Depends(database.get_db)):
    crud.delete_application(db=db, application_id=application_id)
    return {"message": "Job application deleted"}
