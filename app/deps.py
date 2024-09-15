# dependency injection and security 
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app import crud, models, schemas, database, config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print('try')
        print(token)
        payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
        print(payload)
        email: str = payload.get("sub")
        if email is None:
            print('em error')
            raise credentials_exception
    except JWTError:
        print('jwt')
        raise credentials_exception

    user = crud.get_user(db, email=email)
    if user is None:
        raise credentials_exception
    return user
