from sqlmodel import SQLModel, Field

class user_db(SQLModel,table=True):
    id: int|None =Field(default=None, primary_key=True,index=True)
    name:str =Field(index=True)
    age: int | None = Field(default=None)
    email: str=Field(index=True, unique=True)
    phone: str =Field(index=True)
    password: str = Field(min_length=6)
    disabled: bool = Field(default=False)

class sites_db(SQLModel, table=True):
    id: int | None=Field(default=None,index=True,primary_key=True)
    name: str=Field(index=True)
    url: str
    userid: int = Field(foreign_key="user_db.id")
    
class orders_db(SQLModel,table=True):
    id: int | None=Field(default=None,index=True,primary_key=True)
    url: str
    userid: int = Field(foreign_key="user_db.id")