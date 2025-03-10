from pydantic import BaseModel, Field
from typing import Optional

class Task(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    completed: bool = False
