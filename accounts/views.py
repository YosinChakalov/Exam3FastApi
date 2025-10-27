import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Response,Request
from .schemas import *
from sqlalchemy.orm import Session
from db_config import get_my_db
from .helpers import *
from .models import *
from .permission import *

account_app = APIRouter()



@account_app.post("/register")
async def register_view(user_data:UserSchema,db:Session = Depends(get_my_db)):
    hashed_password = hash_password(user_data.password)
    user =  UserModel(username = user_data.username,email=user_data.email,password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return f'User created succesfully'

@account_app.post("/login")
async def login_view(user_data:LoginSchema,response:Response,db:Session = Depends(get_my_db)):
    user = authenticate(user_data.username,user_data.password)
    if not user:
        raise ValueError('No such user exists')

    session_id = db.query(SessionModel).filter(SessionModel.user_id == user.id).first()

    if not session_id:
        token = str(uuid.uuid4())
        session = SessionModel(token=token,user_id=user.id)
        db.add(session)
        db.commit()

        response.set_cookie(key="session_key",value=token,httponly=True)

        return f'Logged succesfully'
    
@account_app.post("/logout", dependencies=[Depends(is_authenticated)])
async def logout_view(response:Response,request:Request,db:Session = Depends(get_my_db)):
    session_key = request.cookies.get("session_key")
    session = db.query(SessionModel).filter(SessionModel.token == session_key).first()
    
    if session:
        db.delete(session)
        db.commit()
        response.delete_cookie("session_key")
        return {"message": "User logged out"}
    return {"message":"Not logged in user"} 

@account_app.post("/notes-create", dependencies=[Depends(is_authenticated)])
async def create_note(note_data: NoteSchema, db:Session = Depends(get_my_db), request:Request = None):
    user = get_current_user(db, request)
    note = NotesModel(title = note_data.title, description = note_data.description, user_id = user.id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return f"note created"

def get_current_user(db:Session = Depends(get_my_db), request:Request = None):
    session_key = request.cookies.get("session_key")
    session = db.query(SessionModel).filter(SessionModel.token == session_key).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = db.query(UserModel).filter(UserModel.id == session.user_id).first()
    return user

@account_app.get("/notes-list", dependencies=[Depends(is_authenticated)])
async def list_notes(db:Session = Depends(get_my_db), request:Request = None):
    user = get_current_user(db, request)
    notes = db.query(NotesModel).filter(NotesModel.user_id == user.id).all()
    return notes

@account_app.put("/notes-update/{note_id}", dependencies=[Depends(is_authenticated)])
async def update_note(note_id:int,note_data: NoteSchema, db:Session = Depends(get_my_db), request:Request = None):
    user = get_current_user(db, request)
    note = db.query(NotesModel).filter(NotesModel.id == note_id, NotesModel.user_id == user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    note.title = note_data.title
    note.description = note_data.description
    db.commit()
    db.refresh(note)
    return f"note updated"

@account_app.delete("/notes-delete/{note_id}", dependencies=[Depends(is_authenticated)])
async def delete_note(note_id:int, db:Session = Depends(get_my_db), request:Request = None):
    user = get_current_user(db, request)
    note = db.query(NotesModel).filter(NotesModel.id == note_id, NotesModel.user_id == user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    db.delete(note)
    db.commit()
    return f"note deleted"

