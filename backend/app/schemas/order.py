from pydantic import BaseModel
class OrderResponse(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True