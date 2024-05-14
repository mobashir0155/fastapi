from fastapi import Depends, status, HTTPException, Response, APIRouter
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, select
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(limit: int = 5, skip: int = 0, search: Optional[str] = "" ,db: Session = Depends(get_db)):

    post = aliased(models.Post,name="post")
    posts = db.query(post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, post.id == models.Vote.post_id, isouter=True).group_by(post.id).filter(post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = aliased(models.Post,name="post")
    post_result = db.query(post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, post.id == models.Vote.post_id, isouter=True).where(post.id == id).group_by(post.id).first()

    if not post_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found.")
    return post_result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:schemas.User = Depends(auth.get_current_user)):

    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} doest not exist.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthroized to perform action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    current_post_query = db.query(models.Post).filter(models.Post.id == id)
    current_post = current_post_query.first()

    if current_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post wit id:{id} doest not exist.")
    if current_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthroized to perform action")

    
    current_post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return current_post_query.first()
