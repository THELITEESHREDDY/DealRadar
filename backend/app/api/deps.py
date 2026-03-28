from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode
from jwt.exceptions import InvalidTokenError
from sqlmodel import select
from typing import Annotated
from app.database.sessions import get_session
from app.database.models import user_db
from app.core.config import SECRET_KEY, ALGORITHM
from app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email or not isinstance(email, str):
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = session.exec(select(user_db).where(user_db.email==token_data.email)).first() 
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[user_db, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user