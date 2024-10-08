from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordRequestForm
from ..database import get_db
from .. import auth, models, schemas, utils

router = APIRouter(
    tags=["auth"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid username or password")
    if not utils.verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid username or password")
    
    access_token = auth.create_access_token(data={"user_id": user.id})
    return schemas.Token(access_token=access_token,token_type="bearer")