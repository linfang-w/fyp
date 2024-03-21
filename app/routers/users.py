## path operations to users## create user
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from .. import models, schema, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

## create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def user_create(user: schema.UserCreate, db: Session = Depends(get_db)):

    ## create hash for password - user.password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

## get user by id
@router.get("/{id}", response_model=schema.UserOut)
def user_get(id: int, db: Session = Depends(get_db)):

    found_user = db.query(models.User).filter(models.User.id == id).first()

    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"User id: {id} was not found!")
    return found_user

