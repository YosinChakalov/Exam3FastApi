from pydantic import BaseModel, EmailStr, field_validator, model_validator


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm: str

    @model_validator(mode="before")
    def confirm_password(value):
        if value['password'] != value['confirm']:
            raise ValueError('passwords do not match')
        return value
    
class LoginSchema(BaseModel):
    username: str
    password: str

class NoteSchema(BaseModel):
    title: str
    description: str 