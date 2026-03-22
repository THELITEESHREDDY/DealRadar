from fastapi import Depends, FastAPI, HTTPException, Query,status
from sqlmodel import Field, Session,select,func, SQLModel, create_engine, select,and_,or_,
from pydantic import BaseModel,HttpUrl,EmailStr,ValidationError
from typing import Annotated
from passlib.context import CryptContext

#pydantic models
class user_login_model(BaseModel):
    email: EmailStr
    password: str

class user_register_response_model(BaseModel):
    name:str
    age:int|None
    email: EmailStr
    phone: str
    password: str

class user_model(user_register_response_model):
    id:int

class profile(BaseModel):
    name:str
    age:int
    email:EmailStr
    Phone:str

class url_model(BaseModel):
    url:HttpUrl

class dashbord_model(BaseModel):
    site_count:int
    sites:list
    order_count:int
  


#databasemodels
class user_db(SQLModel,table=True):
    id: int|None =Field(default=None, primary_key=True,index=True)
    name:str =Field(index=True)
    age: int | None = Field(default=None)
    email: str=Field(index=True, unique=True)
    phone: str =Field(index=True)
    password: str

class sites_db(SQLModel, table=True):
    id: int | None=Field(default=None,index=True,primary_key=True)
    name: str=Field(index=True)
    url: str
    userid: int
    
class orders_db(SQLModel,table=True):
    id: int | None=Field(default=None,index=True,primary_key=True)
    url: str
    userid: int


sqlite_file_name="database.db"
sqlite_url= f"sqlite:///{sqlite_file_name}"

connected_args={"check_same_thread": False}
engine =create_engine(sqlite_url,connect_args=connected_args)



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

pwd_context=CryptContext(schemes=["bycrypt"],deprecated="auto")
def hash_password(password: str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password: str,hashed_password: str)->bool:
    return pwd_context.verify(plain_password,hashed_password)
    
app= FastAPI(title="DealRadar")
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def welcome():
    return {"message": "Welcome"}

@app.post("/login")
async def login(user: user_login_model,session: SessionDep):

    query= select(user_db).where(and_ (user_db.email==user.email,True==hash_password(user.password)))
    response = session.exec(query).first()
    
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    return {"message": "Logged in successfully"}



@app.post("/register",response_model=user_register_response_model)
async def register(req_user: user_register_response_model,session:SessionDep):
    try:
        user= user_db.model_validate(req_user.model_dump())

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail=e.errors())

    userdb=session.exec(select(user_db).where(user_db.email==user.email))
    if userdb:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user exists with this email")
    
    hashed_password=hash_password(user.password)
    user.password=hashed_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/dashbord/profile",response_model=profile)
async def profile(curr_user: EmailStr,session:SessionDep):

    res_user= session.exec(select(user_db).where(user_db.email==curr_user)).first()
    if not res_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return res_user


@app.get("/dashbord",response_model=dashbord_model)
async def dashbord(session:SessionDep):
    #verify user
    query=select(func.count()).select_from(orders_db.userid==curr_user_id).all()
    orders_count=session.exec(query).one()
    sites=session.exec(select(sites_db.name).where(sites_db.userid==curr_user_id).offset(page).limit(limit)).all()
    site_count=len(sites)

    return {site_count,sites,orders_count}

@app.get("/dashbord/myorders",response_model=list[orders_db])
async def my_orders(session:SessionDep):
    #verify user

    query=select(orders_db).where(orders_db.userid==curr_user_id)
    orders= await session.exec(query).all()

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="orders not found")
    return orders

@app.get("/dashbord/viewsites",response_model=list[sites_db])
async def view_sites(session:SessionDep):
    #verify user
    query=select(sites_db).where(sites_db.userid==curr_user_id)
    sites= await session.exec(query).all()

    if not sites:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="orders not found")
    return sites


@app.post("/dashbord/addsites")
async def add_sites_to_DB(url : url_model):
    
    
    return {"message": "OK"}

@app.delete("/dashbord/sites")
async def delete_site(id:int):
    return {"message": "ok"}


@app.post("/search")
async def search(product:str):
    return {"message":"ok"}


# @app.get("/dashbord/tracklist")
# async def trackList():
#     return {}