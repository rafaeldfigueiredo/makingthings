from fastapi import APIRouter
from app.core.services.event_service import EventService
from app.core.entities.event import Event

router = APIRouter(prefix="/events",tags=["events"])
service = EventService()

@router.post("/")
def create_new_event(event:Event):
  return service.create_event(event)

@router.get("/")
def get_events():
  return service.list_events()
