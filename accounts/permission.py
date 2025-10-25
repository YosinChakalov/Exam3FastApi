from fastapi import Depends,Request,Response,HTTPException,status
from db_config import get_my_db
from .models import SessionModel

def is_authenticated(request:Request):
    credentials_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authorized")
    session_db = get_my_db()
    db = next(session_db)
    session = request.cookies.get("session_key")
    if session:
        token = db.query(SessionModel).filter(SessionModel.token == session).first()
        if token:
            return token.user
        raise credentials_error
    return credentials_error
