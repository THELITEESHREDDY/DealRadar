from fastapi import FastAPI
from app.database.models import SQLModel
from app.database.sessions import engine
from app.api.routes import auth, dashboard

#pydantic models

#databasemodels

#dbstuff

# openssl rand -hex 32

#password verify and hash

#auth user

#create access token

#get current user

#get current active user

#main 

app = FastAPI(title="DealRadar")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(dashboard.router)

@app.get("/")
async def welcome():
    return {"message": "Welcome"}



@app.post("/search")
async def search(product:str):

    sites=["https://www.amazon.in/","https://www.flipkart.com/"]



# @app.get("/dashbord/tracklist")
# async def trackList():
#     return {}