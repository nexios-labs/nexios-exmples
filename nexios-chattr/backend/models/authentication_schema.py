from pydantic import BaseModel, Field
from typing import Optional

class UserCreationSchema(BaseModel):
    username: str = Field(..., max_length=360)
    first_name: str = Field(..., max_length=120)
    last_name: str = Field(..., max_length=120)
    bio: Optional[str] = None  
    password: Optional[str] = None  
    

    class Config:
        from_attributes = True  
        
        
class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=360)
    password: Optional[str] = None  
    
    
    
