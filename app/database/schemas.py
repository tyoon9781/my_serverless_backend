from pydantic import BaseModel
from datetime import datetime

class ItemSchema:
    class NeedCreate(BaseModel):
        title: str
        description: str|None = None

    class All(BaseModel):
        title: str
        description: str|None = None
        id: int
        created_at: datetime