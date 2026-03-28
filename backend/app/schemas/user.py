from pydantic import BaseModel, EmailStr,Field

class user_register_model(BaseModel):
    name:str
    age:int|None
    email: EmailStr
    phone: str = Field(min_length=10, max_length=10)
    password: str = Field(min_length=6)

class user_response_model(BaseModel):
    name:str
    age:int|None
    email: EmailStr
    phone: str
    class Config:
        from_attributes = True

class user_login_model(BaseModel):
    email: EmailStr
    password: str

class user_model(user_register_model):
    id:int
    disabled: bool | None = None

class profile(BaseModel):
    name:str
    age:int
    email:EmailStr
    phone:str