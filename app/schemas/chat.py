from pydantic import BaseModel

class ChatRequest(BaseModel): 
    message: str 
    role:str | None ="user"
    class Config:
            extra = "forbid"

class ChatResponse(BaseModel): 
    response: str 
    class Config:
            extra = "forbid"            