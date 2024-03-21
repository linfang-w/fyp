## path operations to post content
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema, oauth2
from ..database import get_db
from typing import Optional

router = APIRouter(
    prefix="/content",
    tags=['Posts']
)

## decorator for http method (get) at root path 
## get all posts that current user has made
@router.get("/")
def content_get(db: Session = Depends(get_db), get_current_user= Depends(oauth2.get_current_user), limit: int = 3, skip: int =0, search: Optional[str]= ""):

    posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    return posts

## create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def content_create(post: schema.PostCreate, db: Session = Depends(get_db), get_current_user= Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id = get_current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


## FastAPI path parametres work from first instance
### anything here on from content path needs to go above int path from one post get request

## get one post
@router.get("/{id}", response_model=schema.PostResponse)
def content_single(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):                
    ## id is cast with int so prevent random character input

    post = db.query(models.Post).filter(models.Post.id == id).first()

    # checks if post exists
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post id: {id} was not found!")
    # checks if the current logged in user is the owner of the post
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    return post

## delete one post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def content_del (id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

## if post deleted, error exception for 'NoneType' TypeError
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id: {id} does not exist!")

    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)

## update post
@router.put("/{id}", response_model=schema.PostResponse)
def content_update (id: int, post: schema.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    query_post = db.query(models.Post).filter(models.Post.id == id).first()

    # checks if post exists
    if query_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist!")
    
    # checks if the current logged in user is the owner of the post
    if query_post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")

    query_post.title = post.title
    query_post.content = post.content
    db.commit()

    return query_post