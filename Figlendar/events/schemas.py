from pydantic import BaseModel
from typing import Optional

class EventCreate(BaseModel):
  title:str
  date:str
  time:str
class EventUpdate(BaseModel):
  title:Optional[str] = None
  date:Optional[str] = None
  time:Optional[str] = None