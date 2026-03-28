from app.core.security import verify_password, DUMMY_HASH
from app.database.sessions import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from app.schemas.token import Token
from app.schemas.user import user_register_model, user_response_model
from app.database.models import user_db
from app.core.security import get_password_hash
from app.core.jwt import create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

def authenticate_user(email:str, password:str,session=Depends(get_session)):
    user= session.exec(select(user_db).where(user_db.email==email)).first()
    if not user:
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password,user.password):
        return None
    return user

router = APIRouter()


@router.post("/login",response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session=Depends(get_session)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password,session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@router.post("/register", response_model=user_response_model)
async def register(
   req_user: user_register_model, session=Depends(get_session)
    ):

    # check existing user
    existing_user = session.exec(
        select(user_db).where(user_db.email == req_user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    # create user
    user = user_db(
        name=req_user.name,
        age=req_user.age,
        email=req_user.email,
        phone=req_user.phone,
        password=get_password_hash(req_user.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

