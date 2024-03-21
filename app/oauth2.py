from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from . import schema, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

##OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

## secret key
SECRET_KEY = settings.SECRET_KEY
## algorithm
ALGORITHM = settings.ALGORITHM
## expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    encode = data.copy()
    ## time to expire at
    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expire})

    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt

## verify access token
def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= ALGORITHM)
        user_id = str(payload.get("user_id"))
        if user_id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=user_id)

    except JWTError:
        raise credentials_exception
    
    return token_data

    
## when accessing content, we should expect an access token (posts)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user