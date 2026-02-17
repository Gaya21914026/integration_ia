from pydantic import BaseModel

class ProductBase(BaseModel): 
    name: str 
    price: int 
    
class ProductCreate(ProductBase): 
    pass 

class ProductUpdate(BaseModel):
    name: str | None = None
    price: int | None = None


class ProductResponse(ProductBase): 
    id: int 
    
    class Config: 
        from_attributes = True
