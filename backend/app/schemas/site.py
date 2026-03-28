from pydantic import BaseModel,HttpUrl

class url_model(BaseModel):
    url:HttpUrl

class dashbord_model(BaseModel):
    site_count:int
    sites:list[dict]
    order_count:int

class SiteResponse(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        from_attributes = True



  