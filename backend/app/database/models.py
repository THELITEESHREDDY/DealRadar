from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Site(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    base_url: str


class PriceHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str
    site_name: str
    price: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

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