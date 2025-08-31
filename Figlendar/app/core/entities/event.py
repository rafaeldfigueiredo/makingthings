from pydantic import BaseModel

class Event(BaseModel):
  title:str = "New Event"
  description: str = "Description of Event"
  startTime: str = "00:00"
  endTime: str = "23:59"